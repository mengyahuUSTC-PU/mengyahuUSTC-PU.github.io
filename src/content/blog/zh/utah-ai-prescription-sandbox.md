---
title: "“AI 无监督开药”上了头条，协议原文写的是另一回事"
description: "犹他州批准 AI 开具美国第一批初诊处方。媒体说“无人类监督”，但协议里第一阶段每张处方要过两名医师的手——真正被测试的不是 AI，是一套用合同替代执照的监管机制。"
pubDate: 2026-10-06
tags: [health-ai, ai-governance]
lang: zh
slug: utah-ai-prescription-sandbox
translationOf: utah-ai-prescription-sandbox
---

10 月 5 日起，犹他州 18 岁以上居民可以下载一个叫 Nolla Derm 的 app：验证身份、签知情同意、填一份简短问卷、拍五个角度的面部照片，10 到 15 分钟后拿到痤疮治疗方案，符合条件就直接开出处方，发到本州药房。试点价每月 4.99 美元。全程没有医生问诊（[Nolla 官方公告](https://www.nollahealth.com/blog/ai-prescriptions-utah)）。

科技媒体的标题是「犹他成为首个允许 AI 在无直接人类监督下看诊开药的州」（[TechSpot](https://www.techspot.com/news/114111-utah-become-first-state-ai-examine-patients-prescribe.html)）。我去读了州政府的原始文件，两个事实让这个标题变味。

第一，按协议，试点第一阶段每一张 AI 生成的处方，都要经两名犹他执业医师独立审核通过才会发给患者（[犹他商务厅试点页](https://commerce.utah.gov/ai/regulatory-relief-4/authorized-pilots/)）。第二，犹他更早的一个 AI 续方试点 Doctronic，2025 年 10 月签约，运行快一年，至今没拿到进入第二阶段的书面批准——每一单续方仍由执业者放行，州政府中途还修订协议收紧了门槛、删掉了两种药（同上述试点页）。

「无监督」是这套设计的终点，不是现状。而从 Doctronic 的进度看，终点未必到得了。

## 开方的公司是什么来头

Nolla 不是一家临时凑出来的纯软件公司，但也不是医生开的公司。它 2024 年底在挪威起家，先后上线皮肤癌筛查和痤疮治疗两个 app，据公司披露半年内两个 app 合计服务超过 5.5 万名患者，约占挪威人口的 1%（[Beauty Independent 报道](https://www.beautyindependent.com/4-5m-raise-nolla-health-ai-startup-offers-acne-care/)）；2025 年把业务扩展到美国 40 多个州，模式仍是 AI 辅助、医生把关；种子轮 450 万美元由 General Catalyst 领投（[General Catalyst 投资说明](https://www.generalcatalyst.com/stories/seeding-the-future-with-nolla-health)）。

它的获客是纯消费级直购：用户自己从 App Store 下载，不经医生转诊；我也没有检索到它与医院或 Teladoc 一类远程医疗平台的合作公告。规模数字同样来自公司自述：美国版 Nolla Derm 至今下载超过 17.5 万次、覆盖 44 个州（[Nolla 官方公告](https://www.nollahealth.com/blog/ai-prescriptions-utah)）——注意这是下载量，不是付费患者数。潜在市场本身不小：按美国皮肤科学会的统计，痤疮是美国最常见的皮肤病，每年影响近 5000 万人（[AAD 统计页](https://www.aad.org/media/stats-numbers)）。犹他这次最直接的获客手段是价格：Nolla 在其他州的医生把关版服务月费 59 美元（[Beauty Independent](https://www.beautyindependent.com/4-5m-raise-nolla-health-ai-startup-offers-acne-care/)），试点价压到 4.99 美元，不到十分之一。至于广告投放或后续渠道合作的规划，公司没有公开，我没能查到。

创始团队里最接近医学的人是联合创始人 Luis Ruben Soenksen：生物医学工程出身，约翰斯·霍普金斯生物工程硕士、MIT 博士，曾任 MIT 首位「AI 与医疗」方向的 Venture Builder，做了十年皮肤病学方向的 AI 建模研究——但他的身份是工程师和研究者，Nolla 团队页把他列为科学顾问，而非医师。CEO Luis Wenus 则是增长运营出身，此前是 Worldcoin 第一号员工、负责市场拓展；第三位联合创始人是 Sean Geiger。执业医师在公司的位置是顾问层：医学顾问 Zaid Fadul 是家庭医学医师，顾问名单里还有哈佛的皮肤科医师 Omar Badri 和流行病学家 Michael Mina（[Nolla 团队页](https://www.nollahealth.com/our-team)）。至于试点里实际审核处方的两名犹他执业医师与公司是雇佣还是合作关系，官方材料没有写明，这一点我没能核实。

## 州政府凭什么放行

法律基础是犹他 2024 年通过的 [SB 149（AI Policy Act）](https://le.utah.gov/~2024/bills/sbillenr/SB0149.pdf)。这部法律设立了 AI 政策办公室（OAIP）和一个「AI 学习实验室」：公司可以和州签「监管缓解协议」（regulatory mitigation agreement）——在限定范围、限定期限内，州对特定法规暂缓执法；作为交换，公司接受协议里的全部监督条款。这就是常说的监管沙盒：先划一块围起来的场地让新事物跑，边跑边收数据，而不是先立一部管所有情况的法。

为什么是州而非 FDA 在做这件事？因为管辖权本来就切在这里：FDA 管药品和医疗器械本身，无权监管医生的执业行为（[FDA 官方说明](https://www.fda.gov/medical-devices/home-use-devices/fdas-role-regulating-medical-devices)），「谁有资格行医开处方」归各州执照制度管。犹他豁免的正是自己权限内的两条——无照行医的执法、远程医疗的规则要求，且只对协议规定流程内开出的外用痤疮处方生效。

AI 拿到的不是一张空白支票。协议把范围收得很窄：只限轻中度痤疮，只能开固定清单上的外用乳膏和凝胶，异维 A 酸和一切口服药明确禁止；重度痤疮、怀孕或备孕、哺乳期、免疫缺陷、对清单药物有过敏史，任何一条命中都会被挡出流程。

州政府挑的其实不是「皮肤科」，而是外用痤疮药这一个场景。它同时满足几个别的处方场景很难凑齐的条件：痤疮诊断主要靠观察皮损（[AAD 诊疗页](https://www.aad.org/public/diseases/acne/derm-treat/treat)），适合照片判读；外用给药的全身暴露远低于口服，不涉及口服药那样的剂量调整；常见不良反应是局部刺激，患者自己看得见，停药多能缓解。当然「窄」不等于零风险：AAD 同一页面提醒，毛囊炎、口周皮炎等疾病可能被误当成痤疮、治法不同；FDA 的外用克林霉素说明书也警示过经皮吸收，以及罕见但可致命的伪膜性结肠炎（[FDA 药品标签](https://www.accessdata.fda.gov/drugsatfda_docs/label/2019/050537s041%2C050600s018%2C050615s019lbl.pdf)）。只是同一个科室里风险最高的部分被整个切掉了：异维 A 酸致畸、FDA 要求配套验孕和妊娠预防（[iPLEDGE REMS](https://www.fda.gov/drugs/postmarket-drug-safety-information-patients-and-providers/ipledge-risk-evaluation-and-mitigation-strategy-rems)），正是协议禁药清单的第一项。换成其他科室的初诊处方，口服药全身起效、诊断依赖查体和化验，这几条几乎一条都不满足。

监督结构分三阶段。按 Nolla 公告的数字：前 100 名患者，每张处方两名医师事前审核；之后到累计 500 人，AI 直接发处方、医师至少每周回溯复核全部病例；累计 750 人以上，医师每月抽查至少 10% 外加全部不良事件病例。每升一个阶段，都要 OAIP 书面批准。此外：不良事件 24 小时内上报，按月或按季提交 AI 与医师判断的一致率数据，公司必须投保职业责任险，服务条款不得限制公司对损害的赔偿责任，不得出售患者数据。出了事，患者起诉的权利原样保留。

有一点我没能核实到条款细节：进入后两个阶段，处方由 AI 直接发出、医师退到事后复核和抽查，这种情况下医疗事故的过错标准如何适用，官方摘要没有展开。

## 这不是一次性特批

同日犹他还公布了另外四份协议：August AI 做慢病续方（前 250 单全审，患者最多连续三次 AI 续方、之后必须见真人，出现自杀倾向或新副作用自动转人工）；Expect Fitness 做产后盆底物理治疗；犹他大学医院和 Intermountain Health 两家系统签了框架性协议，后续各自的 AI 试点走快速审批。州里还请了六家第三方评估机构做独立技术与临床核验，包括 CHAI 和斯坦福临床卓越研究中心（[商务厅公告](https://commerce.utah.gov/2026/10/05/utah-enhances-pro-human-ai-initiative-with-new-healthcare-pillar-adds-new-pilots-to-its-regulatory-sandbox-and-partners-with-third-party-evaluators/)）。

Nolla 的原话是「美国首个」（nation's first），有媒体把它拔高成「全球首个」（[Interesting Engineering](https://interestingengineering.com/ai-robotics/utah-autonomous-acne-prescriptions)），这要拆成两件事看。「AI 看诊、人类签字」早有先例：上海公司森亿智能（Synyi AI）2025 年 4 月起在沙特艾哈萨地区与当地医疗集团试运行 AI 诊所，AI 医生「Dr. Hua」问诊并出治疗方案，覆盖约 30 种呼吸道疾病，但每份处方须人类医师复核签字才生效（[Bloomberg 报道](https://www.bloomberg.com/news/articles/2025-05-15/chinese-startup-trials-first-ai-doctor-clinic-in-saudi-arabia)）。中国本土医院里 AI 预问诊、辅助诊断铺得也很广——央视《焦点访谈》报道过，仅深圳一市就有近 450 个医疗 AI 产品在各级医疗卫生机构落地（[中央网信办转载](https://www.cac.gov.cn/2025-03/17/c_1743916011485636.htm)）——但监管直接关死了开方这一步：国家卫健委 2022 年发布的《互联网诊疗监管细则（试行）》写明处方应由接诊医师本人开具，「严禁使用人工智能等自动生成处方」（[国家卫健委发布页](https://www.nhc.gov.cn/yzygj/c100068/202203/2072f0e8988249e59d942e1b2a933916.shtml)，[广州市政府门户转载](https://www.gz.gov.cn/zwfw/zxfw/ylfw/content/post_8335006.html)）。犹他的增量在第二件事：监管者白纸黑字给出了一条医师从逐张预审逐步退到事后抽查的升级路径，而且覆盖的是初诊处方。限定在初诊处方这一点上，公开检索范围内我没有找到更早的同类授权——犹他自家的 Doctronic 协议比 Nolla 早一年写下了类似路径，但那管的是续方，不是初诊。也要注意，现阶段 Nolla 每张处方仍要两名医师审核，和沙特诊所的做法实际是同一回事；真正的分界要等第二阶段获批才出现。

7 月我写过 [HIPAA 盯的是机构、不是数据](/blog/chatgpt-health-hipaa-gap)：独立的消费级 AI 应用通常不在它的管辖内，病历交过去就出了保护圈。执照制度有同构的问题：它盯的是「人」，不是「系统」。AI 没有可以吊销的行医执照，监管者手里的老工具对它没有着力点——犹他要豁免「无照行医」执法，原因正在这里（[试点页](https://commerce.utah.gov/ai/regulatory-relief-4/authorized-pilots/)）。犹他给出的替代方案，是把执照换成一份可以收回的合同：达不到一致率就不批升级，出事就终止协议、恢复执法。约束从「资格准入」变成了「持续核数据」。

## 真正被测试的是什么

不是 AI 看痤疮的能力。外用痤疮药这个场景是刻意挑的，它的作用是把临床风险压到地板上，好让另一个东西接受检验：用合同加数据门槛替代执照，这套机制本身转不转得动。

目前最有说服力的证据恰恰是 Doctronic 卡在第一阶段这件事。闸门真的会卡人，升级不是走流程——这比官方新闻稿里任何形容词都更能说明试点的严肃程度。

真正的薄弱环节有两个。一是容量：OAIP 名下的协议已有多份——官方列表上既有运行中的试点，也有框架协议——每一份都带着月报、一致率和事故上报要核；办公室的人手规模没有公开，协议数量增长快于人手时，「持续核数据」会不会退化成「收数据存档」，没人知道。二是复制走样：这类协议是逐案谈判的产物，不是立法条文，其他州跟进时完全可以抄「放行 AI 开药」的结论、不抄「两名医师事前审核」和「书面批准才能升级」的闸门。到那时，头条里的「无监督开药」才会成真。

值得记一个具体时间点：Nolla 的协议 2027 年 10 月 5 日到期。到期前它走没走到第三阶段、AI 与医师的一致率数据是否向公众披露，比「首个州放行 AI 开药」这条新闻本身重要得多。

## 参考来源

- [Utah Enhances Pro-Human AI Initiative with New Healthcare Pillar...（犹他商务厅，2026-10-05）](https://commerce.utah.gov/2026/10/05/utah-enhances-pro-human-ai-initiative-with-new-healthcare-pillar-adds-new-pilots-to-its-regulatory-sandbox-and-partners-with-third-party-evaluators/) — 医疗板块、五份新协议、第三方评估机构、24 小时上报与责任险要求
- [AI Authorized Pilots（犹他商务厅官方试点列表）](https://commerce.utah.gov/ai/regulatory-relief-4/authorized-pilots/) — Nolla/Doctronic/August AI 各协议的范围、排除条件、三阶段结构、豁免内容、Doctronic 停留在第一阶段及协议收紧的事实
- [SB 149 Artificial Intelligence Amendments 正式文本（犹他州议会）](https://le.utah.gov/~2024/bills/sbillenr/SB0149.pdf) — AI Policy Act、OAIP、学习实验室与监管缓解协议的法律授权
- [Utah and Doctronic Announce Groundbreaking Partnership（犹他商务厅，2026-01-06）](https://commerce.utah.gov/2026/01/06/news-release-utah-and-doctronic-announce-groundbreaking-partnership-for-ai-prescription-medication-renewals/) — Doctronic 试点的官方定位与各方表态
- [Nolla Health Launches the Nation's First AI-Powered Prescriptions（Nolla 官方公告）](https://www.nollahealth.com/blog/ai-prescriptions-utah) — 患者流程、试点定价、Nolla Derm 下载量与覆盖州数
- [Seeding the Future with Nolla Health（General Catalyst）](https://www.generalcatalyst.com/stories/seeding-the-future-with-nolla-health) — 种子轮融资、创始人背景、美国扩张
- [With $4.5M Raise, AI Startup Nolla Health Offers Acne Care（Beauty Independent）](https://www.beautyindependent.com/4-5m-raise-nolla-health-ai-startup-offers-acne-care/) — 挪威起家时间线、半年 5.5 万患者、美国版 59 美元月费、三位联合创始人
- [Our Team（Nolla Health 官网）](https://www.nollahealth.com/our-team) — 医学顾问与科学顾问名单
- [Skin conditions by the numbers（美国皮肤科学会）](https://www.aad.org/media/stats-numbers) — 痤疮为美国最常见皮肤病、每年影响近 5000 万人
- [Acne: Diagnosis and treatment（美国皮肤科学会）](https://www.aad.org/public/diseases/acne/derm-treat/treat) — 痤疮靠观察皮损诊断；毛囊炎、口周皮炎等可能被误当成痤疮
- [Cleocin T 外用克林霉素药品标签（FDA）](https://www.accessdata.fda.gov/drugsatfda_docs/label/2019/050537s041%2C050600s018%2C050615s019lbl.pdf) — 外用克林霉素的经皮吸收与伪膜性结肠炎警示
- [iPLEDGE REMS（FDA）](https://www.fda.gov/drugs/postmarket-drug-safety-information-patients-and-providers/ipledge-risk-evaluation-and-mitigation-strategy-rems) — 异维 A 酸的致畸风险与验孕要求
- [FDA's Role in Regulating Medical Devices（FDA）](https://www.fda.gov/medical-devices/home-use-devices/fdas-role-regulating-medical-devices) — FDA 不监管医生的执业行为
- [Chinese Startup Trials First AI Doctor Clinic in Saudi Arabia（Bloomberg，2025-05-15）](https://www.bloomberg.com/news/articles/2025-05-15/chinese-startup-trials-first-ai-doctor-clinic-in-saudi-arabia) — 森亿智能沙特 AI 诊所的流程、病种范围与人类医师签字环节
- [《互联网诊疗监管细则（试行）》发布页（国家卫健委）](https://www.nhc.gov.cn/yzygj/c100068/202203/2072f0e8988249e59d942e1b2a933916.shtml) — 中国对 AI 自动生成处方的禁止性规定（原始发布）
- [《互联网诊疗监管细则（试行）》：严禁使用人工智能等自动生成处方（广州市政府门户转载）](https://www.gz.gov.cn/zwfw/zxfw/ylfw/content/post_8335006.html) — 同上条款的官方转载页，条款原文经此页核对
- [《焦点访谈》AI+医疗报道（央视，中央网信办转载）](https://www.cac.gov.cn/2025-03/17/c_1743916011485636.htm) — 中国医疗机构 AI 落地规模（深圳近 450 个医疗 AI 产品）
- [Utah launches world's first autonomous prescription system without human doctors（Interesting Engineering）](https://interestingengineering.com/ai-robotics/utah-autonomous-acne-prescriptions) — 媒体「全球首个」说法的实例
- [Nolla Health Launches AI-Issued Initial Acne Prescriptions in Utah（Unite.AI 转述公司公告）](https://www.unite.ai/nolla-health-launches-ai-issued-initial-acne-prescriptions-in-utah/) — 三阶段具体数字（100/500/750、10%）、公司的「首个」说法
- [TechSpot 报道](https://www.techspot.com/news/114111-utah-become-first-state-ai-examine-patients-prescribe.html) — 选题来源，用于对照媒体标题与协议原文的差距

<!-- 核查备注（不入正文）：
1. 挪威「半年超 5.5 万患者（约人口 1%）」为公司自述数字，Beauty Independent 原句 "amassed over 55,000 patients, an amount equal to about 1% of the Norwegian population across both apps"；General Catalyst 页写 50,000，正文已改挂 Beauty Independent。
2. Soenksen 的学历与 MIT Venture Builder 职位经 MIT innovation 页面与多方报道交叉核实；其「十年皮肤病学 AI 建模研究」出自 General Catalyst 与媒体报道，未逐篇核对其论文列表。「非执业医师」已按核查意见改写为「Nolla 团队页把他列为科学顾问，而非医师」（可由团队页直接证实）。
3. 审核处方的两名犹他执业医师与 Nolla 的关系（雇佣/签约）官方试点页未写明，正文已如实注明未核实。
4. 森亿智能沙特诊所信息源头为 Bloomberg 2025-05-15 报道；「错误率低于 0.3%」为公司自述且测试方法未公开，正文未采用该数字。
5. 《互联网诊疗监管细则（试行）》由国家卫健委、国家中医药局 2022 年发布；正文一手链接为卫健委官网发布页（该页对自动抓取返回 412，条款原文经广州市政府门户官方转载页核对一字不差，两链并挂）。
6. 「Nolla Derm 下载超 17.5 万次、覆盖 44 州」为公司官方公告自述数字，无独立验证。「无平台合作」为检索未见，非官方否认，正文已改为第一人称「我也没有检索到」。
7. 「全球首个」媒体实例：Interesting Engineering 标题 "Utah launches world's first autonomous prescription system without human doctors"，已核实并补链。
8. 一致率上报频率按商务厅公告原文 "monthly or quarterly" 改为「按月或按季」。外用药风险段按 FDA Cleocin T 标签与 AAD 诊疗页改写，删去「几乎不进入血液循环」「误诊通常只是没治好」「最坏不良反应仅局部刺激」三处失实表述。
9. 本次修订的文件写入因权限未获批未能落盘，以本文全文为准。
-->
