---
title: "见过前沿模型全部实力的，全世界大约只有五千人"
description: "Karpathy 说对 LLM 能力的认知正收窄成一个尖漏斗。拆开看：近八成用量落在模型进步最小的那一面，能力每四个月翻倍而印象只采样一次，披露权限又按层分配，差距按复利拉大。"
pubDate: 2026-10-11
tags: [ai-governance, model-evaluation]
lang: zh
slug: llm-capability-perception-funnel
translationOf: llm-capability-perception-funnel
---

10 月 11 日，Karpathy 把自己四月的一条推文翻出来重发（[10 月推文](https://x.com/karpathy/status/2109361546505966046)、[4 月原帖](https://x.com/karpathy/status/2042334451611693415)）。四月他的说法是「两群人各说各话」：一边是试过免费版 ChatGPT、就此定型了对 AI 看法的人，一边是在专业领域用前沿 agent 模型的人。现在他改口：不是两群人，是一个尖漏斗。他给了一组毛估——约 60 亿人（全球人口约 75%）几乎没接触过 LLM；10 到 20 亿人是免费聊天产品的轻度用户，把它当更好的搜索加写作辅助；约 2000 万人（0.2%）在数学和代码领域日常用前沿模型，亲眼见过以前要花几周几个月的项目被 agent 一个 prompt 做完；最里面大约五千人，能在实验室内部摸到未发布的系统，看一队 agent 花数周协作完成大型软件项目。他归因于三件事：你带给模型的问题规模、能力在不同领域分布极不均匀、免费/付费/内部的权限落差。

这组数字全是他的估算，没有一手统计。但分层本身有数据可以对上，而且拆开看，这个漏斗不是静态的认知差异，是一台会自己拉大差距的机器。（这条我在[当天的快讯](/blog/briefing-2026-10-11)里收录过，这篇把「为什么会拉大」拆开讲。）

## 近八成用量，落在模型进步最小的那一面

OpenAI 去年 9 月发过一份用量研究《[How People Use ChatGPT](https://cdn.openai.com/pdf/a253471f-8260-40c6-a2cc-aa93fe9f142e/economic-research-chatgpt-usage-paper.pdf)》：截至 2025 年 7 月，ChatGPT 每周用户超 7 亿，消息里近八成落在三类——生活事务指导、查信息、写作；编程只占 4.2%。绝大多数人对 AI 的全部体验，采样自「当搜索用、当文书助手用」这一面。

而过去两年能力增量最大的恰恰不是这一面。后训练的主力是强化学习，RL 需要可验证的奖励信号，于是能力提升集中砸在代码、数学这类对错可判、经济价值高的领域。查资料、写邮件的体验一年里变化有限，幻觉还时不时可见；同一时间，agent 能独立完成的工程任务长度在指数增长。两层人的经验都是真的，只是采样自同一个模型差距越拉越大的两个切面。

## 增速是指数的，印象是一次性的

METR 去年提出用「任务时长」度量 agent 能力：模型能以 50% 成功率完成的任务，折算成人类完成它需要的工作时长（[arXiv:2503.14499](https://arxiv.org/abs/2503.14499)）。2019 到 2024 年，这个时长每约 7 个月翻一倍；2024 年之后加速到约 4 个月；到 2026 年 3 月，前沿模型已能完成人类要花 14 个小时以上的编码任务（[AI Digest 跟踪页](https://theaidigest.org/time-horizons)）。

指数增速遇上一次性印象，差距就按复利累积。一个人 2025 年初试过免费版、形成「会一本正经地胡说」的判断，到今天中间隔着三四个翻倍周期。他的认知没有变错，是过期了，而过期的速度本身还在加快。这是「漏斗在变尖」的算术内核：刷新认知的成本不变，不刷新的代价每四个月翻一倍。

第三个机制是披露的结构。最内层那五千人看到的是未发布模型、不设产品限额的算力；外界等到发布才能校准，拿到的还是带成本、速率和安全约束的产品形态，评测细节对外通常只有 system card 级别的摘要。监管侧有一条专门通道——美国 AI 安全研究所 2024 年 8 月与 OpenAI、Anthropic 签了预部署访问协议（[NIST 公告](https://www.nist.gov/news-events/news/2024/08/us-ai-safety-institute-signs-agreements-regarding-ai-safety-research)），可以在发布前后拿到主要新模型。但这条通道只把信息差缩小到评测员，公众和多数立法者不在其中。

## 决策者多数站在漏斗外两层

这个结构对治理的含义很直接：公共讨论和立法的输入，默认采样自最宽的两层。按「聊天机器人会出错」的心智模型设计规则，规则生效时对象已经是能自主跑几周的 agent 系统；反过来，没有一手体验的决策者也容易被供应商叙事带着高估。两种错配共用同一个病根：证据不是自己采的。企业内部同理，用免费层体验否决预算，和看一场 demo 全盘押注，犯的是同一个错误。

所以我现在评估任何人（包括我自己）关于 AI 能力的论断，先问两个问题：证据采样自漏斗哪一层？什么时候采的？第二个问题往往比第一个更致命。

自我校准其实没那么贵，不需要内部权限：拿付费前沿模型加 agent 工具，在自己的领域跑一个真实的、以天为单位的任务，这一手经验比读十篇转述更能刷新判断。漏斗最危险的位置不在最外层，60 亿没用过的人至少知道自己不知道；危险在中间——拿着第二层的体验、以为自己看到了全部的决策者。

## 参考来源

- [Karpathy 2026 年 10 月 11 日推文](https://x.com/karpathy/status/2109361546505966046) — 漏斗分层毛估与三个成因
- [Karpathy 2026 年 4 月原帖](https://x.com/karpathy/status/2042334451611693415) — 「两群人各说各话」的最初表述
- [How People Use ChatGPT（OpenAI/NBER，2025 年 9 月）](https://cdn.openai.com/pdf/a253471f-8260-40c6-a2cc-aa93fe9f142e/economic-research-chatgpt-usage-paper.pdf) — 7 亿周用户、三类用途近八成、编程占 4.2%
- [Measuring AI Ability to Complete Long Tasks（METR）](https://arxiv.org/abs/2503.14499) — 任务时长度量方法、7 个月翻倍
- [AI Digest: Time Horizons 跟踪页](https://theaidigest.org/time-horizons) — 2024 年后约 4 个月翻倍、2026 年 3 月达 14 小时以上
- [NIST：美国 AI 安全研究所与 Anthropic、OpenAI 签署协议](https://www.nist.gov/news-events/news/2024/08/us-ai-safety-institute-signs-agreements-regarding-ai-safety-research) — 预部署访问条款
