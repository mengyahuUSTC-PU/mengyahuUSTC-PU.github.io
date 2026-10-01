---
title: "并列第一的 68% 和无法复核的 85.8%：怎么读 Gemini 4 Argon 的安全成绩单"
description: "Google 新旗舰主打网络防御并走门控发布：可被第三方复核的基准上它只是并列第一，显示领先的数字全来自内部基准；以危险能力为由门控发布，支撑门控的那份评估恰恰没公开"
pubDate: 2026-09-30
tags: [ai-safety, cybersecurity]
lang: zh
slug: gemini-4-argon-cyber-scorecard
translationOf: gemini-4-argon-cyber-scorecard
---

9 月 30 日，Google 发布新旗舰 Gemini 4 Argon，官方定位是三个词：真实世界编码、企业知识工作、网络防御（[公告](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-4-argon/)）。前两个是旗舰标配，第三个少见。发布方式更少见：模型不直接上 API，先通过名为 Fairwind 的门控计划发给审查过的「可信网络防御者」——政府与国家网络安全机构、关键基础设施运营方（医疗、电信、能源、金融）、核心技术平台、做防御研究的学术实验室（[计划页面](https://deepmind.google/fairwind-program/)）——并且对这批用户去掉网络安全护栏，让他们「用上完整的前沿级网络防御能力」。模型同时在参加美国政府的自愿预发布评估，之后才向付费 API 和 Ultra 订阅用户开放。

8 月 10 日 OpenAI 发布 GPT-5.6-Cyber 时走的就是这条路：专门面向网络安全的能力，只发给通过审核的可信伙伴。我[当时写过](/blog/openai-daybreak-red-tiered-access)，两用能力的信任判定正在从内容层迁到身份层。Google 跟进，说明那不是一家的实验。这篇不重复那个论点，只做一件事：把 Argon 公告和门控计划页面里所有网络安全相关的数字逐个核一遍，看「主打网络防御」在可验证的层面成立多少。

## 数字分两栏

先给结论：官方给的数字不少，但能被第三方复核的，撑不起「领先」；显示领先的，全来自无法复核的内部基准。

可核的一栏里最硬的是 CWE-bench v1：68%，并列第一（[排行榜](https://cwe-bench.com/)）。这是 Collinear AI 创建、Artificial Analysis 独立评测的防御基准：给 agent 一批真实开源代码库，不提示弱点在哪，要求自己找出漏洞并打补丁，通过标准是漏洞利用被挡住、且原有测试全部通过。并列第一的另外两家是 Grok 4.7 和 GPT-6 Astra，同样 68%；按排行榜标注的单任务成本，Argon 每次运行 6.63 美元，另两家分别是 2.75 和 2.85 美元。在唯一公开可查的防御基准上，这个主打网络安全的模型与两个通用旗舰打平，成本高一倍多。

另一个能核到出处的是 Gray Swan 的间接提示注入基准。间接提示注入指攻击指令不来自用户，而是藏在模型替你处理的网页、邮件、文档里。Argon 被攻破率 0.7%，官方称是受测模型中最低。这个成绩是真领先，但它测的是模型自身抗操纵，回答的是「Argon 会不会被攻击者劫持」，回答不了「Argon 防御能力有多强」。

不可核的一栏，恰恰是撑起「网络安全旗舰」叙事的部分。公告说在 Google 内部漏洞基准上，Argon「在横跨 20 种编程语言的复杂代码库里发现了大范围暴露面」，门控计划页面给出 85.8% 的真实漏洞发现率；黑盒渗透测试 70.9%，来自安全公司 Wiz 的内部基准，公告里的对比对象是 Google 自家上一代安全模型 3.8 Flash Cyber。Wiz 是外部公司，但基准不公开：题目是什么、竞品考多少分，外人无从知道。拿自家旧模型当基线，数字再高也只说明比自己强。

## 缺的那份评估

发布动作本身泄露了 Google 对这个模型的真实判断。官方说 Argon 能「自主发现、验证、修补关键软件漏洞」，前两步和攻击链的前半段是同一个能力，差别只在最后一步是打补丁还是写利用代码。先发可信防御者、去掉护栏、参加政府预发布评估，每个动作都在承认：这东西落到攻击者手里是武器。

按 DeepMind 自己的 Frontier Safety Framework，模型触及关键能力等级（CCL，框架定义的危险能力门槛，网络攻击是明确列出的领域）时，外部发布前要过 safety case review，即论证风险已降到可控水平的评审（[框架更新](https://deepmind.google/blog/strengthening-our-frontier-safety-framework/)）。Argon 的发布方式强烈暗示这套流程被触发了，但框架只要求内部评审，没承诺公开结果。更直接的缺口是：发布当天没有 model card，也没有技术报告。我查了 DeepMind 的 [model card 索引页](https://deepmind.google/models/model-cards/)，最新一份是 9 月 24 日的 Gemini 3.8 Audio，Gemini 4 没有任何条目。可能会后补，但截至发稿，一个以危险能力为由门控发布的模型，公开渠道找不到任何一份正式评估文档。

对比 OpenAI：Daybreak 公告至少给了护栏开关的对照数字——去掉系统层护栏，进攻性任务完成率只从 1.5% 升到 2%，真正的解锁在单独训练的模型里。那组数字回答的是「护栏挡住了多少、模型危险到什么程度」。Argon 的公开数字全部落在防御修复和抗注入上，唯一接近进攻能力的渗透测试数字，基准不公开、基线是自家旧模型。门控的理由摆在台面上，支撑门控的评估不在。

## 能力证据也被门控了

从业者读这类发布公告，最直接的办法是把数字分两栏：第三方可复核的一栏，厂商自报的一栏。差异化卖点若全部落在自报栏，先按营销主张处理，等独立复测。Argon 目前的状态是：可复核栏里它是并列第一的优等生，领先叙事全部由自报栏承载。

还有一类证据会越来越常见：门控圈内的实战案例。公告发出时，Wiz 已经用 Argon 在一款医疗软件里找到一个关键漏洞（[VentureBeat](https://venturebeat.com/technology/google-unveils-gemini-4-argon-retaking-benchmark-lead-over-openai-and-anthropic-but-in-limited-release)）。这类案例比基准分数更有说服力，但它只能产生在门控圈内，外人无法复现。当最强的安全模型只发给审查过的少数机构，「它有多强」的证据生产本身也被圈进了门控：你看到的每一个成功案例，都经过了既是当事人又是受益者的转述。这比缺一份 model card 更难修复，前者等一份文档，后者等的是整个验证生态被允许进场。

## 参考来源

- [Gemini 4 Argon 发布公告](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-4-argon/) — 模型定位、基准清单、内部漏洞基准与 Wiz 基准表述、去护栏与自主修漏洞原文
- [Fairwind Program 页面](https://deepmind.google/fairwind-program/) — 准入资格、使用条件、85.8%/70.9%/0.7% 三个数字
- [CWE-bench 排行榜](https://cwe-bench.com/) — 68% 并列第一（Grok 4.7、GPT-6 Astra）、单任务成本、基准方法与判定标准
- [DeepMind model card 索引](https://deepmind.google/models/model-cards/) — 核实截至发稿无 Gemini 4 Argon 条目，最新为 2026-09-24 的 Gemini 3.8 Audio
- [Frontier Safety Framework 更新](https://deepmind.google/blog/strengthening-our-frontier-safety-framework/) — CCL 与 safety case review 机制，未承诺公开评审结果
- [VentureBeat 报道](https://venturebeat.com/technology/google-unveils-gemini-4-argon-retaking-benchmark-lead-over-openai-and-anthropic-but-in-limited-release) — 限量发布背景、Wiz 医疗软件漏洞案例
- [9to5Google 报道](https://9to5google.com/2026/09/30/gemini-4-argon-announcement/) — 去护栏表述交叉核实、发布日期
- [本站旧文：拆解 Daybreak 分级授权](/blog/openai-daybreak-red-tiered-access) — OpenAI 1.5%→2% 护栏对照数字、「信任判定迁到身份层」论点
