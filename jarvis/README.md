# Jarvis: a personal AI assistant that runs at home and gets checked

Jarvis is my personal AI assistant. It runs on a home PC with a GPU, not in someone else's cloud, and it works alongside a second AI agent. Each one checks the other's work before anything counts as done.

This is the story so far. It covers the narrative and early design notes. Code comes later.

![Jarvis at a glance](assets/jarvis-architecture.svg)

## What Jarvis does today

- **Runs as a gateway at home.** Jarvis takes requests over chat and a local API, and runs its own scheduled jobs.
- **Keeps a notes vault in sync.** A job syncs my notes vault every 15 minutes so my phone and PC stay in step.
- **Supervises.** Every few hours it sweeps the project board and CI, and re-checks "Done" claims against live data.
- **Compares models.** A weekly job tests hosted models against local ones running on the GPU.

## What makes it interesting

### Two agents that check each other
Jarvis is the supervisor; a second agent handles execution. Neither one gets to sign off on its own work. A "Done" claim needs the observed result to match the expected result, plus a link to the proof. Each agent works on its own branches and labels, so you can tell who did what.

### It writes up its own mistakes
On Sep 30, 2026, Jarvis made some project-board changes that were outside its agreed role. It filed a blameless incident report on itself, named the root cause (a chat request read more broadly than the written agreement allowed), and turned the lesson into a rule: chat instructions never widen its role.

### The watchdog lives outside the thing it watches
On Oct 3, 2026, a chat command stopped the Jarvis gateway. The step that was supposed to restart it ran inside the same process, so it died too. A separate session noticed and brought it back about four minutes later. The fix was a watchdog run by the operating system's task scheduler, outside the gateway. It relaunches only after two failed checks in a row, and waits an hour between relaunches so it can't get stuck in a crash loop. The lesson: a watcher has to live outside the failure's blast radius.

### Spending has a hard cap
The cloud model key Jarvis uses has a hard spending limit set at the provider, and heavy jobs check the remaining balance before they run. In an earlier sandbox trial, a budget hard stop paused an agent when its reported cost hit the cap.

### The sandbox was tested, not just configured
On Sep 30, 2026, I trialed an agent sandbox on the home PC. It passed 10 of 10 enforcement tests: outbound traffic blocked by default, per-program network rules, a blocked HTTP POST, filesystem lockdown, and an audit trail of every connection attempt. Sandboxes started in about 1 to 2 seconds. A real agent hasn't run inside it yet, and that speed may be too slow for voice replies.

## The glasses

![Rokid Glasses](assets/rokid-glasses.jpg)

The next step is giving Jarvis a face, or rather a pair of eyes and ears. The plan is to connect it to [Rokid Glasses](https://store.rokid.com/products/rokid-glasses), lightweight AI glasses with a display, camera, and microphones. Jarvis would register as a custom agent through Rokid's supported agent path. No sideloading, and the glasses and the Rokid app stay stock. A small bridge on the home PC handles authentication and filters out stray wake words before passing requests to Jarvis. This part is a prototype, not shipped.

Getting the glasses was its own project. When I went to buy them, ordering directly for US delivery wasn't a reliable option, and eBay ended up being the best way to get a pair. I wasn't alone. Other US buyers [reported the same checkout problem in March 2026](https://www.reddit.com/r/rokid_official/comments/1rwc06j/rokid_glasses_not_shipping_to_the_united_states/), and at least one also bought from eBay. Rokid has since [said it is expanding US retail](https://www.globenewswire.com/news-release/2026/03/12/3255022/0/en/rokid-highlights-its-u-s-retail-strategy-at-vision-expo-2026.html), so this may be easier now.

## What's still open

- Jarvis still uses a broad personal access token. A narrower, Jarvis-only token is designed but not created yet.
- Some long-lived cloud credentials remain on the home PC and are planned to be replaced.
- The sandbox hasn't been tested with a real agent inside it.
- The orchestrator role is a trial.
- A daily self-improvement loop (log friction, propose wording fixes, ask before any rule change) is a draft awaiting approval.

## More

- [Architecture](docs/architecture.md)
- [Lessons learned](docs/lessons-learned.md)
- [Image credits](assets/CREDITS.md)
