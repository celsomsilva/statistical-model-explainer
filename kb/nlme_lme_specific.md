# Interpretation of nlme::lme Models

The `lme()` function from the `nlme` package uses a different syntax than `lme4::lmer()`.

## Syntax Structure

lme(
  fixed = y ~ predictors,
  random = list(Group1 = ~ slope, Group2 = ~ slope),
  data = ...
)

Unlike lmer(), random effects are specified via named lists.

## Nested Structure

Dept %in% Store indicates departments nested within stores.

This represents hierarchical nesting:

Level 1: observations  
Level 2: departments  
Level 3: stores  

## Log-Cholesky Parameterization

The covariance structure of random effects is estimated using a positive-definite matrix representation.

StdDev values represent:

- Between-group variability
- Random slope variability
- Residual variance

## REML

REML is the default in nlme and is preferred for variance component estimation.

Model comparison across fixed effects should use ML instead.

