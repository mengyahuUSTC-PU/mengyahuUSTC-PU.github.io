---
title: "租 4 年、保 16 年：AI 大厂把 1.65 万亿美元债务放进了脚注"
description: "拆解 Meta Hyperion 合资结构：表外融资如何合规地把 AI 基建债务移出资产负债表，风险最终落在谁头上"
pubDate: 2026-07-23
tags: [ai-infrastructure, finance, industry-trends]
lang: zh
slug: ai-off-balance-sheet-debt
translationOf: ai-off-balance-sheet-debt
---

2025 年 10 月 21 日，Meta [官宣](https://www.prnewswire.com/news-releases/meta-announces-joint-venture-with-funds-managed-by-blue-owl-capital-to-develop-hyperion-data-center-302590584.html)与资管公司 Blue Owl Capital 成立合资企业，共同开发路易斯安那州的 Hyperion 数据中心，总开发成本约 270 亿美元，被 [Bloomberg](https://www.bloomberg.com/news/articles/2025-10-16/blue-owl-seals-largest-private-capital-deal-for-meta-s-ai-growth) 称为迄今规模最大的私募资本交易。

细读公告，有三个数字放在一起很怪。Meta 在合资公司里只持股 20%，Blue Owl 持股 80%；Meta 与合资公司签的租约，初始租期只有 4 年；但 Meta 同时提供了一份覆盖约 16 年的剩余价值担保（residual value guarantee，即租约终止时若资产贬值超过约定水平，由 Meta 补足差额，设有上限）。更妙的是，Meta 把土地和在建工程装进合资公司后，反手从中拿走了约 30 亿美元的一次性分配。

一家账上现金及有价证券约 800 亿美元（见其 [2025 年年报](https://www.sec.gov/Archives/edgar/data/1326801/000162828026003942/meta-20251231.htm)）、发债利率与美国国债的利差只有[几十个基点](https://www.fi-desk.com/origination-meta-sold-us30-billion-of-ai-bonds-on-30-october/)的公司，为什么要绕这么大一个圈子？答案藏在会计处理里。这笔总额约 300 亿美元的融资中，[约 270 亿美元是发行给 PIMCO 等债券投资者的私募债](https://www.bloomberg.com/news/articles/2025-10-16/blue-owl-seals-largest-private-capital-deal-for-meta-s-ai-growth)，挂在合资公司名下；Meta 对合资公司按权益法核算、不并表——年报给出的理由不是持股比例低，而是 Meta 并未主导对该实体经济表现影响最大的活动、不构成会计准则所说的「主要受益人」。于是这笔债务不出现在 Meta 的资产负债表上（年报同时在脚注披露，Meta 对该实体的最大损失敞口约 460 亿美元）。

## 这不是个案，是行业标准动作

[日经的调查](https://asia.nikkei.com/business/technology/five-us-tech-giants-hidden-debts-soar-to-1.65tn-on-opaque-ai-funding)统计，Alphabet、Microsoft、Amazon、Meta、Oracle 五家公司与 AI 基建相关的表外义务——数据中心租约、GPU 采购合同、SPV（特殊目的实体，为单一项目设立的法律独立公司）安排——合计已达约 1.65 万亿美元，超过了这五家表内报告的 1.35 万亿美元债务，且四年间膨胀了约八倍。其中 Meta 一家约 4200 亿美元，接近其表内债务的三倍。

评级机构比媒体动手更早。穆迪今年 2 月的报告（[Fortune 报道](https://finance.yahoo.com/news/moody-flags-662-billion-risk-081000616.html)）给出了更细的切片：截至 2025 年底，五大厂商「已签约但尚未开始」的数据中心租赁承诺达 6620 亿美元，占其全部未折现租赁承诺（9690 亿美元）的三分之二以上——这些钱一分都不在资产负债表上。

## 机制：三道合规的门

把债务留在脚注里，靠的不是造假，而是三条现行规则的组合拳。

**第一道门：租约「未开始」就不入表。** 美国现行租赁准则 ASC 842（2016 年发布）本已把经营租赁请上了资产负债表，但确认时点是租约开始——数据中心还在打地基，签了约的未来租金就只需要在财报脚注里披露。6620 亿美元属于这一类。

**第二道门：短租期 + 续约选项。** [传统数据中心租约是 10–15 年](https://finance.yahoo.com/news/moody-flags-662-billion-risk-081000616.html)，如今大厂签的初始租期短至几年，附带一串续约选项。入表的负债只覆盖「合理确定」会执行的期限，而大厂可以说：AI 硬件寿命只有 4–6 年，四年后的需求谁说得准？于是续约期不计入负债。Meta 的 Hyperion 租约初始期 4 年，正是这个打法。

**第三道门：担保只有「很可能触发」才算负债。** 出资方不傻：你只租 4 年，凭什么让我掏 20 年的钱？于是大厂补上剩余价值担保。但按现行规则，担保只有在「很可能」（probable）赔付时才确认为负债。穆迪报告里的例子：Meta 披露的一批 2029 年开始的数据中心租约，入表承诺 123 亿美元，同时挂着门槛高达 280 亿美元的剩余价值担保——因被管理层判定为「不太可能触发」，一分未计。

三道门合起来的效果：经济实质接近「可以用上 20 年的基础设施 + 兜底担保」（4 年初始期之外多为续约选择权），而在租约开始之前，报表正文里连那 4 年初始租金都尚未确认为负债——一切只躺在脚注里。

## 像安然吗？像 2008 吗？都不像，但都沾边

先说不像的地方，这很重要。安然的 SPE 是欺诈：所谓的外部股权由内部人控制、并未真正承担风险，担保被刻意隐瞒（[SEC 起诉书](https://www.sec.gov/litigation/complaints/comp17762.htm)记录了这些细节）。今天的结构——至少本文拆解的 Meta Hyperion——走的是现行规则，条款都写进了证券申报文件，只是写在脚注里；常用的杠杆指标不会自动把脚注里的承诺算进去，评级机构虽会在「调整后债务」里手工加回，但那是少数人才做的功课。问题不是隐藏，是**披露了但很少有人折现**。

真正相似的是 2008 年的一个教训：风险转移往往是假的。当年银行把资产装进表外的结构化投资工具（SIV），却保留了显性或隐性的支持承诺，市场一冻结，[花旗等发起银行只得把自家 SIV 资产接回表内](https://elischolar.library.yale.edu/cgi/viewcontent.cgi?article=1592&context=journal-of-financial-crises)。今天的对应物就是剩余价值担保和运营依赖——租约到期时若 AI 需求不及预期，Meta 可以不续租，但若届时资产公允价值低于约定的递减门槛，就要在上限内赔付差额；若需求持续，租约开始、续约确认，负债则大规模回表。穆迪的判断是后一种情形也不轻松：随着租约陆续启动，调整后债务将激增，可能造成信用状况的「实质性」恶化（[穆迪报告原文](https://dkf1ato8y5dsg.cloudfront.net/uploads/52/504/1-sector-in-depth-accounting-us-hyperscalers-23feb2026-pbc-1467708.pdf)）。

关键区别在于风险这次停在谁手里。2008 年是银行体系自持，杠杆加期限错配，传导快而猛。这次接住风险的是私募市场：Blue Owl 管理的基金持有合资公司 80% 股权，PIMCO 等机构认购了债券，而这类私募信贷基金的主要出资人是[养老金、保险公司和主权财富基金](https://www.bis.org/publ/qtrpdf/r_qt2503b.htm)这样的长线资金。私募信贷资产没有实时市价，[估值不透明、更新不频繁](https://www.bis.org/publ/arpdf/ar2024e1.htm)，对冲击的反应因此滞后——传导会更慢，但也更不透明：等你看到亏损，往往已经是既成事实。

## 读者能带走什么

第一，看 AI 大厂财报时，市盈率之外多翻三处脚注：未开始的租赁承诺、采购义务、担保安排。表内债务已经是这五家杠杆故事里信息量最小的数字。

第二，有一个几乎免费的观测指标：**初始租期与担保期限的差值**。Meta 愿意担保 16 年，却只肯承诺租 4 年——这等于 Meta 自己给「AI 需求能否持续到 2030 年之后」标了价：不确定到不愿写进合同正文，只肯放在担保条款里。厂商的会计选择，比它们的公开发言诚实。

第三，如果这轮基建投资最终不及预期，裂缝会从哪里先显形？这是判断题，没有现成数据可引，我的推演是：最先承压的未必是大厂股价，而更可能是私募信贷组合的估值，以及持有这些债权的保险和养老资金——正因为估值更新滞后，等裂缝显形时，损失往往已经积累了很久。在我看来，这套结构对 Meta 们更像一份便宜的看跌期权：需求兑现，续租即可；需求落空，最坏情形是按上限赔付担保、把折旧中的机房留给债权人。期权的另一头——收着利差、实际承担「AI 需求持续」尾部风险的私募信贷投资人——才是这个故事里更该睡不着的人。

## 参考来源

- [Meta Announces Joint Venture with Funds Managed by Blue Owl Capital to Develop Hyperion Data Center](https://www.prnewswire.com/news-releases/meta-announces-joint-venture-with-funds-managed-by-blue-owl-capital-to-develop-hyperion-data-center-302590584.html) — Meta 官方公告：股权比例、270 亿美元开发成本、4 年初始租期、16 年剩余价值担保、30 亿美元一次性分配、面向 PIMCO 等债券投资者的私募债
- [Blue Owl Seals Largest Private Capital Deal for Meta's AI Growth — Bloomberg](https://www.bloomberg.com/news/articles/2025-10-16/blue-owl-seals-largest-private-capital-deal-for-meta-s-ai-growth) — 「迄今最大私募资本交易」说法出处、约 270 亿美元债务与股权的融资拆分
- [Meta Platforms 2025 Form 10-K — SEC](https://www.sec.gov/Archives/edgar/data/1326801/000162828026003942/meta-20251231.htm) — 年末现金及有价证券约 816 亿美元、Hyperion 合资实体不并表的「主要受益人」判定、最大损失敞口披露、担保未确认负债的表述
- [Five US tech giants' hidden debts soar to $1.65tn on opaque AI funding — Nikkei Asia](https://asia.nikkei.com/business/technology/five-us-tech-giants-hidden-debts-soar-to-1.65tn-on-opaque-ai-funding) — 1.65 万亿美元表外义务、1.35 万亿表内债务对比、四年八倍、Meta 约 4200 亿美元
- [Moody's flags $662 billion risk at the heart of the data-center buildout — Fortune (via Yahoo Finance)](https://finance.yahoo.com/news/moody-flags-662-billion-risk-081000616.html) — 穆迪 2026 年 2 月报告：6620 亿/9690 亿美元租赁承诺、10–15 年传统租期与租期缩短原因、Meta 123 亿承诺对 280 亿担保门槛的案例
- [Moody's：Accounting — US hyperscalers（报告原文，2026-02-23）](https://dkf1ato8y5dsg.cloudfront.net/uploads/52/504/1-sector-in-depth-accounting-us-hyperscalers-23feb2026-pbc-1467708.pdf) — 调整后债务「实质性」增加、信用状况恶化警告的原始出处
- [Meta sold US$30 billion of AI bonds on 30 October — The DESK](https://www.fi-desk.com/origination-meta-sold-us30-billion-of-ai-bonds-on-30-october/) — Meta 公司债各期限对美债利差（5 年期 50 个基点至 40 年期 110 个基点）
- [The global drivers of private credit — BIS Quarterly Review](https://www.bis.org/publ/qtrpdf/r_qt2503b.htm) — 私募信贷基金主要出资人为养老金、保险公司与主权财富基金
- [BIS Annual Economic Report 2024, Chapter I](https://www.bis.org/publ/arpdf/ar2024e1.htm) — 私募市场估值不透明、更新不频繁导致的滞后反应
- [SEC v. Andrew S. Fastow（起诉书）](https://www.sec.gov/litigation/complaints/comp17762.htm) — 安然 SPE 外部股权不独立、担保被隐瞒的记录
- [SIV 案例研究 — Journal of Financial Crises (Yale)](https://elischolar.library.yale.edu/cgi/viewcontent.cgi?article=1592&context=journal-of-financial-crises) — 2008 年危机中发起银行救助并合并 SIV 资产的经过
- [AI Companies Are Trying to Hide a Staggering Amount of Debt — Futurism](https://futurism.com/artificial-intelligence/ai-companies-hide-debt-off-balance-sheet) — 选题来源（聚合报道，正文事实均已改引一手来源）
