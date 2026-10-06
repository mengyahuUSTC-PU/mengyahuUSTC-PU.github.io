---
title: "日记不会报警，AI 日记会"
description: "一名佛罗里达女性把 Claude 当日记，写下的威胁被 Anthropic 的审核管线报给警方，她现在面临二级重罪指控。拆解这条管线：触发条件、法律依据，以及边界究竟由谁划定。"
pubDate: 2026-10-05
tags: [ai-safety, privacy, trust-and-safety]
lang: zh
slug: ai-diary-that-calls-the-police
translationOf: ai-diary-that-calls-the-police
---

9 月 26 日，佛罗里达州 Bonita Springs 的 Carli Michelle Heller 在 Claude 里写下一句话：她要去「扫射」李县警长办公室（Lee County Sheriff's Office）。第二天她又写，自己弄到了一把新枪。几天后，警员出现在她家门口（[swfl.io 根据逮捕报告的报道](https://swfl.io/2026/09/30/woman-arrested-after-ai-threat-against-lee-county-sheriffs-office-investigators)）。她被控「书面暴力威胁」，佛州法规 836.10 条下的二级重罪，最高可判 15 年。被捕后她解释：自己只是把 Claude 当日记用。

这中间没有黑客、没有举报人、也没有搜查令。按逮捕报告的描述，Anthropic 的安全系统监测到威胁内容，升级给人工审核团队，审核员判断威胁可信，主动联系了警方。整条链路都在产品设计之内，运行得和说明书一样。

## 上报管线长什么样

从逮捕报告能还原的流程分三步。第一步，自动监测：报告称 Anthropic 用「安全与安保措施监控关键短语和潜在威胁内容」，也就是分类器（自动扫描文本、给内容打标签的模型）在读每一段对话。第二步，内容严重到某个阈值，升级人工：一个真人审核团队会读到这段对话。第三步，人工判断「威胁可信」，报警。

注意信息来源：以上描述全部出自警方的逮捕报告，是执法方转述的 Anthropic 做法。Anthropic 没有对此案公开表态，也从未公布这条管线的触发标准（[TechSpot](https://www.techspot.com/news/114091-florida-woman-used-claude-diary-anthropic-reported-shoot.html) 与 [Futurism](https://futurism.com/artificial-intelligence/anthropic-claude-ai-chatbot-police-violence-safety) 均未获得公司回应）。

法律依据倒是公开的。Anthropic 的[隐私政策](https://www.anthropic.com/legal/privacy)写明，当公司基于善意相信「披露是防止任何人或财产遭受严重伤害的合理必要手段」时，可以共享个人数据。美国《存储通信法》也给这类操作留了门：服务商若善意相信存在死亡或重伤的紧急风险，可以不经任何法律程序、主动向政府披露通信内容（[18 U.S.C. § 2702(b)(8)](https://www.law.cornell.edu/uscode/text/18/2702)）。很多人对「警察调数据要搜查令」有模糊印象，但搜查令约束的是警方来要数据的那个方向；公司主动送上门，法律本来就是允许的。

## 匿名只隔两次披露

Heller 不是八月以来的第一例。8 月 11 日，圣安东尼奥一名 22 岁男子在 Claude 里写下要去附近一所小学「开枪扫射孩子」。据[当地电视台拿到的宣誓书](https://news4sanantonio.com/news/local/man-arrested-after-using-ai-to-threaten-elementary-school-arrest-affidavit-says)，FBI 的全国威胁行动科（National Threat Operations Section，负责接收和分流威胁线报的部门）8 月 28 日向地方警方通报了这段对话；线报从哪来，宣誓书没有写明。随后的身份确认过程更说明问题：警方向 T-Mobile、Charter 和 Google 发出紧急披露请求，用 IP 流量、电话号码和地址，把聊天账号钉到了具体的人身上。

从一段「匿名」对话到敲门，只需要两层：AI 公司识别出账号，通信服务商把账号连到人。李县警长 Carmine Marceno 的话可以当结论用：「用户需要明白，你从来不是真正匿名的。」

另据 [The Next Web 的梳理](https://thenextweb.com/news/anthropic-claude-chat-reported-police-florida-arrest)，8 月 14 日还有一名用户在 Claude 里威胁 Anthropic CEO Dario Amodei 并提到买了 AR-15，公司通知了旧金山警方，未逮捕。这一起我没能在原始信源里独立核实。即便只算坐实的两起，两个月内管线至少触发两次并走到执法环节，这是常态运行，不是特例。

## 安全机制自己补齐了犯罪要件

最值得细看的一层在法律文本里。佛州 [836.10 条](http://www.leg.state.fl.us/statutes/index.cfm?App_mode=Display_Statute&URL=0800-0899/0836/Sections/0836.10.html)的构成要件是：以「任何可能被他人查看的方式」发送、张贴或传输书面威胁。它不要求威胁送达受害者，只要求可能被另一个人看到。

写进纸质日记的话，没有「另一个人」，够不上这条罪。写给 Claude 的话呢？检方大概率会主张：输入即传输，而 Anthropic 的监控管线恰恰保证了「另一个人可能看到」，因为分类器会把内容送到人工审核员眼前。换句话说，安全机制本身补齐了「可被他人查看」这个要件。这本日记之所以在法律上变成「传输威胁」，正是因为它装了会叫人来读的警报器。这个论证在法庭上是否成立，还没有先例可循；据 The Next Web，提讯定在 11 月 2 日。

## 边界由谁划、写在哪

把 OpenAI 放旁边看，差别很清楚。OpenAI 在 2025 年 8 月的[官方博客](https://openai.com/index/helping-people-when-they-need-it-most/)里把规则写成了明文：涉及伤害他人的对话会发给受训的人工团队复核，若判定存在对他人严重人身伤害的迫近威胁，可能转交执法；自残和自杀内容明确不报警，理由是尊重这类互动的私密性。你可以不同意这条线划的位置，但它被公开划了出来。Anthropic 这边，目前能拿到的只有隐私政策里一句概括性授权，加上散落在逮捕报告里的流程碎片：什么内容触发人工审核、「可信威胁」按什么标准判、一年主动上报多少次，全都没有公开。

就这起案子本身，我不认为报警是错的：具体的袭击目标，第二天又出现一把真枪，这是任何审核团队都应该上报的组合。我之前写过[人工逐条审批为什么拦不住恶意命令](/zh/human-approval-is-not-a-security-boundary)，那篇的结论是人工审核的真实价值在少数高风险节点上引入人的判断；这次管线正是这么用的，机制层面没有意外。

真正的问题是，用户要到被捕之后、通过逮捕报告，才第一次看清这条管线的存在。「日记」是用户单方面的想象，受监控的通信服务才是产品的实际形态，而产品没有给任何信号提醒这个落差：界面不会告诉你哪些话会升级人工，政策页上那句「防止严重伤害」也撑不起具体预期。写作、陪伴、心理倾诉类的 AI 产品全都坐在这个落差上，它们卖的体验越私密，这个落差就越大。

接下来我盯两个点。一是 Anthropic 的透明度报告会不会开始披露主动上报执法的数量和判定标准，这类数字 OpenAI 同样没有公布过，谁先publish谁就立了行业基线。二是 11 月 2 日之后，法庭如何处理「写给聊天机器人算不算传输」：这个问题的答案会决定写给 AI 的话在刑法里算什么，比本案本身大得多。

## 参考来源

- [Woman arrested after AI threat against Lee County Sheriff's Office（swfl.io）](https://swfl.io/2026/09/30/woman-arrested-after-ai-threat-against-lee-county-sheriffs-office-investigators) — 原始本地报道：逮捕报告细节、9 月 26/27 日两条内容、警长表态、11 月过堂
- [Florida woman used Claude as a diary（TechSpot）](https://www.techspot.com/news/114091-florida-woman-used-claude-diary-anthropic-reported-shoot.html) — 选题来源；确认 Anthropic 未回应、836.10 二级重罪
- [Anthropic Reports User to the Police（Futurism）](https://futurism.com/artificial-intelligence/anthropic-claude-ai-chatbot-police-violence-safety) — 人工复核流程描述、Anthropic 无公开声明
- [Anthropic Privacy Policy](https://www.anthropic.com/legal/privacy) — 「防止严重伤害」披露条款原文（已直接核对）
- [18 U.S.C. § 2702（Cornell LII）](https://www.law.cornell.edu/uscode/text/18/2702) — 《存储通信法》自愿紧急披露条款
- [Florida Statute 836.10 原文](http://www.leg.state.fl.us/statutes/index.cfm?App_mode=Display_Statute&URL=0800-0899/0836/Sections/0836.10.html) — 「可能被他人查看」要件、二级重罪（已直接核对法条文本）
- [Man arrested after using AI to threaten elementary school（News4SA）](https://news4sanantonio.com/news/local/man-arrested-after-using-ai-to-threaten-elementary-school-arrest-affidavit-says) — 圣安东尼奥案宣誓书：FBI NTOS 通报、三家服务商紧急披露确认身份
- [Florida woman arrested after Anthropic reported her Claude chat（The Next Web）](https://thenextweb.com/news/anthropic-claude-chat-reported-police-florida-arrest) — 案件汇总：8 月 14 日 Amodei 威胁事件、11 月 2 日提讯日期
- [Helping people when they need it most（OpenAI）](https://openai.com/index/helping-people-when-they-need-it-most/) — OpenAI 的人工复核与转交执法规则、自残不报警的明文立场（页面抓取受阻，内容经 Techdirt、CADE、Yahoo 等多方引文交叉核实）
