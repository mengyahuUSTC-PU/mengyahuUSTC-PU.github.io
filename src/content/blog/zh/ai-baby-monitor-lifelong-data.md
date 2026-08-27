---
title: "从摇篮到 100 岁：婴儿监视器公司想要一份跟人一辈子的档案"
description: "拆解 Nanit 的数据采集机制：婴儿房里的 AI 摄像头到底收了什么、流向哪里、监管为什么管不住，以及家长评估这类产品该问的三个问题。"
pubDate: 2026-08-26
tags: [privacy, consumer-ai, iot]
lang: zh
slug: ai-baby-monitor-lifelong-data
translationOf: ai-baby-monitor-lifelong-data
---

8 月初，《纽约时报》记者 Sapna Maheshwari 发了一篇 Nanit 的特写（[原文有付费墙，此为 Techmeme 条目](https://www.techmeme.com/260803/p8)，标题 "Aw, It's Baby's First A.I. Surveillance System"）。Nanit 的主打产品是一台架在婴儿床正上方的摄像头：高清画面传到服务器，机器学习算法记下宝宝每一次睁眼和闭眼的确切时刻，再汇总成图表——每晚一个 0 到 100 的「睡眠效率」分数、入睡用了几分钟、家长半夜被叫起来几次。

安全研究者 Bruce Schneier [转发这篇报道](https://www.schneier.com/blog/archives/2026/08/spyware-for-babies.html)时，标题只用了三个词：Spyware for Babies，给婴儿的间谍软件。

这话听着刺耳。但先看规模，再看它刺不刺耳。

## 这不是小众玩具

Nanit 自称有 100 万日活用户、年收入超过 1 亿美元（《纽约时报》报道中的公司口径）。2025 年 12 月，它完成了 [5000 万美元的增长轮融资](https://www.prnewswire.com/news-releases/nanit-raises-50m-to-expand-its-ai-powered-systems-giving-parents-real-time-insights-into-infant-health-and-development-302643439.html)，由 Springcoast Partners 领投，Upfront Ventures 和 JVP 跟投。

钱的用途写得很直白：2026 年推出一套「Parenting Intelligence System」（育儿智能系统），在睡眠之外追踪呼吸模式、动作特征、大运动里程碑、语音和语言发展，还要识别「预示代谢、情绪或认知挑战的趋势」。官方新闻稿里的两个数字更说明方向：Nanit 已累计采集了 100 多个国家、超过 50 亿小时的婴儿睡眠数据；70% 的活跃用户在孩子满 4 岁后还在继续用摄像头。CEO Anushka Salinas 的原话是：「我们设想一个未来，人们可以追踪和调取自己从出生到 100 岁的完整健康数据。」

从出生到 100 岁。婴儿监视器这个品类存在几十年了，此前它一直是个传输设备：麦克风加喇叭，孩子哭了你能听见，仅此而已。Nanit 做的事在商业上换了物种——设备只是入口，生意是数据平台。《纽约时报》挖到的一个细节把这层意图说破了：为 Nanit 做品牌的咨询公司在案例研究里写，这个项目的核心挑战是「如何把这项新技术引入育儿市场，同时超越『监控』一词的负面含义」。

## 政策文本里的采集清单

判断一款产品，比营销页可靠的是它的隐私政策，因为那是写给监管者看的。我通读了 Nanit 的[隐私政策](https://www.nanit.com/policies/privacy-policy)（最近一次更新是 2026 年 2 月 10 日），采集清单大致分三层：

关于家长：姓名、邮箱、电话、支付信息、IP 地址，还有你家 WiFi 网络的名称。关于孩子：姓名、头像、性别、出生日期，以及家长手动记录的照护日志。关于婴儿房：视频和音频录制、温度、湿度，并用计算机视觉分析睡眠中的呼吸动作。

数据用途一栏里，除了提供服务，还有一句标准但值得逐字读的表述：基于「正当利益」开展「直接营销、研究与开发」，包括「custom audiences 广告和跨设备追踪」。这两个词需要翻译一下。custom audiences（自定义受众）指的是公司把手里的用户名单上传给 Meta、Google 这类广告平台，平台匹配出同一批人，再向他们精准投放；跨设备追踪则是把你在手机、平板、电脑上的行为拼成同一个人的画像。也就是说，一个哄睡工具的用户数据，接入的是和电商、游戏 App 同一套广告基础设施。

「我们不出售个人信息」这句 Nanit 说了，但要读全。政策原文的表述是：按加州消费者隐私法（CCPA，美国目前最严的州级隐私法）的定义不构成「出售」，但同时承认，它使用的第三方分析工具「可能被解释为出售」。CCPA 把「出售」定义得比日常语义宽：数据换任何有价值的对价都算，不一定要收钱。所以这句免责声明的准确读法是：我们没拿数据直接换钱，但数据确实在向第三方流动。

另外两点：政策没有给出具体的数据保留期限，只说保留「与使用服务的时间一致或达成收集目的所必需」；政策明确写了不响应浏览器的 DNT（Do Not Track，「请勿追踪」）信号。我还专门找了有没有条款明确限制把视频、音频用于训练 AI 模型——没有找到。

## 安全做得不差，但安全不等于隐私

要说公道话：Nanit 的[安全页](https://www.nanit.com/pages/privacy-security)列的措施在消费级产品里算认真的。视频流用 256 位 AES 加密；视频只能从摄像头单向推送到你的设备，外部无法直接从摄像头拉流；多因素认证（MFA，登录时除密码外还需第二重验证）是强制的；公司声明普通员工无权访问用户视频流；云端存储录像需要用户主动订阅 Insights 计划才开启。

但这些措施回答的问题是「外人能不能偷看」。隐私的核心问题是另一个：公司自己拿这些数据做什么。加密挡得住黑客，挡不住商业模式。这两个问题经常被产品页混在一起说，家长评估时得拆开。

还有第三个容易被忽略的问题：数据本身准不准。《纽约时报》的报道里提到，摄像头会把实际没发生过的探视和哭闹也记录在案。哥伦比亚大学儿科医生 Rebekah Diamond 在报道中的担忧则更根本：「家长正在失去一点自己判断和决策的肌肉。」当一个分数每天早上告诉你昨晚带娃带得好不好，你会慢慢用它替代自己的观察——哪怕分数的口径你并不了解。

## 监管为什么接不住

美国现有的隐私法框架，对这类产品几乎是空转的，原因值得拆开看。

HIPAA（美国医疗隐私法）管的是医院、保险公司这类「涵盖实体」。Nanit 采集呼吸、睡眠这些高度类医疗的数据，但它是消费电子公司，不在 HIPAA 管辖范围内。同样的数据，从医院设备里出来受严格保护，从婴儿床上方的摄像头里出来就只受公司自己的隐私政策约束。

COPPA（儿童在线隐私保护法）看起来对口，实际也接不住。它的核心机制是「可验证的家长同意」——防的是公司绕开家长偷偷收集孩子数据。但在婴儿监视器的场景里，家长就是买家和安装者，同意环节自动满足。法律设计时假设家长是孩子隐私的守门人，没有预想到「家长主动把数据交出去」这种结构。而数据的真正主体——那个婴儿——要十八年后才有行为能力，等他能表达意见时，档案已经积累了十八年。

## 家长可以问的三个问题

落到可操作的层面，评估这类产品，我认为要问三个问题。

一，数据在哪里处理。只在设备本地分析、不上传，和上云存储分析，是两种风险等级。Nanit 的模式是云端；市面上也有主打本地处理的监视器。买之前先弄清这一点。

二，公司靠什么赚钱。硬件加订阅费是一种模式，数据变现是另一种。判断依据不听宣传，看隐私政策里有没有营销、广告、第三方共享条款——上面拆过，Nanit 的政策里这些都有。

三，退出成本多高。能不能删除数据（Nanit 提供删除请求通道 privacy@nanit.com，承诺 45 天内响应）；隐私政策可以单方面修改，今天的承诺不约束明天的版本；公司将来被收购时，数据通常作为资产一并转移——这是行业通行做法，评估任何一家创业公司的数据承诺时都该把这一条计入。

还有一条通用的读法：把功能清单当成采集清单读。产品页上每多一项「洞察」——呼吸监测、语言发展、情绪趋势——背后就多一条数据管道。功能升级就是采集升级，没有例外。

婴儿数据和成人数据有两点本质不同：当事人无法同意，以及不可重置。密码泄露可以改密码，一个人从出生第一天起的呼吸模式、睡眠曲线、语言发展轨迹泄露了，没有任何补救手段。当 Nanit 的 CEO 说「从出生到 100 岁」时，她描述的不是愿景，而是这家公司资产负债表上最值钱的那一行。摄像头本身不是问题，问题是「从第 0 天开始建档、由别人代为同意」正在变成默认设置——而默认设置，从来是最难被重新谈判的东西。

## 参考来源

- [Aw, It's Baby's First A.I. Surveillance System（《纽约时报》，2026-08-02，Sapna Maheshwari；via Techmeme](https://www.techmeme.com/260803/p8) — 核心特写事实：睡眠效率分、睁闭眼记录、100 万日活与 1 亿美元收入的公司口径、品牌咨询公司引语、误报细节、Diamond 医生引语
- [Spyware for Babies — Schneier on Security](https://www.schneier.com/blog/archives/2026/08/spyware-for-babies.html) — 选题来源，正文仅引用其标题
- [Nanit Privacy Policy](https://www.nanit.com/policies/privacy-policy) — 采集清单、数据用途、CCPA「出售」表述、保留期限、DNT
- [Nanit Privacy & Security](https://www.nanit.com/pages/privacy-security) — 加密、单向视频流、MFA、员工访问限制、Insights 订阅与云存储的关系
- [Nanit Raises $50M…（PR Newswire 官方新闻稿，2025-12）](https://www.prnewswire.com/news-releases/nanit-raises-50m-to-expand-its-ai-powered-systems-giving-parents-real-time-insights-into-infant-health-and-development-302643439.html) — 融资细节、Parenting Intelligence System、50 亿小时数据、70% 留存、CEO 引语
- [Democratic Underground 论坛转录](https://www.democraticunderground.com/100221417047) — 用于逐字核对《纽约时报》原文引语（品牌咨询、误报、Diamond 引语）
- [The Hustle: Even babies are living in an AI-powered surveillance state](https://thehustle.co/news/even-babies-are-living-in-an-ai-powered-surveillance-state) — 交叉核对 NYT 报道要点，正文未直接引用其独有数字
