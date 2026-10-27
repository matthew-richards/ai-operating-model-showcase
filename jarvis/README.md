# Jarvis: a personal AI that goes where I go

Jarvis is my personal AI assistant. The goal is simple: an AI that helps me wherever I'm wearing my glasses. It's also the real system I use to test guardrails, try out architecture ideas, and compare AI models on accuracy and speed, including speech-to-text.

![Rokid Glasses](assets/rokid-glasses.jpg)

The front end is a pair of stock [Rokid Glasses](https://store.rokid.com/products/rokid-glasses): lightweight AI glasses with a display, camera, microphones and a speaker. Jarvis registers as a custom agent on Rokid's supported agent platform, so I say "Hi Rokid, open Jarvis" and nothing on the glasses has to be modified or sideloaded. The glasses link is still a prototype.

## How it works

![How Jarvis works](assets/jarvis-architecture.svg)

1. **Voice in.** I speak to the glasses. Speech-to-text currently runs on Rokid's cloud speech recognition. The transcript arrives with a callback from Rokid's cloud.
2. **Cloudflare as the front door.** The callback doesn't reach my hardware directly. It lands on Cloudflare's edge, where a web application firewall and Cloudflare Access check it first. A Cloudflare Tunnel then carries it home. The tunnel dials *out* from my hardware, so no inbound ports are open and nothing at home listens on the internet. The app checks its own credentials and an allowlist too, so passing the edge isn't enough on its own. The front door is designed to be swappable, so Cloudflare could be replaced later without touching the glasses or the bridge.
3. **A containerized bridge.** A small bridge service in a container translates between Rokid's agent protocol and an OpenAI-compatible model interface. It streams the answer back to the glasses as it's generated, so the display and speaker start responding before the full answer is done.
4. **Model routing: local first.** The bridge talks to a local model first (Ollama on my own GPU) and can use hosted cloud models when a task needs them. Because the interface is standard, swapping models is a configuration change, not a rewrite.
5. **Answer out.** The response streams to the glasses' display and speaker, formatted for a small heads-up display: one main message and only a few steps.
6. **Memory and notes.** Jarvis keeps its own memory, and my notes vault stays in sync on a schedule, so what I capture on the go ends up with the rest of my notes.
7. **GitHub as home base.** The bridge code, design docs, runbooks and decision records live on GitHub. Changes go through pull requests with automated checks, and work is tracked on a project board.

## Guardrails, and where they act

Jarvis is something I actually depend on, so it's a good place to test guardrails on something real instead of a demo.

- **At the edge:** Cloudflare filters and authenticates traffic before it reaches home, and the app checks credentials again on its own.
- **Around actions:** I evaluated a container-based sandbox for running tools and actions. It passed all 10 enforcement tests, including blocking outbound traffic by default, per-program network rules, filesystem lockdown and a full audit trail. Sandboxes started in about 1–2 seconds, which matters when a voice reply needs to land in a few seconds.
- **Around spending:** Cloud model use has a hard spending cap, and heavy jobs check the remaining budget before they run.
- **Around uptime:** After an outage, Jarvis got a watchdog that runs outside the system it watches. It only acts after repeated failed checks, and it waits between restarts so it can't loop.
- **Around its role:** When Jarvis once went beyond its agreed role, it wrote a blameless report on itself and the lesson became a written rule. Corrections become rules, not reminders.

## Experimenting with architecture

Jarvis is also a living lab for designing a personal AI:

- **Local vs cloud.** What runs on my own GPU, and what's worth sending to a hosted model.
- **Swappable parts.** The front door, the model, and the speech-to-text stage all sit behind standard interfaces, so I can trade one out and compare.
- **Latency budget.** A voice turn has to feel instant, so every piece (edge, tunnel, sandbox, model) is judged by what it adds to the response time.

Some experiments stick and some get dropped. Either way, I learn from a system I use every day.

## Testing AI models

Jarvis also gives me a real-world way to compare AI models on **accuracy and speed**:

- **Language models.** A scheduled weekly sweep runs the same tests across a set of hosted models and my local models. It flags any model whose results drift from the previous run and picks up newly released models.
- **Speech-to-text.** Wearing the glasses means real-world voice testing, so I can compare speech-to-text models on how accurately and how quickly they understand me.

## Getting the glasses

Getting the glasses was its own project. When I tried to buy them, ordering directly for US delivery wasn't a reliable option, and eBay ended up being the best way to get a pair. Other US buyers [reported the same checkout problem](https://www.reddit.com/r/rokid_official/comments/1rwc06j/rokid_glasses_not_shipping_to_the_united_states/), and Rokid has since [said it is expanding US retail](https://www.globenewswire.com/news-release/2026/03/12/3255022/0/en/rokid-highlights-its-u-s-retail-strategy-at-vision-expo-2026.html).

[Image credits](assets/CREDITS.md)
