"""Unit checks for the simulation engine (no network, deterministic).

Run: python3 tests.py
Each check asserts a *mechanical* property of the agreed rules. Threshold
pass/fail from the plan is evaluated by run.py, not here.
"""

import random
import sys

sys.path.insert(0, __file__.rsplit("/", 1)[0])

from engine import (Person, apply_final_order, draw, exact_conditioned_distribution,
                    recency_newest_share, total_variation, weight_of, weighted_shuffle,
                    Params)


def check(name, cond):
    print(f"  {'OK ' if cond else 'FAIL'} {name}")
    assert cond, name


def main():
    rng = random.Random(42)
    params = Params()

    # 1. Singleton session is excluded from history.
    p = Person("Solo")
    res = draw(rng, [p], params)
    apply_final_order([p], res.order, res.birthday_reserved)
    check("singleton excluded from counted history", p.counted == [])

    # 2. Absence pauses: absent person untouched.
    a, b, c = Person("A"), Person("B"), Person("C")
    a.counted = [0.9]
    res = draw(rng, [b, c], params)
    apply_final_order([a, b, c], res.order, res.birthday_reserved)
    check("absent person history untouched", a.counted == [0.9])

    # 3. Birthday pause: celebrated person skipped, others counted.
    a, b, c = Person("A"), Person("B"), Person("C")
    res = draw(rng, [a, b, c], params, birthdays=("A",))
    assert res.order[0].name == "A"
    apply_final_order([a, b, c], res.order, res.birthday_reserved)
    check("birthday person paused", a.counted == [])
    check("others counted after birthday draw", len(b.counted) == 1 and len(c.counted) == 1)

    # 4. No-repeat holds whenever a valid order exists (2000 random draws).
    people = [Person(f"P{i}") for i in range(6)]
    violations = 0
    for _ in range(2000):
        for q in people:  # randomize histories
            q.counted = [rng.random() for _ in range(rng.randint(0, 6))]
            q.last_first = rng.random() < 0.3
            q.last_last = rng.random() < 0.3
        present = [q for q in people if rng.random() > 0.2] or people[:2]
        before = {q.name: (q.last_first, q.last_last) for q in present}
        res = draw(rng, present, params)
        if res.fallback_level == 0 and len(res.order) > 1:
            first, last = res.order[0], res.order[-1]
            if before[first.name][0] or before[last.name][1]:
                violations += 1
    check("no-repeat: 0 unintended violations at level 0", violations == 0)

    # 5. Fallback: n=2, both were first -> last protected, level >= 1.
    a, b = Person("A"), Person("B")
    a.last_first = b.last_first = True
    res = draw(rng, [a, b], params)
    check("joint impossibility -> fallback level >= 1", res.fallback_level >= 1)

    # 6. Exact fidelity: sampled distribution matches exact Plackett-Luce.
    people = [Person(f"P{i}") for i in range(4)]
    people[0].counted = [0.9, 0.8, 1.0, 0.7, 0.9, 1.0]
    people[1].counted = [0.1, 0.2, 0.0, 0.3, 0.1, 0.2]
    people[2].counted = [0.5, 0.4, 0.6, 0.5, 0.4, 0.5]
    people[3].counted = [0.3, 0.7, 0.2, 0.8, 0.4, 0.6]
    weights = [weight_of(p, params) for p in people]
    exact = exact_conditioned_distribution(people, weights, lambda o: True)
    counts = {}
    for _ in range(20000):
        order = weighted_shuffle(rng, people, weights)
        key = tuple(p.name for p in order)
        counts[key] = counts.get(key, 0) + 1
    sampled = {k: v / 20000 for k, v in counts.items()}
    tv = total_variation(sampled, exact)
    check(f"exact fidelity TV={tv:.4f} < 0.02", tv < 0.02)

    # 7. Smoothing formula: exact value after one counted last-place.
    p = Person("T")
    p.counted = [1.0]
    w = weight_of(p, Params(k=1.0, smoothing="n_over_6"))
    check("smoothing n/6: weight == 1 + 1*(1/6)*0.5", abs(w - (1 + 1 / 12)) < 1e-9)

    # 8. All-boosted is neutral (Plackett-Luce is scale-invariant).
    people = [Person(f"P{i}") for i in range(4)]
    for i, p in enumerate(people):
        p.counted = [0.1 * i, 0.9 - 0.1 * i]
    w0 = [weight_of(p, params) for p in people]
    w1 = [weight_of(p, params, boosted=True) for p in people]
    d0 = exact_conditioned_distribution(people, w0, lambda o: True)
    d1 = exact_conditioned_distribution(people, w1, lambda o: True)
    check("all-boosted distribution identical", max(abs(d0[k] - d1[k]) for k in d0) < 1e-9)

    # 9. Absent priority is compacted out.
    a, b, c = Person("A"), Person("B"), Person("C")
    res = draw(rng, [a, c], params, priorities=("A", "B", "C"))
    check("absent priority compacted: A first, C second",
          [p.name for p in res.order] == ["A", "C"])

    # 10. Recency shares: linear 6-window newest <= 30%.
    check("linear recency newest share <= 0.30",
          recency_newest_share(6, "linear") <= 0.30)
    print(f"     linear newest share = {recency_newest_share(6, 'linear'):.4f}")
    print(f"     exponential(1.25) newest share = {recency_newest_share(6, 'exponential'):.4f}")

    print("ALL TESTS PASSED")


if __name__ == "__main__":
    main()
