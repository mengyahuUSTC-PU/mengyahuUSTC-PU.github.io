---
title: "Opus 5 满月复盘：年化 650 亿美元的公司，消费端为什么只有 9%"
description: "Opus 5 不是为扭转消费端设计的。价格不动、能力翻倍，这是一次瞄准 API 市场的定价进攻，而订阅用户从头到尾感知不到。"
pubDate: 2026-08-23
tags: [anthropic, model-release, ai-market]
lang: zh
slug: claude-opus-5-one-month-later
translationOf: claude-opus-5-one-month-later
---

7 月 24 日，Anthropic 发布 [Claude Opus 5](https://www.anthropic.com/news/claude-opus-5)。这篇不是发布速报——到今天它刚好满一个月。我特意等到现在写，是因为发布当天只有官方口径，一个月后独立评测和市场数据都齐了，可以把两件事放在一起看。

这两件事是：Bloomberg 报道 Anthropic 截至 7 月底的年化营收 run rate 达到 650 亿美元（[TechCrunch 转述](https://techcrunch.com/2026/08/17/anthropics-annualized-revenue-surges-to-65b/)），去年底这个数字还是 90 亿；同期第三方流量统计里，Claude 在全球消费级聊天应用的 web 访问份额只有 9.2%，不到 ChatGPT（53.9%）的五分之一（[Momentic 8 月汇总](https://momenticmarketing.com/blog/top-ai-chatbots)，美国市场稍好，13.4%）。

先解释一下口径，两个数字都容易读歪。「年化 run rate」是把最近的月收入乘以 12，衡量的是当前的收入速度，不是全年实收——它天然放大高增长公司的数字。而 9.2% 统计的是 web 访问量在七大聊天应用里的占比，不是付费用户数，属于流量面板估算，方法细节并未公开。但即便都打上折扣，反差依然成立：企业市场在狂奔，消费端长期是个位数。

每逢旗舰发布，总有人问：新模型能不能扭转消费端？看完这一个月的数据，我的判断是，Opus 5 从设计上就没打算回答这个问题。

## 发布了什么：价格不动，能力翻倍

Opus 5 定价 5 美元/百万输入 token、25 美元/百万输出 token，和前代 Opus 4.8 完全一致（[官方发布页](https://www.anthropic.com/news/claude-opus-5)）。官方给出的能力口径是：在自家 Frontier-Bench v0.1 上比 Opus 4.8 翻倍以上；在 CursorBench 3.2 上与旗舰 Fable 5 的峰值分数差距在 0.5% 以内，成本只有一半；在 OSWorld 2.0（电脑操作类任务）上超过 Fable 5 的最好成绩，成本约三分之一。

这里需要交代一下 Anthropic 现在的产品阶梯：Fable 5 是今年推出的最高档模型，Opus 从旗舰降为次旗舰。所以 Opus 5 的定位翻译过来就是一句话：接近旗舰的能力，一半的价格。

价格标签一分没动，但单位能力的价格砍半了。这是变相降价，而且是模型厂商之间价格战的典型打法——标价不动，把每一档价格能买到的能力往上顶。

另一个同方向的设计是推理力度档位：同一个模型可以按任务调节投入多少计算，低档位省 token、高档位出满力。这不是宣传话术，ARC Prize 的独立评测就分别测了 High 和 Max 两档。对按 token 付费的买家，这等于把成本控制的旋钮交到了自己手里。

## 独立评测怎么说

官方 benchmark 是自家口径，第三方验证更值得看。ARC-AGI 是 ARC Prize 基金会维护的抽象推理测试：题目是模型从未见过的小型图形和交互谜题，专门设计成没法靠背题解决，用来测「面对全新问题的推理能力」。其中 ARC-AGI-3 是交互式游戏环境版本，模型要自己摸索规则。

[ARC Prize 的独立结果](https://arcprize.org/results/anthropic-claude-opus-5)：Opus 5（High 档）在 ARC-AGI-3 上拿到 30.2%，此前没有模型超过 8%（[The Decoder](https://the-decoder.com/anthropics-opus-5-blows-past-fable-5-and-gpt-5-6-sol-on-the-benchmark-designed-to-measure-real-intelligence/)），还解出了五个此前从未被任何模型完成的公开演示环境。ARC-AGI-1 上 97.5%、ARC-AGI-2 上 90.4%（Max 档）。ARC Prize 也给了成本注脚：与此前的领先模型相当，但略贵。

安全侧有个容易被略过的细节：发布页明确写了 Opus 5 的生物研究能力不越过现有前沿，网络攻防能力落后于 Mythos 5（Anthropic 只对审批过的机构开放的版本）——漏洞识别接近，漏洞利用开发被刻意拉开距离。能力分层从研究实践变成了产品结构。另外官方称自动化行为审计给出 2.3 的失准行为分，是其历代最低；这是 Anthropic 自己的自动化审计，不是第三方结论，我没找到独立复现。

## 这是一次定价进攻，目标是按 token 算账的人

把上面几件事放在一起——标价冻结、单位能力减半、可调推理档位、agent 类 benchmark（电脑操作、自动化流水线）当主打成绩——指向的买家画像非常清楚：大规模跑 agent 工作负载的企业和开发者。

这类买家的决策方式和消费者完全不同。他们算的是「完成一个任务花多少钱」：一条每天跑几十万次的代码审查流水线，单任务成本降一半，直接体现在损益表上。模型换名字、换头衔都无所谓，cost-per-task 曲线下移才是购买理由。Opus 5 的整个发布设计，就是冲着把这条曲线压下去。

而营收数据说明这个市场当下有多值钱：650 亿的年化 run rate，5 月还是 470 亿，同期 OpenAI 是 400 亿（同一篇 TechCrunch 报道）。这轮增长是模型 API 和企业产品拉动的，Anthropic 增速能压过 OpenAI，靠的正是这一侧。

## 为什么消费端无感

同一次发布，消费者那边几乎听不到声音。这不是宣传失误，是机制使然。

第一，订阅制隔断了价格信号。消费者付的是固定月费，API 降价一分钱也落不到他们账单上。「单位能力价格砍半」这个最重磅的变化，对订阅用户是不可见的。

第二，聊天场景测不出能力差距。ARC-AGI 上三倍于前纪录的推理能力，在「帮我改封邮件」里表现不出来。两代模型在日常问答上的差距，要专门出题才能测出来，而消费者不出题。

第三，消费端的竞争变量本来就不在模型层。换一个聊天 app 的成本是习惯、历史对话、记忆功能、和其他工具的打通——这些都是产品和分发问题。ChatGPT 的 53.9% 是先发、品牌和默认入口积累出来的，不是当前模型分数领先的结果；反过来，Claude 的模型分数再涨，也不直接动摇这些东西。

所以「新模型能否扭转消费端」这个问题，前提就错了。消费端份额和模型质量在当前市场上已经明显脱钩，指望一次模型发布去解决分发问题，等于用错了工具。

## 满月之后的判断

一个月看下来，Opus 5 是一次执行得很干净的定价进攻：在自己已经领先的市场（API、编码、agent）把性价比优势再拉开一档，对自己落后的市场（消费级 app）不做任何承诺。从 650 亿对 90 亿的增长曲线看，这个取舍暂时没什么可指摘的——钱在哪里，发布就冲着哪里。

对从业者，我觉得有两条可以直接用。一是选型时盯 cost-per-task 和档位可调性，别看旗舰头衔：次旗舰在多数任务上以一半成本贴近旗舰，已经是这代模型的常态。二是读懂价格战的形态：标价三个月不动不等于没降价，单位能力价格才是真实战场。

风险留给 Anthropic 自己：消费端不只是收入，还是品牌认知和用户数据的入口。把它长期让给 ChatGPT 和 Gemini，代价不会体现在今年的 run rate 里，会体现在几年后「普通人默认打开哪个 app」上。Opus 5 回答的问题和消费者关心的问题不是同一个，Anthropic 显然清楚这一点——它只是决定了先赢好赢的那场。

## 参考来源

- [Introducing Claude Opus 5 — Anthropic](https://www.anthropic.com/news/claude-opus-5) — 发布日期、定价、官方 benchmark 口径、能力分层与行为审计表述
- [Claude Opus 5 — ARC-AGI Results](https://arcprize.org/results/anthropic-claude-opus-5) — ARC-AGI-1/2/3 独立分数、High/Max 档位配置、成本评价
- [Anthropic's annualized revenue surges to $65B — TechCrunch](https://techcrunch.com/2026/08/17/anthropics-annualized-revenue-surges-to-65b/) — 年化 run rate 650 亿/470 亿/90 亿、OpenAI 400 亿对比（援引 Bloomberg）
- [Top AI Chatbots by Market Share — Momentic](https://momenticmarketing.com/blog/top-ai-chatbots) — 消费级 web 访问份额：ChatGPT 53.9%、Gemini 27.9%、Claude 9.2%、美国 13.4%
- [Anthropic's Opus 5 blows past Fable 5 and GPT-5.6 Sol — The Decoder](https://the-decoder.com/anthropics-opus-5-blows-past-fable-5-and-gpt-5-6-sol-on-the-benchmark-designed-to-measure-real-intelligence/) — ARC-AGI-3 此前纪录不足 8% 的背景
