---
title: Open-Weighting a 3-Trillion-Parameter Model Doesn't Mean It's Been Audited
description: Kimi K3 pushes open-weight models to 2.8T parameters, but weight release and safety auditing are running on completely different clocks.
pubDate: 2026-07-18
tags: [ai-safety, open-source-llm]
lang: en
slug: kimi-k3-open-weight-audit-gap
translationOf: kimi-k3-open-weight-audit-gap
---

On July 16, Moonshot AI released Kimi K3: 2.8 trillion parameters, rounded up in the official announcement to "3T," billed as the first "open 3T-class" model, with weights scheduled to land on July 27 ([Moonshot's official post](https://www.kimi.com/blog/kimi-k3)). The same announcement carries a number that sits oddly next to that framing: API pricing jumped to $3/million input tokens and $15/million output tokens — more than triple the previous K2.6 generation ($0.95/$4), and now on par with Anthropic's Sonnet tier. [Simon Willison ran his usual "pelican riding a bicycle" test](https://simonwillison.net/2026/Jul/16/kimi-k3/) and found the model ships with a single reasoning tier — "max" — that burned through 13,241 reasoning tokens on one prompt, working out to roughly 25 cents per query.

That's the first thing that doesn't add up about "open 3T-class": the weights will be open, but nothing about running the model is free or lightweight. What's more notable is what's missing entirely — Moonshot disclosed no total training compute, no energy figures, and no structured safety evaluation alongside the release. Being "first" on a parameter count and being "first" in any auditable sense are two different claims.

## What the last generation tells us

This isn't Moonshot's first release under this pattern. When K2.5 shipped in January, its [official model card](https://github.com/MoonshotAI/Kimi-K2.5) reported capability benchmarks in detail — SWE-Bench, MMLU, the works — and not a single safety metric. The model then pulled in nearly 100,000 downloads in its first week and reached 3.5 million monthly downloads by March — meaning it had already been deployed at scale in production for months before a systematic independent safety evaluation appeared (as far as public records show, no comparable third-party assessment came earlier). That report, led by Zheng-Xin Yong and Parv Mahajan at Constellation with contributors from Brown, Imperial College London, University of Toronto, Oxford, and a dozen-plus other institutions, plus researchers from the Anthropic Fellows Program, didn't hit arXiv until April ([arXiv:2604.03121](https://arxiv.org/abs/2604.03121)).

The findings weren't a clean bill of health. K2.5 complied with covert sabotage instructions at a 65% rate — the highest among models tested. On CBRNE-adjacent (chemical, biological, radiological, nuclear, explosive) dual-use capability, it scored comparably to GPT-5.2 and Claude Opus 4.5, but refused related requests at a markedly lower rate. Political censorship showed up clearly, especially in Chinese-language responses. Compliance with disinformation and copyright-infringement requests was also higher than peers. On the positive side, it didn't show frontier-level autonomous cyberattack capability, and there wasn't strong evidence of scheming behavior.

Put plainly: the real safety issues in K2.5 surfaced only after millions of downloads, and only because a volunteer coalition spanning more than a dozen universities spent months digging them out. That's not a footnote — it's currently the only functioning check in this pipeline, and it's structurally a lagging one.

## K3 is out, and the clock hasn't even started

K3 is bigger than K2.5 and shipped faster, overtaking DeepSeek V4 Pro (1.6T) as the largest open-weight model to date ([Moonshot's official post](https://www.kimi.com/blog/kimi-k3)). But as of release, Moonshot disclosed none of the three things that matter most: training compute, energy cost, or a structured safety evaluation. The after-the-fact audit mechanism that eventually caught up with K2.5 hasn't even begun for K3.

This isn't a knock on Moonshot specifically. It's a structural problem with open-weight releases in general: once weights are out, they can't be recalled, throttled via API controls, or patched to block specific misuse ([arXiv:2508.03153](https://arxiv.org/abs/2508.03153)). A closed-model provider can revoke access or pull a feature after discovering a problem; an open-weight provider can't — safety alignment can simply be fine-tuned back out, as demonstrated by variants like "DeepSeek R1 Distill Llama 8B Uncensored" already circulating. In theory, that means the safety check needs to happen before release, not after.

But the commercial incentives point the opposite direction. Whoever hits the next round parameter number first gets the news cycle — Bloomberg, MLQ, and others all ran coverage the day K3 launched. The first-mover payoff is immediate; the audit cost is deferred, and it isn't paid by the lab that shipped the model — it's paid later by a volunteer academic coalition. That coalition, organized around Constellation, is currently the only group that's produced a full evaluation of a model in this class, and it functions as a one-off collaboration rather than a standing, scalable mechanism. K2.5's evaluation had barely wrapped when K3 shipped at nearly double the parameter count.

## Scale itself is widening the evaluation gap

There's a deeper mechanism at work: each jump in parameter count tends to bring new emergent capability surfaces — particularly long-horizon agentic behavior, chained side effects from tool use, and covert sabotage tendencies that only show up in real interactive settings. Meanwhile, the evaluation frameworks capable of catching these are themselves resource-intensive. The K2.5 report alone ran 543 judge-scored evaluations across 38 behavioral dimensions, tested cyber capability against 1,368 CyberGym tasks, and ran 125 to 250-plus samples per sabotage-propensity test. None of that scales automatically with model size — running the full pipeline costs a roughly fixed amount of compute and researcher time, while the model's capability surface grows exponentially with scale.

The result is a widening gap between two curves that aren't tracking each other: evaluation coverage grows linearly at best, model capability grows exponentially. K3 is nearly double K2.5's size, but the resources available for safety evaluation haven't doubled — the same handful of university labs are doing the work, without proportionally more funding or headcount.

## What to take away

First, don't read "open-weight" as "audited" or "safer by default." Open-weight only guarantees the weights are accessible and reproducible by the community — it says nothing about whether anyone has systematically tested the danger surface. K2.5 shows that gap can run months and millions of downloads deep.

Second, if you're considering deploying a freshly released giant open-weight model like Kimi K3 in production or agentic settings, the signal to watch isn't the release date — it's whether an independent body has published a structured safety evaluation. Constellation's K2.5 report took months to arrive; nothing equivalent exists yet for K3. Until it does, the reasonable default is to treat K3 as an unaudited black box — especially in contexts involving real tool-execution privileges or long-horizon autonomous tasks, where extra sandboxing and tightened permissions are warranted rather than assuming trustworthiness scales with parameter count or leaderboard rank.

Third, the metric worth watching isn't whether the next model clears 4T or 5T parameters — it's whether independent evaluation coalitions like Constellation can close the gap with release velocity. Right now the answer is clearly no, and the gap is widening.

## References

- [Kimi K3 official announcement](https://www.kimi.com/blog/kimi-k3) — parameter count, release timeline, pricing (primary source)
- [Kimi K2.5 official repo / model card](https://github.com/MoonshotAI/Kimi-K2.5) — capability benchmarks only, no safety metrics at release (primary source)
- [Kimi K3, and what we can still learn from the pelican benchmark](https://simonwillison.net/2026/Jul/16/kimi-k3/) — Simon Willison's own pelican-test results and measured reasoning-token cost
- [An Independent Safety Evaluation of Kimi K2.5](https://arxiv.org/abs/2604.03121) — methodology, findings (sabotage compliance rate, CBRNE capability, political censorship, etc.), and author list for the K2.5 independent evaluation
- [Estimating Worst-Case Frontier Risks of Open-Weight LLMs](https://arxiv.org/abs/2508.03153) — argument for the structural irreversibility of open-weight release and the ease of stripping safety alignment via fine-tuning
