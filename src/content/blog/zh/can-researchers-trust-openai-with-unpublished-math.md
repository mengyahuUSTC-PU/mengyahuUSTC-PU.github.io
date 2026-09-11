---
title: "OpenAI 拿出了十个数学证明，却拿不出数学家要的那一个"
description: "一周之内，两位数学家先后公开要求 OpenAI 证明：他们未发表的成果没有流进模型。指控无法证实，否认无法证伪，这个僵局比任何一方的对错都更值得拆解。"
pubDate: 2026-09-10
tags: [research-integrity, ai-governance, openai]
lang: zh
slug: can-researchers-trust-openai-with-unpublished-math
translationOf: can-researchers-trust-openai-with-unpublished-math
---

9 月 9 日，[德累斯顿工业大学的群论学家 Andreas Thom](https://tu-dresden.de/mn/math/geometrie/thom) 在 [Mathstodon 上公开](https://mathstodon.xyz/@andreasthom/117240535270608201)了他与 OpenAI 研究员的通信。8 月初，[OpenAI 宣布](https://openai.com/index/ten-advances-in-mathematics/)其内部模型解决了十个数学与理论计算机科学的开放问题，其中一个的证明核心恰好建立在 Thom 与 Gábor Kun 的工作之上。Thom 给 OpenAI 的研究员发邮件，问了两个问题：我过去几个月和 ChatGPT 讨论这些数学时的对话，有没有进入训练数据？产出证明的系统，能不能访问到这些对话？

研究员 Mark Sellke 的回复只有一句：「至于你和 ChatGPT 的那些对话：那件事没有发生。」

一个月后，OpenAI 在另一场更大的争议里发了[官方声明](https://x.com/OpenAI/status/2097375276384567642)，其中一句等于替 Thom 把第一个问题的诚实答案补上了：「虽然可能性不大，但我们无法排除：源自他们使用我们产品的去标识化数据，帮助改进了我们的模型。」

Thom 是一周之内第二位公开向 OpenAI 要说法的数学家。先看第一位。

## 一周，两位数学家

Navier-Stokes 方程描述流体如何运动，对应的[千禧年大奖问题（2000 年提出）](https://www.claymath.org/millennium-problems/)问的是：从光滑的初始状态出发，方程的解会不会在有限时间内「爆破」，也就是解失去题目要求的光滑性、方程不再能描述这股流动。[Clay 研究所的官方题面](https://www.claymath.org/wp-content/uploads/2022/06/navierstokes.pdf)给了四个可选命题，证出任何一个都算解决；其中两个「爆破」版本允许在方程里加一个光滑的外力项。

纽约大学的 Tristan Buckmaster 和 Anthropic 的数学家 Levent Alpöge 以个人身份合作，花了近一年时间用 AI 模型（Claude、OpenAI 的 Codex 等）追打这条爆破路线。路线的基本思想来自 Diego Córdoba 和 Luis Martínez-Zoroa 两位数学家多年经营的带外力爆破纲领；Buckmaster 在[公开的四页声明](https://cims.nyu.edu/~tristanb/statement.pdf)里说，据他所知这条路几乎没有其他人在走，而两人整个项目的全部草稿都放在 Codex 会话里。声明记录的时间线是（另见 [TechCrunch 报道](https://techcrunch.com/2026/09/08/openai-fought-dirty-on-career-making-math-problem-says-nyu-mathematician/)）：9 月 3 日，他把项目进展告诉了 OpenAI 的一位数学家，说明这是与两家公司都无关的个人项目；三天后，OpenAI 研究员 Sébastien Bubeck 在通话中告知他，内部模型已经产出一份带外力 Navier-Stokes 有限时间爆破的约百页证明，走的正是同一条路线。声明还指控 OpenAI 提议让他以独著形式发表、把任职于 Anthropic 的 Alpöge 从署名中去掉，并称他在表示要公开此事时被问「你为什么要毁掉自己的职业生涯？」。Bubeck [否认了署名指控，并公开承认两人工作的优先权](https://the-decoder.com/openai-researcher-allegedly-pressured-mathematician-to-drop-anthropic-co-author-from-math-breakthrough-paper/)。

9 月 7 日，两人赶在 OpenAI 之前公开了三个相邻方程（不可压缩多孔介质方程、二维 Boussinesq 方程、三维不可压缩 Euler 方程）带光滑外力的有限时间爆破证明；按声明的说法，这是把 Córdoba 与 Martínez-Zoroa 原本在粗糙外力下的爆破构造，借助 LLM 推进到光滑外力、并推广到 Euler 等方程。Terence Tao [当天在博客里](https://terrytao.wordpress.com/2026/09/07/finite-time-blowup-with-smooth-forcing-term-for-the-incompressible-porous-medium-boussinesq-and-incompressible-euler-equations/)介绍了这组工作，指出论证大量借助了 AI，且方法很有希望推广到 Navier-Stokes 本身。OpenAI 随后照样[宣布解决了带外力的 Navier-Stokes 爆破](https://www.cnbc.com/2026/09/09/openai-navier-stokes-math-problem-solved.html)，并表示不申领 100 万美元奖金。Alpöge 对 OpenAI 那句「无法排除」的[回应](https://x.com/__alpoge__/status/2097383870773748190)带着挖苦：这算他们爽快认账了。

Thom 的故事线更早。1999 年，Gromov 提出一个问题：是否每个群（描述对称性的代数结构）都能被有限的置换很好地近似？能被近似的群后来称作 [sofic 群](https://mathworld.wolfram.com/SoficGroup.html)，27 年间没人造出反例。OpenAI 8 月 1 日公布的十个成果里就有第一个 non-sofic 群的构造，其证明的关键一步直接建立在 [Kun 2016 年的定理](https://arxiv.org/abs/1606.04471)和 [Kun–Thom 2019 年的论文](https://arxiv.org/abs/1901.03963)之上；据 [Northeast Times 报道](https://northeasttimes.com/2026/09/10/two-mathematicians-demand-answers-from-openai-on-training-data/)，最初的成果介绍没有提到两人的贡献，被数学家指出后才悄悄补上。这个结果已有数学界的后续工作跟进：已有数学家作为回应[构造出无挠（torsion-free）的 non-sofic 群](https://arxiv.org/abs/2608.02025)。

让 Thom 起疑的是路线选择。用他[在 Mathstodon 帖子里](https://mathstodon.xyz/@andreasthom/117240535270608201)的话说，Kun–Thom 这条路「从来不是领先候选」，圈内原本更看好借道量子计算复杂度的另一条路线；而他恰好花了几个月时间，和 ChatGPT 反复讨论 expander 匹配问题（expander 是一类连接性极强的稀疏图）以及 Kun–Thom 工作的延伸。模型偏偏沿着这条冷门路线走通了。他 6 月 29 日关掉了账户里「用我的数据改进模型」的开关，但按 [OpenAI 的官方说明](https://help.openai.com/en/articles/8983099-does-the-improve-the-model-for-everyone-setting-sync-between-web-and-mobile-devices)，这类开关只约束今后的新对话；之前的对话有没有进过训练，OpenAI 也不提供逐对话的使用记录（[数据控制说明](https://help.openai.com/en/articles/7730893-data-controls-faq)），用户无从查证。

## 三句否认，三个口径

先把立场说清楚：目前没有公开证据表明 OpenAI 拿了这两组人的成果（[Axios 的梳理](https://www.axios.com/2026/09/08/openai-math-solution-navier-stokes-credit)同样停在疑问层面）。Buckmaster 在声明里写得很直接：「我没有在指控任何人」，他陈述的只是自己被告知了什么、何时、以及被提议了什么；Thom 提出的也是疑问而非断言。Buckmaster 的核心疑问是时机与路线的巧合，Thom 的核心疑问是没人正面回答他。真正值得拆的是 OpenAI 三句否认的结构。

Sellke 对 Thom 说「那件事没有发生」。Thom 问了两个问题，这句话按最自然的读法只覆盖第二个，也就是解题时有没有访问他的对话；训练数据那一问，[截至发稿 OpenAI 没有公开回答](https://northeasttimes.com/2026/09/10/two-mathematicians-demand-answers-from-openai-on-training-data/)。

OpenAI 对 Buckmaster 事件的官方声明说：「在他们公开发表之前，我们（研究员和智能体）没有通过任何途径看到过他们的工作。特别是，为解决这个问题，没有访问任何特定用户数据。」否认的对象是人看过草稿、以及解题时检索了特定用户的数据。这两件事都足够窄，窄到可以干脆地否认。

同一份声明里才出现那句关键的话：无法排除去标识化的使用数据改进了模型。数学家真正问的正是这一层，而这一层的答案是排除不了。

三句话摆在一起，我读出的模式是：每次否认都精确地覆盖能够否认的最窄口径，最宽的那个口径留白，直到舆论压力把它逼出来。我不认为这是公关失误。我的推测是，训练管道这一层 OpenAI 自己也未必给得出干净的答案：公开资料里看不到任何能把一条对话追溯到某个训练批次的机制。

## 为个人隐私造的工具，护不住未发表的定理

这场争议容易被读成「隐私问题」，但为个人隐私设计的那套工具，在保护未发表成果这件事上帮不上多少忙，原因有三层。

第一层是保护对象错位。隐私合规的整套工具（[去标识化](https://csrc.nist.gov/publications/detail/nistir/8053/final)、匿名聚合、opt-out）保护的是身份。把 Thom 的名字从对话里抹掉，剩下的数学思想一点没少；而学术优先权的载体恰恰是内容本身，跟身份无关。这是 Thom 论证里最锋利的一点：为个人数据设计的保护，对「想法被学走」不起作用。

第二层是时间方向。训练开关只管以后，不管以前；OpenAI 也没有提供「哪条对话进了哪个训练批次」的记录，用户无从事后对账。[Hacker News 上的讨论](https://news.ycombinator.com/item?id=49639408)（截至发稿有 600 多条评论）里，多位用户还报告这个开关会在不知情时被重置回「开」。我没有验证过重置的说法，但方向不重要，要害在于：整个机制的可信度建立在厂商单方面的执行上，官方没有给用户任何可核验的凭据。

第三层最根本：自查不可证伪。学术界处理同类利益冲突靠制度。期刊审稿人负[保密义务](https://publicationethics.org/files/Ethical_Guidelines_For_Peer_Reviewers.pdf)，不得利用稿件为自己谋利，违反要承担职业后果，而且有编辑部这个第三方来裁决争议。AI 公司如今坐在结构相同的位置上：既是研究者的工具供应商，又在同一批问题上和研究者竞赛。但配套机制是零：OpenAI 公开的信息里，看不到可逐条追溯的训练数据来源记录，也看不到开放给第三方审计的模型 checkpoint，而在这场争议里，迄今所有的调查和声明都出自 OpenAI 自己。相当于让期刊审稿人自己决定要不要抢投稿人的结果，出事后再由他本人出具调查报告。

## 研究者现在能做什么

给正在用这些工具做研究的人，我能给出两条具体判断。

把消费级账户里的对话，按「已向一家潜在竞争者披露」来管理。企业和 API 客户拿得到[合同级的不训练承诺](https://openai.com/enterprise-privacy/)，[我此前拆解过 OpenAI 的零数据留存政策](/zh/openai-zero-data-retention-private-safety-processing)，那套保障个人账户默认都没有。HN 讨论里有一条建议我完全同意：高校和研究机构应该像企业客户一样去谈合同条款，而不是让每位研究者各自面对一个自己无法审计的开关。

优先权要靠时间戳，别靠完美的成稿。Buckmaster 和 Alpöge 的优先权能得到对方公开承认，靠的是 9 月 7 日抢先把远称不上完善的版本公开，Buckmaster 自己在声明里都为这些稿子的完成度道了歉。在 AI 公司也下场解题的环境里，「攒一个漂亮 writeup 再发」的代价结构已经变了：早挂出来的粗糙版本，比晚发的精致版本值钱。

至于 AI 公司这一侧，Tao 的批评点在另一个层面：他[公开表示](https://fortune.com/2026/09/08/openai-says-it-cracked-navier-stokes-math-grand-challenge-buckmaster-accusation-cheating-intimidation-tao-lament/)，AI 公司正把这些悬置多年的难题当作展示模型实力的营销素材，并警告说，不加节制地把开放问题当矿藏采掘，可能会毁掉未来数学技术赖以生长的生态。顺着这条批评还能再看远一步：Gromov 的问题悬了 27 年，Navier-Stokes 悬了 26 年，这批开放问题是几代数学家攒下的存货。AI 工具消化存货的速度一旦上来，稀缺的能力就会从解题挪向提出问题：判断哪些新问题值得解、把它们表述成能着手攻的形式，这件事眼下我还看不到模型能替人做。我的判断更窄一些：这一周真正被消耗的，是 AI 公司做科学研究的信用。数学界对优先权的计较全行业出名，一次含糊的否认，在这个圈子里的代价来得格外快。数学家只是最先把这笔账算清楚的人；同样的结构性冲突，摆在每一个把未发表的想法喂进闭源工具的行业面前。

## 参考来源

- [Andreas Thom 的 Mathstodon 帖子](https://mathstodon.xyz/@andreasthom/117240535270608201) — Thom 的两个问题、Sellke 回复原文、与 OpenAI 声明的对照
- [OpenAI: Ten advances in mathematics and theoretical computer science](https://openai.com/index/ten-advances-in-mathematics/)（[配套 GitHub 仓库](https://github.com/openai/ten-proofs)） — 十个成果清单、non-sofic 群构造、Lean 形式化说明
- [OpenAI 官方 X 声明](https://x.com/OpenAI/status/2097375276384567642) — 「没有访问特定用户数据」与「无法排除去标识化数据」两句原文
- [Buckmaster 的四页声明（PDF）](https://cims.nyu.edu/~tristanb/statement.pdf) — 9 月 3 日至 6 日的完整时间线、两个提议、被引用的原话、对 Córdoba 与 Martínez-Zoroa 的致谢
- [Kun & Thom, Inapproximability of actions and Kazhdan's property (T)（arXiv:1901.03963）](https://arxiv.org/abs/1901.03963) — 被 OpenAI 证明引用的 2019 年论文
- [Fournier-Facio, A torsion-free non-sofic group（arXiv:2608.02025）](https://arxiv.org/abs/2608.02025) — 数学界在 OpenAI 结果基础上的后续工作
- [Clay 研究所官方题面（Fefferman）](https://www.claymath.org/wp-content/uploads/2022/06/navierstokes.pdf) — 四个可选命题，爆破版本允许光滑外力
- [Terence Tao 博客（2026-09-07）](https://terrytao.wordpress.com/2026/09/07/finite-time-blowup-with-smooth-forcing-term-for-the-incompressible-porous-medium-boussinesq-and-incompressible-euler-equations/) — Alpöge–Buckmaster 三个爆破结果的介绍与评价
- [TechCrunch：OpenAI fought dirty on career-making math problem](https://techcrunch.com/2026/09/08/openai-fought-dirty-on-career-making-math-problem-says-nyu-mathematician/) — Buckmaster 声明的报道与 Bubeck 的回应
- [The Decoder 的报道](https://the-decoder.com/openai-researcher-allegedly-pressured-mathematician-to-drop-anthropic-co-author-from-math-breakthrough-paper/) — Bubeck 对署名指控的否认与对两人优先权的承认
- [Fortune 的综合报道](https://fortune.com/2026/09/08/openai-says-it-cracked-navier-stokes-math-grand-challenge-buckmaster-accusation-cheating-intimidation-tao-lament/) — Tao 对 AI 公司做数学的批评
- [CNBC 报道](https://www.cnbc.com/2026/09/09/openai-navier-stokes-math-problem-solved.html) — OpenAI 宣布解决带外力 Navier-Stokes、不申领奖金
- [Northeast Times 报道](https://northeasttimes.com/2026/09/10/two-mathematicians-demand-answers-from-openai-on-training-data/) — 署名补正、Thom 的 opt-out 时间（6 月 29 日）等细节
- [Alpöge 的 X 回应](https://x.com/__alpoge__/status/2097383870773748190) — 对 OpenAI「无法排除」措辞的回应
- [Hacker News 讨论](https://news.ycombinator.com/item?id=49639408) — 开关重置报告、机构谈判合同的建议
- [本站前文：拆解 OpenAI 的「私有安全处理」](/zh/openai-zero-data-retention-private-safety-processing) — 零数据留存的合同保障范围
