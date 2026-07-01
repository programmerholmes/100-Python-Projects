# Reflection

This was a pure data-science project: take a big, messy, real-world dataset and
turn it into insight through cleaning and visualisation. The fun (and the work)
was almost entirely in getting the data into a usable shape — once it's clean, the
charts fall out easily.

I approached it in the order the data demanded: **explore, clean, then visualise.**
The exploration flagged the problems, and I fixed each one before drawing anything:

- Two junk `Unnamed` index columns to drop, and a handful of duplicate rows.
- **`Price`** was text with thousands-separators (`"5,000.0"`) and mostly missing —
  strip the commas, coerce to numbers, and keep the NaNs honest instead of faking
  values.
- **`Date`** was the sneaky one: most rows looked like `"Fri Aug 07, 2020 05:12 UTC"`
  but ~130 had no time at all. Pandas guessed one format and silently turned the
  odd ones into `NaT`. Stripping `" UTC"` and parsing with `format="mixed"`
  recovered every single date.
- **Country** had to be pulled out of a long location string, with real-world
  messiness — sea launches (`Pacific Ocean`, `Barents Sea`), renamed places, and
  names the ISO library didn't recognise (Iran, the Koreas) — all needing manual
  mapping to 3-letter codes before the choropleths would work.

The easiest and most satisfying part was Plotly: the choropleth maps and the
sunburst turned a table of 4,300 rows into something you can read at a glance —
the USSR's Cold-War dominance and the modern rise of China jump straight off the
map.

My biggest takeaway is that **data cleaning is the project**, and that you have to
be suspicious of "successful" parses — the `NaT` dates parsed *without error*,
they were just wrong, and I only caught it by checking the count. A number that
looks fine can still be silently dropping data.

One practical decision I'm happy with: rendering the Plotly charts as static
images so the notebook actually *shows its charts on GitHub*, where interactive
Plotly renders blank. If I extended the project I'd add the mission *payload* type
(from the `Detail` column) and look at reusable vs expendable rockets over time.
