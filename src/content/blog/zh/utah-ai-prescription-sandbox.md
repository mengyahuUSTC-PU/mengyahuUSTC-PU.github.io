---
title: "“AI 无监督开药”上了头条，协议原文写的是另一回事"
description: "犹他州批准 AI 开具美国第一批初诊处方。媒体说“无人类监督”，但协议里第一阶段每张处方要过两名医师的手——真正被测试的不是 AI，是一套用合同替代执照的监管机制。"
pubDate: 2026-10-06
tags: [health-ai, ai-governance]
lang: zh
slug: utah-ai-prescription-sandbox
translationOf: utah-ai-prescription-sandbox
---

10 月 5 日起，犹他州 18 岁以上居民可以下载一个叫 Nolla Derm 的 app：验证身份、签知情同意、填一份简短问卷、拍五个角度的面部照片，10 到 15 分钟后拿到痤疮治疗方案，符合条件就直接开出处方，发到本州药房。试点价每月 4.99 美元。全程没有医生出场（[Nolla 公告，经 Unite.AI 转述](https://www.unite.ai/nolla-health-launches-ai-issued-initial-acne-prescriptions-in-utah/)）。

科技媒体的标题是「犹他成为首个允许 AI 在无直接人类监督下看诊开药的州」（[TechSpot](https://www.techspot.com/news/114111-utah-become-first-state-ai-examine-patients-prescribe.html)）。我去读了州政府的原始文件，两个事实让这个标题变味。

第一，按协议，试点第一阶段每一张 AI 生成的处方，都要经两名犹他执业医师独立审核通过才会发给患者（[犹他商务厅试点页](https://commerce.utah.gov/ai/regulatory-relief-4/authorized-pilots/)）。第二，犹他更早的一个 AI 续方试点 Doctronic，2025 年 10 月签约，运行快一年，至今没拿到进入第二阶段的书面批准——每一单续方仍由执业者放行，州政府中途还修订协议收紧了门槛、删掉了两种药（同上述试点页）。

「无监督」是这套设计的终点，不是现状。而从 Doctronic 的进度看，终点未必到得了。

## 州政府凭什么放行

法律基础是犹他 2024 年通过的 [SB 149（AI Policy Act）](https://le.utah.gov/~2024/bills/sbillenr/SB0149.pdf)。这部法律设立了 AI 政策办公室（OAIP）和一个「AI 学习实验室」：公司可以和州签「监管缓解协议」（regulatory mitigation agreement）——在限定范围、限定期限内，州对特定法规暂缓执法；作为交换，公司接受协议里的全部监督条款。这就是常说的监管沙盒：先划一块围起来的场地让新事物跑，边跑边收数据，而不是先立一部管所有情况的法。

为什么是州而非 FDA 在做这件事？因为管辖权本来就切在这里：FDA 管药品和医疗器械本身，「谁有资格行医开处方」归各州执照制度管。犹他豁免的正是自己权限内的两条——无照行医的执法、远程医疗的规则要求，且只对协议规定流程内开出的外用痤疮处方生效。

AI 拿到的不是一张空白支票。协议把范围收得很窄：只限轻中度痤疮，只能开固定清单上的外用乳膏和凝胶，异维 A 酸和一切口服药明确禁止；重度痤疮、怀孕或备孕、哺乳期、免疫缺陷、对清单药物有过敏史，任何一条命中都会被挡出流程。换句话说，州政府挑了全医学里几乎风险最低的处方场景做试验：最坏的已知不良反应是局部皮肤刺激。

监督结构分三阶段。按 Nolla 公告的数字：前 100 名患者，每张处方两名医师事前审核；之后到累计 500 人，AI 直接发处方、医师至少每周回溯复核全部病例；累计 750 人以上，医师每月抽查至少 10% 外加全部不良事件病例。每升一个阶段，都要 OAIP 书面批准。此外：不良事件 24 小时内上报，每月提交 AI 与医师判断的一致率数据，公司必须投保职业责任险，服务条款不得限制公司对损害的赔偿责任，不得出售患者数据。出了事，患者起诉的权利原样保留。

有一点我没能核实到条款细节：进入后两个阶段后，处方上不再有执业医师签字，医疗事故的过错标准如何适用，官方摘要没有展开。

## 这不是一次性特批

同日犹他还公布了另外四份协议：August AI 做慢病续方（前 250 单全审，患者最多连续三次 AI 续方、之后必须见真人，出现自杀倾向或新副作用自动转人工）；Expect Fitness 做产后盆底物理治疗；犹他大学医院和 Intermountain Health 两家系统签了框架性协议，后续各自的 AI 试点走快速审批。州里还请了六家第三方评估机构做独立技术与临床核验，包括 CHAI 和斯坦福临床卓越研究中心（[商务厅公告](https://commerce.utah.gov/2026/10/05/utah-enhances-pro-human-ai-initiative-with-new-healthcare-pillar-adds-new-pilots-to-its-regulatory-sandbox-and-partners-with-third-party-evaluators/)）。

Nolla 称自己是美国首个获州监管机构授权、由 AI 开具初始处方（而非续方）的公司。在公开检索范围内，我没有找到更早的同类授权。

7 月我写过 [HIPAA 盯的是机构、不是数据](/blog/chatgpt-health-hipaa-gap)，所以病历一旦交给消费级 AI 就出了保护圈。执照制度有同构的问题：它盯的是「人」，不是「系统」。AI 没有可以吊销的行医执照，监管者手里的老工具对它没有着力点。犹他给出的替代方案，是把执照换成一份可以收回的合同：达不到一致率就不批升级，出事就终止协议、恢复执法。约束从「资格准入」变成了「持续核数据」。

## 真正被测试的是什么

不是 AI 看痤疮的能力。外用痤疮药这个场景是刻意挑的，它的作用是把临床风险压到地板上，好让另一个东西接受检验：用合同加数据门槛替代执照，这套机制本身转不转得动。

目前最有说服力的证据恰恰是 Doctronic 卡在第一阶段这件事。闸门真的会卡人，升级不是走流程——这比官方新闻稿里任何形容词都更能说明试点的严肃程度。

真正的薄弱环节有两个。一是容量：OAIP 是个小办公室，现在要同时盯七八个试点的月报、一致率和事故上报，协议数量增长快于人手时，「持续核数据」会不会退化成「收数据存档」，没人知道。二是复制走样：这类协议是逐案谈判的产物，不是立法条文，其他州跟进时完全可以抄「放行 AI 开药」的结论、不抄「两名医师事前审核」和「书面批准才能升级」的闸门。到那时，头条里的「无监督开药」才会成真。

值得记一个具体时间点：Nolla 的协议 2027 年 10 月 5 日到期。到期前它走没走到第三阶段、AI 与医师的一致率数据是否向公众披露，比「首个州放行 AI 开药」这条新闻本身重要得多。

## 参考来源

- [Utah Enhances Pro-Human AI Initiative with New Healthcare Pillar...（犹他商务厅，2026-10-05）](https://commerce.utah.gov/2026/10/05/utah-enhances-pro-human-ai-initiative-with-new-healthcare-pillar-adds-new-pilots-to-its-regulatory-sandbox-and-partners-with-third-party-evaluators/) — 医疗板块、五份新协议、第三方评估机构、24 小时上报与责任险要求
- [AI Authorized Pilots（犹他商务厅官方试点列表）](https://commerce.utah.gov/ai/regulatory-relief-4/authorized-pilots/) — Nolla/Doctronic/August AI 各协议的范围、排除条件、三阶段结构、豁免内容、Doctronic 停留在第一阶段及协议收紧的事实
- [SB 149 Artificial Intelligence Amendments 正式文本（犹他州议会）](https://le.utah.gov/~2024/bills/sbillenr/SB0149.pdf) — AI Policy Act、OAIP、学习实验室与监管缓解协议的法律授权
- [Utah and Doctronic Announce Groundbreaking Partnership（犹他商务厅，2026-01-06）](https://commerce.utah.gov/2026/01/06/news-release-utah-and-doctronic-announce-groundbreaking-partnership-for-ai-prescription-medication-renewals/) — Doctronic 试点的官方定位与各方表态
- [Nolla Health Launches AI-Issued Initial Acne Prescriptions in Utah（Unite.AI 转述公司公告）](https://www.unite.ai/nolla-health-launches-ai-issued-initial-acne-prescriptions-in-utah/) — 患者流程、定价、三阶段具体数字（100/500/750、10%）、公司的「首个」说法
- [TechSpot 报道](https://www.techspot.com/news/114111-utah-become-first-state-ai-examine-patients-prescribe.html) — 选题来源，用于对照媒体标题与协议原文的差距
