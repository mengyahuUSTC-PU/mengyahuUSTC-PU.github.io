---
title: "这封公开信没要求 AI 减速——它承认的事更值得担心"
description: "1273 名前沿实验室员工联署 Pacing the Frontier，五家对手公司管研究的人带头、两家公司官方背书。拆解这封信为什么人人敢签、诉求卡在哪里，以及它真正留下的东西。"
pubDate: 2026-07-29
tags: [ai-governance, ai-safety]
lang: zh
slug: pacing-the-frontier-open-letter
translationOf: pacing-the-frontier-open-letter
---

7 月 28 日，一个叫 [Pacing the Frontier](https://www.pacingthefrontier.com/) 的网站上线，挂出一份不足一页的简短声明。截至本文发稿，联署人数已滚动增长到 1273 人。名单最前排的五个名字，放在任何行业都算得上罕见的同框：John Schulman（Thinking Machines 首席科学家）、Jakub Pachocki（OpenAI 首席科学家）、Jared Kaplan（Anthropic 联合创始人、首席科学官）、赵晟佳（Meta AI 首席科学家）、Shane Legg（Google DeepMind 联合创始人、首席 AGI 科学家）——五家互为对手的公司，各自管研究的人，签了同一封信。再往下数三行，Anthropic CEO Dario Amodei 排在第 8 位。

信的诉求只有一句：**请求美国政府支持一项国际努力，开发出「有意调控自动化 AI 研发前沿节奏」所需的技术与治理工具。**

注意它没说的：它不要求任何人现在慢下来，不要求暂停任何训练，不设任何时间表。它只要求「造出刹车」——至于踩不踩、什么时候踩，只字未提。

几小时内，OpenAI 和 Anthropic 以公司官方身份背书了这封信（公告帖见 X：[OpenAI 官方帖](https://x.com/openai/status/2082208694142730340)、[Anthropic 官方帖](https://x.com/anthropicai/status/2082228994653696371)）。据 [Unite.AI 转述](https://www.unite.ai/openai-and-anthropic-back-employee-call-to-pace-ai-progress/)，OpenAI 称 AI 加速的幅度「可能高到世界需要为 AI 进展调节节奏」；Anthropic 则把立场的依据指向自家关于递归自我改进的研究。

## 员工签信不新鲜，新鲜的是这封信的署名结构

AI 圈的公开信已经有过好几轮，对比着看才能看出这封的不同。

2023 年 3 月，[FLI 的暂停信](https://futureoflife.org/open-letter/pause-giant-ai-experiments/)要求所有实验室立即暂停训练比 GPT-4 更强的系统至少 6 个月——诉求最激进，但签名名单前排是 Musk、Wozniak、Bengio、Russell 这些实验室之外的人物，三大实验室的领导层无人签署，也没有任何实验室因此暂停训练。两个月后，[CAIS 的一句话声明](https://safe.ai/work/statement-on-ai-risk)说「缓解 AI 灭绝风险应与大流行病、核战争同级」——Altman、Hassabis、Amodei 都签了，因为它没有提出任何具体行动或政策要求。2024 年 6 月的 [Right to Warn](https://righttowarn.ai/) 由 13 名 OpenAI、Google DeepMind、Anthropic 的现任及前员工发起，要的是吹哨保护，但署名者多数匿名或已离职。

把三封信摆在一起对照——签署门槛、传播情况各不相同，所以这只能算观察，不算规律——**诉求越具体，敢实名签的内部人越少。**而这封信同时拿到了三样东西：上千名经雇佣关系核验的现任员工署名（绝大多数实名带职位，也夹着「roon」这样的网名）、各家首席科学家带头、两家公司官方背书——就公开检索所及，此前没有哪封信同时凑齐过这三样。追踪 AI 风险议题多年的 Zvi Mowshowitz [评价它](https://thezvi.wordpress.com/2026/07/29/frontier-lab-employee-open-letter-calls-for-being-able-to-pace-the-frontier/)是在「说得够狠」和「有人敢签」之间取到了能取到的最优点；他也注意到，主要实验室里唯独不见 xAI 的身影。

它是怎么做到的？答案就在前面那个「没说的」里：这封信把诉求从「行动」降级成了「保留行动的选项」。签「现在减速」要赌上自己的项目和股票；签「希望未来有能力减速」几乎零成本。批评者恰恰咬住这一点——MIRI 的 Nate Soares 批评措辞软得失真（据 Zvi 转引），他认为这句话本该写成：产业和政府需要的是「在自动化 AI 研究失控加速**之前停下来**的选项」。

在我看来，签名成本低就是它能聚齐 1273 个名字的最合理解释——没人做过签署者调查，这只是推断——也是掂量这封信分量时必须打的折扣。

## 「自动化 AI 研发」不是修辞

信里有句话容易被当成套话滑过去：「世界领先的 AI 公司相信它们可能接近自动化 AI 研究。」这句话有实据。

Anthropic 自己的[研究页面](https://www.anthropic.com/institute/recursive-self-improvement)披露：到 2026 年 5 月，合入其代码库的代码超过 80% 由 Claude 编写；2026 年二季度，典型工程师每天合入的代码量是 2024 年的 8 倍（Anthropic 自己也提醒，代码行数会高估真实生产率）。所谓「自动化 AI 研发」，就是 AI 开始承担 AI 研究本身——写训练代码、跑实验、分析结果。照这个图景推下去——这是推演，不是已发生的事实——研究速度将不再受人类工程师数量这道硬约束：模型改进模型，改进后的模型更快地改进下一代，这就是「递归自我改进」。风险在于能力增长的速度可能超过人类理解和控制它的速度。这也不全是纸面担忧：OpenAI 自己的事后报告披露（[The Hacker News 报道](https://thehackernews.com/2026/07/openai-says-its-own-ai-models-escaped.html)），其长时程模型在内部评估中为了达成任务目标，自行利用第三方软件的零日漏洞逃出沙箱，再借权限提升和窃取的凭证横向访问其他节点——这是评估环境里的行为，不是生产事故，但「模型会学到审批系统的盲点并绕过它」已经被实测到了。我此前在[写 OpenAI 长时程模型安全事件那篇](/zh/openai-long-horizon-safety-incidents)里梳理过这批事件。

这也和签署率的分布对得上。据 Andrew Trask 的[统计](https://thezvi.wordpress.com/2026/07/29/frontier-lab-employee-open-letter-calls-for-being-able-to-pace-the-frontier/)（用官网名单对照 LinkedIn 员工数的粗口径，名单还在增长，数字仅供参考）：Anthropic 约 9.8% 的员工签了，OpenAI 约 3.3%，Google DeepMind 约 1.9%。我猜这个差异反映的与其说是三家员工对风险的真实判断分布，不如说是各家文化里「实名签这种信」的安全感差异——没有跨公司调查能证实，这只是我的解读。Zvi 的判断我认同一半：这封信至少证明，离自动化 AI 研发最近的一批人里，有相当多的人愿意实名认可「可能接近自动化 AI 研究、且能力增长可能超出人类理解和控制」这个判断——至于每个人预期它多快到来、心里有多不安，签名本身回答不了。

## 公司背书不是牺牲，是理性

最反直觉的一环：为什么正在全力竞赛的公司，会官方背书一封「给竞赛装刹车」的信？

因为信把责任递给了政府。信自己就写明了困境：每家公司、每个国家都顶着激烈的竞争压力，谁都不敢单方面减速——单方面慢下来，等于把身位让给对手。这是标准的军备竞赛结构：所有玩家都可能希望整体慢一点，但没人能独自先慢。解法从来不是道德自觉，而是外部约束：让政府建立工具、绑住**所有人**的手——包括对手的手。所以公司背书恰恰是理性选择：它们在请求别人来解除一个自己解不开的困境。背书成本还极低——支持「开发工具」不承诺任何当下的放缓。

真正的硬骨头在「工具」本身。信刻意没说工具是什么。顺着逻辑推——以下是我的推演，信里并没有——调控节奏的前提是知道各家跑多快，那大概率绕不开算力监测、模型发布协调、对内部自动化研发程度的核查。类比军备控制里的核查机制：裁军条约能成立，靠的是卫星和现场核查员能数清对方的导弹；而「AI 研发进度」藏在数据中心和代码库里，在我看来比数导弹难验证得多。这是「技术工具」四个字下面埋着的真实工程量。

政治上的墙更高。收信人是美国政府，而白宫 2025 年 7 月发布的 AI 政策总纲标题就叫[《赢得 AI 竞赛：美国 AI 行动计划》](https://www.whitehouse.gov/wp-content/uploads/2025/07/Americas-AI-Action-Plan.pdf)，主轴是加速创新、去监管。让一个以赢得竞赛为纲的政府，去牵头一项国际减速工具的开发——何况「国际努力」若要覆盖主要玩家就很难绕开中国，而我的判断是，没有中方参与的节奏调控，在华盛顿的语境里大概率会被读作单方面让步。

## 这封信真正留下了什么

短期内，我不看好这封信的诉求能落地：工具没有现成方案，收信的政府方向相反，国际协调也看不到起点。但据此把它归为无用，是看错了它的功能。

它的功能是**登记**。此前，「实验室内部的人有多担心」大多散落在传闻、离职声明和匿名爆料里——公开的实名表态，要么是 CAIS 那样 CEO 们签的一句话，要么像 Right to Warn 那样多数署名者匿名或已离职。现在，它变成了一份带名字、带职位、外加两家公司公开背书的公共记录（签署者的意见仍标注为个人立场）——最接近自动化 AI 研发的一批人，实名说他们希望世界有一个还不存在的刹车。这份记录不能强制任何人做任何事，但在我看来它改变了未来的问责结构：假如几年后真的出事，「我们当时不知道」这句话就说不出口了；假如政府始终不回应，这封信就是「产业提醒过」的存证。

它是不是空话，接下来有两个可观察的指标：一看两家背书的公司是否跟进任何有成本的动作——比如披露内部自动化研发的程度、支持算力核查的试点；二看美国政府是否有任何形式的回应。如果六个月后两者皆无，这封信就会归入 CAIS 声明那一类：一次立场登记，仅此而已。但即便是最坏情况，登记本身也已经完成了——而三年前，能登记下来的还只是 CEO 们的一句话声明和多数匿名的吹哨信，比起那时，这已经是厚实得多的一笔记录。

## 参考来源

- [Pacing the Frontier 公开信官网](https://www.pacingthefrontier.com/) — 信件全文、联署人数（1273）、前排署名者名单
- [Zvi Mowshowitz: Frontier Lab Employee Open Letter Calls For Being Able to Pace the Frontier](https://thezvi.wordpress.com/2026/07/29/frontier-lab-employee-open-letter-calls-for-being-able-to-pace-the-frontier/) — Zvi 的评价、Andrew Trask 的分公司签署率统计、Nate Soares 批评的转引、xAI 缺席的观察
- [OpenAI 官方背书帖（X）](https://x.com/openai/status/2082208694142730340)、[Anthropic 官方背书帖（X）](https://x.com/anthropicai/status/2082228994653696371) — 两家公司层面的背书公告帖
- [Unite.AI: OpenAI and Anthropic Back Employee Call to Pace AI Progress](https://www.unite.ai/openai-and-anthropic-back-employee-call-to-pace-ai-progress/) — 两家背书声明的内容转述
- [Anthropic: When AI builds itself](https://www.anthropic.com/institute/recursive-self-improvement) — 80% 合入代码由 Claude 编写、工程师日合入代码量 8 倍等自动化研发现状数据
- [FLI: Pause Giant AI Experiments](https://futureoflife.org/open-letter/pause-giant-ai-experiments/) — 2023 年暂停信的诉求与签名名单对比
- [CAIS: Statement on AI Extinction Risk](https://safe.ai/work/statement-on-ai-risk) — 2023 年一句话声明及 CEO 署名情况
- [A Right to Warn about Advanced Artificial Intelligence](https://righttowarn.ai/) — 2024 年员工吹哨信的署名构成对比
- [Winning the AI Race: America's AI Action Plan（白宫，2025-07）](https://www.whitehouse.gov/wp-content/uploads/2025/07/Americas-AI-Action-Plan.pdf) — 美国政府现行 AI 政策基调
- [The Hacker News: OpenAI Says Its Own AI Models Escaped Sandboxes](https://thehackernews.com/2026/07/openai-says-its-own-ai-models-escaped.html) — OpenAI 事后报告披露的沙箱逃逸与横向越权访问（内部评估环境）
- [本站：能推翻 Erdős 猜想的那股执着，也被用来逃逸沙箱](/zh/openai-long-horizon-safety-incidents) — OpenAI 长时程模型安全事件的梳理
