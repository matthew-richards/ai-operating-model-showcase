# Jarvis: a personal AI assistant that gets checked

Jarvis is my personal AI assistant. It runs on my own hardware and works alongside a second AI agent. Each one checks the other's work before anything counts as done.

This page covers the story so far. Code comes later.

![Jarvis, conceptually](assets/jarvis-architecture.svg)

## What makes it interesting

- **Two agents check each other.** Jarvis reviews, and a second agent executes. Neither one signs off on its own work, and "done" needs proof.
- **It learns from its own mistakes.** When Jarvis stepped outside its agreed role, it wrote a blameless report on itself and turned the lesson into a rule.
- **It recovers on its own.** After an outage, Jarvis got a separate watchdog that brings it back if it goes down.
- **Spending has a hard cap.** Cloud model use has a firm limit, so a runaway job can't run up a bill.
- **It was tested in a sandbox.** Before trusting agents with real actions, I ran a sandbox trial that passed all of its enforcement tests.

## The glasses

![Rokid Glasses](assets/rokid-glasses.jpg)

The next step is giving Jarvis eyes and ears through [Rokid Glasses](https://store.rokid.com/products/rokid-glasses), lightweight AI glasses with a display, camera, and microphones. The plan is to connect Jarvis through Rokid's supported agent path, so the glasses stay stock. This part is still a prototype.

Getting the glasses was its own project. When I tried to buy them, ordering directly for US delivery wasn't a reliable option, and eBay ended up being the best way to get a pair. Other US buyers [reported the same checkout problem](https://www.reddit.com/r/rokid_official/comments/1rwc06j/rokid_glasses_not_shipping_to_the_united_states/), and Rokid has since [said it is expanding US retail](https://www.globenewswire.com/news-release/2026/03/12/3255022/0/en/rokid-highlights-its-u-s-retail-strategy-at-vision-expo-2026.html).

## More

- [Lessons learned](docs/lessons-learned.md)
- [Image credits](assets/CREDITS.md)
