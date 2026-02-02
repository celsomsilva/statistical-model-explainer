# Mixed Effects Models (Multilevel Models)

## Definition
Models that include both fixed effects (shared across all groups) and random effects (vary by group).

## Formula
Yij = β₀ + β₁Xij + u₀j + u₁jXij + εij

## Interpretation
- Fixed effects: overall effect across all units.
- Random effects: deviations specific to groups (e.g., stores, schools).

## Example
Weekly Sales ~ Unemployment + (1 | Store)
→ The intercept varies by Store.
