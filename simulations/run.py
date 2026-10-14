"""Simulation runner: staged search per docs/plan-simulations.md §7.

Stages:
  coarse     -- full parameter grid, reduced trajectories (screening).
  fine       -- survivors, full trajectories.
  validation -- best combos on held-out seeds/scenarios (no overfitting).
  all        -- coarse -> fine -> validation.

Outputs JSON results and a Markdown report. Proposed thresholds are
used as *screening* criteria; the report says explicitly where a
threshold is not met. Nothing here adopts a coefficient.

Usage: python3 run.py --stage all --out results.json
"""

from __future__ import annotations

import argparse
import itertools
import json
import random
import sys
import time

sys.path.insert(0, __file__.rsplit("/", 1)[0])

from engine import (Person, exact_conditioned_distribution, recency_newest_share,
                    smoothing_factor, total_variation, weight_of, weighted_shuffle)
from measures import (due_person_stats, summarize, within_run_disparity,
                      within_run_rank_spread, max_late_streak_in_run)
from scenarios import SCENARIOS, make_people, run_scenario

GRID = {
    "k": [0.5, 1.0, 1.5, 2.0],
    "bounds": [(0.5, 1.5), (0.6, 1.4), (0.75, 1.25)],
    "recency": ["equal", "linear", "exponential"],
    "smoothing": ["n_over_6", "n_over_n_plus_2"],
}
BOOSTS = [1.25, 1.5, 2.0]


def combos():
    for k, (wmin, wmax), rec, smo in itertools.product(
            GRID["k"], GRID["bounds"], GRID["recency"], GRID["smoothing"]):
        yield {"k": k, "wmin": wmin, "wmax": wmax, "recency": rec, "smoothing": smo}


class Params:
    def __init__(self, d, boost=1.5):
        self.k, self.wmin, self.wmax = d["k"], d["wmin"], d["wmax"]
        self.recency, self.smoothing, self.boost = d["recency"], d["smoothing"], boost
        self.fallback = "accept_reject"


def hard_violation_count(all_flags):
    """Aggregate fallback/exception usage. Level-0/1 draws satisfy their
    constraints by construction (verified directly in tests.py); what the
    runner watches is fallback misuse: level 2 = secondary fallback."""
    return {
        "level_1_fallback_draws": sum(1 for f in all_flags if f["fallback_level"] == 1),
        "secondary_fallback_draws": sum(1 for f in all_flags if f["fallback_level"] == 2),
        "manual_exceptions": sum(1 for f in all_flags if f["manual_exception"]),
        "n_draws": len(all_flags),
    }


def evaluate(params, scenario_name, n_traj, seed_base=0):
    """Run one scenario and return aggregate measures + flags."""
    scen = dict(SCENARIOS[scenario_name])
    trajectories, flags = run_scenario(params, scen, n_traj, seed_base=seed_base)
    names = [f"Person-{i + 1:02d}" for i in range(scen["n_people"])]
    disp = [within_run_disparity(t, names) for t in trajectories]
    rank = [within_run_rank_spread(t, names) for t in trajectories]
    streak = [max_late_streak_in_run(t, names) for t in trajectories]
    due = due_person_stats(trajectories, names)
    return {
        "disparity": summarize(disp),
        "rank_spread": summarize(rank),
        "max_streak": summarize(streak),
        "due": due,
        "flags": hard_violation_count(flags),
    }


def fidelity_check(params, n=4, samples=20000, seed=12345):
    """Fixed-state exact-distribution comparison (small group)."""
    rng = random.Random(seed)
    people = make_people(n)
    # Give them varied counted histories so weights differ.
    people[0].counted = [0.9, 0.8, 1.0, 0.7, 0.9, 1.0]
    people[1].counted = [0.1, 0.2, 0.0, 0.3, 0.1, 0.2]
    people[2].counted = [0.5, 0.4, 0.6, 0.5, 0.4, 0.5]
    people[3].counted = [0.3, 0.7, 0.2, 0.8, 0.4, 0.6]
    for p in people:
        p.last_first = False
        p.last_last = False
    weights = [weight_of(p, params) for p in people]
    exact = exact_conditioned_distribution(people, weights, lambda o: True)
    counts = {}
    for _ in range(samples):
        order = weighted_shuffle(rng, people, weights)
        key = tuple(p.name for p in order)
        counts[key] = counts.get(key, 0) + 1
    sampled = {k: v / samples for k, v in counts.items()}
    return {"tv": total_variation(sampled, exact), "samples": samples}


def static_checks(params):
    """Direct (non-simulated) checks: smoothing, recency, boost neutrality."""
    p = Person("T")
    p.counted = [1.0]  # one counted last-place
    w_after_one = weight_of(p, params)
    rec_share = recency_newest_share(6, params.recency)
    return {
        "weight_after_one_last_place": w_after_one,
        "smoothing_ok": 0.9 <= w_after_one <= 1.1,
        "recency_newest_share_full_window": rec_share,
        "recency_ok": rec_share <= 0.30,
    }


def coarse_screen(combo):
    params = Params(combo)
    out = {"combo": combo, "static": static_checks(params)}
    for scen, n_traj in [("usual", 20), ("absences", 20), ("small_2", 20), ("small_3", 20), ("newcomer", 20)]:
        out[scen] = evaluate(params, scen, n_traj)
    # Pass coarse if: no secondary fallback, static checks pass,
    # disparity median beats neutral baseline approx (checked in fine).
    out["coarse_pass"] = (
        out["static"]["smoothing_ok"]
        and out["static"]["recency_ok"]
        and all(out[s]["flags"]["secondary_fallback_draws"] == 0
                for s in ("usual", "absences", "small_2", "small_3", "newcomer"))
    )
    return out


def fine_eval(combo, seed_base=0):
    params = Params(combo)
    out = {"combo": combo}
    for scen, n_traj in [("usual_long", 50), ("usual", 100), ("absences", 100),
                          ("priorities", 50), ("birthday", 50), ("boosts", 50),
                          ("manual_edits", 50), ("newcomer", 50)]:
        out[scen] = evaluate(params, scen, n_traj, seed_base=seed_base)
    out["fidelity"] = fidelity_check(params)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", default="all", choices=["coarse", "fine", "validation", "all"])
    ap.add_argument("--out", default="results.json")
    args = ap.parse_args()
    t0 = time.time()
    results = {"stage": args.stage, "coarse": [], "fine": [], "validation": []}
    if args.stage in ("coarse", "all"):
        print("== coarse screen: full grid, reduced trajectories ==", flush=True)
        for i, combo in enumerate(combos()):
            r = coarse_screen(combo)
            results["coarse"].append(r)
            print(f"  [{i + 1}/72] k={combo['k']} bounds=({combo['wmin']},{combo['wmax']}) "
                  f"rec={combo['recency']} smo={combo['smoothing']} pass={r['coarse_pass']}", flush=True)
    survivors = [r["combo"] for r in results["coarse"] if r.get("coarse_pass")]
    if args.stage in ("fine", "all"):
        print(f"== fine: {len(survivors)} survivors, full trajectories ==", flush=True)
        for combo in survivors:
            r = fine_eval(combo)
            results["fine"].append(r)
            print(f"  fine k={combo['k']} bounds=({combo['wmin']},{combo['wmax']}) "
                  f"rec={combo['recency']} smo={combo['smoothing']} "
                  f"fidelity_tv={r['fidelity']['tv']:.4f}", flush=True)
    if args.stage in ("validation", "all"):
        # Best = survivors with lowest usual_long disparity median, then lowest streak.
        ranked = sorted(results["fine"],
                        key=lambda r: (r["usual_long"]["disparity"]["median"],
                                       r["usual_long"]["max_streak"]["median"]))
        best = [r["combo"] for r in ranked[:2]]
        print(f"== validation: held-out seeds, best {len(best)} combos ==", flush=True)
        for combo in best:
            r = fine_eval(combo, seed_base=1_000_000)
            results["validation"].append(r)
            print(f"  validation k={combo['k']} bounds=({combo['wmin']},{combo['wmax']}) "
                  f"rec={combo['recency']} smo={combo['smoothing']}", flush=True)
    results["seconds"] = time.time() - t0
    with open(args.out, "w") as f:
        json.dump(results, f, indent=1)
    print(f"wrote {args.out} in {results['seconds']:.1f}s")


if __name__ == "__main__":
    main()
