"""Analysis helpers for the report: neutral baseline (k=0) and the
boost-effect check in the plan's defined scenario.

- Baseline: k=0 makes every weight exactly 1.0 (recency/smoothing
  irrelevant) -- the matched unweighted baseline with the same hard
  constraints. Run with the same trajectory counts as the fine stage.
- Boost effect: repeated single draws from a FIXED neutral state
  (everyone eligible for first, no reservations, baseline P(first) > 0).
  Compare the boosted person's P(first) and P(first half) with the boost
  on vs off. This isolates the boost factor; it is not a trajectory
  measure.

Usage: python3 analyze.py
"""

import json
import random
import sys

sys.path.insert(0, __file__.rsplit("/", 1)[0])

from engine import Person, draw, weight_of, Params
from run import Params as RunParams, evaluate


def baseline():
    params = RunParams({"k": 0.0, "wmin": 0.5, "wmax": 1.5,
                        "recency": "equal", "smoothing": "n_over_6"})
    out = {}
    for scen, n_traj in [("usual_long", 50), ("usual", 100),
                         ("absences", 100), ("boosts", 50)]:
        out[scen] = evaluate(params, scen, n_traj)
    return out


def boost_effect(boost, draws=40000, seed=999):
    """Fixed neutral state, 12 people, Person-01 boosted or not."""
    rng = random.Random(seed)
    people = [Person(f"Person-{i + 1:02d}") for i in range(12)]
    # Neutral histories: everyone has the same counted history so the
    # only difference is the boost. Eligibility: nobody was first/last.
    for p in people:
        p.counted = [0.4, 0.5, 0.6, 0.5, 0.4, 0.5]
        p.last_first = False
        p.last_last = False
    results = {}
    for boosted in (False, True):
        params = Params(k=1.0, boost=boost)
        first = half = 0
        for _ in range(draws):
            res = draw(rng, people, params,
                       boosted=("Person-01",) if boosted else ())
            names = [p.name for p in res.order]
            if names[0] == "Person-01":
                first += 1
            if names.index("Person-01") < 6:
                half += 1
        results["boosted" if boosted else "plain"] = {
            "p_first": first / draws, "p_half": half / draws}
    plain = results["plain"]
    boosted_r = results["boosted"]
    return {
        "boost": boost,
        "p_first_plain": plain["p_first"],
        "p_first_boosted": boosted_r["p_first"],
        "first_relative_increase_pct": 100 * (boosted_r["p_first"] / plain["p_first"] - 1),
        "p_half_plain": plain["p_half"],
        "p_half_boosted": boosted_r["p_half"],
    }


def main():
    print("== neutral baseline (k=0) ==")
    base = baseline()
    for scen, r in base.items():
        print(f"  {scen}: disparity median={r['disparity']['median']:.4f} "
              f"p90={r['disparity']['p90']:.4f} | streak median={r['max_streak']['median']:.2f} "
              f"| due(b) rate={r['due']['due_first_half_rate']:.4f} "
              f"({r['due']['due_first_half_hits']}/{r['due']['due_first_half_total']})")
    print("== boost effect (fixed neutral state, eligible, unreserved) ==")
    for b in (1.25, 1.5, 2.0):
        r = boost_effect(b)
        print(f"  boost={b}: P(first) {r['p_first_plain']:.4f} -> {r['p_first_boosted']:.4f} "
              f"({r['first_relative_increase_pct']:+.1f}%) | "
              f"P(half) {r['p_half_plain']:.4f} -> {r['p_half_boosted']:.4f}")
    with open("baseline_boost.json", "w") as f:
        json.dump({"baseline": base, "boosts": [boost_effect(b) for b in (1.25, 1.5, 2.0)]}, f, indent=1)
    print("wrote baseline_boost.json")


if __name__ == "__main__":
    main()
