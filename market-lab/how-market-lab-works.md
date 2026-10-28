# How Market Lab works

[← Back to Market Lab](README.md)

This walks through one capture session, start to finish.

## The steps

1. **Jobs wake up.** Before the open, scheduled jobs start and wait for the session.
2. **I confirm sign-in.** If the data provider asks, the check comes to my phone and I approve it.
3. **Calls pass the rate gate.** Every script shares one call limit, so no job can flood the feed.
4. **Capture runs.** Scripts record market depth and quotes during set windows.
5. **Data lands locally.** Each run writes to a dated folder. Raw data never goes to Git.
6. **The watchdog keeps watch.** If capture stops, it restarts it and tells me what it did.
7. **Sizes are logged.** After the close, a job records how much data and how many calls the session used.
8. **A rundown is written.** An agent turns the session into a summary and charts.
9. **I review it.** The rundown goes to my notes through a pull request.

## Around every turn

- **Read only.** Nothing in the project can act in the market.
- **Private data.** Raw feed data stays on my computer. Only summaries and charts leave.
- **Labeled results.** Each result says where its data came from, and gaps are tracked.
- **Reviewed changes.** Code and notes change only through pull requests.
