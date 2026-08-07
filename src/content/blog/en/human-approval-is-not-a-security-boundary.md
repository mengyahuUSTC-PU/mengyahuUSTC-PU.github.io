---
title: "409,000 clicks on Allow: why human approval fails as a security boundary for AI agents"
description: "A browser game logged 40,000+ sessions of people approving AI agent commands under time pressure. They missed a third of the malicious ones. From a content moderation perspective, the failure is built into per-command confirmation itself."
pubDate: 2026-08-06
tags: [ai-agents, ai-safety, human-in-the-loop]
lang: en
slug: human-approval-is-not-a-security-boundary
translationOf: human-approval-is-not-a-security-boundary
---

Engineer Alex Wauters recently built a browser game called [LLM Game](https://llmgame.scalex.dev). You play the human supervisor of an AI coding agent: commands appear one at a time (`git status`, `npm test`, `rm -rf`...) and you approve or deny each one before a timer runs out. Letting a malicious command through costs points. So does blocking a legitimate one. After the game landed on [Hacker News](https://news.ycombinator.com/item?id=48308376), it collected over 40,000 sessions and 409,000 individual approval decisions ([the data writeup](https://scalex.dev/blog/ai-agent-permissions-stats/)).

The results: players caught about two thirds of the threats and missed the rest. 32.9% of sessions ended with a negative score. 7% of players approved everything. Only 20.8% caught every threat while keeping their false-alarm rate at or below 20% of safe commands.

Who were these players? The writeup doesn't report demographics, so I can't give exact proportions. What's known is the distribution channel: the game spread through Hacker News. From that, my guess is the players were mostly developers and technical people. Not random visitors, not trained security reviewers, but roughly the population that clicks "Allow" on coding-agent prompts every day. If that guess holds, these scores describe the actual user base of agent approval dialogs.

Human-in-the-loop review, where a person confirms each sensitive action an AI takes, is often treated as the last line of defense for agent safety. In most coding agents today, a sensitive operation still ends in a dialog asking "allow this?". This dataset puts a number on how much that line of defense holds. I work in content moderation, and these numbers look familiar. The players weren't careless; per-command human confirmation has a ceiling, and this is what it looks like.

## What people caught, and what they let through

Broken down by threat type, miss rates form a clean gradient: obviously destructive commands, 11.7%; persistence attacks (changes that survive a restart, like editing a shell config file), 23.8%; data exfiltration and code execution, 33.4%; scope violations (commands that aren't destructive in themselves but exceed what the current task plausibly needs), 35.0%.

The single most-approved malicious command was `npm run analyze`: 64.7% of players let it through. The name sounds like static analysis. The script it invokes contains a curl call that ships local data to an external server. And the game's history log displayed the script's contents; one glance would have exposed it. The three npm scripts of this kind, harmless names wrapping malicious payloads, had a pooled miss rate of 52.5%, against 28.4% for other exfiltration attacks. A friendly name nearly doubled the miss rate.

Meanwhile, legitimate commands got blocked in bulk. `npm config set registry`, a routine way to switch npm mirrors, was denied by 59% of players. `rm -rf dist/`, deleting a build output directory, was denied by 45%.

Put together, the two patterns point at one diagnosis: under time pressure, people judge what a command looks like, not what it does. `rm -rf` looks scary, so it gets blocked. `npm run analyze` looks harmless, so it gets approved. The script contents sitting right there in the log? Available information and used information are two different things.

## Why this happens

**First, the rarer the threat, the worse humans are at seeing it.** In the game, roughly 34% of commands were threats, one in three. Visual search research quantified this "low-prevalence effect" long ago: in [Wolfe, Horowitz and Kenner's 2005 Nature experiment](https://www.nature.com/articles/435439a), observers missed 7% of targets when targets appeared 50% of the time, and 30% when prevalence dropped to 1%. Airport baggage screening and radiology both wrestle with the effect ([a 2007 follow-up study](https://pmc.ncbi.nlm.nih.gov/articles/PMC2662480/) examines those two settings specifically). No one has published a measurement of malicious-command prevalence in real agent workflows; my inference is that it sits far below 1%, since most developers may go months without encountering one. On that inference, the game is the easy mode: players knew they were being tested and knew threats were dense. Real approvers face a far sparser threat stream, and the low-prevalence effect points one way, toward a real-world miss rate higher than the game's.

**Second, approval buttons train muscle memory.** After a few dozen harmless commands in a row, "Allow" stops being a judgment and becomes a motion. The game data shows the trend: players improve over their first several commands, then miss rates climb steadily. The author is careful to note this could also be timer stress rather than pure fatigue. Content moderation treats reviewer attention as a consumable. Standard practice is shift rotation, random spot checks, and seeding the queue with known-answer test items to monitor reviewer state. Those mechanisms cost real money, and they exist precisely because the industry accepts that attention runs out. Agent approval dialogs hand the same cognitive load to every developer with essentially none of that. Some products reduce prompt counts with auto-approve rules, but for the decisions that do reach a human there is no rotation and no spot check. In the game, 7% of players approved everything. The real-world counterpart is users flipping on the skip-approvals switch (Claude Code's [`--dangerously-skip-permissions`](https://code.claude.com/docs/en/permission-modes) is one example). Same logic: once confirmations outrun the attention budget, people surrender judgment wholesale.

**Third, many commands have no context-free right answer.** The most divisive command in the game was `cat ~/.zshrc`, reading the shell config file: 45.9% approved it. Should they have? Depends on the task. An agent debugging your terminal setup obviously needs to read your shell config. An agent writing a web scraper reading it is alarming. Anyone in content moderation knows this shape: on borderline items, annotators disagree, because the deciding information lives in the context, not in the item itself. An approval dialog carries very little context, usually the command text plus a one-line explanation, with the task-level context mostly stripped away. Asking someone to make the "correct" call on a context-free command in two seconds is an ill-posed demand.

## What this means for agent permission design

The conclusion first: per-command human approval is an audit tool, not a security boundary. Its real value is leaving a decision trail for later investigation, and bringing human judgment to a small number of genuinely high-stakes moments. Treating it as the main line of defense stakes your security on an assumption the research has falsified over and over: that humans can stay alert for rare threats inside a stream of mostly-safe decisions.

Why isn't "users should pay more attention" a fix? Because the failure is structural. Attention is finite and command volume keeps growing. An agent that runs a few hundred commands a day, each reviewed seriously, turns the developer's entire job into approvals. The arithmetic fails before the attitude does.

The data itself sketches the workable directions.

Shrink the stream that reaches a human. Deterministic rules go first: read-only and allowlisted commands are approved automatically, and only decisions that need judgment reach a person. Claude Code's [tiered permissions](https://code.claude.com/docs/en/permissions) (read-only operations skip review, shell commands pass through rules) is one instance of this idea. But the low-prevalence effect cuts back here: the cleaner the stream, the rarer and harder to see the remaining threats, so every decision left to the human has to arrive with full context.

Show consequences, not command text. The `npm run analyze` episode shows that putting the payload in a log and hoping someone reads it accomplishes nothing. An approval interface should answer directly: what will this command read, what will it write, where will it send data. Let people judge effects instead of guessing at semantics.

Structural containment as the backstop. The game's author recommends the same: sandboxed execution, isolating credentials and environment variables, restricting network egress. None of these depend on a human staying sharp. Their job is to keep the damage inside the box when a malicious command does get approved.

Agent permission design is retracing a path content moderation already walked: treat human judgment as a scarce resource, spend it where it's actually needed, and stop spreading it evenly across every item. The difference is who's doing the clicking. Content moderation staffs trained reviewers, with rotations and spot checks behind them. Agent approval dialogs get a developer trying to wrap up before dinner.

## References

- [Statistics on AI agent permissions (scalex.dev)](https://scalex.dev/blog/ai-agent-permissions-stats/) — full game data: 40,000+ sessions, 409,000 decisions, miss rates by category, false-positive rates, fatigue trends, and the author's notes on limitations
- [LLM Game](https://llmgame.scalex.dev) — the game itself
- [Hacker News discussion](https://news.ycombinator.com/item?id=48308376) — how the game spread
- [Wolfe, Horowitz & Kenner, "Rare items often missed in visual searches", Nature (2005)](https://www.nature.com/articles/435439a) — the low-prevalence effect: 7% miss rate at 50% target prevalence, 30% at 1%
- [Wolfe et al., "Low target prevalence is a stubborn source of errors in visual search tasks", J. Exp. Psychol. General (2007)](https://pmc.ncbi.nlm.nih.gov/articles/PMC2662480/) — the low-prevalence effect in airport baggage screening and medical screening
- [Claude Code permissions documentation](https://code.claude.com/docs/en/permissions) — an instance of tiered permissions
- [Claude Code permission modes documentation](https://code.claude.com/docs/en/permission-modes) — bypassPermissions mode and the corresponding CLI flag
