---
title: "租 4 年、保 16 年：AI 大厂把 1.65 万亿美元债务放进了脚注"
description: "拆解 Meta Hyperion 合资结构：表外融资如何合规地把 AI 基建债务移出资产负债表，风险最终落在谁头上"
pubDate: 2026-07-23
tags: [ai-infrastructure, finance, industry-trends]
lang: zh
slug: ai-off-balance-sheet-debt
translationOf: ai-off-balance-sheet-debt
---

2025 年 10 月 21 日，Meta [官宣](https://www.prnewswire.com/news-releases/meta-announces-joint-venture-with-funds-managed-by-blue-owl-capital-to-develop-hyperion-data-center-302590584.html)与资管公司 Blue Owl Capital 成立合资企业，共同开发路易斯安那州的 Hyperion 数据中心，总开发成本约 270 亿美元，被 [CNBC](https://www.cnbc.com/2025/10/21/meta-blue-owl-capital-partner-on-27-billion-ai-data-center-project-.html) 等媒体称为迄今最大规模的私募信贷交易。

细读公告，有三个数字放在一起很怪。Meta 在合资公司里只持股 20%，Blue Owl 持股 80%；Meta 与合资公司签的租约，初始租期只有 4 年；但 Meta 同时提供了一份覆盖约 16 年的剩余价值担保（residual value guarantee，即租约终止时若资产贬值超过约定水平，由 Meta 补足差额，设有上限）。更妙的是，Meta 把土地和在建工程装进合资公司后，反手从中拿走了约 30 亿美元的一次性分配。

一家账上趴着上千亿美元现金、发债利率接近美国国债的公司，为什么要绕这么大一个圈子？答案藏在会计处理里：这 270 亿美元的开发债务由 PIMCO 牵头的私募债权人持有，挂在合资公司名下——Meta 只占 20% 股权、不并表，这笔钱就不出现在 Meta 的资产负债表上。

## 这不是个案，是行业标准动作

[日经的调查](https://asia.nikkei.com/business/technology/five-us-tech-giants-hidden-debts-soar-to-1.65tn-on-opaque-ai-funding)统计，Alphabet、Microsoft、Amazon、Meta、Oracle 五家公司与 AI 基建相关的表外义务——数据中心租约、GPU 采购合同、SPV（特殊目的实体，为单一项目设立的法律独立公司）安排——合计已达约 1.65 万亿美元，超过了这五家表内报告的 1.35 万亿美元债务，且四年间膨胀了约八倍。其中 Meta 一家约 4200 亿美元，接近其表内债务的三倍。

评级机构比媒体动手更早。穆迪今年 2 月的报告（[Fortune 报道](https://finance.yahoo.com/news/moody-flags-662-billion-risk-081000616.html)）给出了更细的切片：截至 2025 年底，五大厂商「已签约但尚未开始」的数据中心租赁承诺达 6620 亿美元，占其全部未折现租赁承诺（9690 亿美元）的三分之二以上——这些钱一分都不在资产负债表上。

## 机制：三道合规的门

把债务留在脚注里，靠的不是造假，而是三条现行规则的组合拳。

**第一道门：租约「未开始」就不入表。** 安然事件后的会计改革（ASC 842）本已把经营租赁请上了资产负债表，但确认时点是租约开始——数据中心还在打地基，签了约的未来租金就只需要在财报脚注里披露。6620 亿美元属于这一类。

**第二道门：短租期 + 续约选项。** 传统数据中心租约是 10–15 年，如今大厂签的初始租期短至几年，附带一串续约选项。入表的负债只覆盖「合理确定」会执行的期限，而大厂可以说：AI 硬件寿命只有 4–6 年，四年后的需求谁说得准？于是续约期不计入负债。Meta 的 Hyperion 租约初始期 4 年，正是这个打法。

**第三道门：担保只有「很可能触发」才算负债。** 出资方不傻：你只租 4 年，凭什么让我掏 20 年的钱？于是大厂补上剩余价值担保。但按现行规则，担保只有在「很可能」（probable）赔付时才确认为负债。穆迪报告里的例子：Meta 披露的一批 2029 年开始的数据中心租约，入表承诺 123 亿美元，同时挂着门槛高达 280 亿美元的剩余价值担保——因被管理层判定为「不太可能触发」，一分未计。

三道门合起来的效果：真实承诺是「20 年的基础设施 + 兜底担保」，报表呈现是「4 年租金」。

## 像安然吗？像 2008 吗？都不像，但都沾边

先说不像的地方，这很重要。安然的 SPE 是欺诈：所谓的外部股权是自己人假扮的，担保被刻意隐瞒。今天大厂的结构完全合规，且都披露了——只是披露在脚注里，而脚注不进任何自动计算的杠杆率。问题不是隐藏，是**披露了但没人折现**。

真正相似的是 2008 年的一个教训：风险转移往往是假的。当年银行把资产装进表外的结构化投资工具（SIV），但留了隐性流动性支持，市场一冻结资产全部回表。今天的对应物就是剩余价值担保和运营依赖——租约到期时若 AI 需求不及预期，Meta 可以走人，但要触发担保赔付；若需求持续，租约开始、续约确认，负债则大规模回表。穆迪的判断是后一种情形也不轻松：随着租约陆续启动，调整后债务将激增，可能造成信用状况的「实质性」恶化。

关键区别在于风险这次停在谁手里。2008 年是银行体系自持，杠杆加期限错配，传导快而猛。这次的债权人是 Blue Owl、PIMCO 这样的私募信贷机构，背后是保险公司和养老金的钱。私募信贷没有活跃二级市场，估值靠模型而非市价——传导会更慢，但也更不透明：等你看到亏损，往往已经是既成事实。

## 读者能带走什么

第一，看 AI 大厂财报时，市盈率之外多翻三处脚注：未开始的租赁承诺、采购义务、担保安排。表内债务已经是这五家杠杆故事里信息量最小的数字。

第二，有一个几乎免费的观测指标：**初始租期与担保期限的差值**。Meta 愿意担保 16 年，却只肯承诺租 4 年——这等于 Meta 自己给「AI 需求能否持续到 2030 年之后」标了价：不确定到不愿写进合同正文，只肯放在担保条款里。厂商的会计选择，比它们的公开发言诚实。

第三，如果这轮基建投资最终不及预期，第一张倒下的多米诺骨牌大概率不是大厂股价，而是私募信贷组合的估值，以及持有这些债权的保险和养老资金。对 Meta 们来说，这套结构是一份便宜的看跌期权：需求兑现，续租即可；需求落空，赔付有上限的担保、把折旧中的机房留给债权人。期权的卖方——收着几个点利差、承担着「AI 需求永续」尾部风险的私募信贷投资人——才是这个故事里真正该睡不着的人。

## 参考来源

- [Meta Announces Joint Venture with Funds Managed by Blue Owl Capital to Develop Hyperion Data Center](https://www.prnewswire.com/news-releases/meta-announces-joint-venture-with-funds-managed-by-blue-owl-capital-to-develop-hyperion-data-center-302590584.html) — Meta 官方公告：股权比例、270 亿美元开发成本、4 年初始租期、16 年剩余价值担保、30 亿美元一次性分配、PIMCO 私募债
- [Five US tech giants' hidden debts soar to $1.65tn on opaque AI funding — Nikkei Asia](https://asia.nikkei.com/business/technology/five-us-tech-giants-hidden-debts-soar-to-1.65tn-on-opaque-ai-funding) — 1.65 万亿美元表外义务、1.35 万亿表内债务对比、四年八倍、Meta 约 4200 亿美元
- [Moody's flags $662 billion risk at the heart of the data-center buildout — Fortune (via Yahoo Finance)](https://finance.yahoo.com/news/moody-flags-662-billion-risk-081000616.html) — 穆迪 2026 年 2 月报告：6620 亿/9690 亿美元租赁承诺、租期缩短原因、Meta 123 亿承诺对 280 亿担保门槛的案例、「实质性」信用恶化警告
- [Meta partners with Blue Owl Capital on $27 billion AI data center project — CNBC](https://www.cnbc.com/2025/10/21/meta-blue-owl-capital-partner-on-27-billion-ai-data-center-project-.html) — 交易规模的第三方佐证、「最大私募信贷交易」说法出处
- [AI Companies Are Trying to Hide a Staggering Amount of Debt — Futurism](https://futurism.com/artificial-intelligence/ai-companies-hide-debt-off-balance-sheet) — 选题来源（聚合报道，正文事实均已改引一手来源）
