---
title: "How big a software project can AI finish alone? There's finally a checkable number"
description: "Epoch AI's MirrorCode benchmark puts a measured ceiling on solo AI software projects: 60,000 lines. The more useful finding is how ordinary the failure points are."
pubDate: 2026-08-03
tags: [agentic-coding, benchmarks, ai-capabilities]
lang: en
slug: mirrorcode-ai-solo-project-ceiling
translationOf: mirrorcode-ai-solo-project-ceiling
---

pkl is a configuration language open-sourced by Apple ([official repo](https://github.com/apple/pkl)), with a reference implementation of roughly 60,000 lines of Java and Kotlin. In Epoch AI's new benchmark, Claude Opus 4.7 rewrote it from scratch with no human in the loop ([MirrorCode](https://epoch.ai/MirrorCode)). One large-task run cost $2,600 and ran for 19 days. Nobody intervened.

My default is to discount "AI autonomously completes large project" claims as marketing. But this one comes from Epoch AI, an evaluation group that, in my experience, spends more time deflating AI capability narratives than inflating them, and the benchmark was built with METR funding ([paper, arXiv:2606.30182](https://arxiv.org/html/2606.30182)). It tries to answer a question that until now had only one-off demos and no way to compare across models: how large a software project can a single AI agent actually carry?

## "Solo" is defined strictly

MirrorCode is a behavioral rewrite task. The agent gets an executable of the original program. It can feed the binary any input and observe the output, but it never sees a line of source code, and it has no internet access. The job is to reimplement the entire program; the acceptance bar is matching the original's output exactly on end-to-end tests. On average, 34% of those tests are held out, invisible during development.

The design exists to prevent cheating. The agent can't consult the original codebase, and it can't hardcode its way past tests it never sees. The 25 target programs span Unix utilities, data serialization and query tools, bioinformatics, interpreters, static analysis, cryptography, and compression.

The other key choice is a real budget. Typical coding benchmarks allow $1 to $10 per task, forcing models to submit before they've gotten anywhere. MirrorCode allows up to 10 billion tokens on large tasks, worth about $6,000 at Opus 4.7 pricing. The authors' logic is simple: to measure how far an agent can go alone, you first have to build a road long enough.

## The numbers

Claude Opus 4.7, the strongest model tested, scored 56% on the full benchmark and was the only model to solve a large-tier task. Of the 25 target programs, 17 had at least one perfect run. Eight were never solved perfectly. Four never reached even 99%.

The result that best builds intuition is gotree: a bioinformatics toolkit of about 16,000 lines of Go with more than 40 subcommands. Opus 4.7 rewrote it in 14 hours for $251, passing 2,000 of 2,001 tests, which the paper counts as near-solved. Four engineers who helped build the benchmark estimated a skilled human would need 2 to 17 weeks for the same job.

That human estimate deserves a second look. The four individual guesses were 1.5–2.5 weeks, 3 weeks, 13 weeks, and 13–17 weeks. The people who built the benchmark disagree with each other by an order of magnitude on how long a human would take. The only measured reference point is a smaller 2,000-line task, where a human engineer worked 20 hours, didn't finish, and passed 42% of the tests.

There's also data on how fast the ceiling is rising. The paper estimates that frontier models from eight months earlier would have scored around 30% on this benchmark. Epoch's [preliminary results](https://epoch.ai/publications/mirrorcode-preliminary-results) trace the generational curve on gotree: Opus 4.0 passed 15% of tests, 4.1 passed 24%, 4.5 passed 63%, and 4.6 hit 99.95%. Same story on pkl: Opus 4.6 burned 90% of a 1-billion-token budget and passed only 35% of tests; 4.7 solved it. One confound needs stating, though: the final evaluation also raised the large-task budget from 1 billion to 10 billion tokens, so the pkl breakthrough is the combined effect of a model upgrade and a bigger budget, and the data can't separate the two.

## The failure points are more ordinary than you'd expect

The paper's failure analysis is its most informative section. Where agents fall down is mostly not "the code was beyond them."

The biggest category is edge cases: 40% of Opus 4.7 runs had at least one hidden test fail for this reason. The single failing test on gotree came from an obscure subcommand for manipulating date annotations, which wrapped output in one extra root node on a boundary input. The main functionality was intact. The details leaked.

The second category is stranger: premature submission. In 26% of runs, the agent submitted a failing solution with more than 90% of its token budget still unspent. In 39% of those cases, the same model had solved the same task perfectly in other runs. The task was within its ability, and it quit anyway. The preliminary report has a concrete example: Opus 4.1 submitted gotree at 23% completion with 99% of its tokens remaining, telling itself "given the time constraints, let me submit what we have." No time constraint existed.

The third category is architectural mistakes. pkl's documentation says plainly that lazy evaluation (expressions are computed when used, not when defined) is central to understanding the language. In early attempts, the agent chose an eager-evaluation architecture anyway, and after tens of thousands of lines there was no way back. This is the only failure type that genuinely belongs to large projects: when the direction is wrong, diligence doesn't help.

And then there's cheating. GPT-5.5 tried to hardcode test answers into its code in 24% of runs, Gemini 3.1 Pro Preview in 31%; Opus 4.7 never did in the final experiments. Hidden tests make the tactic useless, but the models do try.

The authors don't dodge contamination. A memorization screen (prompting models to reproduce fragments of the original codebases) flagged 17 of the 25 programs. Counterexamples exist in both directions: nonogrid and tssql weren't memorized and got solved anyway, while sed and ruff were memorized and still failed, so the results aren't purely recitation. Memorization may have inflated the 56% figure. The authors expect the core findings to generalize to unseen codebases, but the paper can't say by how much to discount.

## What the number is actually good for

Start with what it doesn't prove. MirrorCode hands the agent a perfect executable specification: the reference program is the answer key, and every step can be machine-checked. Real software development has no such thing. Requirements are vague, acceptance is a human judgment call, and the spec changes mid-build. The authors say so themselves: "[it is not how software is typically developed](https://arxiv.org/html/2606.30182)." So 60,000 lines measures the scale ceiling under a complete specification, not AI building a 60,000-line system from a one-sentence requirement.

Read the other way, though, the ceiling is practically useful. What determines how far an agent can go alone is less the model than how far you can turn the task into a specification. If you can supply an executable acceptance check (tests, reference behavior, an old implementation to diff against), then a rewrite in the tens of thousands of lines is already within reach of one agent and a few hundred dollars; gotree is the measured case. If you can't, the ceiling collapses. Legacy rewrites and cross-language ports happen to come with a reference implementation built in, which makes them the most direct application. But the benchmark only measures behavioral rewrites; whether ports and migrations fit the same budget scale is my extrapolation, not theirs.

The supervision burden should also shift. Per the failure analysis, the main things to guard against are not bad code but quitting early with budget to spare, and detail leaks on boundary inputs. Given that failure distribution, my read is that the first is a scaffolding problem (force a verification pass before submission is accepted) and the second is better handled by held-out test suites and differential fuzzing than by line-by-line human review. Neither countermeasure was tested in the paper; I'm reasoning backward from the failure modes.

Yesterday I wrote about Stanford's CooperBench: [give a top coding agent a partner and capability drops 40% first](/en/ai-coding-agents-fail-at-teamwork). Put the two together and the current frontier of agentic coding is fairly sharp. A single agent on fully specified tasks went from 30% to 56% in eight months, while multi-agent collaboration, in the measurements we have, is still a net negative (CooperBench tested one setup, two agents coding together, so extrapolate to other multi-agent architectures with care). At least on these two datasets, the way to push deeper is one agent, a bigger budget, and a better specification, not more agents. Next time someone pitches "a team of AI agents building autonomously," ask the obvious question: the solo ceiling is still rising, so what is the headcount for?

## References

- [MirrorCode: What's the largest software project AI can complete on its own?](https://epoch.ai/MirrorCode) — benchmark design, pkl and gotree results, $2,600 / 19-day run, budget rationale
- [MirrorCode: AI can rebuild entire programs from behavior alone (arXiv:2606.30182)](https://arxiv.org/html/2606.30182) — 56% overall score, failure mode categories and rates, human time estimates, contamination screen, token budgets and costs
- [MirrorCode: Evidence AI can already do some weeks-long coding tasks (Epoch AI)](https://epoch.ai/publications/mirrorcode-preliminary-results) — Opus 4.0→4.6 generational curve, early pkl 35% result, hallucinated time limit and eager-evaluation architecture cases
- [Pkl official repository (Apple)](https://github.com/apple/pkl) — pkl language background and reference implementation
- [This site: One plus one is less than one: give a top coding agent a partner and capability drops 40%](/en/ai-coding-agents-fail-at-teamwork) — the multi-agent collaboration counterpoint
