---
title: "对手实验室都点头了，反对 AI 调速的为什么是卖芯片的？"
description: "Dario Amodei 发文 48 小时：Altman、Musk、Hassabis 表态同意，反对票来自黄仁勋和一通打进峰会现场的总统电话。拆解表态队形为什么精确沿着供应链分布，以及三步方案还剩哪一步可核查。"
pubDate: 2026-09-14
tags: [ai-governance, ai-safety]
lang: zh
slug: pace-the-frontier-veto-map
translationOf: pace-the-frontier-veto-map
---

9 月 14 日上午，洛杉矶 All-In 峰会。黄仁勋正在台上和主持人讨论 Dario Amodei 两天前发表的《We Must Pace the Frontier》，他的手机响了，来电的是 Trump。据 [TechCrunch 的现场报道](https://techcrunch.com/2026/09/14/nvidia-ceo-jensen-huang-tells-trump-were-not-going-to-let-an-ai-slowdown-happen/)，Trump 在电话里说：「机器人不会接管世界，AI 不会接管世界，整件事是个骗局」；「他们正好落进一帮不想看到它发生的人的算计里——可能是政客，也可能是中国。我们不会让这发生」；「我们得稍微小心一点，做事要审慎，但这不意味着我们要叫停一个行业」。黄仁勋回答：「您说得对。我们不会让那发生，先生。」台下鼓掌。

这通电话把一件事摆到了明面上：Amodei 的调速提案发出 48 小时，同意和反对的名单已经齐了，而队形分得异常整齐——造模型的都点了头，说不的，是卖芯片的和管政府的。

## 48 小时表态清单

先交代提案本身。9 月 12 日，Amodei 在[个人网站发文](https://darioamodei.com/post/we-must-pace-the-frontier)，给「放慢前沿模型能力提升的速度」开出三步：第一步，每家前沿公司让第三方评估团队以等同员工的权限常驻办公室（工位、门禁卡、可自主发表调查发现），Anthropic 单方面即刻执行；第二步，民主国家的前沿公司在政府反垄断豁免保护下协调共同的安全标准和速率上限；第三步，民主政府与威权政府谈判，从禁止生物武器用途一路谈到给递归自我改进设「限速」。方案细节我在[当天的快讯](/zh/briefing-2026-09-12)里拆过，这里不重复。

然后是各方表态，按时间排：

- **9 月 12 日当天**，Sam Altman 发帖：「我同意 Dario，我们需要给前沿调速……承诺让独立评估员以等同员工的权限驻场是个好主意，我们会做同样的事」（据 [Zvi 的汇总](https://thezvi.wordpress.com/2026/09/14/we-must-pace-the-frontier/)转引，下同）。注意后半句：这是 OpenAI 对第一步的跟进承诺，有具体内容，可核查。
- Elon Musk 的表态只有三个词：「Dario is right」。Demis Hassabis 说方向是对的。Bernie Sanders 嫌不够，要求彻底暂停而非调速——批评声里有一支来自「太温和」一侧。
- **9 月 13 日**，前白宫 AI 事务负责人、现任总统科学技术顾问委员会（PCAST）联合主席 David Sacks [回应](https://twitter.com/DavidSacks/status/2098973625252708460)：「请便，你们自己就是前沿」——想减速自己减，别拿这个换反垄断豁免。我[昨天写过](/zh/briefing-2026-09-13)，这等于把方案里需要政府配合的部分整体挡了回去。
- **9 月 14 日**，就是开头那一幕。按 TechCrunch 的说法，黄仁勋在现场讨论中与 Amodei 立场相左；被完整记录下来的表态，就是回给 Trump 的那句「我们不会让那发生」。

截至发稿，我没有检索到 Meta 方面对这篇文章的公开表态。已公开表态的模型实验室掌门人里，没有一个反对调速本身。反对最硬的两票，一票来自算力供应商，一票来自华盛顿。

## 黄仁勋反对的不是安全论述，是货单

这个队形不需要阴谋论来解释，看各家卖什么就够了。

模型实验室卖的是能力的使用权。一个对所有人生效的对称速率上限，冻结的是相对位次：你慢我也慢，谁也没让出身位——这正是 Amodei 文中反复强调的设计前提（调速「必须让民主国家对威权国家的领先尽可能大」）。而前沿竞赛本身是实验室最大的成本项，出了事故，责任和名誉损失也记在实验室账上。顺着这个结构推——这是我的推演，没人会这么承认——一个绑住所有对手的上限，对实验室未必是坏生意：烧钱速度降下来，排名不变，尾部风险还小了。

Nvidia 的账完全相反。它卖的就是竞赛的投入品。Amodei 方案里「按原料调速」那一条，点名要限制的三样东西——训练算力、训练方式、内部用 AI 改进 AI 的程度——第一样就是 Nvidia 的货。全行业协调减速，直接砍的是它的订单增速。而且砍的还不只是未来订单：Nvidia 这两年一直在给自己的买家出钱——承诺在 2032 年前兜底购买 CoreWeave 至多 63 亿美元卖不掉的算力（[SEC 8-K](https://www.sec.gov/Archives/edgar/data/1769628/000176962825000047/crwv-20250909.htm)），对 OpenAI 承诺与 10 吉瓦系统部署绑定的至多 1000 亿美元投资（[官方公告](https://nvidianews.nvidia.com/news/openai-and-nvidia-announce-strategic-partnership-to-deploy-10gw-of-nvidia-systems)）。《经济学人》上周[把它比作 AI 的央行](https://www.economist.com/interactive/briefing/2026/09/03/nvidia-is-the-central-bank-of-ai)（[我的拆解](/zh/briefing-2026-09-12)）：借出去的钱都押在客户继续扩张上。对这样一张资产负债表，「调速」是个系统性风险词。

还有第二条战线。Amodei 文中重申了他的出口管制立场：「不要向中国出售强大的 AI 芯片或半导体制造设备，并打击芯片走私。」黄仁勋在这个问题上的立场同样公开：2025 年 5 月他在 Computex 说「总的来看，出口管制是一次失败」，并给出数字——Nvidia 在中国的市场份额从 2021 年的约 95% 掉到了 50%（[CNBC](https://www.cnbc.com/2025/05/21/nvidia-ceo-jensen-huang-slams-us-chip-restrictions-as-a-failure.html)）。

所以 9 月 14 日那句话不是即兴发挥。2025 年 6 月，黄仁勋就在巴黎 VivaTech 上说他「几乎不同意 Amodei 说的每一件事」，并把对方的立场概括成三条：AI 可怕到只有他们该做、贵到别人做不起、强到所有人会失业，「所以只有他们公司该做这件事」；他自己的主张是「要安全就公开地做，别躲在暗屋里做完告诉我这很安全」（[Fortune](https://fortune.com/2025/06/12/jensen-huang-has-a-bone-to-pick-with-dario-amodei)，Anthropic 当时否认 Amodei 说过「只有 Anthropic 该做」）。十五个月过去，双方的论点都没变，变的是这次有一位总统打电话进来站队。

## 激励地图解释不了 Musk

把表态全部还原成买卖关系，有一个明显的反例：Musk。xAI 是重度买卡方，若立场纯由货单决定，他该站黄仁勋一边；7 月那封 Pacing the Frontier 联署信，主要实验室里唯独 xAI 缺席（[我当时的拆解](/zh/pacing-the-frontier-open-letter)）。这次他却说「Dario is right」。

我对这个反例的读法是：它恰好标出了表态的价格。「Dario is right」三个词，零成本，和他从 2014 年起的 AI 风险言论完全兼容，不承诺 xAI 做任何事。Altman 的表态里唯一有分量的部分，也是那半句有具体内容的「我们会做同样的事」。7 月我写过那封联署信为什么能聚齐上千个签名：它把诉求降级成「保留减速的选项」，签名几乎零成本。Amodei 这篇往前走的一步，恰恰是给表态标了价——驻场评估员要占工位、发门禁卡、让出发表权。价格一出现，口头同意和掏钱同意就分开了。

## 方案还剩下什么

按这 48 小时的回应盘点三步方案：第三步（国际协调）的收信人在直播电话里说这是骗局；第二步依赖的反垄断豁免，被 PCAST 联合主席顶了回去；剩下的是第一步——不需要任何人点头的那一步——现在有 Anthropic 的单方面承诺，加上 OpenAI 的跟进承诺。

这就是「单方倡议在缺乏约束力时能起多大作用」的实测答案：它拦不住任何一个反对者，但它逼着每个玩家在两天之内亮出了自己和「速度」的利益关系，而且这份记录是公开的。7 月的联署信登记的是「谁担心」，这一轮登记的是「谁的营收绑在不减速上」——两张名单以后都赖不掉。

接下来可观察的节点也随之收窄成三个：METR 这类机构的评估员有没有真的在 Anthropic 拿到工位和权限、第一份不经公司编辑的独立报告何时出现；OpenAI 那句「我们会做同样的事」落不落成同等权限；口头同意的 xAI 们有没有任何一个跟进有成本的动作。刹车若真造得出来，第一脚只能踩在实验室自己楼里——这 48 小时已经证明，楼外没人肯让它踩到自己。

## 参考来源

- [Dario Amodei: We Must Pace the Frontier](https://darioamodei.com/post/we-must-pace-the-frontier) — 三步方案全文、「按原料调速」清单、出口管制立场、「调速须保持民主国家领先」的设计前提
- [TechCrunch: Nvidia CEO Jensen Huang tells Trump 'we're not going to let (an AI slowdown) happen'](https://techcrunch.com/2026/09/14/nvidia-ceo-jensen-huang-tells-trump-were-not-going-to-let-an-ai-slowdown-happen/) — All-In 峰会现场经过、Trump 与黄仁勋的原话（Trump 发言另经 [Benzinga](https://www.benzinga.com/markets/tech/26/09/61779374/trump-calls-jensen-huang-live-on-stage-at-the-all-in-summit-robots-will-not-be-taking-over-its-all-a-hoax)、[CNBC](https://www.cnbc.com/2026/09/14/trump-phones-nvidia-huang-all-in-calls-data-center-opposition-hoax.html) 交叉核实）
- [Zvi Mowshowitz: We Must Pace The Frontier](https://thezvi.wordpress.com/2026/09/14/we-must-pace-the-frontier/) — Altman、Musk、Hassabis、Sanders 表态的转引汇总
- [David Sacks 回应帖（X）](https://twitter.com/DavidSacks/status/2098973625252708460) 及 [RealClearPolitics 署名评论](https://www.realclearpolitics.com/2026/09/13/my_response_to_dario_amodei_nobody_is_stopping_you_710814.html) — 「请便」回应原文
- [Fortune: Jensen Huang has a bone to pick with Dario Amodei（2025-06）](https://fortune.com/2025/06/12/jensen-huang-has-a-bone-to-pick-with-dario-amodei) — 黄仁勋 VivaTech 发言与 Anthropic 回应
- [CNBC: Jensen Huang slams US chip restrictions as a failure（2025-05）](https://www.cnbc.com/2025/05/21/nvidia-ceo-jensen-huang-slams-us-chip-restrictions-as-a-failure.html) — 「出口管制是一次失败」、中国份额 95%→50%
- [The Economist: Nvidia is the central bank of AI](https://www.economist.com/interactive/briefing/2026/09/03/nvidia-is-the-central-bank-of-ai)、[CoreWeave SEC 8-K](https://www.sec.gov/Archives/edgar/data/1769628/000176962825000047/crwv-20250909.htm)、[Nvidia–OpenAI 合作公告](https://nvidianews.nvidia.com/news/openai-and-nvidia-announce-strategic-partnership-to-deploy-10gw-of-nvidia-systems) — 循环融资结构与具体金额
- [本站：这封公开信没要求 AI 减速——它承认的事更值得担心](/zh/pacing-the-frontier-open-letter) — 7 月联署信的签名成本分析、xAI 缺席的观察
- [本站快讯 2026-09-12](/zh/briefing-2026-09-12)、[2026-09-13](/zh/briefing-2026-09-13) — 方案机制拆解、Sacks 回应的时间线
