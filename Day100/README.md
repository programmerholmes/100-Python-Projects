# Predicting Earnings — Multivariable Regression 💵

A machine-learning project that builds, analyses and improves a regression model
for predicting people's hourly earnings, using the **National Longitudinal Survey
of Youth 1997–2011 (NLSY97)** — a rich, nationally-representative US survey.

📓 **The completed notebook:**
[`Determinants_of_Earnings.ipynb`](673%20%5Bassignment_file%5D%20Predict%20Earnings%20using%20Multivariable%20Regression/Determinants_of_Earnings.ipynb)
(in the assignment folder, next to the CSV files).

## What it does

1. **Explore & clean** — inspect the 2,000-row survey, remove 513 duplicate rows.
2. **Visualise** — the (right-skewed) earnings distribution, schooling, and a
   correlation heatmap of the candidate predictors.
3. **Split** the data 80/20 into training and out-of-sample test sets.
4. **Simple regression** — `EARNINGS ~ S` (schooling): interpret the coefficient
   (~\$1.22/hr per extra year of school) and inspect the residuals.
5. **Multivariable regression** — add work experience (`EXP`).
6. **Predict** — e.g. a bachelor's degree (16 years) + 5 years' experience ≈
   **\$19.71/hr**.
7. **Improve the model:**
   - add more predictors (ability `ASVABC`, hours, tenure, sex, ethnicity, age);
   - **log-transform** earnings (they're highly skewed), which fits far better;
   - use **statsmodels OLS** to see which predictors are statistically significant.

The fit improves at each step: **R² ≈ 0.08 → 0.12 → 0.17 → 0.24**.

## How to read the results

The model is trained on **observational survey data**, so it shows **associations,
not causes**. A coefficient describes how earnings tend to differ with a feature
*holding the others constant* — it is not proof that changing that feature would
cause the change, and unmeasured factors also matter. The sex and ethnicity
coefficients describe patterns in the sample after adjusting for the included
variables; they are not causal effects. And even the improved model leaves most of
the variation in earnings unexplained.

## How to run it

Open in Jupyter, VS Code, or Google Colab and *Run All*. Uses `pandas`, `numpy`,
`matplotlib`, `seaborn`, `plotly`, `scikit-learn` and `statsmodels`. Charts are
saved as static images so they display everywhere (including GitHub).

---

*This is the final project of the 100 Days of Code course. 🎉*
