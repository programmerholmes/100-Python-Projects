# Analysing the Space Race 🚀

A data-exploration & visualisation project on **every space mission since 1957**
(4,300+ launches, scraped from nextspaceflight.com). Cleaned with **pandas** and
visualised with **matplotlib / seaborn / Plotly** — including choropleth maps and
a sunburst chart.

📓 **The completed notebook:**
[`Space_Missions_Analysis.ipynb`](673%20%5Bassignment_file%5D%20Analyse%20and%20Visualise%20the%20Space%20Race/Space_Missions_Analysis.ipynb)
(in the assignment folder, next to `mission_launches.csv`).

## What's inside

- **Data cleaning** — dropping junk index columns, parsing a messy mixed-format
  `Date`, turning `Price` text (`"5,000.0"`) into numbers, and deriving each
  launch's **Country** + 3-letter **ISO code** (with manual fixes for sea launches
  and renamed countries).
- **Launches by organisation**, active vs retired rockets, mission-status mix.
- **Cost analysis** — distribution, total & per-launch spend by org, price over time.
- **Choropleth maps** of launches and failures by country.
- A **sunburst** of Country → Organisation → Mission Status.
- **Time trends** — launches per year, month-on-month with a rolling average, and
  the busiest calendar months.
- **Cold War USA vs USSR** — pie, year-on-year lines, failures, and the falling
  failure rate over time.
- **Year-by-year leaders** — which country and which organisation led each year.

## A few findings

- The Soviet **RVSN USSR** is by far the most prolific launcher (~1,780 missions),
  and the **USSR out-launched the USA through most of the Cold War**.
- The **USA led the most individual years** (32), Russia/USSR close behind (24) —
  but **China (CASC) has led most recently** (2018–2020).
- **Space got much safer:** the failure rate fell from ~70% in 1958 to low single
  digits today.
- **December** is the busiest launch month, **January** the quietest.

## How to run it

Open the notebook in Jupyter, VS Code, or Google Colab and *Run All*. It uses
`pandas`, `numpy`, `matplotlib`, `seaborn`, `plotly`, `kaleido` and `iso3166`
(the notebook installs `iso3166` itself).

The charts are saved as **static images** so they display anywhere — including on
GitHub, which can't render interactive Plotly. To get fully **interactive** charts
instead, delete the `pio.renderers.default = "png"` line near the top and re-run.

## Files

```
673 [assignment_file] .../mission_launches.csv          the dataset
673 [assignment_file] .../Space_Missions_Analysis.ipynb the completed analysis
673 [assignment_file] .../..._(start).ipynb             the original starter
reflection.md                                           project notes
```
