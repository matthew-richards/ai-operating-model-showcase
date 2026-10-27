# AI Operating Model: governing AI agents with security controls as code

![Control plane: AI agents run inside an agent sandbox (OpenShell) that confines files, processes, and system calls, with an API rate limit in the sandbox. Every network call leaves through the OpenShell supervisor, which checks policy and swaps in the real credential from the OpenShell provider store, fed at runtime by the secrets manager. Tool calls go to the MCP gateway, which checks tools, arguments, and caller, logs each call, and fronts one MCP servers group (for example GitHub, AI Operating Model, knowledge base). Model calls go to model providers (OpenRouter, Ollama). The Internet edge enforces limits outside the sandbox. The GitHub gate is the human gate: the owner approves PRs and merges. Opik traces model calls; the gateway tool-call trace is planned](../diagrams/01-control-plane.png)

*The control plane: OpenShell is the outer boundary, every tool call goes through the MCP gateway, and anything consequential routes back to me.*

## Problem

AI assistants are powerful but forget everything between sessions. Left ungoverned, an agent can make unreviewed changes, exhaust API quotas, or mishandle credentials. I wanted my own agents to run under the same controls I'd expect from an enterprise security program.

## Approach

I built a personal "operating model": a version-controlled layer of process docs, reusable skills, and state records. Agents read it for context and must follow it when they act. Chat is only the interface. The record lives in reviewable files.

## Governing multiple AI agents

I run multiple autonomous AI agents that work in the same repositories and on the same agile board on GitHub. Without rules, they would collide: editing the same branch, picking up the same task, or quietly overwriting each other's work. I treat them the way I'd treat any team of privileged operators. The rules are written per agent, not per pair, so adding another agent means giving it an owner identity and a branch prefix, not rewriting the policy.

- **Claim before work.** An agent claims an issue before starting it, and each issue or branch has exactly one owner. If two claims conflict, the earlier one wins.
- **Separation of work.** Each agent works on its own branch prefix and never edits another agent's open branch or pull request. Pull requests are the only merge path.
- **Shared hard rules.** Every agent loads the same rules card on every run, so their policy can't drift apart.
- **Evidence, not chat.** A handoff is a link to a pull request or issue. A chat message doesn't count as proof that work was done.

**Incident ledger.** When an agent breaks a rule, the deviation is written up as an incident covering what happened, why, and what changed. Each incident feeds back into the rules. Real incidents have exposed gaps, and core rules have been amended because of them. An agent logs its own deviations, even against rules it drafted.

**Status.** These rules are written policy, plus a ledger I review. They are not yet technically enforced, so an agent could still break one. That gap is tracked as future work.

## Human approval gates

Agents work on their own when the work is routine and reversible. Anything with real consequences stops and waits for me.

- **What needs approval.** Sending a message or email, deleting anything, spending money, publishing something publicly, and changing a calendar based on something an agent read in email.
- **What doesn't.** Drafting, researching, opening a pull request, and other work that can be reviewed or undone.
- **Drafts, not sends.** Outgoing messages are prepared as drafts I review and send myself. A request to "handle it" is never permission to send.
- **Visible waits.** Work that needs my decision gets a human-in-the-loop label on the agile board, so a pending approval is visible instead of silently stalling.
- **Refusals are final.** If I decline or don't answer, the agent doesn't retry or find another route to the same action.

**Status.** Send and approval prompts for outgoing messages are enforced by the agent platform. Approval before deleting, spending money, publishing, and changing a calendar from email is written policy that the agents follow.

## Observability

I can't govern what I can't see, so agent activity is meant to be visible and traceable after the fact.

- **Visible commands.** Policy requires agents to show every command in a visible terminal before it runs and log it with a timestamp. Hidden background commands are not allowed.
- **Traced model calls.** Model calls routed through OpenRouter are traced in Opik, an open-source LLM tracing tool, so the data can be used to compare models, catch quality drift, and keep spending in check.
- **Review, not trust.** When something goes wrong, the logs and traces are the evidence behind the incident ledger, not an agent's own account of what it did.

**Status.** Opik tracing is in place for OpenRouter calls. Visible and logged commands are written policy that the agents follow, and they aren't yet enforced across every agent.

## Architecture

- **Work taxonomy.** Every piece of work has an identity (`domain | workstream | subject | purpose`), so context, ownership, and status are never ambiguous.
- **API budget gates.** A small control plane tracks rolling-window budgets for each rate-limited API. Agents check it before bulk calls instead of finding the limit by hitting it.
- **Backup before mutation.** A restore path is recorded before any code or config change.
- **Blocker taxonomy.** Every wait is classified (human, vendor, or external), so stalled work stays visible instead of silently rotting.

![Change gate: a change becomes a pull request, must pass the Definition of Done, gitleaks, and Markdown lint checks, then the no-bypass ruleset, before it reaches main](../diagrams/02-change-gate.png)

*One path to main, with no bypass.*

## Case study: a rate-limited API collector

One of my projects collects data from a vendor API with strict rate limits. Going over them means throttling or lost data, and several agents may want to call the same APIs.

- **One control plane, many adapters.** A shared gate tracks rolling-window budgets for each rate-limited API through a small interface: acquire before a call, record the result, report a snapshot, and back off. GitHub has a full gate of its own, and the collector plugs in through an adapter that wraps its existing limiter instead of rewriting it.
- **Check before bulk calls.** Agents read the shared snapshot before a large batch of calls instead of finding the limit by hitting it.
- **One pattern, not many.** A new API gets a new adapter in the same place, not a parallel mechanism.
- **Visible budgets.** A combined snapshot feeds a regular digest, so quota use is reviewed like any other operating metric.

**Lesson.** Rate limits are a shared resource. Treating them as a control plane, instead of leaving each script to handle its own, keeps every agent inside the same budget.

## Security by design

- **Two layers for tool use.** They are separate controls with separate permission models. Both are tested, and now rolling out more widely.
  - **Agent sandbox ([OpenShell](https://github.com/NVIDIA/OpenShell)), the outer boundary.** The agents run inside it. It confines files, processes, and system calls, and every network call leaves through its supervisor. Rule changes wait for my approval.
  - **MCP gateway, the chokepoint for tool calls.** It sits outside the sandbox. It decides which tools an agent can call, with what arguments, and as which caller, and it logs each call. It fronts one group of MCP servers, such as GitHub, the AI Operating Model, and the knowledge base.
  - **Credentials stay out of the agent.** The real credential sits in OpenShell's provider store, and the supervisor swaps it in only for an approved destination.
  - **Rate limits on both sides.** API rate limiting runs in the sandbox. The Internet edge enforces limits outside it.
  - **Human gate.** I approve PRs and merges at the GitHub gate. Agents reach it through the pipeline, not through MCP.
  - **Known limits.** Responses aren't filtered yet, so I use only MCP servers I trust, each with its own least-privilege token. See [OpenShell's architecture](https://docs.nvidia.com/openshell/latest/about/architecture).
  - **Why both.** The gateway limits what an agent can ask for. The sandbox limits what it can touch if it ignores that or gets prompt-injected.
- **Observability.** Opik traces model calls from OpenRouter, Ollama, and local resources. Tracing gateway tool calls is planned.
- **One secrets store.** Credentials are injected at runtime from a secrets manager, to the sandbox's provider store only. Nothing is committed, and CI does not keep a second copy.
- **Least-privilege CI.** Pipeline jobs get a read-only token. Cloud access is off by default, and short-lived federated credentials are the only allowed pattern.
- **Controls are enforced, not suggested.** Every change includes a Definition of Done checklist. GitHub Actions checks that the list is present and fully ticked. Items are self-attested. A GitHub ruleset blocks force-push and branch deletion and allows no bypass, not even for me. The ruleset requires the Definition of Done, gitleaks secrets scan, and Markdown lint checks before merge.
- **Sensitive operational state** (quota counters, local data) is excluded from version control by policy.

## Lessons

- A control that can be skipped will be skipped, by agents and by people. Make the check mandatory.
- Keep knowledge and executable process in separate systems of record, or both decay.
