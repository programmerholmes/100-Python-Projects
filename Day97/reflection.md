# Reflection

The brief was to automate something tedious from real life, so I picked a chore
I actually recognise: a Downloads folder that turns into a junk drawer of
installers, screenshots, PDFs and random files. A script that files everything
into type-based folders is small, genuinely useful, and something I'll keep using.

The biggest thing I thought about wasn't the sorting logic — mapping extensions
to categories is easy — it was **safety**. This program *moves the user's real
files*, so a bug or a surprise could be genuinely annoying. That shaped the whole
design:

- It **previews by default** and only moves when you explicitly pass `--apply`.
- It **never deletes** — clashing names become `file (1).ext` instead of
  overwriting.
- Every real run is **logged to JSON so it can be undone**, which also removes the
  empty folders it created.
- It **skips** folders, hidden files and OS junk so it can't wander somewhere it
  shouldn't.

Writing the undo feature was the most interesting part: I had to record the
*actual* destination of each file (after clash-renaming), then reverse the list
on the way back. Testing was where I was most careful — I ran everything against a
throwaway temp folder full of dummy files and asserted the results, rather than
pointing it at my own Downloads.

My biggest takeaway is that for automation that changes real things, the *feature*
is the easy half; the important half is making it **safe, previewable and
reversible**, and testing it somewhere disposable first. "Show me before you do
it, and let me undo it" turns a scary script into one you actually trust.

If I extended it, I'd add per-user rules from a config file (custom folders,
"put anything with 'invoice' in Documents/Invoices"), and a proper filesystem
watcher instead of polling.
