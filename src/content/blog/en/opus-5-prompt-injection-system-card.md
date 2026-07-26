---
title: "Is Prompt Injection Getting 'Solved'? The Page Anthropic Buried in the Opus 5 Launch"
description: "Opus 5 cuts indirect prompt injection success to 2% — a number that appears nowhere in the launch announcement, only on page 73 of the system card. How to read it, and how far it is from 'solved.'"
pubDate: 2026-07-24
tags: [prompt-injection, ai-safety, agent-security]
lang: en
slug: opus-5-prompt-injection-system-card
translationOf: opus-5-prompt-injection-system-card
---

Anthropic released [Claude Opus 5](https://www.anthropic.com/news/claude-opus-5) on July 24. The announcement is a standard capability narrative: new state-of-the-art results on Frontier-Bench and GDPval-AA, an ARC-AGI 3 score three times the next-best model, and a line about it being "our most aligned model to date."

But if you work on agent security, the most important information in this release isn't in the announcement at all. I read the whole thing; the phrase "prompt injection" never appears. It lives in Section 5.2 of the [system card](https://www.anthropic.com/claude-opus-5-system-card), pages 71 through 76. Even Anthropic's own people found this odd. Boris Cherny — creator of Claude Code, per Anthropic's [official event page](https://www.anthropic.com/webinars/claude-code-service-delivery) — [posted on X](https://twitter.com/bcherny/status/2080713091688583312) after the launch:

> "Opus 5 is our least prompt injectable model yet. It is a bit buried in the system card, but across PI evals and red teaming, Opus 5 is very hard to prompt inject successfully."

One thing to establish up front: "least prompt injectable model yet" is a claim from an employee's personal post. The system card's formal language is that Opus 5 is "on par with or better than Claude Opus 4.8 on our agentic safety suite," with the "largest gains in prompt injection robustness across coding, computer use, and browser use." This isn't pedantry. Which document a claim comes from, and how much it commits to, determines whether you can build a deployment decision on it: a personal post expresses an employee's impression; the system card is the document the vendor is willing to stand behind.

## The numbers: from 5.5% to 2.0%

Indirect prompt injection means an attacker hides malicious instructions inside content an agent will read — a web page, an email, a document — so the model executes them as if they were user instructions. It's one of the main security risks blocking agent deployment: OWASP ranks prompt injection [first in its Top 10 risks for LLM applications](https://genai.owasp.org/llm-top-10/). An assistant that can read your email and book your flights can also be directed, by a single email, to forward your inbox to someone else. That's not a hypothetical — OWASP's [Excessive Agency entry](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/) uses exactly this scenario: a malicious email tricks an agent into scanning the inbox and exfiltrating sensitive information to the attacker.

The system card cites an indirect prompt injection benchmark from the security evaluation firm Gray Swan. The core numbers (from the chart on page 73 of the system card; the full table values are cross-checked against multiple secondary transcriptions, see References):

| Model | Success rate, 1 attempt | Success rate, within 15 attempts |
|---|---|---|
| Opus 5 | 0.2% | 2.0% |
| Opus 4.8 | 0.5% | 5.5% |
| Mythos 5 | 0.3% | 2.6% |
| GPT-5.6 Sol | 3.1% | 20.0% |
| Gemini 3.1 Pro | 14.2% | 49.2% |

Three observations.

First, the longitudinal progress is real, and fast. Eight months ago, the Opus 4.5 system card reported Gray Swan results of 4.7% for a single strong attack and 33.6% within ten attempts ([The Decoder's coverage at the time](https://the-decoder.com/claude-opus-4-5-resists-prompt-injections-better-than-rivals-but-still-falls-to-strong-attacks-alarmingly-often/)). The two generations of evaluations may not be strictly comparable — benchmark versions and attack budgets can both change — but the order-of-magnitude trend is clear: from "enough retries will always get through" to "2% within a 15-attempt budget," in under a year.

Second, the horizontal gap is an order-of-magnitude gap. GPT-5.6 Sol sits at 20% under the 15-attempt budget — ten times Opus 5. Gemini 3.1 Pro's number is close to half, but the system card notes it participated in the competition that sourced this benchmark's attack samples, so its results can't be directly compared with the other models; keep that in mind when reading across the row. Even setting Gemini aside, prompt injection robustness is currently not a race where the labs are bunched together — the distribution spans a factor of ten.

The third detail is easy to miss: Opus 5 (2.0%) actually edges out Mythos 5 (2.6%). A quick note on Anthropic's naming for this model batch, so the table doesn't confuse: Mythos is a new capability tier that the [official announcement](https://www.anthropic.com/news/claude-fable-5-mythos-5) says sits "above our Opus class in capability," currently available only to Project Glasswing cybersecurity partners, with access planned for select biology researchers. The generally available, safeguarded version is Claude Fable 5 — the same underlying model as Mythos 5, with classifier guardrails added for high-risk topics like cybersecurity and biochemistry (when triggered, the response is handled by Opus 4.8 instead). So the comparison in the table is: the higher-positioned Mythos 5 has a slightly *higher* injection success rate than Opus 5. At least on this evaluation, injection robustness does not rise in lockstep with model capability — which is also why this number deserves its own line of scrutiny and can't be inferred from capability benchmarks.

## 2% isn't "solved" — it's a higher attack cost

Now put the number in a real deployment. The "15 attempts" in the eval is a budget cap for the attacker, but a real attack surface doesn't meter by attempts: an agent that processes a few hundred emails and browses dozens of pages a day has an exposure volume far beyond the eval's setup. Discount the extrapolation appropriately — in practice, the content an agent reads isn't a stream of i.i.d. attack samples, attackers usually don't know your exact deployment, and repeated attempts raise their own exposure — but the direction holds: for a continuously exposed system, the multi-attempt success rate is closer to real risk than the single-attempt number. That's why the 15-attempt column is the one to read first. Attackers aren't in a hurry.

Another set of numbers in the system card makes the structure of this even clearer: in browser-use scenarios with no safeguards, attack success drops from 31.5% on Opus 4.8 to 3.7% on Opus 5; with Anthropic's runtime safeguards layered on top, the success rate is 0% across 129 test environments.

The correct way to read this is in layers: 3.7% is the model's intrinsic robustness; 0% is the combined result of "model plus system-level defenses." Both are useful, but they mean different things. The model-level improvement travels with the model wherever you deploy it. The 0% line includes Anthropic's own runtime safeguards, which the system card only confirms for Anthropic's own product surfaces — in a different deployment stack, there may be no ready equivalent. And stopping all 129 environments is not the same as zero in the wild: the benchmark environments are finite, real adversaries adaptively optimize against the defense itself, and a published "0% in evals" is exactly the kind of target the next round of red teaming aims at.

## Three judgments for deployers

**When you read a system card, find the multi-attempt success rate, and check whether it measures the bare model or the defended system.** Vendors have every incentive to put the best-looking line where you'll see it. The information layering in this release is itself telling: capability numbers went into the announcement headline, safety numbers went to page 73 of the system card — and this time the buried numbers happened to be good, which is why an employee pointed you to them. Run that logic in reverse: the pages nobody points to are the ones worth reading.

**Keep architecting as if injection will happen.** The right architecture in the 2% era is the same one as in the 33% era: [least privilege and human approval for sensitive actions](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/) (OWASP's standard mitigations for excessive agency), plus isolating untrusted content from the instruction channel. What changed is that these measures went from being the only line of defense to being the outer layers of defense in depth. If your agent is running with full permissions and no guardrails, no amount of model robustness will save you.

**Treat prompt injection robustness as an independent procurement criterion.** This release's data shows it doesn't track model capability — it doesn't even track the same vendor's higher-tier model. When choosing an agent foundation, ask for capability benchmarks and injection robustness separately, and verify them separately. Vendors won't always volunteer the latter; whether it's in the system card at all, and at what level of detail, varies by lab — and not being able to get it is itself a signal.

Prompt injection has not been solved. It is moving from "can't be defended" to "can be engineered down." The curve is still falling, but no point on it replaces system design — 0.2% per attempt looks close to zero until exposure compounds daily, and the model can't be the only layer you have.

## References

- [Introducing Claude Opus 5 (Anthropic official announcement)](https://www.anthropic.com/news/claude-opus-5) — release date, capability claims; verified that the announcement text never mentions prompt injection
- [Claude Fable 5 and Claude Mythos 5 (Anthropic official announcement)](https://www.anthropic.com/news/claude-fable-5-mythos-5) — Mythos tier sits "above our Opus class in capability"; Fable 5 and Mythos 5 share the same underlying model; fallback to Opus 4.8 when guardrails trigger; Mythos 5 currently limited to Glasswing partners and, later, select biology researchers
- [Claude Opus 5 System Card (PDF)](https://www.anthropic.com/claude-opus-5-system-card) — Section 5.2 (pp. 71–76), original wording "largest gains in prompt injection robustness across coding, computer use, and browser use"
- [Boris Cherny's post on X](https://twitter.com/bcherny/status/2080713091688583312) — "least prompt injectable model yet" quote (the original post could not be fetched directly; the quote is verified against [Simon Willison's transcription](https://simonwillison.net/2026/Jul/25/boris-cherny/))
- [Anthropic official event page](https://www.anthropic.com/webinars/claude-code-service-delivery) — Boris Cherny's role ("inventor of Claude Code," Head of Claude Code)
- [OWASP GenAI: LLM Top 10](https://genai.owasp.org/llm-top-10/) and [LLM06: Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/) — prompt injection ranked first as LLM01; the malicious-email inbox-exfiltration example scenario and mitigation guidance
- [MarkTechPost coverage](https://www.marktechpost.com/2026/07/24/meet-the-new-claude-opus-5-frontier-class-agentic-coding-and-computer-use-at-unchanged-opus-pricing/) — cross-check for the Gray Swan 15-attempt figures and the browser-use 31.5% → 3.7% → 0% (129 environments) numbers
- [JAIKIN: Opus 5 benchmarks](https://www.jaikin.eu/blog/opus-5-benchmarks) — cross-check for the full Gray Swan comparison table (including single-attempt and Gemini 3.1 Pro values)
- [The Decoder: Claude Opus 4.5 prompt injection coverage](https://the-decoder.com/claude-opus-4-5-resists-prompt-injections-better-than-rivals-but-still-falls-to-strong-attacks-alarmingly-often/) — historical Opus 4.5 figures (4.7% single attempt, 33.6% within ten attempts)
