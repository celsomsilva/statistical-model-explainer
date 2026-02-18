# Interpreting Coefficients

## Definition
Coefficients represent the relationship between predictors and the outcome.

## Basic Interpretation
- Positive coefficient → Predictor increases the outcome.
- Negative coefficient → Predictor decreases the outcome.
- Magnitude shows the effect size.

### Example
Model: Sales ~ StoreType + Promo  
Coefficient(Promo=Yes) = 3.2  
→ Sales increase by 3.2 units when promotion is active.

## Advanced Interpretation
### Odds Ratios (Logistic Regression)
- Logistic regression coefficients are in **log-odds scale**.  
- Exponentiating a coefficient gives the **odds ratio**: exp(β).  
- Example: β = 0.7 → exp(0.7) ≈ 2.01, meaning the odds are about twice as high.

### Interactions
- Coefficients in interaction terms represent the **combined effect** of two or more variables.  
- Example: `Week:Type_B = -0.01` → The weekly effect is slightly lower for Type B stores compared to the baseline.

