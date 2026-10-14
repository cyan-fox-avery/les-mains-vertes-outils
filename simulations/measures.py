"""Measures for the simulation plan (docs/plan-simulations.md §4).

All measures operate on *trajectories*: one trajectory = the sequence of
draws for one weekday group. Cross-trajectory statistics (median, 90th
percentile) are computed over independent seeded trajectories. Per-person
pooled averages are sanity checks only, never principal evidence.
"""

from __future__ import annotations

import statistics


def median(xs):
    return statistics.median(xs) if xs else float("nan")


def percentile(xs, q):
    """Nearest-rank percentile (q in 0..100)."""
    if not xs:
        return float("nan")
    s = sorted(xs)
    idx = min(len(s) - 1, max(0, int(q / 100.0 * len(s))))
    return s[idx]


def summarize(values):
    """Distribution of a per-trajectory measure across trajectories."""
    return {
        "mean": statistics.mean(values) if values else float("nan"),
        "median": median(values),
        "p90": percentile(values, 90),
        "min": min(values) if values else float("nan"),
        "max": max(values) if values else float("nan"),
        "n": len(values),
    }


def first_half_shares(trajectory, names):
    """Per-person share of first-half placements within one trajectory."""
    counts = {n: 0 for n in names}
    totals = {n: 0 for n in names}
    for order in trajectory:
        n = len(order)
        half = n // 2
        for idx, person in enumerate(order):
            totals[person.name] += 1
            if idx < half:
                counts[person.name] += 1
    return {n: (counts[n] / totals[n] if totals[n] else 0.0) for n in names}


def within_run_disparity(trajectory, names):
    """Max-minus-min per-person first-half share *within* one trajectory."""
    shares = first_half_shares(trajectory, names)
    vals = list(shares.values())
    return max(vals) - min(vals) if vals else 0.0


def normalized_avg_ranks(trajectory, names):
    """Per-person mean normalized position within one trajectory."""
    sums = {n: 0.0 for n in names}
    totals = {n: 0 for n in names}
    for order in trajectory:
        n = len(order)
        if n <= 1:
            continue
        for idx, person in enumerate(order):
            sums[person.name] += idx / (n - 1)
            totals[person.name] += 1
    return {n: (sums[n] / totals[n] if totals[n] else 0.0) for n in names}


def within_run_rank_spread(trajectory, names):
    """Max-minus-min per-person mean normalized rank within one trajectory."""
    ranks = normalized_avg_ranks(trajectory, names)
    vals = list(ranks.values())
    return max(vals) - min(vals) if vals else 0.0


def longest_late_streak(trajectory, name):
    """Longest run of second-half placements for one person in one trajectory."""
    best = cur = 0
    for order in trajectory:
        n = len(order)
        half = n // 2
        names = [p.name for p in order]
        if name not in names:
            cur = 0
            continue
        idx = names.index(name)
        if idx >= half:
            cur += 1
            best = max(best, cur)
        else:
            cur = 0
    return best


def max_late_streak_in_run(trajectory, names):
    """Worst (longest) late streak across people within one trajectory."""
    return max((longest_late_streak(trajectory, n) for n in names), default=0)


def due_person_stats(trajectories, names):
    """Due-person improvement vs what the trajectories show.

    (a) mean longest late streak per trajectory.
    (b) P(first half next draw | 3 consecutive second-half placements),
        estimated over all qualifying (person, draw) windows.
    Returns dicts with numerator/denominator for (b)."""
    streaks = [max_late_streak_in_run(t, names) for t in trajectories]
    hits = total = 0
    for traj in trajectories:
        # sliding windows of 3 consecutive draws per person
        for i in range(len(traj) - 3):
            window = traj[i:i + 3]
            nxt = traj[i + 3]
            for name in names:
                ok = True
                for order in window:
                    order_names = [p.name for p in order]
                    if name not in order_names:
                        ok = False
                        break
                    if order_names.index(name) < len(order) // 2:
                        ok = False
                        break
                if not ok:
                    continue
                nxt_names = [p.name for p in nxt]
                if name not in nxt_names:
                    continue
                total += 1
                if nxt_names.index(name) < len(nxt) // 2:
                    hits += 1
    return {
        "mean_max_streak": statistics.mean(streaks) if streaks else float("nan"),
        "due_first_half_hits": hits,
        "due_first_half_total": total,
        "due_first_half_rate": (hits / total if total else float("nan")),
    }
