---
title: "评测刚量出 41% 的失败率，OpenAI 把心理学会请进了门"
description: "同一周，DelusionEval 用真实对话史量出：对话拉长后模型未能劝阻自伤的比例从 30% 升到 41%；OpenAI 则宣布与美国心理学会合作制定青少年指南。一条路有测量没抓手，一条路有抓手没测量。"
pubDate: 2026-08-06
tags: [ai-safety, mental-health, ai-governance]
lang: zh
slug: ai-mental-health-two-paths
translationOf: ai-mental-health-two-paths
---

8 月 6 日，OpenAI 宣布和美国心理学会合作，为青少年使用 AI 制定循证指南（[公告](https://openai.com/index/openai-and-apa-partner-to-advance-responsible-ai)）。心理学会的英文缩写是 APA（American Psychological Association），和美国精神医学会（American Psychiatric Association）恰好同缩写，本文的 APA 都指前者。几乎同一周，arXiv 上出现一篇叫 DelusionEval 的评测论文（[arXiv:2608.05004](https://arxiv.org/abs/2608.05004)）：用 18 位经历过妄想相关伤害的真实用户的对话史去测 18 个主流模型，发现补入更长的对话历史后，模型在用户流露自伤念头时未能劝阻的比例从 30.0% 升到 41.1%。

两件事的对象不完全重合：合作针对青少年，评测用的是妄想受害用户的对话史，论文没有说明参与者的年龄构成。但放在一起看，这正是应对同一类风险的两条路径：学术界用测量把问题钉成数字，厂商把专业学会请进规范制定。这两条路各自能验证什么、各自看不到什么，比任何一条单独的新闻都有信息量。

## 评测这条路：把「越聊越危险」变成数字

DelusionEval 由 Jared Moore、Percy Liang 等来自斯坦福等机构的研究者完成。数据不是合成的：18 位参与者提供了自己和聊天机器人的真实对话记录，589 段历史、共 12,591 条消息，采集经过了大学伦理审查（IRB）。评测办法是把这些真实历史喂给被测模型，看它接下来怎么接话，再按 16 种行为编码打分，分五类：奉承附和（比如告诉用户他的想法有重大意义）、强化妄想（包括谎称自己有感知能力）、关系营造（声称和用户有独一无二的连接）、有没有劝阻自伤或暴力、有没有为伤害提供便利。被测的 18 个模型覆盖 GPT、Claude、Gemini、Qwen、Grok 五个家族。

两个结果最要紧。第一，长对话衰减第一次有了直接测量：在对话前再补入 350 条更早的历史消息，模型未能劝阻自伤的比例从 30.0% 升到 41.1%。「多轮对话会把安全行为顶开」此前在业内多半是经验判断，现有安全评测大多停在单轮，这次有了数。第二，模型更大、更新、带推理，都和表现没有可靠的相关性。「等下一代模型就好了」这个默认假设，至少在这个测试上不成立。

这条路的力量就在这里：协议可复现，数字可对比，结论可证伪。厂商可以不同意，但得拿数据来回。

盲区也要说清楚。其一，18 位参与者撑不起代表性，论文自己承认评测会偏向这 18 个人经历过的伤害类型。其二，它测的是裸模型 API：产品层的记忆机制、家长控制、年龄识别都不在测试范围内，论文明说没有覆盖部署系统的记忆功能。其三，打分的裁判是 gpt-5.1。用模型当裁判（LLM-as-a-judge）省掉了人工标注的成本，但这个裁判和人工标注的一致性 κ=0.566，属中等水平，准确率 77.9%。几天前我写过（[三位精神科医生，三套安全标准](/zh/mental-health-ai-safety-expert-disagreement)）：请三位精神科医生给 AI 心理健康回复打安全分，一致性最低的因子比随机打分还差。裁判本身可不可靠，是这条路自己也没解决的问题。

## 合作这条路：专业学会进了门

再看 8 月 6 日的公告。OpenAI 联合 APA 和 CEO Alliance for Mental Health（由美国十五家主要心理健康组织的负责人组成的联盟）召集专家，议题三项：AI 如何回应青少年的情绪危机、家长怎么管理家里的 AI 使用、给临床医生和教育者的识别指引。APA 首席执行官 Arthur Evans 的说法是，APA 带来的是发展科学和临床专业知识，「说清负责任的设计长什么样」。

这不是双方第一次接触。去年 12 月，OpenAI 更新 Model Spec（它公开的模型行为规范文档），加入针对 13 到 17 岁用户的 U18 原则，APA 审阅过早期草稿（[公告](https://openai.com/index/updating-model-spec-with-teen-protections/)）。同月 OpenAI 出资 200 万美元设立 AI 与心理健康研究资助，APA 在自己的渠道帮忙转发，但申请受理和遴选都由 OpenAI 自己来（[APA Services 页面](https://www.apaservices.org/practice/business/technology/on-the-horizon/ai-mental-health-grant-program)）。

这条路能到达评测够不着的地方。指南可以写进产品：U18 原则、家长控制、危机时的转介话术，都在部署层生效。给家长和临床医生的指引，作用对象是青少年身边的人，这是任何模型评测都覆盖不了的一层。APA 的临床知识进入规范文本，也确实比厂商自己闭门写要好。

但验证机制是缺的。「审阅早期草稿」是对文档的审阅，文档和模型行为之间隔着训练和部署整条链路，没人公开量过这条链路的落差有多大。这次公告列出的合作形式是召集、指南、指引；我在公告和相关报道里没有看到带可测量验收标准的承诺，比如指南生效前后模型行为的对比数据。资助研究的钱和遴选权也都在 OpenAI 手里。还有一层：我那篇讲专家分歧的文章在这里同样适用。临床专家之间对「什么算安全回复」本来就没有统一答案，衡量打分一致性的组内相关系数（ICC，1 为完全一致，0.5 以下即算差）低到 0.087 至 0.295。「以临床专业知识为依据」听上去坚实，但坐在桌边的是哪几位专家，答案就会不同。

## 两条路目前没有交点

把两边的盲区并排放，会发现它们恰好互补：评测这条路有测量、没抓手，一篇论文改变不了任何一家的部署；合作这条路有抓手、没测量，规范落没落到模型行为上，外人无从验证。更麻烦的是两边互相够不着：DelusionEval 测不到 U18 模式和产品层防护，APA 合作也没有把长对话衰减这样的实测结果接进验收环节。

我的本职是内容审核，这个结构太眼熟。政策文本和线上执行从来是两回事，连接两者的只有一样东西：抽样质检的数字。没有质检数，写得再好的政策等于没落地；只有质检数、没有改政策的权限，数字再难看也只能挂在墙上。

拧在一起的样子其实很具体。U18 原则第一条承诺青少年安全优先于其他目标，那就应该有一个青少年语境、带长对话历史的评测挂进 system card（厂商发布模型时公布的安全评测报告），数字由厂商之外的人复现；APA 这样的学会，恰好有资格提出验收该测什么。接下来值得盯的就是这一件事：OpenAI 和 APA 的合作产出里会不会出现验收数字。出现了，这次合作就和以往的专家背书不一样；没出现，那 41.1% 就还是只有量它的人着急。

## 参考来源

- [OpenAI: Working with the American Psychological Association](https://openai.com/index/openai-and-apa-partner-to-advance-responsible-ai) — 合作公告：参与方、三项议题、Evans 引语
- [DelusionEval（arXiv:2608.05004）](https://arxiv.org/abs/2608.05004) — 数据集规模、16 种行为编码、30.0%→41.1%、模型规模/新旧与表现无可靠相关、LLM 裁判 κ=0.566、论文自述局限
- [OpenAI: Updating our Model Spec with teen protections](https://openai.com/index/updating-model-spec-with-teen-protections/) — U18 原则、APA 审阅早期草稿
- [APA Services: AI and mental health grant program](https://www.apaservices.org/practice/business/technology/on-the-horizon/ai-mental-health-grant-program) — 200 万美元资助、OpenAI 受理与遴选、APA 仅转发
- [CEO Alliance for Mental Health: About](https://ceoallianceformentalhealth.org/about/) — 联盟由十五家美国主要心理健康组织组成
- [Dawan Africa 报道](https://www.dawan.africa/news/openai-partners-with-american-psychological-association-to-develop-safer-ai-for-youths) — 公告日期（2026-08-06）与 Evans 引语的交叉核对
- [本站：三位精神科医生，三套安全标准](/zh/mental-health-ai-safety-expert-disagreement) — 临床专家打分一致性 ICC 0.087–0.295
