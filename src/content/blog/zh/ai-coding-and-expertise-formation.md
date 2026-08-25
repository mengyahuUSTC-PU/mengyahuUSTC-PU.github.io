---
title: "快两分钟，差两个等级：AI 编码欠下的学习账"
description: "「AI 依赖会毁掉编程专业能力」长期停留在资深工程师的直觉层面，Anthropic 的随机对照试验给出了数字：AI 组任务只快了两分钟，理解测验却低了 17 个百分点，掉分最狠的是把任务整个交给 AI 的用法。"
pubDate: 2026-08-24
tags: [ai-coding, skill-formation]
lang: zh
slug: ai-coding-and-expertise-formation
translationOf: ai-coding-and-expertise-formation
---

一篇标题很冲的文章这两天冲上了 Hacker News 首页：[《AI 编码将阻断专业能力》](https://larsfaye.com/articles/ai-coding-will-prevent-expertise)（AI Coding will Prevent Expertise）。截至我写这篇时，[讨论串](https://news.ycombinator.com/item?id=49421554)已经积累了 497 分、485 条评论。

作者 Lars Faye 是位写了几十年代码的工程师，他的论证核心是一个死循环：AI 编码工具需要专业判断力才能用好，可它恰恰绕开了造就专业判断力的那些摩擦。他的原话是：「如果这些工具需要专业能力才能驾驭，而它们又能主动绕开培养专业能力的摩擦，那一个人要靠什么路径成为能驾驭这些工具的专家？」初级开发者被推着用 AI 保持竞争力，却还没攒下驾驭 AI 所需的底子；而这个底子，本来要靠亲手写、亲手卡壳才能攒出来。他管这种状态叫「只长信心，不长理解」。

这类担忧不新鲜，通常停留在资深工程师的个人直觉上，评论区照例吵成两派。但这次我想认真对待它，因为现在已经有了直接针对这个问题的实验数据——其中一份还出自 AI 编码工具的厂商自己。

## 直觉的担忧，有了对照组

今年 1 月底，Anthropic 发布了一项[随机对照试验](https://www.anthropic.com/research/AI-assistance-coding-skills)：把 52 名（多为初级）软件工程师随机分成两组，任务是学习 Trio——一个所有参与者都没用过的 Python 异步编程库——并用它实现两个功能。两组唯一的区别是能否使用 AI 助手，其他条件相同，这样结果差异才能归因到 AI 本身。写完代码后马上测验，考四类能力：找错（debugging）、读代码、写代码、概念理解。

结果：AI 组平均 50 分，手写组 67 分，差 17 个百分点，按美国课堂的字母等级算差了将近两档，统计上显著且效应量不小（Cohen's d = 0.738）。而 AI 组换来的速度优势只有约两分钟，且不显著。四类题目里，两组差距最大的是 debugging。

一个细节让这份研究格外有分量：它出自 Anthropic，也就是 [Claude Code](https://claude.com/claude-code) 的开发商。卖铲子的自己测出铲子伤手，这种对自己不利的证据，通常比第三方的抨击可信得多。

## 学习发生在卡住的那一刻

为什么会这样？Anthropic 在报告里的解释很直接：「认知上的努力——甚至痛苦地卡住——很可能是形成掌握的关键。」学新东西时，从脑子里调取、试错、修正的过程本身就是记忆和直觉形成的过程，记忆研究对此有成熟证据：主动从记忆里提取信息，是形成长期记忆的[关键环节](https://doi.org/10.1016/j.tics.2010.09.003)。AI 把这一步整个接走了：代码如期产出，学习没有发生。Faye 用了个德语词 Fingerspitzengefühl，「指尖的感觉」，指老手多年实操磨出来的那种说不清但很准的直觉。摩擦被抹掉，这层直觉就没有生长的土壤。

更麻烦的是，这种损失自己感觉不到。[METR 去年的实验](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/)让 16 位资深开源维护者在自己维护的大型项目里做 246 个真实 issue，随机决定每个 issue 能否用 AI。结果用 AI 时实际慢了 19%，但开发者事前预计能快 24%，事后仍然相信自己快了 20%。这项研究测的是速度不是学习，但它证明了同一件事：对 AI 效果的主观感受和客观测量可以差出四十个百分点。写完能跑的代码带来的胜任感，未必对应真实的理解。

不过 Anthropic 的数据里还有第二层：AI 组内部分化很大。得分高的参与者用法明显不同：有人在生成代码后追问「为什么这么写」，有人让 AI 给代码时同时给解释，还有人只问概念问题、报错一律自己解决。得分最低的是把任务整个丢给 AI 等结果的用法，其他几种重度依赖的用法平均分也都不到 40%。要说明的是，这部分是事后按用法分组的观察，Anthropic 自己明确写了不能从交互模式直接推因果——随机分组证明的是「能否用 AI」这个条件的因果效应，「哪种用法伤害多大」目前只是相关证据。

还有一组数据指向相反方向。两位研究者利用 Claude Code 在开发者群体中先后被采用的时间差，对 5,346 名 GitHub 开发者的月度数据做了[准实验分析](https://arxiv.org/abs/2605.25438)——作者自己注明，由于采用是自愿的，结果是事件时间上的关联，不是确定的因果效应。采用之后，开发者活跃使用的编程语言平均多了 2.5 门（同期基线趋势是 0.9 门），首次尝试的新语言多了 1.2 门，而且新语言的尝试集中在那些原本技术面最窄的专精型开发者身上。也就是说，一边是 Anthropic 实验里被压缩的即时理解，另一边是这项研究观察到的广度扩张：以前不敢碰的领域，现在敢进了。当然，两份证据测的是两件不同的事，「用了一门新语言」和「掌握了一门新语言」是两码事——这项研究测的是使用行为，不是理解水平。

最后要说清证据的边界。Anthropic 的测验是在编码任务结束几分钟后做的，测的是即时理解，它没有回答「十年后专家会不会断代」。Faye 的断言是长期的，实验证据目前只覆盖短期。从「一次任务少学 17 个百分点」推到「一代人的专业能力崩塌」，中间隔着一个复利假设：每次学新东西都用代写式用法，损失会逐次累积。这个推演合理，但有没有纵向研究直接验证过，我没能找到；Anthropic 也把「即时测验成绩能否预测长期技能发展」[列为这项研究没有解决的问题](https://www.anthropic.com/research/AI-assistance-coding-skills)。

## 计算器为什么没欠下学习账

写这篇时我脑子里一直有个参照物：计算器。加减乘除我们全交给它了，真让我手算也还会，只是慢。没人惋惜这门手艺的退化，我们转身去干别的了。AI 编码会不会也一样，不过是又一次工具换代，二十年后回头看纯属虚惊？

比对下来，我的判断是这个类比只对了一半，而错的那一半正好是要害。

对的一半是卸载本身：手算是机械劳动，交出去不可惜，写熟了的样板代码同理。错的一半有两处。一是顺序。至少在我自己经历的数学教育里，计算器是在学会算术之后才进场的：先亲手算了好几年，摩擦完整保留在学习期，工具接手的是已经掌握的东西，正好落在 Faye 说的「卸载」一侧。数学教育界也把这个顺序当回事：美国国家数学咨询委员会（National Mathematics Advisory Panel）[警告过，「计算器的使用若妨碍了自动化能力的形成，计算的熟练程度就会受到不利影响」](https://files.eric.ed.gov/fulltext/ED500486.pdf)。而今天入行的初级开发者拿到工具的顺序通常是反的：AI 从第一天就在场，它所要求的判断力还没来得及建立。二是验收。计算器做的是基础运算，结果确定可复现，同样的输入永远给同样的结果，核对起来毫不费力；AI 生成的代码能编译、能通过给它的测试，却仍然可能是错的：有研究者[扩充了一个标准代码生成基准的测试集](https://arxiv.org/abs/2305.01210)，补上的测试查出了此前未被发现的错误 LLM 生成代码，足以把通过率最多拉低 19.3–28.9%。而验收 AI 代码恰恰需要那种只能靠亲手写攒出来的判断力。何况两者接手的东西不在一个量级：计算器只代劳流程固定的单步运算，agent 接走的是从技术选型到实现细节的整条决策链，每一环都可能错。所以计算器淘汰的能力（手算）和用好计算器所需的能力（知道该算什么）是两回事，而 AI 淘汰的能力和用好 AI 所需的能力是同一种。Faye 的死循环在计算器身上从来不存在，在 AI 编码上是结构性的。

顺着这个类比还有一个更大的问题：如果有一天 AI 写的代码真的不需要人验收了呢？那时类比就完全成立，人可以像放下手算一样放下编程。再往前推一步，编程、报表这类白领工作本来就是工业社会造出来的岗位，对人类未必「自然」；也许硅基确实比碳基适合干这些，人应该被释放去户外、去真实世界。我不觉得这个想象荒谬，但它说的是终局，而这篇文章里的所有数据都只关于过渡期。过渡期的别扭之处在于：AI 还没好到免验收的程度，METR 的减速数据、debugging 上的差距都在提醒这一点，Anthropic 也明确说[人仍然需要有能力发现错误、为高风险部署把关](https://www.anthropic.com/research/AI-assistance-coding-skills)，社会仍然需要一批有判断力的工程师兜底；可判断力的供给管道已经先被 AI 改写了。就算终局真是人类退出编程，走完过渡期也得靠一代还有判断力的人。至于终局什么时候到、到了之后人该去干什么，我拿不准，也不假装拿得准。

## 把摩擦留在打算长本事的地方

Faye 提出的区分我认为是全文最有用的一刀：认知卸载（cognitive offloading）和认知负债（cognitive debt）。把已经掌握的机械劳动交出去，是卸载，没问题；把还没建立起来的判断力交出去，是负债，迟早要还。落到操作上：

- 学新框架、新语言、新领域时，别让 AI 代写。让它当答疑对象：要解释、追问、报错自己修。Anthropic 数据里得分靠前的恰好是这几种用法。Faye 的说法更极端：「用 AI 编码工具能发生的最高效学习，是它几乎不生成任何代码的时候。」
- debugging 尽量亲手做。这是两组差距最大的题型，也是最有理由保留摩擦的地方：Faye 在文中引用的 François Chollet 把 LLM 称作「插值引擎」（interpolation engines），而软件工程「是一场适应与解决全新问题的练习」。
- 已经熟练的领域放心交给 AI，并顺手用它扩广度。想碰没碰过的技术栈时更值得试：GitHub 面板数据里，新语言的首次尝试恰好集中在原本技术面窄的开发者身上。
- 带团队的人需要刻意设计。Anthropic 给管理者的建议是：「考虑用系统性机制或有意的设计选择，确保工程师在工作中持续学习。」我的具体建议是两条：新人培养期保留无 AI 的练习环节；code review 时要求作者解释每一段生成的代码，解释不了就不合入。

专业能力不会因为 AI 的存在就自动崩塌。现有数据能说的是：至少在即时理解上，掉分多少和用法有关——这个规律 Anthropic 自己也只以相关性证据的形式报告；长期会不会崩塌，我没能找到能回答的研究。而把任务整个丢过去等结果，这种最省事的用法，恰好是实验里掉分最狠的那种。摩擦不再是编程的默认配置了，它变成一种需要主动选择保留的东西。选在哪里保留，决定你五年后还剩多少不可替代的判断力。

## 参考来源

- [AI Coding will Prevent Expertise — Lars Faye](https://larsfaye.com/articles/ai-coding-will-prevent-expertise) — 选题原文；核心悖论、cognitive debt/offloading 区分及各处引文
- [Hacker News 讨论串](https://news.ycombinator.com/item?id=49421554) — 讨论热度（497 分 / 485 评论，截至写作时）与正反方观点
- [How AI assistance impacts the formation of coding skills — Anthropic](https://www.anthropic.com/research/AI-assistance-coding-skills) — RCT 设计与全部量化结果（52 人、50% vs 67%、两分钟不显著、debugging 差距最大、高分者的用法、给管理者的建议）
- [Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity — METR](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/) — 16 人 / 246 issue、慢 19%、事前预计快 24%、事后自认快 20%
- [Agentic Delegation and the Language Frontier of Software Developers: A Model and Evidence from Claude Code on GitHub — arXiv:2605.25438](https://arxiv.org/abs/2605.25438) — 5,346 名开发者面板数据、活跃语言 +2.5（基线 0.9）、新语言 +1.2、集中于原本专精型开发者；作者注明结果为事件时间关联而非确定因果
- [The critical role of retrieval practice in long-term retention — Roediger & Butler, Trends in Cognitive Sciences](https://doi.org/10.1016/j.tics.2010.09.003) — 主动提取记忆对长期记忆形成的作用
- [Is Your Code Generated by ChatGPT Really Correct? Rigorous Evaluation of Large Language Models for Code Generation — arXiv:2305.01210](https://arxiv.org/abs/2305.01210) — 扩充测试集（HumanEval+）查出此前未被发现的错误 LLM 生成代码，pass@k 最多下降 19.3–28.9%
- [Foundations for Success: The Final Report of the National Mathematics Advisory Panel — U.S. Department of Education, 2008](https://files.eric.ed.gov/fulltext/ED500486.pdf) — 「计算器的使用若妨碍自动化能力的形成，将不利于计算熟练度」的警告
