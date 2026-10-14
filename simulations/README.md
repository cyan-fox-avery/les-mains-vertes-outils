# Simulation harness — Les Mains Vertes fair selector

**Test engineering only, not production code.** This harness implements the
agreed rules (`docs/regles-selecteur.md`) so the simulation plan
(`docs/plan-simulations.md`) can be executed. Fictitious people only.
Standard library only — no dependencies.

## Files

- `engine.py` — person state, weights (recency + smoothing + bounds),
  Plackett–Luce weighted shuffle, constrained sampling (acceptance /
  rejection + exact enumeration for small groups), fallback hierarchy,
  history update (only saved final orders count).
- `measures.py` — within-trajectory measures (disparity, rank spread,
  late streaks), due-person stats, cross-trajectory summaries.
- `scenarios.py` — the 12 plan scenarios + trajectory runner.
- `run.py` — staged search: coarse → fine → held-out validation.
  Writes JSON results.
- `tests.py` — unit checks (mechanics of the agreed rules).

## Run

```sh
python3 tests.py            # unit checks (fast)
python3 run.py --stage all --out results.json
```

## Operationalizations (harness choices, not adopted rules)

The plan leaves exact curves open; the harness tests these concrete forms:

- Recency: `equal` (all 1), `linear` (oldest→newest 1..n),
  `exponential` (1.25^i, oldest→newest).
- Smoothing: `n_over_6` (n/6) or `n_over_n_plus_2` (n/(n+2)),
  with n = min(counted selections, 6).
- Weight: `1 + k × smoothing × (recency-weighted mean − 0.5)`,
  clamped to [Wmin, Wmax]; boost multiplies the weight.
- Feasibility is decided explicitly via (first, last) pairs before any
  sampling; fallback never triggers from retry exhaustion.

## Interpreting results

- Proposed thresholds from the plan are used as *screening* criteria.
  If a threshold is not met, the report says so — thresholds and rules
  are revised explicitly (with review), never silently relaxed.
- Per-person pooled averages are sanity checks only. The principal
  evidence is within-trajectory disparity vs a matched unweighted
  baseline.
- Validation uses held-out seeds/scenarios not used for selection.
