---
title: "病历交给 ChatGPT 的那一刻，HIPAA 的保护就结束了"
description: "ChatGPT Health 面向全美开放，可接入病历和 Apple Health。它不违反任何医疗隐私法——这正是问题所在：HIPAA 盯的是机构，不是数据。"
pubDate: 2026-07-23
tags: [health-ai, privacy, ai-governance]
lang: zh
slug: chatgpt-health-hipaa-gap
translationOf: chatgpt-health-hipaa-gap
---

7 月 23 日，OpenAI 把 ChatGPT Health [推向了全美所有 18 岁以上用户](https://openai.com/index/health-in-chatgpt/)，免费版也能用（[MacRumors](https://www.macrumors.com/2026/07/23/chatgpt-apple-health-integration/)）。用户可以把自己的电子病历直接连进来——通过与聚合平台 b.well 的合作，覆盖 Epic、Oracle Health 等主流病历系统，b.well 的网络号称接入约 220 万医疗服务提供者（[Fierce Healthcare](https://www.fiercehealthcare.com/ai-and-machine-learning/openai-launches-chatgpt-health-connect-data-health-apps-medical-records)、[TechCrunch](https://techcrunch.com/2026/07/23/openai-makes-chatgpt-health-available-to-all-u-s-users/)）。再加上 Apple Health、MyFitnessPal 这些应用，ChatGPT 从此可以对着你真实的化验单、用药记录和睡眠数据回答问题。

先把一件事说清楚：这整个流程不违反 HIPAA 的任何一个条款。

这不是 OpenAI 找到了什么漏洞。我入行 Responsible AI 的第一个项目，就是和医疗 AI 公司 Nuance 合作，给医患对话的自动摘要做幻觉检测——AI 进医疗场景后哪些环节容易出问题、哪些风险法规根本没接住，我是从那时开始亲手摸的。这些年我见过太多「合规」和「受保护」被当成同义词用的场合——ChatGPT Health 是把这两个词拆开的最好教材：产品可以全程合规，而你的病历自始至终不在法律保护之内。

## 空白不是钻出来的，是法律本来就长这样

HIPAA 是美国 1996 年的医疗隐私法。很多人以为它保护的是「医疗数据」这个类别，其实不是——它约束的是一份实体名单：医疗服务提供者、保险计划、清算机构（合称 covered entities，受覆盖实体），外加替这些机构处理数据的承包商（business associates，业务伙伴）。名单之外的公司，拿到同样的病历，不受 HIPAA 任何约束。华盛顿的智库 Center for Democracy and Technology 在点评这次发布时说得直白：AI 公司通常根本不在 HIPAA 覆盖范围内（[Fierce Healthcare](https://www.fiercehealthcare.com/ai-and-machine-learning/openai-launches-chatgpt-health-connect-data-health-apps-medical-records)）。

更关键的是数据出口这一环。HIPAA 赋予患者「访问权」（right of access）：你有权要求医院把病历发给你指定的任何第三方应用，医院一般不得拒绝。美国卫生与公众服务部（HHS）2019 年的[官方指南](https://www.hhs.gov/hipaa/for-professionals/privacy/guidance/access-right-health-apps-apis/index.html)把责任边界划得清清楚楚：只要接收方应用是患者自己选的、不是医院提供的，病历送达之后应用怎么用、怎么共享，医院一概不担责；HIPAA 对接收方的使用「不施加任何限制」。

也就是说，保护不是被谁绕开的——它在设计上就终止于交接那一刻。医院不但拦不住这次传输，故意设障反而可能违反信息封锁（information blocking）的规定。病历跨过 API 的那条线，监管就从「有专门法律、有联邦执法机构、有法定患者权利」切换成「看用户协议」。

## 承诺替代法律之后，差的是什么

OpenAI 给出的隐私承诺本身不算含糊：连接的病历和 Apple Health 数据、以及用到这些数据的对话，不用于训练基础模型，不用于广告定向；健康数据有额外的加密和隔离；每次调用病历前请求许可；断开连接后 30 天内删除数据（[MacRumors](https://www.macrumors.com/2026/07/23/chatgpt-apple-health-integration/)、[Glitchwire](https://glitchwire.com/news/openai-relaunches-health-in-chatgpt-with-expanded-us-access-after-a-six-month-re/)）。我不怀疑这些承诺是认真的。要比的不是诚意，是「承诺」和「法律」这两种约束在机制上差在哪。拆三个具体的看。

**第一，隔离承诺和产品方向在对着走。** OpenAI 自己披露，1 月试点期间超过 70% 的健康对话发生在专门的 Health 空间之外——用户安排饭菜时顺口问过敏，查食谱时提到忌口（[Glitchwire](https://glitchwire.com/news/openai-relaunches-health-in-chatgpt-with-expanded-us-access-after-a-six-month-re/)）。所以 7 月这版重新设计的卖点，恰恰是让健康上下文经用户授权后可以进入日常对话，而不是关在单独空间里。这在产品上完全合理，但它意味着「健康数据与其他对话隔离」这堵墙，正是产品要拆的那堵。一旦化验结果作为上下文进过日常对话、沉淀进跨对话记忆，「断开连接、30 天删除」删的是数据源，散落在别处的衍生信息怎么清理，公开材料没有讲细。

**第二，删除承诺让位于法律程序。** 这不是假设。2025 年《纽约时报》诉 OpenAI 版权案中，法院曾下令 OpenAI 保留全部用户对话日志——包括用户已经删除的——OpenAI [公开抗辩](https://openai.com/index/response-to-nyt-data-demands/)，但在保留令收窄前只能照办。这件事和健康无关，机制教训却直接适用：聊天记录在法律上是普通的商业记录，可以被诉讼保全、被取证。病历在医院手里时，HIPAA 对司法程序中的披露有专门规则和最小化要求；同一份内容进了聊天记录，就只是又一份电子证据。「我们会删除你的数据」这句话，永远默认附带一行小字：除非法院不让。

**第三，广告承诺有过先例，先例的结局不好。** OpenAI 正在探索广告收入，专家因此提醒健康数据与广告系统之间的隔离必须严丝合缝（[Fierce Healthcare](https://www.fiercehealthcare.com/ai-and-machine-learning/openai-launches-chatgpt-health-connect-data-health-apps-medical-records)）。而「承诺不拿健康数据做广告、后来做了」在这个行业有现成判例：处方折扣平台 GoodRx 曾向用户保证健康信息不外流，实际把用药数据传给了 Facebook 等广告平台，2023 年被 FTC 依据健康数据泄露通知规则（Health Breach Notification Rule）[罚款 150 万美元](https://www.ftc.gov/news-events/news/press-releases/2023/02/ftc-enforcement-action-bar-goodrx-sharing-consumers-sensitive-health-info-advertising)——这是该规则生效十四年来第一次动用。这就是 HIPAA 之外的执法现状：FTC 管的是「说话不算数」，事后追责，而不是像 HIPAA 那样事前规定你能做什么；用户协议还可以单方面修订，今天的承诺约束不了明天的版本。

顺带一个值得记下的对照：这次发布只覆盖美国，欧洲经济区、瑞士和英国都不在名单上（[Fierce Healthcare](https://www.fiercehealthcare.com/ai-and-machine-learning/openai-launches-chatgpt-health-connect-data-health-apps-medical-records)）。欧洲的 GDPR 和 HIPAA 走的是相反的路线：它按数据类别保护——健康数据属于特殊类别，无论落到谁手里，处理者都要担同样的法定义务。数据走到哪，保护跟到哪。HIPAA 盯机构、GDPR 盯数据，ChatGPT Health 的监管空白只在前一种架构下存在。

## 能带走什么

我不打算劝人别用。用自己的真实化验单提问，比让模型对着一句模糊描述瞎猜要好，医疗问答本来就是 ChatGPT 最大的使用场景之一，OpenAI 认真做这个产品比放任用户在普通对话框里贴病历要负责任。何况 OpenAI 条款里也写明了：该服务不用于任何疾病的诊断或治疗（[TechCrunch](https://techcrunch.com/2026/07/23/openai-makes-chatgpt-health-available-to-all-u-s-users/)）。

但连接之前，值得用正确的心智模型做决定：这是一次实质上不可逆的披露，不是一次可以随时撤销的授权。30 天删除是政策承诺而非法定权利，诉讼保全可以压过它，衍生上下文未必删得干净。粒度也在你手里——想解读一张化验单，贴那一张就够了，不必把整个病历库直连进来。

更大的判断是：这个空白填不上，除非立法。HHS 的指南写明了保护止于何处，FTC 2024 年[更新了](https://www.ftc.gov/business-guidance/blog/2024/04/updated-ftc-health-breach-notification-rule-puts-new-provisions-place-protect-users-health-apps)泄露通知规则、把健康应用明确纳入，华盛顿州等地也开始为脱离 HIPAA 的健康数据单独立法，但这些都是补丁：通知规则管泄露后的告知，不管日常怎么用；州法只覆盖本州。1996 年的法律假设病历只在医院和保险公司之间流转，2026 年的产品让病历流进了对话式 AI 的上下文窗口。在两者之间的落差被立法填上之前，「你的病历受保护」这句话，在你点下「连接」按钮之后，语法上就该改成过去时。

## 参考来源

- [Launching Health in ChatGPT — OpenAI](https://openai.com/index/health-in-chatgpt/) — 官方公告（站点反爬未能直接抓取，关键内容经多家报道交叉核对）
- [OpenAI launches ChatGPT Health to connect data from health apps, medical records — Fierce Healthcare](https://www.fiercehealthcare.com/ai-and-machine-learning/openai-launches-chatgpt-health-connect-data-health-apps-medical-records) — b.well 合作与网络规模、CDT 评论、广告风险提醒、欧洲不在首发范围
- [ChatGPT's Apple Health Integration Now Rolling Out to U.S. Users — MacRumors](https://www.macrumors.com/2026/07/23/chatgpt-apple-health-integration/) — 发布时间、覆盖用户与平台、隐私承诺、1 月试点背景
- [OpenAI makes ChatGPT Health available to all U.S. users — TechCrunch](https://techcrunch.com/2026/07/23/openai-makes-chatgpt-health-available-to-all-u-s-users/) — Epic/Oracle Health 病历接入、条款免责声明、试点数据
- [OpenAI Relaunches Health in ChatGPT — Glitchwire](https://glitchwire.com/news/openai-relaunches-health-in-chatgpt-with-expanded-us-access-after-a-six-month-re/) — 70% 对话发生在 Health 空间外、30 天删除、一月试点到七月重发的过程
- [The access right, health apps, & APIs — HHS](https://www.hhs.gov/hipaa/for-professionals/privacy/guidance/access-right-health-apps-apis/index.html) — 患者访问权下第三方应用不受 HIPAA 约束的官方指南
- [FTC Enforcement Action to Bar GoodRx from Sharing Consumers' Sensitive Health Info for Advertising — FTC](https://www.ftc.gov/news-events/news/press-releases/2023/02/ftc-enforcement-action-bar-goodrx-sharing-consumers-sensitive-health-info-advertising) — GoodRx 150 万美元罚款、HBNR 首次执法
- [Updated FTC Health Breach Notification Rule — FTC](https://www.ftc.gov/business-guidance/blog/2024/04/updated-ftc-health-breach-notification-rule-puts-new-provisions-place-protect-users-health-apps) — 2024 年规则更新纳入健康应用
- [How we're responding to The New York Times' data demands — OpenAI](https://openai.com/index/response-to-nyt-data-demands/) — NYT 诉讼中的用户日志保留令

<!-- 待核实：应用户要求加入 Nuance 合作经历（医患对话自动摘要的幻觉检测，按上下文推断用户所说 "alligator detection" 为 hallucination detection 的笔误）。Nuance 为 Microsoft 子公司，此处仅保留高层次描述、未涉及项目细节，但请用户确认该合作经历可公开提及、不涉及雇主内部信息（编辑方针雇主边界条款）。 -->
