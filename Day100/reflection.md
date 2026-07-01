# Reflection

The final project brought together the whole data-science toolkit into one task:
take real survey data and build a *model* that predicts something — here, hourly
earnings — then judge how good it is and make it better.

I approached it as a ladder, starting simple and adding one idea at a time so I
could see the effect of each change. A regression on schooling alone explains very
little (R² ≈ 0.08). Adding work experience helped; adding ability, hours, tenure
and demographics helped more; and log-transforming earnings — because they're
badly skewed and grow multiplicatively — gave the biggest single jump, roughly
tripling the explained variance to R² ≈ 0.24. Building it step by step made the
"why" of each improvement obvious rather than reaching for a big model straight away.

The most valuable habits were the un-glamorous ones. Checking for duplicates caught
**513** identical rows that would have quietly biased everything. Looking at the
residuals — not just the R² — showed *why* the first model was weak: they were
skewed and fanned out, which is exactly the pattern a log transform fixes. And
using `statsmodels` alongside `scikit-learn` gave me p-values, so I could say which
predictors actually mattered instead of trusting every coefficient.

The part I was most careful about was **interpretation**, because the data includes
sex and ethnicity. A regression coefficient on observational data is an
*association*, not a cause, so I framed every result that way and resisted turning a
correlation into a story about cause and effect. A model can be technically correct
and still be misread if you over-claim what it shows.

My biggest overall takeaway from the project — and honestly from the whole 100
days — is that the interesting work lives in the boring, careful steps: clean the
data, look at it, question the result, and be honest about the limits. If I did
this one again I'd try regularisation and interaction terms, and cross-validation
instead of a single train/test split, to see how stable the story really is.
