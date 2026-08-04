---
title: "There's no magic prompt in Terence Tao's chat transcript"
description: "After the 87-year-old Jacobian conjecture fell, Terence Tao published his full ChatGPT transcript from digesting the counterexample. Readers went looking for prompting tricks; Sean Goedecke read it and concluded the opposite: LLMs reward domain expertise. Three field experiments show where the 'AI levels the playing field' story holds, and where it breaks."
pubDate: 2026-08-03
tags: [llm, expertise, ai-productivity]
lang: en
slug: llms-reward-expertise
translationOf: llms-reward-expertise
---

In the early hours of July 20, Levent Alpöge, a mathematician at Anthropic, posted one line on X: "hello there the jacobian conjecture is false thanx", followed by a polynomial map in three variables. That post was the entire announcement; there was no formal writeup to go with it ([The Conversation reconstructed the sequence of events](https://theconversation.com/hello-there-the-jacobian-conjecture-is-false-thanx-why-a-tiny-social-media-post-has-mathematicians-rethinking-ai-283883)). The casualty was the Jacobian conjecture, posed in 1939: a polynomial map that is locally invertible everywhere (constant nonzero Jacobian determinant) should be globally invertible. After 87 years in suspension, the conjecture is now false in dimension three and above; the two-dimensional case remains open. Alpöge's tool was Claude Fable 5, released only weeks earlier. Mathematicians have publicly checked the symbolic computation behind the map; a formal paper and peer review are still on the way.

The next day, Terence Tao published a [blog post "digesting" the counterexample](https://terrytao.wordpress.com/2026/07/21/a-digestion-of-the-jacobian-conjecture-counterexample/), breaking a construction that seemed to appear out of nowhere into a few steps that make geometric sense. He also published the complete transcript of his ChatGPT conversations from that work.

Open that transcript and the natural expectation is a lesson in how one of the world's best mathematicians writes prompts. Sean Goedecke, an engineer, [read it and came away with the opposite conclusion](https://www.seangoedecke.com/llms-reward-expertise/): there is nothing in it to copy.

## What's actually special in that transcript

Goedecke (a [Staff engineer at GitHub](https://newsletter.pragmaticengineer.com/p/shipping-projects-at-big-tech-with) who has written a good deal about working with LLMs) listed his observations in a July 24 post. Tao's messages are short. He uses jargon without preamble, and the model responds by switching into what Goedecke calls talking-to-mathematicians mode rather than explaining things to a layperson. Tao stays skeptical of the model's output, but he doesn't contradict it head-on; he redirects instead, asking whether an idea can be restated in a formalism he already knows well. The most striking observation: **he almost never takes the model's suggestions about where to go next.** The direction stays in his hands throughout; the model checks calculations, reformulates, scouts ahead. Tao himself gives it one dry line at the end of his post: he used an AI chatbot to discuss various aspects of the problem and to confirm several of the calculations.

From this Goedecke draws his central claim: the most important skill in prompting is expertise in the domain you're prompting for. And a pricklier one: for many tasks, the bottleneck is the human, not the model.

That runs straight against the most popular story of the past two years.

## But the leveling story has real evidence too

"AI is an equalizer and novices gain the most" is not an empty claim. The [NBER customer-support study](https://www.nber.org/papers/w31161) (Brynjolfsson et al.) tracked over five thousand support agents; AI assistance raised issues resolved per hour by 14% on average, with novice and low-skill workers gaining 34% while experienced agents barely moved. In the [BCG field experiment](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4573321) (Dell'Acqua et al., 758 consultants), on 18 consulting tasks designed to sit within the model's capabilities, consultants using AI completed 12.2% more tasks on average, worked 25.1% faster, and scored more than 40% higher on quality; split by baseline skill, consultants below the average line improved 43% while those above it improved only 17%.

Both datasets point the same way: novices gain more. So is Goedecke wrong? I think neither side is. They're measuring different terrain.

## The mechanism: frontier, verification, navigation

The variable that actually matters is which side of the model's capability frontier a task falls on, and who catches the errors; who is using the AI turns out to be secondary. "Capability frontier" is the BCG paper's term: tasks the model can do well end to end are inside the frontier, tasks it can't are outside, and the boundary is jagged, so two tasks of apparently similar difficulty can sit on opposite sides.

Leveling happens inside the frontier. The tasks that produced the gains in both experiments, NBER's support replies and BCG's 18 inside-frontier consulting tasks, all sit on that side: the model's answer is good enough to adopt as is, a novice who takes it lands near a veteran's level, and mistakes are cheap. So novices gain the most and the gap genuinely narrows. To be clear, every gain figure above comes from inside-frontier tasks; the BCG experiment also planted one task outside the frontier, which is where this goes next.

Outside the frontier the picture inverts. On the task the BCG team deliberately designed to exceed the model's capability, consultants using AI were 19 percentage points less likely to produce a correct solution than the control group. The reason is that fluency does not degrade along with correctness: as [MIT Sloan's explainer on this research](https://mitsloan.mit.edu/ideas-made-to-matter/working-definitions/what-is-jagged-ai-frontier) puts it, AI-generated answers can look credible even when they're wrong. The prose is equally polished either way; the answer isn't. Out here, how much value you extract from the model depends on whether you can spot what's off. Tao's usage reads as a reference pattern for this side of the frontier: have the model verify, have it restate and scout, never let it set the direction.

There is a third case. [METR's experiment last year](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/) had 16 experienced open-source developers use early-2025 AI tools on 246 tasks in codebases they had maintained for years. They came out 19% slower on average, while believing afterward that they had been 20% faster. METR did not settle on a single cause, only a list of candidate factors; the two that fit the mechanism here best are that the developers knew their codebases extremely well, so their unassisted baseline was already high, and that time spent reviewing and correcting model output ate the time that generation saved. So expertise includes one more layer: knowing when not to use the tool at all.

This mechanism matches what I see every day in my own work. I work in content moderation, and for the past two years part of that has involved using LLMs to help adjudicate borderline content. The model's rationale for a call is always fluent: it cites policy clauses and lays out a plausible-looking chain of reasoning. But whether a borderline call is right comes from policy intent and an accumulated body of precedent, and fluency can't establish it. In the cases I've handled, borderline content is precisely where trained annotators genuinely disagree with each other; I have never seen a line that everyone accepts. In my experience, someone who hasn't reviewed a few thousand borderline cases has trouble telling "the model cited the correct clause" apart from "that clause actually applies to the item in front of us," because the two outputs look identical on the surface. That is the judgment Goedecke is pointing at: you can only tell that this answer is wrong if you already know roughly what a right one looks like.

## Where the leveling story holds

Put the two bodies of evidence together and the picture is coherent: at least on the tasks and models these experiments cover, AI raised the floor on routine work inside the frontier, and on those tasks the gap between novices and veterans genuinely narrowed. The next step is my inference, not something the experiments measured: once the routine portion is done in bulk, competition shifts outside the frontier, where the returns to expert judgment grow rather than shrink.

Two implications for individuals. First, standalone prompting tricks are thin: in my own experience, tricks bound to a specific model's behavior have to be relearned every time the model changes; what lasts is domain judgment, meaning the ability to recognize a wrong output and the ability to say clearly what a right one looks like. Second, keep the navigation. Use the model as a calculator-checker and a scout, and keep your hands on the wheel. Navigation and coordination are scarce resources in their own right: [I wrote recently](/en/ai-coding-agents-fail-at-teamwork) about how even two top coding agents pairing on one task lose thirty to forty percent of their capability to coordination failures (about 30% by the paper's headline figure, 41% by its AUC metric), let alone handing a model the entire direction.

Honestly, two discounts apply. Tao's transcript is a single sample, and the most extreme one available. And the three experiments cover models and tools from the GPT-3 generation through early 2025 (the NBER data was collected in 2020–2021); the capability frontier keeps moving outward, and a task outside it today may be inside it next year. But outward movement only changes which tasks belong to the experts. It doesn't change the structure itself, which is that the tasks outside the frontier are theirs.

Next time you see the claim that AI makes everyone an expert, think about that transcript. The same model sits in front of all of us, but what Tao can pull out of it is not what we can pull out of it. The difference isn't on the model's side.

## References

- [LLMs reward expertise (Sean Goedecke)](https://www.seangoedecke.com/llms-reward-expertise/) — core argument, all observations on Tao's conversational style
- [A digestion of the Jacobian conjecture counterexample (Terence Tao)](https://terrytao.wordpress.com/2026/07/21/a-digestion-of-the-jacobian-conjecture-counterexample/) — background on the counterexample, statement of the conjecture, Tao's own note on his AI use
- [The Conversation's report on Alpöge's announcement](https://theconversation.com/hello-there-the-jacobian-conjecture-is-false-thanx-why-a-tiny-social-media-post-has-mathematicians-rethinking-ai-283883) — how the result surfaced, the model used, verification and review status (the result was first made public via a post on X)
- [Generative AI at Work (NBER w31161)](https://www.nber.org/papers/w31161) — issues resolved per hour +14%, novices +34%
- [Navigating the Jagged Technological Frontier (SSRN 4573321)](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4573321) — 758 consultants; inside-frontier +12.2% / +25.1% / quality +40%; below-average +43% vs. above-average +17%; outside-frontier −19 percentage points; the "jagged frontier" concept
- [What is the jagged AI frontier? (MIT Sloan)](https://mitsloan.mit.edu/ideas-made-to-matter/working-definitions/what-is-jagged-ai-frontier) — wrong AI answers can still look credible
- [Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity (METR)](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/) — 16 developers, 246 tasks, 19% slower, self-assessed 20% faster, candidate explanations
