# Reflection

This project analysed a sensitive, politically charged subject — fatal police
shootings — so before writing any code I decided how I'd *present* it: stick to
what the data records, show my working, and add caveats wherever a chart could be
easily misread. That framing mattered more than any single chart.

Technically it was a multi-dataset join problem: one fatalities table plus four
census tables (~29,000 rows each) that all needed cleaning before they'd combine.
The census columns hid their missing values as text (`-`, `(X)`) and median income
had ranges like `250,000+`, so `pd.to_numeric(errors='coerce')` and a bit of string
cleaning were needed to get real numbers. The fatalities dates were `DD/MM/YY`
(easy to parse the wrong way round — I checked the resulting date range to be sure
the first records really were early January 2015), and the race column was
single-letter codes that I expanded to readable names.

The most important lesson wasn't a pandas trick — it was **interpretation**. The
starter prompts ask which cities and states are "most dangerous", and the honest
answer is that the raw-count charts *don't* say that: California, Texas and Florida
top the map mostly because they're the biggest states. So I reframed those charts
around **counts vs. per-capita rates**, and flagged that comparing groups needs
population context and that correlation (poverty vs. graduation) isn't causation.
A chart that's technically correct can still mislead if you let it imply more than
the data supports.

The easiest part was the visualisation itself — Plotly and Seaborn make the charts
almost fall out once the data is clean. The hardest part was resisting the pull of
a tidy narrative and keeping every statement to exactly what the numbers show.

If I extended it, I'd bring in state/city **populations** to compute true
per-capita rates (the analysis the count charts can only hint at), and look at how
the patterns changed year to year rather than over the whole period at once.
