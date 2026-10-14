"""Scenario definitions (plan §5) and the trajectory runner.

A scenario is a dict describing one workplace situation. The runner
executes independent seeded trajectories for a scenario and returns the
trajectories (lists of final orders) plus per-draw flags, so measures.py
can aggregate them.

Fictitious people only: names are Person-01, Person-02, ...
"""

from __future__ import annotations

import random

from engine import Person, apply_final_order, draw


def make_people(n):
    return [Person(f"Person-{i + 1:02d}") for i in range(n)]


def run_trajectory(params, scenario, seed):
    """Run one trajectory (one weekday group) and return (orders, flags).

    orders: list of final orders (lists of Person).
    flags: list of dicts per draw: fallback_level, manual_exception, etc.
    """
    rng = random.Random(seed)
    people = make_people(scenario["n_people"])
    by_name = {p.name: p for p in people}
    orders = []
    flags = []
    n_draws = scenario["n_draws"]
    for t in range(n_draws):
        # Attendance.
        present = []
        for p in people:
            if scenario.get("absence_rate", 0.0) > 0 and rng.random() < scenario["absence_rate"]:
                continue
            if scenario.get("long_absence") and t < scenario["long_absence_until"] and p.name == scenario["long_absence"]:
                continue
            present.append(p)
        if not present:
            continue
        # Birthdays.
        bday = ()
        if scenario.get("birthday_mode") == "always" and t % scenario.get("birthday_every", 26) == 0:
            bday = (scenario.get("birthday_person", "Person-01"),)
        if scenario.get("birthday_mode") == "two" and t % 26 == 0:
            bday = ("Person-01", "Person-02")
        # Priorities.
        prio = ()
        if scenario.get("priority_mode") == "recurrent" and t % 2 == 0:
            prio = (scenario.get("priority_person", "Person-03"),)
        elif scenario.get("priority_mode") == "random" and rng.random() < 0.3:
            prio = (rng.choice(present).name,)
        # Boosts.
        boosted = ()
        if scenario.get("boost_mode") == "one" and t % 3 == 0:
            boosted = (scenario.get("boost_person", "Person-04"),)
        if scenario.get("boost_mode") == "all":
            boosted = tuple(p.name for p in present)
        # Manual correction (reorder) on some draws.
        correction = None
        if scenario.get("correction_mode") == "swap" and t % 5 == 4:
            def correction(order, _rng=rng):
                if len(order) >= 2:
                    order[0], order[1] = order[1], order[0]
                return order
        result = draw(rng, present, params, birthdays=bday, priorities=prio,
                      boosted=boosted, correction=correction)
        apply_final_order(people, result.order, result.birthday_reserved)
        orders.append(result.order)
        flags.append({
            "fallback_level": result.fallback_level,
            "manual_exception": result.manual_exception,
            "priority_override": result.priority_override,
            "n_present": len(present),
        })
    return orders, flags


def run_scenario(params, scenario, n_trajectories, seed_base=0):
    """Run all trajectories for a scenario. Returns (trajectories, all_flags)."""
    trajectories = []
    all_flags = []
    for i in range(n_trajectories):
        orders, flags = run_trajectory(params, scenario, seed_base + i * 7919)
        trajectories.append(orders)
        all_flags.extend(flags)
    return trajectories, all_flags


# The 12 plan scenarios (plan §5), in compact executable form.
SCENARIOS = {
    "usual": {"n_people": 12, "n_draws": 26, "absence_rate": 0.0},
    "usual_long": {"n_people": 12, "n_draws": 500, "absence_rate": 0.0},
    "absences": {"n_people": 12, "n_draws": 26, "absence_rate": 0.2},
    "small_2": {"n_people": 2, "n_draws": 26, "absence_rate": 0.0},
    "small_3": {"n_people": 3, "n_draws": 26, "absence_rate": 0.0},
    "priorities": {"n_people": 12, "n_draws": 26, "absence_rate": 0.0, "priority_mode": "recurrent"},
    "newcomer": {"n_people": 12, "n_draws": 26, "absence_rate": 0.0,
                 "long_absence_until": 13, "long_absence": "Person-12"},
    "manual_edits": {"n_people": 12, "n_draws": 26, "absence_rate": 0.0, "correction_mode": "swap"},
    "birthday": {"n_people": 12, "n_draws": 26, "absence_rate": 0.0, "birthday_mode": "always"},
    "birthday_two": {"n_people": 12, "n_draws": 26, "absence_rate": 0.0, "birthday_mode": "two"},
    "boosts": {"n_people": 12, "n_draws": 26, "absence_rate": 0.0, "boost_mode": "one"},
    "boosts_all": {"n_people": 12, "n_draws": 26, "absence_rate": 0.0, "boost_mode": "all"},
}
