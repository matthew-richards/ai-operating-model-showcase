# Market Lab: market data for backtesting

[← Back to the AI Operating Model](../README.md)

Market Lab captures live market data for backtesting.
The plan is a private data lake that stores the data as Parquet files.
It's analysis only. It never places anything in the market.

It's designed so a data platform can be swapped by writing a new adapter.
The platform I use in development is one implementation, not the product.

It's also where I practice running scheduled jobs, guardrails, and AI agents against real, messy data.

## How it works

For a step-by-step walkthrough, see [How Market Lab works](how-market-lab-works.md).

![How Market Lab works: a data provider sends data one way through the provider adapter to capture, then to private storage and backtests that I review; capture requests pass an API budget gate, and a watchdog watches capture and alerts me](assets/market-lab-architecture-simple.svg)

*One capture session, simplified. Solid arrows carry data. Dashed arrows are requests.*

1. **Jobs wake up.** Before the open, scheduled jobs start and wait for the session.
2. **Requests go through the adapter.** Capture talks to one provider adapter, not to a platform directly.
3. **Requests pass the API budget gates.** Every job shares the same limits. See [API budget gates](../docs/overview.md).
4. **Capture runs.** Jobs record market data during set windows.
5. **Data lands privately.** Raw data goes to private, dated folders. Today that's my computer. After the move, it's a private cloud data lake.
6. **The watchdog keeps watch.** It watches capture and alerts me if it stops. Automatic restart is planned.
7. **Sizes are logged.** After the close, a job records how much data and how many calls the session used.
8. **Backtests and rundowns run.** The lab engine runs backtests on the stored data. An agent writes a summary with charts.
9. **I review it.** Results come to me through a pull request.

## Current state vs future state

![Market Lab current state vs future state: today capture, storage, and backtests ran on my computer and are paused; in the plan, capture and storage move to AWS](assets/market-lab-current-vs-future.svg)

*Capture and storage move to AWS. Backtests and review stay the same.*

**Current state: on hiatus.** Capture is paused on purpose while it moves to AWS.
It stopped in late October 2026. Until then it ran on my own computer, with raw data in private, dated folders.

**Future state: migration to AWS (planned).** The code moves to a virtual machine on AWS with more resources.
The planned pieces are:

- **A private data lake for backtesting.** Raw data is stored as Parquet, with public access blocked and encryption on.
- **Infrastructure as code.** The cloud setup is defined in files and reviewed like any other change.
- **Short-lived cloud credentials.** Pipelines sign in with temporary credentials instead of long-lived ones.
- **A hosted store for cleaned data.** The choice between options is still open.

**What it unlocks.** Capture no longer runs on my personal computer.
The bigger machine leaves room for more capture and heavier backtests.
The provider adapter also lets me add or swap a data platform later.

## Guardrails, as a threat model

Before the hiatus, these controls ran on my computer. They carry over to AWS.
Each line names a threat, the control, and whether it's enforced today or planned.

- **The lab acts in the market.** *Planned:* read-only market-data credentials and no code path that can act in the market. Today the code is built for analysis only, by design.
- **Jobs flood the provider.** *Enforced:* shared API budget gates cover every job, with limits set below the provider's ceiling.
- **Credentials leak.** *Enforced:* credentials live in a secrets manager, never in the repo, and every pull request runs a secrets scan.
- **Licensed data leaks.** *Enforced:* raw data is licensed for private use. It stays out of Git. Only summaries and charts leave.
- **Capture fails silently.** *Enforced:* the watchdog watches capture and alerts me. *Planned:* automatic restart.
- **Results overclaim.** *Enforced:* every result is labeled with where its data came from, and known gaps are tracked in a register.
- **A bad change slips in.** *Enforced:* code changes go through pull requests with security scans, like every repo here.
- **The cloud lake is exposed.** *Planned:* public access blocked, encryption on, and temporary credentials only.

## Experimenting with architecture

Market Lab is a place to try ideas on a small, real system:

- **Swappable providers.** Keeping the data platform behind one adapter, so it can change without touching capture or storage.
- **Storage tiers.** Comparing local folders with a hosted lake and database before choosing one.
- **Safe migration.** Planning the move to AWS so existing data keeps building with no reset.
- **Pluggable backtests.** A lab engine where each piece of a test run can be swapped.

## AI agents in the loop

AI agents do much of the work around the data. They write the rundowns, draft the charts, and propose code changes.
I review what they produce. Every change still comes to me through a pull request.
