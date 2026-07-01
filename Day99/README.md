# Deaths Involving Police in the United States 📊

A data-exploration project analysing **The Washington Post's database of fatal
police shootings** (2015 to mid-2017 in this snapshot) alongside **US census
data** — poverty rate, high-school graduation, median income and racial
demographics.

📓 **The completed notebook:**
[`Fatal_Force.ipynb`](673%20%5Bassignment_file%5D%20Analyse%20Deaths%20involving%20Police%20in%20the%20United%20States/Fatal_Force.ipynb)
(in the assignment folder, next to the CSV files).

## How to read this analysis

This is a sensitive topic, so the notebook sticks to **what the data records** and
adds caveats where they matter:

- It covers **fatal police shootings only** — not all deaths in custody, nor
  non-fatal incidents — over roughly 2.5 years.
- Most charts show **raw counts**. Counts track how many people live somewhere, so
  "more incidents" usually means "more people", not "more risk". Comparing risk
  fairly needs **per-capita rates**.
- **Correlation is not causation.**

## What's inside

- **Cleaning** the census data (text placeholders like `-`, `(X)`, `250,000+` →
  numbers) and the fatalities data (parsing `DD/MM/YY` dates, expanding the
  W/B/H/A/N/O race codes).
- **Census by state:** poverty rate, high-school graduation rate, median income,
  and the racial makeup of each state (stacked bar).
- **Poverty ↔ graduation:** a dual-axis line, a Seaborn KDE joint plot, and a
  linear regression (correlation ≈ **−0.5**).
- **The fatalities data:** deaths by race (donut), by gender (~96% men), age
  distribution overall and by race, whether the person was armed (~7% unarmed),
  and signs of mental illness (~25%).
- **Geography & time:** the cities and states with the most incidents, a US
  **choropleth**, and the month-by-month trend.

## A few factual observations

- ~**96%** of those killed were men; the **median age was 34**.
- In most cases the person was **armed** (most often a gun); about **7%** were
  recorded as unarmed.
- Incident **counts** are highest in the most populous states/cities (California,
  Texas, Florida; Los Angeles) — which is why per-capita **rates**, not counts,
  are the right comparison for risk.
- At the state level, **higher poverty correlates with lower graduation rates**.

## How to run it

Open the notebook in Jupyter, VS Code, or Google Colab and *Run All*. It uses
`pandas`, `numpy`, `matplotlib`, `seaborn`, `plotly` and `kaleido`. Charts are
saved as **static images** so they display everywhere (including GitHub); delete
the `pio.renderers.default = "png"` line for interactive Plotly charts.

For The Washington Post's own analysis, see their
[police-shootings database](https://www.washingtonpost.com/graphics/investigations/police-shootings-database/).
