# Jarvis architecture (early notes)

![Jarvis at a glance](../assets/jarvis-architecture.svg)

These notes describe the design as of October 2026. Items marked **policy** are written rules the agents follow, not technically enforced controls.

## Components

| Component | Where it runs | Status |
|---|---|---|
| Jarvis gateway (chat, local API, scheduled jobs) | Home PC with a GPU | Running |
| Local models, with cloud models as fallback | Home PC GPU | Running |
| Watchdog | OS task scheduler, outside the gateway | Running since Oct 3, 2026 |
| Notes vault sync (every 15 min) | Home PC | Running |
| Supervisor sweep (board + CI) | Home PC | Running |
| Weekly hosted-vs-local model comparison | Home PC | Running |
| Glasses bridge (auth, normalization, wake filter) | Home PC | Prototype |
| Agent sandbox for tool execution | Home PC | Trialed, not adopted |

## Roles

- **Matthew** approves consequential decisions: credentials, spending, rule changes.
- **Jarvis (supervisor)** re-checks claims against live reads, runs the sweep, and records evidence. It proposes changes as pull requests on its own branches. *Policy:* it doesn't move project status or clear human-approval gates.
- **Execution agent** does the work and moves the board. It leaves the verification field blank on its own work so Jarvis fills it in.

## Done means evidence

A "Done" claim is a row: `{date, item, check, expected, observed, link}`. `observed` stays `unverified` until someone does a live read, and the link has to be the proof.

## Glasses path (prototype)

Glasses (voice + camera) → Rokid's agent platform (streamed events) → bridge on the home PC (auth, normalize, wake filter) → Jarvis through an OpenAI-compatible chat endpoint. The glasses aren't modified. Jarvis registers as a custom third-party agent.

## Safety rails

- **Spending:** a hard limit on the cloud model key, set at the provider. Heavy jobs check the remaining balance first.
- **Recovery:** the watchdog runs outside the gateway. It relaunches only after two failed probes in a row and waits an hour between relaunches.
- **Sandbox (trial):** 10 of 10 enforcement tests passed on Sep 30, 2026. These covered default-deny outbound traffic, per-program network rules, an HTTP method block, filesystem confinement, and an audit trail. Not yet tested: a real agent inside the sandbox, and end-to-end mutual TLS.
- **Exposure:** *policy* says local control-plane services stay on loopback with no open ports.

## Known gaps

- Jarvis-only, read-mostly access token: designed, not created.
- Long-lived cloud credentials on the home PC: to be replaced.
- One restart script still relaunches after its irreversible step. Moving that relaunch into a separate task is flagged but not done.
