# How Market Lab works

[← Back to Market Lab](README.md)

This walks through one capture session, start to finish.
Capture is paused on purpose while it moves to AWS. The steps stay the same after the move.

## The steps

1. **Jobs wake up.** Before the open, scheduled jobs start and wait for the session.
2. **Requests go through the adapter.** Capture talks to one provider adapter, not to a platform directly.
3. **Requests pass the API budget gates.** Every job shares the same limits, so no job can flood the provider.
4. **Capture runs.** Jobs record market data during set windows.
5. **Data lands privately.** Each run writes to a private, dated folder. Raw data never goes to Git.
6. **After the move,** raw data lands in a private cloud data lake instead of local folders.
7. **The watchdog keeps watch.** It watches capture and alerts me if it stops. Automatic restart is planned.
8. **Sizes are logged.** After the close, a job records how much data and how many calls the session used.
9. **Backtests and rundowns run.** The lab engine runs backtests on the stored data. An agent writes a summary with charts.
10. **I review it.** Results come to me through a pull request.

## Around every turn

- **Analysis only.** The lab is built to read market data, never to act in the market.
- **Private data.** Raw data stays private. Only summaries and charts leave.
- **Labeled results.** Each result says where its data came from, and gaps are tracked.
- **Reviewed changes.** Code and notes change only through pull requests.
