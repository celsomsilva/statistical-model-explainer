# Advanced Interpretation of Multilevel (Mixed Effects) Models

## 1. Model Structure

Multilevel (hierarchical) models are used when data has nested structure:

- Level 1: individual observations (e.g., weeks, students)
- Level 2: groups (e.g., stores, schools)
- Possibly Level 3: higher-level clusters

Example:
Weeks nested within Departments nested within Stores.

---

## 2. Fixed Effects

Fixed effects represent the average effect across all groups.

Example:
β1 = -1.20 for Unemployment

→ On average, across all stores, a one-unit increase in Unemployment is associated with a 1.20 decrease in the outcome.

This is analogous to coefficients in linear regression but adjusted for hierarchical structure.

---

## 3. Random Effects

Random effects capture group-specific deviations.

Random intercept:
(1 | Store)

→ Each store has its own baseline level.

Random slope:
(Week | Store)

→ The effect of Week varies by Store.

Interpretation:
The variance of random effects indicates how much groups differ from each other.

Large variance → substantial heterogeneity across groups.
Small variance → groups behave similarly.

---

## 4. Variance Components

Multilevel models partition variance into:

- Between-group variance
- Within-group variance

Example:
Var(Store Intercept) = 12.5  
Residual variance = 30.0  

Interpretation:
Part of the variability is explained by differences between stores.

---

## 5. Intraclass Correlation (ICC)

ICC = Between-group variance / Total variance

It measures the proportion of total variance attributable to group-level structure.

High ICC → hierarchical modeling is justified.
Low ICC → multilevel structure may not be necessary.

---

## 6. REML vs ML

REML (Restricted Maximum Likelihood):
- Preferred for variance component estimation.
- Less biased in small samples.

ML:
- Used when comparing models with different fixed effects.

---

## 7. Shrinkage (Partial Pooling)

Multilevel models shrink group-specific estimates toward the global mean.

Small groups → more shrinkage.
Large groups → less shrinkage.

This improves stability and prevents overfitting.

---

## 8. Model Comparison

AIC and BIC can still be used.
However:

- Use ML (not REML) when comparing different fixed effects structures.
- REML is appropriate for variance estimation.

---

## 9. Why Multilevel Instead of Linear Regression?

Ignoring hierarchical structure can:

- Underestimate standard errors
- Inflate Type I error
- Produce misleading inference

Multilevel models correct for dependency within groups.

