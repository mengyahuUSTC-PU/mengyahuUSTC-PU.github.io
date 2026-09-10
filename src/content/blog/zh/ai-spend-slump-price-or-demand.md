---
title: "人均 AI 支出单月跌一成：企业不想用了，还是 AI 在降价？"
description: "Ramp 八月指数显示头部企业人均 AI 支出下滑近 10%。把这个数字拆开看，降价、换便宜模型、用量放缓三股力混在一起，真正值得担心的只有一个。"
pubDate: 2026-09-09
tags: [ai-economics, enterprise-ai]
lang: zh
slug: ai-spend-slump-price-or-demand
translationOf: ai-spend-slump-price-or-demand
---

支付公司 Ramp 发布了[八月 AI 指数](https://ramp.com/data/ai-index-august-2026)，标题起得很重：「AI 论题出现裂缝」（Cracks in the AI thesis）。核心数字有两个。一是在它覆盖的约 7 万家企业客户里，付费使用 AI 产品的比例停在 56%，环比只涨了 0.4 个百分点（[TechCrunch](https://techcrunch.com/2026/09/09/ai-spend-per-employee-slumped-at-top-firms-in-august-summer-doldrums-or-a-warning-sign/) 报道）。二是花钱最多的前 1% 企业，人均 AI 支出中位数降到 7,205 美元，单月降幅接近 10%。

前 1% 这个群体不是陪衬。市场此前的预期是，AI 收入接下来的增长主要靠这批「重度用户」加深使用来拉动。现在恰恰是他们在减支。

但「支出下降」是一个会骗人的指标。同一个月里，Ramp 数据显示企业实际支付的平均 token 价格是每百万 0.68 美元，而今年 3 月的峰值是 1.15 美元，降了四成。当单价在快速下跌，美元口径的支出下降，既可能是用得少了，也可能只是买同样的东西更便宜了。这篇文章就做一件事：把这两股力拆开。

## 支出 = 单价 × 用量，先拆单价

单价下跌有三个来源，性质完全不同。

第一是厂商直接降价。Ramp 首席经济学家 Ara Kharazian 对 TechCrunch 的说法是：「OpenAI 和 Anthropic 之间的竞争在让 AI 更易得，也在把企业付的价格压下来。」这是供给侧竞争，对买方是纯利好。

第二是企业主动换便宜的型号。TechCrunch 援引 Ramp 的观察称，客户在转向更便宜的旧型号，比如 OpenAI 的 GPT-5.6 Terra 和 Anthropic 的 Sonnet，而不是顶配的前沿模型。这一条我认为被普遍读得太悲观。试点阶段用最强模型验证「能不能做到」，跑通之后换成本优化的型号上生产，这是软件采购的正常路径，说明用法在成熟，不是在退烧。

第三是开放权重模型的替代。Ramp 官方页面显示，使用模型托管平台（提供开源模型和部分中国模型）的企业占比升到 6.1%，环比继续上涨。份额还小，但方向是持续分流闭源 API 的高价用量。

三条加起来，就是 3 月以来单价四成的跌幅。如果用量不变，光降价本身就足以让支出账面上大跌。

## 再看用量：这才是真问题

麻烦在于，Kharazian 给出了一个更硬的判断：目前的数据显示，**降价还没有被增长的用量补回来**。换句话说，实际 token 消耗量在涨，但涨幅追不上单价的跌幅。如果企业需求真的旺盛，降价四成应该刺激出远超四成的用量增长，收入曲线不该向下弯。

Ramp 报告里最扎眼的证据是关于 Fable 5 的。这是 Anthropic 目前性能最强的模型，定价约每百万 token 10 美元，是 OpenAI 的 GPT-5.6 Sol 的两倍。结果是：Fable 5 只占 Anthropic 全部 token 用量的 6%，占其收入的 11.4%；对比之下 GPT-5.6 Sol 占 OpenAI 用量的 25%。Kharazian 的结论是，这暴露了企业为 AI 付费意愿的一个新上限：性能最强不等于企业买单，超过某个价位，企业宁可用次一档的模型。

这一点对模型厂商的商业模式是实质威胁。过去两年的定价假设是「前沿溢价」：最新最强的模型定高价，靠企业为能力差距付钱。如果企业的实际行为是把模型当可互换的大宗商品来比价采购，前沿溢价就撑不住，整个行业的收入预期都要下修。

## 是不是只是暑假效应

有一个不能跳过的对照：去年同期发生过几乎一样的事。Ramp 的指数在 2025 年 8 月到 10 月也几乎没有增长，年底又重新涨起来。8 月有假期，试点项目暂停、预算周期空转，都会压低当月数字。所以单看这一个月，「季节性回调」和「采用曲线进入平台期」这两种解释在数据上还分不出来，任何一边的断言现在都是抢跑。

顺带交代两处我没能完全核实的口径问题。其一，Ramp 官方页面写 7 月前 1% 企业的人均支出中位数是 7,400 美元，这与「降至 7,205 美元、降幅近 10%」在算术上对不上，差异可能来自数据修正或统计口径，我没能找到解释。其二，衡量整体经济的基准可以参考美国人口普查局的 [BTOS 抽样调查](https://www.census.gov/programs-surveys/btos.html)：TechCrunch 引 8 月 23 日更新的数据称只有 22% 的美国企业报告在用 AI，而人口普查局自己发布的今年上半年数据在 17% 到 20% 之间，22% 更接近其中「未来六个月预期使用」的口径。两个来源都指向同一个事实：全经济范围的 AI 渗透率只有两成上下，Ramp 客户群（偏科技友好的中型企业）的 56% 远不能代表整体。

## 该盯什么指标

把上面的拆解合起来，我的判断是三句话。

美元口径的 AI 支出指数正在失真。单价一年内近乎腰斩的行业里，支出下降不能直接读成需求下降，就像通缩期的名义 GDP 读不出真实产出。真正该盯的是 token 消耗量这个「实物量」指标，Ramp 恰好有 token 级数据，后续几期值得逐月追。

需求端确实有一个真信号，但不是「企业不用 AI 了」，而是付费意愿封顶：Fable 5 的份额数据说明，企业对单位能力的出价存在上限，前沿溢价的商业模式第一次撞到了天花板。受伤的是模型厂商的收入模型，不是 AI 的实际渗透。

分辨季节性还是平台期，要等 10 月到 11 月的数据：如果重演 2025 年的路径，年底前 56% 这个采用率会重新爬升、前 1% 的支出企稳；如果 Q4 没有回暖，那才轮到「平台期」这个词登场。在那之前，泡沫论和爆发论都还只是立场，不是结论。

## 参考来源

- [Ramp AI Index: August 2026 — Cracks in the AI thesis](https://ramp.com/data/ai-index-august-2026) — 厂商采用率（Anthropic 43.5%、OpenAI 39.7%、xAI 4%）、开放模型平台占比 6.1%、Fable 5 与 GPT-5.6 Sol 的 token/收入份额与定价、7 月前 1% 人均 7,400 美元、「付费意愿新上限」论断
- [TechCrunch: AI spend per employee slumped at top firms in August](https://techcrunch.com/2026/09/09/ai-spend-per-employee-slumped-at-top-firms-in-august-summer-doldrums-or-a-warning-sign/) — 56%（+0.4pp）、前 1% 降至 7,205 美元（近 10%）、token 均价 0.68 美元 vs 3 月峰值 1.15 美元、转向 GPT-5.6 Terra/Sonnet、Kharazian 引语、「量未补价」判断、2025 年 8–10 月先例、Census 22%
- [U.S. Census Bureau: Business Trends and Outlook Survey](https://www.census.gov/programs-surveys/btos.html) — 全经济 AI 使用率基准（2025 年 12 月–2026 年 5 月为 17%–20%）
- [U.S. Census Bureau: Large Firms Biggest AI Users](https://www.census.gov/library/stories/2026/05/ai-use-businesses.html) — BTOS 口径与企业规模差异背景
