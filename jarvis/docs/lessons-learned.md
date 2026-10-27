# Lessons learned

Each lesson came from a real incident or trial and was turned into a written rule. These are rules the agents follow (policy), not enforced technical controls, unless noted.

## 1. Chat steering doesn't widen an agent's role (Sep 30, 2026)
**What happened:** I asked Jarvis to "put it on the board." It created and updated board items itself, even though board status moves belong to the execution agent.
**Root cause:** The working agreement was written that same day, and the task ran before Jarvis had absorbed the new role rules. A broad token also made the writes possible.
**Rule:** When a task starts or finishes a piece of work, Jarvis writes the brief as a pull request and the execution agent puts it on the board. Jarvis reported the mistake on itself, blamelessly.

## 2. Watchers live outside the blast radius (Oct 3, 2026)
**What happened:** A chat-issued stop shut down the gateway. The relaunch step belonged to the agent inside that process, so it never ran. Chat was down for about four minutes until a separate session noticed. This was the third failure of this kind.
**Rule:** Agents inside the gateway never do a stop-then-relaunch from chat; they use the built-in restart command. Unattended recovery belongs to the watchdog, which the OS scheduler runs (enforced).
**Side lesson:** Check the tool's built-in commands before building new tooling. The built-in restart existed but went unused.

## 3. Test the sandbox, don't just trust it (Sep 30, 2026)
The sandbox trial passed 10 of 10 enforcement tests. About five provisioning attempts failed first, all traced to one networking setting that's now documented. Not everything was tested, and the write-up lists what wasn't.

## 4. Spending needs a hard stop, not a reminder
The cloud key has a provider-side limit (enforced by the provider), and jobs check the balance first. An earlier trial confirmed a budget hard stop pauses an agent when it hits its cap.

## 5. Corrections should become rules (draft)
A proposed loop: when I correct an agent, it files a rule-change proposal within 24 hours. Wording fixes can batch. Real rule changes wait for my explicit yes, capped at three a day, and a silent digest never counts as consent. This is still a draft.
