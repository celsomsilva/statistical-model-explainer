# AIC and BIC

## AIC – Akaike Information Criterion
- Balances model fit and complexity.
- Formula: AIC = 2k - 2ln(L)

## BIC – Bayesian Information Criterion
- Similar to AIC but penalizes complexity more strongly.
- Formula: BIC = ln(n)k - 2ln(L)

## Interpretation
- Lower AIC/BIC = better (relative) model fit.
- AIC favors predictive accuracy; BIC favors simplicity.

## Example
Model A: AIC=120, BIC=140
Model B: AIC=130, BIC=135
→ AIC prefers A, BIC prefers B.
