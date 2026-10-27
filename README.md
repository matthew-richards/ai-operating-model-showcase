# AI Operating Model

A working pattern for running AI agents under enterprise security controls.

**Bottom line:** my AI agents work under the same kind of rules, gates, and audit trail I'd expect from a security program, and this repository shows how.

## What you'll find

- **Governance for multiple agents.** How agents claim work, stay in their own lanes, and log their own rule breaks in an incident ledger.
- **Approval gates and enforced controls.** What runs on its own, what waits for a human, and which controls a machine actually enforces.
- **Jarvis.** A personal AI on Rokid Glasses that I use as a real-world lab for guardrails and model testing.

![Control plane: AI agents act through a version-controlled governed layer with secrets injected at runtime, API budget gates, and an operating model whose rules and required checks live in GitHub, and consequential actions wait for the human owner's approval](diagrams/01-control-plane.png)

*The control plane: agents act through a governed layer, and anything consequential routes back to me for approval.*

## Featured: Jarvis

<a href="jarvis/README.md"><img src="jarvis/assets/rokid-glasses.jpg" alt="Rokid Glasses, the stock smart glasses Jarvis runs on" width="160" align="right"></a>

Jarvis is my personal AI assistant, built around Rokid Glasses. I also use it to test guardrails, try architecture ideas, and compare AI models, speech-to-text included, on accuracy and speed.

**[Explore Jarvis →](jarvis/README.md)**

<br clear="right">

## Why

AI agents are capable, but they forget everything between sessions and act with whatever access they are given. Without structure, they make unreviewed changes, burn through API quotas, and step on each other's work. This project treats agents as privileged operators. Their process lives in version-controlled files. Their changes go through a gated pipeline. Anything consequential waits for a human.

## What it covers

**Multi-agent governance and an incident ledger.** Each agent claims work before starting, works on its own branch prefix, and hands off with a link to a pull request, not a chat message. When an agent breaks a rule, the deviation is written up as an incident, and the incident feeds back into the rules.

**Human approval gates.** Routine, reversible work runs on its own. Sending messages, deleting anything, spending money, and publishing stop and wait for the owner. Outgoing messages are prepared as drafts. A declined request is final.

**Observability.** Agent commands should be visible and logged. Model calls routed through OpenRouter are traced in Opik. When something goes wrong, the logs and traces are the evidence, not the agent's own account.

## What is enforced vs. written policy

Not every control here is enforced by a machine yet. This table says which is which.

| Control | Status | How |
|---|---|---|
| Definition of Done, gitleaks secrets scan, and Markdown lint checks required before merge to main | Enforced | CI workflows run on every pull request, and the ruleset requires them |
| Prose style check (Vale) | Advisory | Runs on pull requests and leaves notes; it never blocks a merge |
| No bypass of the ruleset, including the owner | Enforced | Ruleset has an empty bypass list |
| Force-push and deletion of main blocked | Enforced | Ruleset rules |
| Tracing of model calls through OpenRouter | In place (monitoring, not a gate) | Opik tracing records calls; it does not block anything |
| Send and approval prompts for outgoing actions | Platform-enforced | Built into the agent platform |
| Agent claim and branch-ownership rules | Written policy | Shared rules card loaded on every run, plus incident ledger |
| Visible, logged commands for every agent | Written policy | Not yet enforced across all agents |
| Approval before publishing, deleting, spending money, or changing a calendar from email | Written policy | Followed by agents, reviewed through the ledger |

Closing the gap between written policy and enforcement is tracked as future work.

## How changes reach main

![Change gate: a change becomes a pull request, must pass the Definition of Done, gitleaks, and Markdown lint checks, then the no-bypass ruleset, before it reaches main](diagrams/02-change-gate.png)

*Every change takes one path to main, and a failed check sends it back for a fix.*

This repository uses the gate it describes. CI runs the Definition of Done check, the gitleaks secrets scan, and a Markdown lint on every pull request, and the main branch ruleset requires all three. The ruleset also blocks force-push and deletion, with no bypass. A Vale prose check runs too, as advice only. See [docs/ruleset.json](docs/ruleset.json).

## Repository layout

| Path | Contents |
|---|---|
| `docs/overview.md` | Full write-up: architecture, a case study on a shared control plane for rate-limited APIs, and lessons learned |
| `docs/ruleset.json` | Main branch ruleset applied to this repository |
| `jarvis/` | Jarvis, my personal AI on Rokid Glasses ([rundown](jarvis/README.md), [image credits](jarvis/assets/CREDITS.md)) |
| `diagrams/` | Diagram sources (SVG) and PNG exports |
| `.github/` | Pull request template and CI workflows |

## License

MIT. See [LICENSE](LICENSE).
