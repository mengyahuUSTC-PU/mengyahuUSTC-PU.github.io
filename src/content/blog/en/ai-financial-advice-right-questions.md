---
title: "AI financial advice beat something. It wasn't a human advisor"
description: "MIT Sloan had 1,000 adults write their own prompts asking LLMs for financial advice, then simulated a lifetime of following it. The result is real. But look at who's in the control group, and where the advice breaks."
pubDate: 2026-08-01
tags: [personal-finance, llm-evaluation, ai-fairness]
lang: en
slug: ai-financial-advice-right-questions
translationOf: ai-financial-advice-right-questions
---

In late July, an MIT Sloan study made the rounds on [Hacker News](https://news.ycombinator.com/item?id=49139102) (200+ comments) under a headline that carries its own conclusion: [AI financial advice is surprisingly good, especially if you ask the right questions](https://mitsloan.mit.edu/ideas-made-to-matter/ai-financial-advice-surprisingly-good-especially-if-you-ask-right-questions).

My first question after reading it: good compared to what? The headline says good, not better. It names no comparison. But to judge whether advice is any good, you need a reference point.

The answer sits in the study design, and it's more interesting than the headline.

## What the study actually measured

The paper is [AI Financial Advice: Supply, Demand, and Life Cycle Implications](https://tahachoukhmane.com/wp-content/uploads/2026/03/CdSLA-2026-AI-Financial-Advice.pdf), by Taha Choukhmane, Weidong Lin, and Matthew Akuzawa of MIT Sloan and Tim de Silva of Stanford GSB. It won the Swiss Finance Institute's 2026 Outstanding Paper Award ([MIT Sloan working paper 7377-26](https://mitsloan.mit.edu/centers-initiatives/cfi/ai-financial-advice-supply-demand-and-life-cycle-implications)).

The design has three steps. First, recruit 1,000 representative US adults and have them write their own prompts asking GPT-5.2 and Gemini 3 Flash for spending and investing advice. Their own prompts is the point: no researcher wording, because the study wants to see how real users actually ask.

Second, parse each model response into executable rules: how much to save, what share to put in stocks.

This step also fixes the study's scope. "Financial advice" is a broad label, but this study tests one strand of it: long-horizon consumption-savings and portfolio allocation. The abstract is explicit that respondents were asked to write spending and investing prompts, and the simulator runs only those two variables over time. Home buying, mortgages, credit, insurance, tax planning: all equally routine financial decisions, all outside the test. Every "good" or "bad" verdict below covers only that one strand.

Third, drop those rules into a life-cycle simulator and let a virtual you live out a lifetime following them. Income rises and falls on real labor-market data. You get laid off. You hit bear markets. You pay taxes. The simulation runs from working age through retirement; reported wealth comparisons are a snapshot at age 60, consumption is scored over the whole life.

The scoring standard is life cycle theory, the normative framework of household finance. Its prescription, roughly: when you're young, with a long horizon and decades of wages ahead, hold more stocks; reduce the stock share as you age; keep an emergency buffer; smooth consumption across good years and bad instead of letting it swing.

With the design laid out, "surprisingly good" gets a precise meaning. That phrase is MIT Sloan's own headline, and the thing being praised is the model's advice. Choukhmane put it directly: "We were somewhat surprised by how good the advice was," given the rough prompts people actually wrote. In his words, "regular people are not writing their prompts the way a finance professor is."

Good compared to what, then? On the AI side sits a simulated lifetime: advice parsed into rules, run through the simulator to old age. On the other side sits not another simulated trajectory but respondents' self-reported current behavior, how much they save now and what share they hold in stocks now. The two differ in kind, one a long trajectory and one a present-day snapshot, so the paper scores each against the life-cycle prescription. Result: for most respondents, the trajectory of following the AI's advice lands closer to theory than keeping their current behavior does.

Either way you read that, there is no human financial advisor in the control group. The paper itself lists "how does this compare to other forms of financial advice" as an open question.

How low is that baseline? Per [phys.org's account](https://phys.org/news/2026-07-llms-nudge-users-smart-investing.html), about 40% of the respondents writing prompts had less than $10,000 in savings. De Silva is honest about it: it's "not perfect, but it's better than the way many people make decisions, such as talking to friends and family or doing simple internet searches."

But "better than asking friends" deserves one more turn: better at what? Low savings doesn't mean people don't know they should save. "Save more" is advice you can get anywhere; friends will say it, a search will say it. Many people fail to save not because nobody told them, but because they can't stick with it. If the AI's contribution were just repeating "save more," beating the status quo wouldn't mean much.

The rules being scored in the simulation actually have two parts: how much to save, and what to do with what's saved, meaning the stock share, the glide path down with age, the emergency cash, the consumption smoothing in bad years. That second part is the personalized number that friends and a quick search can't give you. The next section has a concrete example: liquidity, a dimension almost no users thought to ask about, which the models volunteered anyway. How much of the improvement comes from "save more" versus "allocate well," the public materials don't break out; I couldn't verify that split.

And "knows they should save but can't stick with it" is something this study can't test. The virtual person in the simulator complies faithfully for decades and never gives up halfway. So "better than the status quo" is a claim about the quality of the advice, conditional on following it. Whether AI can get a real person to actually put the money away is a different question.

## Three findings, taken one at a time

First, the direction is mostly right. The advice pushes people toward the textbook: more participation in diversified equity funds, stock share falling with age, a real savings buffer. The models also fill gaps unprompted: per phys.org, 83% of responses mentioned liquidity, meaning how much readily accessible cash to keep on hand, while only 6% of users asked about it.

Second, the bar for "asking the right questions" is higher than it sounds. The researchers ran a swap: replace users' own prompts with "academic prompts," and advice quality moves further toward theory, with better consumption smoothing and less reliance on crude rules of thumb. An academic prompt writes the life-cycle framework, complete financial information (income, assets, debts, investment horizon), and explicit economic assumptions into the question.

In other words, "asking the right questions" is not a prompting trick. It roughly equals "you already understand some household finance, and you disclose your full balance sheet." De Silva's advice to individual users is accordingly to build financial literacy first; "the way you write the questions matters a ton," he says, and the basics are what let you get real power out of the tool (per phys.org).

Third, advice quality varies by who's asking, and the penalty lands on the groups already worse off. To be precise about what "varies" means: this is not different starting points producing different endpoints. The simulator runs the same procedure for everyone; the gap is in the advice itself. Simulated to age 60 on the advice each group received, women and users with low financial literacy end up about 4% to 5% behind men and high-literacy users. In dollars, per the [MIT Sloan article](https://mitsloan.mit.edu/ideas-made-to-matter/ai-financial-advice-surprisingly-good-especially-if-you-ask-right-questions): about $50,000 less. Users who had never used AI end up nearly $100,000 (6%) behind experienced users.

Where does the gap come from? For gender, the paper decomposes it into two sources of unequal size.

About two-thirds is demand side: men and women write different prompts to begin with. Per the word-frequency tallies phys.org reports, women more often use words like "family," "grocery," "credit," and "loan"; the models follow that thread and give more conservative advice, more cash, bigger emergency buffers. Men more often write "portfolio," "equity," "strategy," "crypto," and get more aggressive investment advice. Low-literacy users follow the same pattern: their prompts disclose less about their finances, so the advice comes back coarser. This portion isn't the model discriminating against anyone; different input, different output.

The remaining third is supply side, and that part is the model's own skew (the decomposition is from the MIT Sloan article). The researchers ran a controlled test: take the same prompt, word for word, and label it as coming from a woman instead of a man. The recommended stock allocation drops; prompts labeled female get lower equity exposure ([phys.org](https://phys.org/news/2026-07-llms-nudge-users-smart-investing.html), [Stanford GSB](https://www.gsb.stanford.edu/insights/what-ai-tells-people-seeking-low-cost-financial-advice)). As for how a model would know your gender in everyday use: usually it doesn't. Per phys.org, in the naturally written prompts the models generally had no access to that information; the gender labels in the experiment were inserted by the researchers. What the experiment shows is that once a prompt does reveal gender, the advice tilts with it.

Both sources push the same direction, against the disadvantaged. The demand side forms a loop: the people who most need advice are exactly the ones least able to ask good questions. The supply side means that even asking the identical question, some users get a slightly worse answer.

## Why the gains flow to skilled askers

An LLM's output tracks its input. Give it complete information in the right frame and its advice approaches the optimum; write "I'm 30, how should I invest" and it can only hand you a generic template. A human advisor's engagement typically starts with intake, getting your income, assets, and goals on the table before prescribing anything. That's standard industry practice, not something this study measured; the paper doesn't compare intake processes. The models in the study answered in a single turn. They ask no follow-ups; whatever information you supply is all they use. That's a property of this mode of use, not a defect.

The consequence: the barrier to a traditional advisor is price, and only those who can pay get one. LLMs push that price barrier to nearly zero and raise a different barrier in its place: only those who can ask get good advice. In the simulation, the floor does rise; most respondents, if they complied strictly, would end up closer to the theoretical prescription than under their current behavior. But the bulk of the gains flows to users with high financial literacy and AI fluency. The tool is available to everyone. The benefit is not evenly shared.

## Fluent in static principles, bad at dynamic adjustment

Three failure modes surfaced in the simulation, and they're worth more than the headline result. These are recurring patterns across the advice given to different respondents, not one user's unlucky draw:

- After a job loss, the models cut spending too hard. The life-cycle prescription is the opposite: draw down the buffer, smooth consumption, don't let one income shock crater your standard of living.
- Portfolios drift without rebalancing. After stocks run up, their share of the portfolio passively climbs and risk exposure stretches wider; the models rarely tell you to sell some and return to target.
- Retirement spending comes out too conservative, mostly parroting the "withdraw 3-4% of savings per year" safe-withdrawal heuristic. Money that should be spent goes unspent, and consumption smoothing loses again.

The common thread: the models recite general principles well and handle state changes poorly. And that kind of dynamic adjustment is, I'd argue, precisely what people pay a human advisor for. The study didn't test human advisors; that part is my judgment.

## The unregulated recommendation slot

Vanguard, the low-fee index fund giant, appears in 6% of responses. iShares, BlackRock's ETF brand, appears in about 3% (the MIT Sloan article says 3.4%; the current version of the paper's figure shows 2.9%; the two disagree slightly). Fewer than 0.4% of prompts mentioned either firm ([MIT Sloan](https://mitsloan.mit.edu/ideas-made-to-matter/ai-financial-advice-surprisingly-good-especially-if-you-ask-right-questions)).

Today this isn't hurting anyone. Both firms are known for low-cost index products ([Vanguard's own figure](https://investor.vanguard.com/investment-products/mutual-funds/low-cost): average expense ratios 84% below the industry average), and recommending them points the same direction as the textbook. Where the recommendations come from, the paper doesn't analyze; my guess is the natural distribution of the training data, but that is a guess. The worry de Silva raises is structural: model providers know that large numbers of users are making financial decisions with these tools, so an incentive exists to steer users toward particular products (per [phys.org](https://phys.org/news/2026-07-llms-nudge-users-smart-investing.html)). What a "recommendation slot" inside a model's answer is worth, no disclosure rule for LLMs currently addresses. Regulators have met the shape of this problem before: in 2013 the [FTC told search engines](https://www.ftc.gov/news-events/news/press-releases/2013/06/ftc-consumer-protection-staff-updates-agencys-guidance-search-engine-industry-need-distinguish) to clearly distinguish ads from organic results, warning that failure to do so could be a deceptive practice. How that maps onto chatbot answers has no precedent yet. Search's own path from organic ranking to paid placement is the cautionary tale already on file.

## My read: usable, on these terms

Trust the directional part. Whether to build an emergency fund, index funds versus single stocks, how the stock share should shift with age: this comes from textbook consensus, and the study shows the models execute it well.

Discount the dynamic part. After a job loss or a market crash, the simulation shows the models handling the adjustment badly. In those moments, don't act on the model's word alone.

Do the intake yourself. "Full information gets you a custom plan" is not news; a human advisor also needs your full picture before prescribing. The difference is that the human engagement usually opens with the advisor asking, while a single-turn model never asks; leave gaps and it fills them with vague generic answers. So run the checklist on your own: income, assets, debts, age, time horizon, risk tolerance, nothing skipped, then ask the model to state the assumptions it made. The improvement the academic prompts produced in the study came from exactly this information.

Keep the scope in mind. This study tested long-horizon saving and allocation, nothing else. Home buying, mortgages, credit, and insurance are outside it, and those decisions tend to be one-shot, large, and hard to reverse, unlike saving and allocation, which you can correct year by year. On those questions this study provides no evidence, and "surprisingly good" doesn't carry over.

And remember what was measured. The paper tests a virtual person who complies faithfully for decades; real people don't. The translation from advice text to executable rules also passed through the researchers' interpretation. What's demonstrated is the directional quality of the advice text, not realized gains for real users.

Back to the question in the title: what did AI financial advice beat? It beat respondents' own reported status quo. In de Silva's telling, many people's status quo is no advisor at all, decisions made by asking family or running a quick search; formally, the comparison object is people's current behavior, with no separate "friends" or "search" arm in the study. And it won only on the long-horizon saving-and-allocation strand. I believe that result, and it matters, because that status quo is where most people actually are. But this advice has never been compared against a human advisor, never run in the real world, never been tested on one-shot decisions like housing or credit, and it comes back in different quality depending on who you are and how you ask. As a first opinion, worth using. As your only opinion, at your own risk.

## References

- [AI financial advice is surprisingly good — especially if you ask the right questions | MIT Sloan](https://mitsloan.mit.edu/ideas-made-to-matter/ai-financial-advice-surprisingly-good-especially-if-you-ask-right-questions) — source of the story; comparison method (simulated AI-following vs. respondents' current behavior), Choukhmane quotes, $50k/$100k wealth gaps, Vanguard 6% / iShares 3.4% / 0.4% prompt mentions, job-loss and drift failure modes, academic-prompt improvement, gender gap decomposition (about two-thirds from prompt differences, one-third from gender-labeled identical prompts)
- [AI Financial Advice: Supply, Demand, and Life Cycle Implications (paper PDF, author's site)](https://tahachoukhmane.com/wp-content/uploads/2026/03/CdSLA-2026-AI-Financial-Advice.pdf) — the paper itself; experiment design, simulator, and comparison details are authoritative here (the paper's figure puts iShares mentions at 2.9%, slightly different from the article's 3.4%)
- [Paper page | MIT Sloan CFI](https://mitsloan.mit.edu/centers-initiatives/cfi/ai-financial-advice-supply-demand-and-life-cycle-implications) — abstract: respondents wrote spending and investing prompts (scope covers consumption-savings and allocation only, not housing/credit/insurance), models tested were GPT-5.2 and Gemini 3 Flash, three main findings (including better consumption smoothing and less reliance on heuristics), 4-5% retirement wealth gap between groups, supply/demand decomposition, working paper 7377-26, Swiss Finance Institute award
- [Study finds LLMs nudge users toward smart savings and investing habits | phys.org](https://phys.org/news/2026-07-llms-nudge-users-smart-investing.html) — de Silva quotes, ~40% of respondents with under $10k savings, 83%/6% liquidity figures, gendered prompt vocabulary, "models generally don't know user gender" plus lower equity exposure for female-labeled prompts, 3-4% withdrawal failure mode, provider-incentive concern
- [What AI tells people seeking low-cost financial advice | Stanford GSB Insights](https://www.gsb.stanford.edu/insights/what-ai-tells-people-seeking-low-cost-financial-advice) — gender-label controlled experiment (lower stock exposure recommended to women), de Silva interview
- [Hacker News discussion](https://news.ycombinator.com/item?id=49139102) — distribution context (200+ comments)
