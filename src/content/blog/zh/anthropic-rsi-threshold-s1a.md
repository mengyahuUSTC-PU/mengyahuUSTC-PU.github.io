---
title: "Anthropic 说快到线了，可这条线它以前都是事后才看见"
description: "Anthropic 在招股书修订版里说可能很快越过「AI 显著加速研发」的门槛。拆开它公开的测量方法看：现有指标能测什么，测不到什么。"
pubDate: 2026-11-02
tags: [ai-safety, anthropic, ai-governance]
lang: zh
slug: anthropic-rsi-threshold-s1a
translationOf: anthropic-rsi-threshold-s1a
---

11 月 2 日，Anthropic 向 SEC 提交了 IPO 招股书的修订版（[S-1/A](https://www.sec.gov/Archives/edgar/data/2130357/000162828026068676/anthropicpbc-sx1ax1.htm)）。和 10 月 26 日的初版相比，风险因素一节多了几句话。最受关注的一句说，公司内部的估计和对未来模型的预期（"rather than our current models"）表明，它"may imminently meet"自己的负责任扩展政策（RSP）对"dramatically accelerated progress attributable to AI"的定义。[TechCrunch](https://techcrunch.com/2026/11/02/anthropic-warns-that-its-very-close-to-rsi-capability-aka-self-building-ai/) 把这条新闻概括为 Anthropic 接近 RSI，也就是递归自我改进：AI 研发出更强的 AI，更强的 AI 再更快地研发下一代。

同一节新加的另一句话，我认为分量更重："we have in the past not identified"。按 TechCrunch 的概括，意思是 Anthropic 过去用 AI 开发模型时出现过显著的能力加速，当时没有认出来，事后才发现。

两句放在一起读：一家公司说自己快要越线，同时承认这条线过去只能在越过之后才看得见。这篇要回答的是，这条线量的是什么，现有的尺子能不能在越线之前读出数来。

## 线画在哪

RSP 是 Anthropic 自己定的安全承诺文件，规定模型能力到什么程度就必须配上什么防护。AI 研发这条门槛在 4 月的 3.1 版里澄清过一次（[RSP 更新记录](https://www.anthropic.com/rsp-updates)）：原文"把 2018–2024 年两年的 AI 进展压缩进一年"，指的是整体 AI 能力的进步速度翻倍，不是研究员的生产率翻倍。7 月生效的 3.4 版又修订了这条门槛，官方给的理由是"更贴近所担心的威胁模型"。新版的确切措辞我没能核对原文。

关键在于，这条线量的是速度，而且只算"归因于 AI"的那部分。判断越没越线，要回答一个反事实问题：如果没有 AI 参与，同样的进展要花多久。这个问题只能隔着几代模型回头看。一代模型训练、评测完，才知道这一步走了多远；要和历史节奏比，还需要好几个数据点。速度类指标天生滞后，"过去只能事后发现"并不意外。

所以招股书的措辞很小心：说的是未来模型和内部估计，没有把任何现有模型认定为越线。我能查到的公开材料里，没有这些内部估计的具体数字。

## 现在能测的是什么

Anthropic 在官网《[测量 AI 发展速度](https://www.anthropic.com/institute/measuring-pace-of-ai-development)》一文里公开过一套可以实时测的指标。核心是一个研发自动化指数：截至 2026 年 8 月，Claude "主导"（leads）了 26% 的 AI 研发工作，2 月时还不到 1%；AI 参与程度达到"协作"（collaborates）及以上的工作超过 90%；没有任何一类工作由 AI 完全自主完成。

"主导"借用的是 Epoch AI 的六级量表（AL0 到 AL5），对应第五级 AL4：从一个高层指令出发，AI 能端到端完成任务的大部分，人在旁边监督。

数据的来源是这样：7 月每周抽各部门 20% 的员工，让 Claude 研究 agent 读他们的 Slack 消息和内部文档，整理出约 15,000 个任务，归并成一棵固定不变的任务树，共 378 个叶子任务。再由另一个 Claude 当评判，给每类任务打自动化等级，按人时加权。

读这个数字时，有两点必须记住。

第一是标注一致性。评判模型和人的等级完全一致的比例是 59%，人和人之间只有 35%，相差不超过一级的比例是 97%。两个员工看同一项工作，大约三次里有两次给不出同一个等级。26% 统计的是 AL4 及以上，恰好落在"协作"和"主导"的分界上，而分歧最集中的就是相邻两级。我的判断是：从 1% 到 26% 的变化远大于一级误差，趋势可信，精确值不宜较真。

第二，任务篮子是冻结的。页面自己写了，指数上涨"本身不能告诉我们是否出现了新类型的工作"，按人时加权也只是"粗略近似"。这和招股书里"事后才发现"那句话对得上。假如加速来自 AI 做了人以前根本没做过的事，比如同时开几万个 agent 跑实验（该页面给的数字是，最常用的内部平台上任一时刻约有 3 万个 agent 在做研发），那么固定的 378 类任务里就没有它的位置。

## 26% 离"翻倍"有多远

任务占比和进展速度是两个量。做个上限估算：假设这 26% 人时的工作完全不再占用人力，人力这一环的吞吐量最多提升到 1/(1−0.26)，约 1.35 倍。AL4 仍要人监督，实际收益会更低；研发还受算力和实验排队时间限制，这些不会因为人手空出来而缩短。

按这个口径，单靠接管现有任务推不出速度翻倍。翻倍要么来自篮子之外的新工作，要么来自 AI 让每次实验更有效、少走弯路。这两样恰好都是当前指数测不到的。这是我的推演，Anthropic 没有公开它怎样从内部估计推到"imminently"。

## 承诺靠什么兑现

招股书同时加了一条承诺：即便技术上可行，Anthropic 也不打算在没有"meaningful human supervision or understanding"的情况下，用 Claude 完全自主地设计和构建一代代前沿模型；它还在考虑修订 RSP，确保人类掌控前沿模型开发。

"有意义的监督"怎么量？同一页面给出的监督数据是：上述平台上 100% 的 agent 动作在执行前都要经过在线监控；8 月超过 10 亿次决策中，被拦下的占 0.002%，约四万七千分之一；被拦的动作由人在一周内复核。这些数字说明监控覆盖了全部动作，没有说明它漏掉了多少。页面没给漏检率，反倒写了一句建议："开发者应当公布已知的 agent 不当行为有多少被监控抓到。"

还有一个背景：RSP 从 4 月到 7 月出了四版（3.1 到 3.4），AI 研发门槛的表述动了两次。尺子在变，线的位置也在变。

## 对从业者意味着什么

用 Claude 做产品的团队：这条披露讲的是 Anthropic 内部研发的速度，没有说现有模型的能力发生了变化，产品决策不必因此调整。

自己跑 agent 的团队可以照搬这套指标：按自动化等级给任务分层，跟踪各层比例的变化；监控不能只报拦截率，要在流程里主动埋入已知的坏动作，测监控抓到了多少。拦截率低，可能是 agent 守规矩，也可能是监控看不见，只看拦截率分不出这两种情况。

外界第一次能检验"imminently"，是在下一份风险报告。上一份是 8 月发布的[风险报告](https://www.anthropic.com/aug-2026-risk-report)，覆盖期截至 7 月 15 日。如果下一份宣布越线，我会先看它拿出的是速度的证据，还是又一个任务占比。

## 参考来源

- [Anthropic, PBC Form S-1/A（2026-11-02）](https://www.sec.gov/Archives/edgar/data/2130357/000162828026068676/anthropicpbc-sx1ax1.htm) — "may imminently meet""rather than our current models""we have in the past not identified""meaningful human supervision or understanding"等原文措辞；经 SEC EDGAR 全文检索比对，这几句只出现在 11 月 2 日的修订版，10 月 26 日初版里没有
- [Anthropic: Measuring the pace of AI development](https://www.anthropic.com/institute/measuring-pace-of-ai-development) — 26% / <1% / >90% 数据、AL0–AL5 量表、抽样与评判方法、59%/35%/97% 一致率、冻结任务树的局限、3 万个 agent、监控覆盖率与拦截率、一周复核、关于公布漏检率的建议
- [Anthropic: RSP updates](https://www.anthropic.com/rsp-updates) — 3.1 版对 AI 研发门槛"进步速度翻倍"的澄清、3.4 版修订门槛、3.1–3.4 各版生效日期、8 月风险报告覆盖期
- [Anthropic Risk Report: August 2026](https://www.anthropic.com/aug-2026-risk-report) — 上一份风险报告
- [TechCrunch: Anthropic warns that it's very close to RSI capability](https://techcrunch.com/2026/11/02/anthropic-warns-that-its-very-close-to-rsi-capability-aka-self-building-ai/) — 新闻线索；"事后才识别出加速"一句的含义概括
