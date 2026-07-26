---
title: "裁员公告里的 AI，和失业数据里的 AI，不是同一个 AI"
description: "斯坦福 SIEPR 用五套数据核查『AI 失业潮』：总量上几乎看不到，真正的信号窄而具体——集中在高暴露职业的入口岗位。"
pubDate: 2026-07-25
tags: [ai-economy, labor-market]
lang: zh
slug: ai-jobs-data-reality-check
translationOf: ai-jobs-data-reality-check
---

2025 年 10 月 28 日，亚马逊宣布裁减约 1.4 万个办公室岗位。媒体标题几乎众口一词：「亚马逊裁员 1.4 万，拥抱 AI」。但去读[官方备忘录原文](https://www.aboutamazon.com/news/company-news/amazon-workforce-reduction)，措辞其实很谨慎：全文把这轮裁员归因于组织结构——层级太多、要更精简；AI 只出现在对未来的展望里：「这一代 AI 是自互联网以来最具变革性的技术」，公司预计「未来几年」AI 带来的效率提升会缩减办公室岗位总量。

裁员是现在时，AI 是将来时。这两句话被大多数标题合并成了一句。

这种「现在裁员、将来归因」的错位，正是斯坦福经济政策研究所（SIEPR）2026 年 7 月一份政策简报（[原文](https://siepr.stanford.edu/publications/policy-brief/what-really-happening-jobs-separating-ai-hype-reality)）要拆解的问题。作者阵容值得注意：SIEPR 主任 Neale Mahoney、前美国劳工统计局局长 Erika McEntarfer、研究员 Karsen Wahal——其中 McEntarfer 直到 2025 年 8 月还在主管美国官方就业数据的编制。

## 总量数据里没有失业潮

简报的核心方法是「按暴露度分组对比」：给每个职业打一个 AI 暴露度分数（衡量该职业的任务与现有 AI 能力的重合程度），把所有职业按分数分成五档，然后用 IPUMS-CPS 微观数据（2015–2026 年，按季度）比较各档的失业率走势。

结果是全文最硬的一组数字：2022 年以来，暴露度最高一档的失业率上升了 0.77 个百分点，暴露度最低一档上升了 0.85 个百分点。最该被 AI 冲击的人群，失业率涨得反而比最不该被冲击的人群略慢。作者的结论是：这是一个整体走软的劳动力市场，而不是一个被 AI 驱动失业的劳动力市场——真正拖慢招聘的宏观因素（美联储 2022 年 3 月开始加息、疫情期间的超额招聘回调）对所有人一视同仁。

企业侧数据同样平淡。人口普查局的企业调查里，已采用 AI 的企业中只有 5% 报告 AI 影响了用工人数——而且这 5% 里增员和减员各占一半。亚特兰大联储的高管调查里，约 80% 的高管承认 AI 投资尚未改变公司的人员规模或生产率。

那为什么裁员公告言必称 AI？简报作者对企业自报的归因明确持保留态度，理由是激励不对：把裁员说成「为 AI 转型」，比承认「疫情期间招多了」体面得多，也更符合投资者想听的故事——尤其当公司同时在为 AI 基础设施筹措巨额资本开支时，「裁员省下现金投 AI」本身就是叙事的一部分。裁员公告首先是写给资本市场的文本，其次才是对劳动力市场的描述。

## 真正的信号：窄，但真实

简报没有停在「虚惊一场」。它承认有一个信号是真的：入口岗位。

2026 年一季度，美国新毕业生失业率达到 5.6%，比三年前高 1.6 个百分点。更细的证据来自 Brynjolfsson 团队的「煤矿里的金丝雀」研究（[Stanford Digital Economy Lab](https://digitaleconomy.stanford.edu/publication/canaries-in-the-coal-mine-six-facts-about-the-recent-employment-effects-of-artificial-intelligence/)，用 ADP 工资单数据）：22–25 岁年轻人在 AI 暴露度最高的职业里，就业相对下滑约 13%；22–25 岁软件开发者的就业从 2022 年底的峰值到 2025 年 7 月下滑近 20%，而同职业的资深员工基本稳定。下滑集中在 AI 更可能「替代」而非「辅助」人类任务的职业里。

但简报对这个信号也做了减法，列出三个混杂因素：加息始于 2022 年 3 月，早于 ChatGPT 发布；远程办公削弱了入门岗位在工作中学习的机会，本身就压低企业招新人的意愿；而且修订后的分析显示，入门岗位的明显下滑要到 2024 年才出现——如果 AI 是主因，时间线上应该更早、更陡。

所以准确的读法是：入口岗位的困境是真的，AI 是嫌疑人之一，但目前的证据不足以让它单独定罪。

## 量尺问题：同一个问题，四个答案

简报最有方法论价值的部分，是把「AI 采用率」的各种口径摆在一起：问企业（人口普查局调查），约两成在用；问员工（家庭调查），超四成说工作中用 AI；问高管，声称超八成员工在用；看企业实际付费（Ramp 平台数据，样本不具代表性），超半数客户在为 AI 工具花钱。同一个问题，答案从 20% 到 80%,取决于问谁、怎么问。任何一篇拿单一口径下结论的报道，都值得先打个问号。

生产率证据同样撕裂。实验室一侧：呼叫中心研究测得整体生产率提升 15%、新手提升约 30%；GitHub Copilot 实验中开发者完成任务快 56%——增益集中在经验较浅的人身上。但 [METR 的随机对照实验](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/)给了反例：16 名资深开源开发者在自己熟悉的代码库上用 AI 工具，完成任务反而慢了 19%——而他们自己感觉快了 20%。感知与实测的落差高达约 40 个百分点，这解释了为什么高管调查和实测数据经常互相矛盾：所有人都「感觉」AI 提效了。

这不是新故事。经济学家 Solow 在 1987 年就说过「计算机时代处处可见，唯独在生产率统计里看不见」——个人电脑的生产率效应花了十几年才在宏观数据里显形。简报的判断是：AI 在经济中的扩散速度会远慢于技术突破的速度。

## 给行业观测者的三个判断

**一、读任何「AI 导致 X」的就业论断，先查三个口径。** 数据来自谁（企业自报、工资单、还是家庭调查）、时间窗多长（是否覆盖了加息和疫情回调这两个混杂因素）、暴露度怎么定义。口径不亮出来的结论，一律当观点而非事实。

**二、把裁员归因当叙事读，不当证据读。** 亚马逊的例子是标准样本：备忘录本身把 AI 放在将来时，标题把它挪到了现在时。企业有充分动机把结构调整包装成技术转型，数据（5% 报告影响、增减各半）目前不支持这些公告的字面含义。

**三、盯窄信号，别盯宽叙事。** 总量失业率短期内不会给出 AI 信号；值得持续跟踪的是高暴露职业里的入口岗位——年轻软件开发者、客服、初级文书分析岗的招聘量和失业率（Stanford Digital Economy Lab 有[持续更新的仪表盘](https://digitaleconomy.stanford.edu/project/indicators/canaries-dashboard/)）。同时记住这份简报的边界：它只覆盖美国、数据止于 2026 年中，而 agent 类工具 2025 年底才开始成熟——按「扩散慢于突破」的逻辑，现在的数据本来就照不到它们。这不是简报的漏洞，而是它自己反复强调的不确定性。

我的综合判断：AI 对就业的影响目前「真实但窄」——对总量接近于无，对高暴露职业的入口岗位是真实压力。舆论场上两种声音都在失真：失业潮叙事把窄信号放大成了海啸，企业公告把宏观回调包装成了技术必然。技术跑得快、扩散走得慢，这个时间差恰恰是留给政策和个人调整的窗口——前提是我们盯着数据本身，而不是盯着标题。

## 参考来源

- [What is really happening to jobs? Separating AI hype from reality（SIEPR 政策简报）](https://siepr.stanford.edu/publications/policy-brief/what-really-happening-jobs-separating-ai-hype-reality) — 核心数据与结论：0.77/0.85 个百分点、新毕业生 5.6%、采用率各口径、5% 企业报告用工影响、80% 高管称未改变人员规模、呼叫中心与 Copilot 生产率研究转引
- [An update from SVP Beth Galetti on Amazon workforce reduction（亚马逊官方备忘录）](https://www.aboutamazon.com/news/company-news/amazon-workforce-reduction) — 开篇案例：1.4 万岗位裁减的官方归因原文
- [Canaries in the Coal Mine?（Stanford Digital Economy Lab）](https://digitaleconomy.stanford.edu/publication/canaries-in-the-coal-mine-six-facts-about-the-recent-employment-effects-of-artificial-intelligence/) — 22–25 岁高暴露职业就业下滑约 13%、年轻软件开发者下滑近 20%、替代型与辅助型职业的区分
- [Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity（METR）](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/) — 16 名资深开发者实测慢 19%、自感快 20% 的感知落差
