"""Simulation engine for the Les Mains Vertes fair name selector.

Implements the *agreed rules* (see docs/regles-selecteur.md on main) so the
simulation plan (docs/plan-simulations.md) can be executed:

- Six COUNTED selections per person per weekday group (rolling window).
- Absence = pause. Birthday = pause for the celebrated person. A
  single-person session is recorded but excluded from weighting and from
  the consecutive-extremes constraint.
- Manual priorities count normally. An absent priority person is removed
  and the surviving priority list is compacted.
- Birthdays come FIRST, in addition to (not included in) the max-3
  ordinary priorities. A birthday person moved out of the reserved slots
  by manual reorder loses the exemption.
- Manual boosts: positive only, one fixed gentle factor, today only,
  never overriding hard rules.
- Fallback hierarchy: both no-repeat rules first; if jointly impossible,
  protect no-repeat-LAST; if even that is impossible, secondary fallback
  (plain weighted order) with a flag. Fallback NEVER triggers merely
  because a finite number of samples failed.
- Only the explicitly saved FINAL order feeds history. Discarded drafts
  never count.

Everything here uses fictitious people and a seeded RNG. Standard
library only. No production code, no real data.
"""

from __future__ import annotations

import itertools
import math
import random
from dataclasses import dataclass, field


# ---------------------------------------------------------------------------
# Parameters (a *tested* combination, not an adopted rule)
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Params:
    k: float = 1.0                 # weighting strength
    wmin: float = 0.5              # lower weight bound
    wmax: float = 1.5              # upper weight bound
    recency: str = "linear"        # "equal" | "linear" | "exponential"
    smoothing: str = "n_over_6"    # "n_over_6" | "n_over_n_plus_2"
    boost: float = 1.5             # manual boost multiplier (today only)
    fallback: str = "accept_reject"  # "accept_reject" | "exact"


# ---------------------------------------------------------------------------
# Person state
# ---------------------------------------------------------------------------

@dataclass
class Person:
    name: str
    counted: list = field(default_factory=list)  # normalized positions, oldest -> newest, max 6
    last_first: bool = False  # was FIRST in last counted selection
    last_last: bool = False   # was LAST in last counted selection

    def counted_n(self) -> int:
        return min(len(self.counted), 6)


def recency_weights(n: int, kind: str) -> list:
    """Weights for counted selections, oldest -> newest. Sum is normalized by caller."""
    if kind == "equal":
        return [1.0] * n
    if kind == "linear":
        return [1.0 + i for i in range(n)]
    if kind == "exponential":
        return [1.25 ** i for i in range(n)]
    raise ValueError(f"unknown recency kind: {kind}")


def recency_newest_share(n: int, kind: str) -> float:
    """Share of the newest counted selection in the recency weighting."""
    w = recency_weights(n, kind)
    return w[-1] / sum(w)


def smoothing_factor(n_counted: int, kind: str) -> float:
    """Gradual influence of a short history. n is capped at the 6-entry window."""
    n = min(n_counted, 6)
    if kind == "n_over_6":
        return n / 6.0
    if kind == "n_over_n_plus_2":
        return n / (n + 2.0)
    raise ValueError(f"unknown smoothing kind: {kind}")


def weight_of(person: Person, params: Params, boosted: bool = False) -> float:
    """History-based weight. Neutral (1.0) with no counted history."""
    if not person.counted:
        w = 1.0
    else:
        n = min(len(person.counted), 6)
        window = person.counted[-6:]
        rw = recency_weights(n, params.recency)
        mean = sum(a * b for a, b in zip(rw, window)) / sum(rw)
        smooth = smoothing_factor(n, params.smoothing)
        w = 1.0 + params.k * smooth * (mean - 0.5)
        w = max(params.wmin, min(params.wmax, w))
    if boosted:
        w *= params.boost
    return w


# ---------------------------------------------------------------------------
# Weighted shuffle (Plackett-Luce via exponential race / A-ES)
# ---------------------------------------------------------------------------

def weighted_shuffle(rng: random.Random, people: list, weights: list) -> list:
    """One weighted permutation. key = U^(1/w), sort descending."""
    keys = []
    for person, w in zip(people, weights):
        u = rng.random()
        if u <= 0.0:
            u = 1e-12
        keys.append((u ** (1.0 / w), person))
    keys.sort(key=lambda t: -t[0])
    return [p for _, p in keys]


def exact_conditioned_distribution(people: list, weights: list, feasible):
    """Exact Plackett-Luce probabilities over all permutations, conditioned
    on `feasible(order)`. Only for small groups (n <= 8). Returns a dict
    order-tuple -> probability."""
    total = 0.0
    probs = {}
    for perm in itertools.permutations(people):
        if not feasible(perm):
            continue
        # Plackett-Luce probability of this exact order.
        remaining = list(perm)
        wmap = {p.name: w for p, w in zip(people, weights)}
        p = 1.0
        denom = sum(wmap[q.name] for q in remaining)
        for q in perm:
            p *= wmap[q.name] / denom
            denom -= wmap[q.name]
        probs[tuple(q.name for q in perm)] = p
        total += p
    if total <= 0:
        return {}
    return {k: v / total for k, v in probs.items()}


# ---------------------------------------------------------------------------
# Draw
# ---------------------------------------------------------------------------

@dataclass
class DrawResult:
    order: list              # final order (list of Person), generated order unless corrected
    generated: list          # generated order before any manual correction
    fallback_level: int      # 0 = both constraints, 1 = last-only, 2 = secondary (no constraints)
    birthday_reserved: list  # birthday people who kept a reserved slot
    priority_override: bool  # a priority placed first despite a previous first (explicit override)
    manual_exception: bool   # final order violates a no-repeat rule via manual correction


def _feasible_pair_exists(first_fixed, last_candidates, check_first, check_last):
    """Feasibility via (first, last) pairs: only first/last positions matter.
    first_fixed: Person or None. last_candidates: people who may be last."""
    if first_fixed is not None:
        if check_first and first_fixed.last_first:
            return False
        pool = [p for p in last_candidates if p is not first_fixed]
        if not pool:
            return True  # single person left: first == last, singleton logic applies
        return any(not (check_last and p.last_last) for p in pool)
    # first is free: need a (first, last) distinct pair satisfying the checks
    for first in last_candidates:
        if check_first and first.last_first:
            continue
        for last in last_candidates:
            if last is first:
                continue
            if check_last and last.last_last:
                continue
            return True
    return False


def draw(rng: random.Random, eligible: list, params: Params,
         birthdays: tuple = (), priorities: tuple = (),
         boosted: tuple = (), correction=None) -> DrawResult:
    """Run one draw.

    eligible: people present at the draw (Person objects).
    birthdays: names celebrating today (only those present get a reserved slot).
    priorities: names in staff-specified order (absent ones are compacted out).
    boosted: names receiving today's manual boost.
    correction: optional callable(generated_order) -> final_order (manual reorder).
    """
    present = {p.name for p in eligible}
    bday = [p for p in eligible if p.name in set(birthdays)]
    # Birthday order between celebrants is random.
    bday = [p for _, p in sorted(((rng.random(), p) for p in bday))]
    prio = [p for p in eligible if p.name in set(priorities)]
    # Compact priorities in staff order, absent ones dropped.
    prio = sorted(prio, key=lambda p: list(priorities).index(p.name))
    reserved = bday + prio
    remaining = [p for p in eligible if p not in reserved]
    boosted_set = set(boosted)

    # Birthday-reserved first is exempt from the no-repeat-first rule.
    first_exempt = bday[0] if bday else None
    priority_override = False
    if prio and not bday and prio[0].last_first:
        # Ordinary priority repeating first: allowed only as explicit override.
        priority_override = True

    def sample_conditioned(check_first, check_last, tries=20000):
        """Sample a weighted order conditioned on the given constraints."""
        if not remaining:
            return list(reserved)
        weights = [weight_of(p, params, p.name in boosted_set) for p in remaining]
        if params.fallback == "exact" and len(remaining) <= 8:
            dist = exact_conditioned_distribution(
                remaining, weights,
                lambda perm: _pair_ok(list(reserved) + list(perm), check_first, check_last, first_exempt))
            if not dist:
                return None
            r = rng.random()
            acc = 0.0
            for names, prob in dist.items():
                acc += prob
                if r <= acc:
                    by_name = {p.name: p for p in remaining}
                    return list(reserved) + [by_name[n] for n in names]
            return list(reserved) + [remaining[0]]
        for _ in range(tries):
            order = list(reserved) + weighted_shuffle(rng, remaining, weights)
            if _pair_ok(order, check_first, check_last, first_exempt):
                return order
        return None

    def _pair_ok(order, check_first, check_last, first_exempt):
        if len(order) <= 1:
            return True
        if check_first:
            first = order[0]
            # Birthday-reserved first is exempt; an ordinary priority repeating
            # first is an explicit override, not a violation.
            override_first = priority_override and prio and first is prio[0]
            if first is not first_exempt and not override_first and first.last_first:
                return False
        if check_last and order[-1].last_last:
            return False
        return True

    # Feasibility: both constraints?
    full = list(reserved) + remaining
    if len(full) <= 1:
        generated = full
        level = 0
    else:
        first_fixed = reserved[0] if reserved else None
        # Both-constraints feasibility: first (fixed or free) + last.
        if first_fixed is not None:
            first_ok = (first_fixed is first_exempt
                        or (priority_override and first_fixed is prio[0])
                        or not first_fixed.last_first)
            both_ok = first_ok and any(
                not p.last_last for p in full if p is not first_fixed)
            if len(full) == 1:
                both_ok = True
        else:
            both_ok = _feasible_pair_exists(None, full, True, True)
        if both_ok:
            generated = sample_conditioned(True, True)
            level = 0
        else:
            # Fallback: protect no-repeat-LAST.
            if first_fixed is not None:
                last_ok = any(not p.last_last for p in full if p is not first_fixed) or len(full) == 1
            else:
                last_ok = any(not p.last_last for p in full)
            if last_ok:
                generated = sample_conditioned(False, True)
                level = 1
            else:
                # Secondary fallback: plain weighted order, flagged.
                weights = [weight_of(p, params, p.name in boosted_set) for p in remaining]
                generated = list(reserved) + (weighted_shuffle(rng, remaining, weights) if remaining else [])
                level = 2
        if generated is None:  # sampling failed despite feasibility (should not happen)
            weights = [weight_of(p, params, p.name in boosted_set) for p in remaining]
            generated = list(reserved) + (weighted_shuffle(rng, remaining, weights) if remaining else [])
            level = 2

    final = list(generated)
    manual_exception = False
    if correction is not None:
        final = correction(list(generated))
        # A manual reorder that creates a repeat is a recorded exception.
        if len(final) > 1 and (final[0].last_first or final[-1].last_last):
            manual_exception = True

    # Birthday exemption survives only if the person kept a reserved slot.
    reserved_slots = set(p.name for p in bday)
    kept = [p for p in final[:len(bday)] if p.name in reserved_slots]
    return DrawResult(order=final, generated=generated, fallback_level=level,
                      birthday_reserved=kept, priority_override=priority_override,
                      manual_exception=manual_exception)


# ---------------------------------------------------------------------------
# History update: only the saved FINAL order counts
# ---------------------------------------------------------------------------

def apply_final_order(people: list, final_order: list, birthday_reserved: list):
    """Advance fairness history from an explicitly saved final order.

    Birthday people who kept a reserved slot pause (skip). Everyone else
    present in the final order counts normally. Absent people untouched.
    A one-person order is recorded as an event but excluded (no entry).
    """
    if len(final_order) <= 1:
        return
    paused = {p.name for p in birthday_reserved}
    n = len(final_order)
    for idx, person in enumerate(final_order):
        if person.name in paused:
            continue
        normalized = idx / (n - 1)
        person.counted.append(normalized)
        person.counted = person.counted[-6:]
        person.last_first = (idx == 0)
        person.last_last = (idx == n - 1)


def total_variation(sampled: dict, exact: dict) -> float:
    """Total variation distance between two distributions over order tuples."""
    keys = set(sampled) | set(exact)
    return 0.5 * sum(abs(sampled.get(k, 0.0) - exact.get(k, 0.0)) for k in keys)
