---
title: "Three quarters of the tasks workers grab with AI aren't seen again a month later"
description: "OpenAI's second task-level study finds only 23.6% of cross-occupation AI use shows up again the following month. What sticks clusters in customer conversations and marketing output. The filter looks like repetition frequency times error tolerance, rather than skill value."
pubDate: 2026-09-16
tags: [ai-economy, labor-market, openai]
lang: en
slug: ai-cross-occupation-tasks-that-stick
translationOf: ai-cross-occupation-tasks-that-stick
---

In late July, OpenAI published the first report in its "Work at the Frontier" series, a task-level study of work: across 800,000-plus work-related ChatGPT messages from US users, 43.5% of occupation-specific usage was doing another occupation's tasks ([first report](https://openai.com/index/how-ai-is-expanding-what-people-do-at-work/); "occupation-specific" means messages that map to a concrete task on some occupation's task list, so generic office work like drafting emails or summarizing doesn't count). I covered it in [that day's briefing](/en/briefing-2026-07-27) and kept one reservation: message classification shows people are trying tasks outside their job, but whether trying counts for anything, that dataset couldn't answer.

On September 16, OpenAI released a second report, "[How workers are unlocking new ways of working](https://openai.com/index/unlocking-new-ways-of-working/)", which takes on exactly that question: after the first try, does it stick?

The answer comes in two halves.

The first half is unflattering: mostly, it doesn't. The study analyzed more than 1.5 million work-related messages from April through July 2026 and tracked worker-task pairs month over month. Of the cases where a worker was observed using AI for another occupation's task one month, only 23.6% were observed again the next month. Read the other way, more than three quarters of these cross-boundary experiments had vanished from the following month's sample. The wording needs care: the study looks at sampled messages, and the [report](https://cdn.openai.com/pdf/work-at-the-frontier-report-202609.pdf) acknowledges that repeat use outside the sample gets missed, so "not seen" is not strictly "abandoned". But only what gets seen can count as evidence.

The second half is the study's real finding: 23.6% is not low. Matched workers who were otherwise comparable but had no observed use of a given task in the prior month picked it up the next month only 8.4% of the time. One observed use makes next-month use roughly 2.8 times as likely. And the part that sticks accumulates: among roughly 6,200 workers observed continuously from April to July, previously used cross-occupation tasks grew from 13.1% of their occupation-specific AI activity in April to 25.9% in July, nearly doubling in four months.

Whether any job descriptions changed along the way, the data doesn't say. What it does show is that by July, a quarter of these continuously observed workers' occupation-specific AI use consisted of tasks taken from other jobs that they had already used before. That number deserves a longer pause than the headline one.

## What sticks

Averaged across all cross-occupation tasks, the next-month return rate is 18.5%. Well above it:

- discussing goods or services with customers: 54%
- writing advertising or promotional copy: 44%
- creating marketing materials: 37%

Near the bottom sits "explaining financial information", at about 15%.

Set against the July report's entry-point data, this list is a little surprising. Back then, financial calculation and technology troubleshooting each ranked among the three most commonly attempted cross-occupation tasks in all seven other occupation groups, and creating marketing materials made the top three in five of them. The most widely shared entry points were finance and tech tasks; the top of the persistence list skews toward marketing and customer conversation. To be clear, this is not a before-and-after of the same attempts: entry volume and next-month persistence are two different metrics from two different reports. I'm only comparing the shape of the two lists.

"AI unlocks new skills" usually conjures marketers learning to run data analysis or HR learning to write scripts. The data's answer is more mundane: within the occupation groups sampled, what most reliably becomes routine is workers taking on their own customer-facing and promotional work.

## Why marketing, of all things

The [report](https://openai.com/index/unlocking-new-ways-of-working/) names candidate factors: whether a task is embedded in a recurring workflow, workplace norms, how much care a task demands and what an error costs. It stops at listing them and tests none. Following that thread, I have two hypotheses. To be explicit: both are hypotheses, and the report tested neither.

The first is the calendar. Marketing output is periodic by nature; picture a typical routine of weekly social posts, promotional emails every campaign cycle, daily customer conversations about the product. Those cadences vary by workplace, and I have no frequency data to cite; the point is the recurrence. Explaining financial information looks more like an occasional need: once you have made sense of a quarterly report or compared two options, you're done. That, too, is my assumption rather than a measured fact. And a next-month return rate is structurally kind to high-frequency tasks: it only checks whether a task reappears in the month right after it was first observed ([report PDF](https://cdn.openai.com/pdf/work-at-the-frontier-report-202609.pdf)). A task needed twice a year would score as "didn't stick" even if AI handled it perfectly every time. So this ranking measures a blend of where AI is useful and how dense the task is on the calendar, and the report doesn't separate the two.

The second is the match between error cost and the user's ability to check the output. A mediocre ad costs you some conversions, and a layperson can tell at a glance whether copy passes. A wrong explanation of financial information feeds wrong decisions, and the layperson is precisely the one who can't spot where it went wrong. Routinely handing an out-of-field task to AI requires either that mistakes are cheap or that you can verify the result yourself. Routine marketing output clears both bars; financial analysis clears neither. This one is a generalization from my own experience, with no direct evidence in the data.

If both hold, "AI turns everyone into a generalist" needs a discount: the filter for what sticks may not be the value of the skill but repetition frequency times error tolerance.

## What this means for workers

Three ledgers.

The skills ledger. The tasks that stick are not all the same kind: in some, the model produces the deliverable (copy, materials); in others, it explains or advises. For the production kind, the model generates the output while the human specifies the need and accepts the result. Judging whether output passes is a real skill, but it is a different thing from having learned marketing. The report measures neither skill acquisition nor retention, so what follows is my judgment rather than its data: the learning survives losing the tool; the output pipeline mostly doesn't. Reading a high return rate as "I've acquired a new skill" overstates what you actually accumulated.

The bargaining ledger. The report's own framing is that AI may rewrite the content of work before job titles change. Translated into the language of interests: the task portfolio widens first, and titles and pay adjust later. Whether the extra work in between gets compensated, the report has no data on, and I have found none elsewhere; my guess is mostly not. To convert the widened boundary into a bargaining chip, you have to make it visible: attributable deliverables, material that enters a performance review, rather than something buried in chat logs.

The absorbed side's ledger. The July data contains an asymmetry: 35.2% of designers' messages were doing other occupations' tasks, while design tasks made up only 1.7% of everyone else's messages. Marketing runs high in both directions, and a quarter of non-marketers' marketing-related usage is directly producing promotional materials (ads, social posts, flyers). Judging from message flows, the marketing work other roles pick up on their own concentrates in this routine-production layer; still, flows are all the usage data can show, and whether the work actually moved out of marketers' hands the data can't answer. Design's apparent immunity is more likely a blind spot than a fact: the studies only see sampled users' ChatGPT messages ([first report PDF](https://cdn.openai.com/pdf/work-at-the-frontier-report.pdf)), and design output produced in dedicated tools like Figma or Midjourney is invisible through this window. That, too, is speculation; the report does not test why design shows so little spillover.

## What the data can and can't say

The same caution applies as with [last month's Enterprise usage report](/en/how-organizations-use-chatgpt): this is OpenAI studying its own product with its own product data, and it measures use, not output quality. Whether the cross-occupation work was done well, and whether customers accepted it, is not in the data. The task classification uses a model to map each message to a specific task entry in [O*NET](https://www.onetcenter.org/database.html), the occupational database sponsored by the US Department of Labor and developed by the National Center for O*NET Development; "cross-occupation" means the task falls outside the O*NET task list of the user's own occupation. The report itself warns this does not mean the task was new to that worker: it may long have been part of their actual job, just outside the occupation's traditional task boundary. Occupations come from the role US ChatGPT Business users entered at sign-up, the analysis covers sampled messages from those users' accounts, and the findings are not extrapolated to Enterprise customers.

23.6% versus 8.4% is a matched comparison, not a randomized experiment, and the [report](https://cdn.openai.com/pdf/work-at-the-frontier-report-202609.pdf) presents the result descriptively, as consistent with repeated demand rather than proof of it. People who try other occupations' tasks in the first place may simply be more inclined to tinker, so how much of the 2.8-fold gap is "used it, therefore kept using it" causation can't be cleanly separated. The comparison group is defined by no observed use, and those workers may well have done the same task in unsampled conversations or in other tools. In the end, this data is the view from one window, and that window is ChatGPT.

## Where this leaves the bigger question

In July I wrote that [aggregate unemployment data shows no visible AI shock](/en/ai-jobs-data-reality-check); the US unemployment rate has stayed in a narrow 4.3%–4.5% band since July 2025, at 4.3% as of May 2026 ([BLS](https://www.bls.gov/opub/ted/2026/unemployment-rate-unchanged-at-4-3-percent-in-may-2026.htm)). This task-level data supplies a candidate for the missing middle layer of mechanism: the change may skip the front door of jobs disappearing and take the side door of task portfolios quietly turning over, before titles or official statistics register anything. The report treats this as one possible path, not a settled outcome.

You can run the method on yourself: look back over the past three months and list the out-of-role tasks you have repeatedly gone back to AI for. That is the direction your job boundary is actually moving. Before it makes it into a job description, work out how to make it visible.

## References

- [How workers are unlocking new ways of working (OpenAI, 2026-09-16)](https://openai.com/index/unlocking-new-ways-of-working/) ([report PDF](https://cdn.openai.com/pdf/work-at-the-frontier-report-202609.pdf)) — 1.5M messages, 23.6% vs 8.4%, 18.5% average return rate, 13.1%→25.9%, task-level persistence rates (54%/44%/37%/15%), metric definitions and matching method
- [How AI is expanding what people do at work (OpenAI, 2026-07-27)](https://openai.com/index/how-ai-is-expanding-what-people-do-at-work/) ([report PDF](https://cdn.openai.com/pdf/work-at-the-frontier-report.pdf)) — 800K messages, 16.8%/43.5%, design 35.2% vs 1.7% asymmetry, financial-calculation and troubleshooting entry-point data
- [TechTimes coverage of the first report](https://www.techtimes.com/articles/321676/20260727/chatgpt-scrambles-specialization-nearly-half-job-specific-ai-use-crosses-role-lines.htm) — cross-check of first-report figures, O*NET methodology
- [Built In's overview of the research](https://builtin.com/articles/openai-task-crossover-study) — eight occupation groups, exclusion of Enterprise users, other methodology details
- [Lead with AI's data breakdown of the first report](https://www.leadwithai.co/article/openai-work-at-the-frontier-impact-per-hour) — task flows (design/engineering/marketing in-and-out shares), composition of non-marketers' marketing usage
- [O*NET Resource Center](https://www.onetcenter.org/database.html) — sponsorship and scope of the occupational task database used for classification
- [Unemployment rate unchanged at 4.3 percent in May 2026 (BLS)](https://www.bls.gov/opub/ted/2026/unemployment-rate-unchanged-at-4-3-percent-in-may-2026.htm) — aggregate labor-market context
- [This site's briefing, 2026-07-27](/en/briefing-2026-07-27) — same-day coverage of the first report, with the original reservation
- [Why the heaviest ChatGPT users in a company are the most junior employees](/en/how-organizations-use-chatgpt) — data caveats for the companion Enterprise usage report
- [The AI in layoff announcements and the AI in unemployment data are not the same AI](/en/ai-jobs-data-reality-check) — the aggregate-statistics view this task-level piece connects to
