---
title: "被 AI 抽掉的不是中层，是通往中层的梯子"
description: "「AI 正在消灭中层工程师」在 HN 上吵了六百多条评论。我翻了 Stanford、Indeed 和 levels.fyi 的一手数据：现有中层没被裁也没降薪，塌掉的是入口。而入口塌方，才是五年后真正的中层危机。"
pubDate: 2026-08-12
tags: [software-engineering, labor-market, ai-impact]
lang: zh
slug: ai-middle-class-software-engineering-data-check
translationOf: ai-middle-class-software-engineering-data-check
---

设想这样一个场景：周末过去，同事用 AI 生成了一个 24,506 行的 PR。评审时你问「这里为什么要这么设计」，得到的回答是一个 Claude 对话链接。

伦敦工程师 Florian Herrengt 用这个虚构场景开头，写了篇博客[《AI is removing the middle class of software engineering》](https://blog.florianherrengt.com/ai-removing-middle-class-software-engineering.html)。论点很干脆：实现已经不值钱，公司付你工资是要你做对决策；顶尖工程师会更贵，平庸工程师会更便宜或者出局，中间地带正在消失。他管这个中间地带叫软件工程的「中产阶层」。

这篇文章这两天冲上 [Hacker News 榜首](https://news.ycombinator.com/item?id=49271994)，截至写稿时 715 个赞、645 条评论。评论区一半在讲自己团队的 AI 烂代码事故（有人说以前烂工程师在被发现之前产不出多少东西，现在「我喝上第一杯咖啡之前，他能产出一万行垃圾」），另一半在争论自己算不算「中层」。

会吵成这样，因为它戳的是饭碗。但「中层正在被消灭」是个可以拿数据检验的断言，而原文没有引用任何劳动力市场数据。我把能找到的一手数据翻了一遍：就业量、职位发布量、薪资分布。结论先说：数据不支持「中层被消灭」，它指向另一件更慢、也可能更麻烦的事。

## 先拆成能检验的断言

博文其实包了三个断言：一，中层工程师的岗位正在收缩；二，薪资分布正在两极拉开；三，工程师的价值正从实现转向判断。第三条是判断题，前两条是数据题。

## 就业数据：收缩全部堆在入口

Stanford 数字经济实验室的 Brynjolfsson 等人有一项持续更新的研究[《Canaries in the Coal Mine?》](https://digitaleconomy.stanford.edu/publication/canaries-in-the-coal-mine-six-facts-about-the-recent-employment-effects-of-artificial-intelligence/)，用 ADP 的数据追踪 AI 对就业的影响。ADP 是美国最大的薪资代发服务商，数据直接来自数百万在职员工的工资单，比任何问卷调查都硬。数据更新到 2026 年 6 月，核心发现是：在 AI 暴露度最高的职业里，22–25 岁员工的就业量，比照同龄人在低暴露职业的走势推算，低了 19%；而有经验的员工没有出现类似下滑。

研究团队的[数据面板](https://digitaleconomy.stanford.edu/project/indicators/canaries-dashboard/)把软件开发者单独拆出来看，形状更清楚：22–25 岁大幅下滑，再往上一档的年龄组小幅下滑，更年长的各组反而还在扩张。

两个机制性细节值得单独说。第一，缺口来自招聘减少，离职和裁员并没有上升；第二，市场的调整发生在就业量上，底薪没动。

拿这个对照博文的断言：如果 AI 在消灭现有中层，工资单数据里应该看到三十多岁员工被裁、就业收缩。没有。收缩全部集中在入口。

## 职位数据：岗位在回来，但门槛上移了一级

[Indeed Hiring Lab 2026 年 7 月的报告](https://hiringlab.indeed.com/2026/07/08/ai-and-job-postings-from-destruction-to-creation/)给出职位发布端的图景。美国软件开发职位总量仍比疫情前（2020 年 2 月）低约 27.5%。2022 到 2026 年，AI 暴露度越高的职业，职位跌得越狠。但 2025 年起这个关系反转了：AI 暴露职业开始领跑反弹。自 Claude Code 在 2025 年 2 月底发布以来，美国软件开发职位涨了近 15%，同期全部职位跌了 7%。

反弹的构成才是重点。2025 年 5 月到 2026 年 5 月，软件开发职位的增量里 71% 是 senior 岗，37% 的职位名称里直接带 AI。

岗位在回来。只是回来的岗位，默认你已经爬完了那段没人再让你爬的梯子。

## 薪资数据：找不到「平庸折价」

[levels.fyi 的 2025 年度报告](https://www.levels.fyi/2025/)（工程师自报薪酬的数据站，硅谷跳槽定薪的常用基准）：美国软件工程师总薪酬中位数整体涨 2.67%。分职级看，入门级 15.5 万美元，senior 31.2 万（+4.2%），staff 45.7 万（+7.52%），principal 55.1 万（反而 -6.58%）。

如果「平庸工程师变得更便宜」已经发生，中位数应该被压下去。没有。能看到的是层级间的增速差，加上 AI 方向的溢价，中间没有塌陷。这和 Stanford 那条「调整走就业量、不走薪资」互相印证。

自报数据有幸存者偏差：失业的人不会来报薪资。所以它只能证明「有工作的中层没降价」，证明不了「中层都保住了工作」。但博文预言的是前者，而前者没有发生。

## 一个我没能验证的口径问题

博文说的「中层」是技能意义上的：够格但不出彩。而以上数据只能按年龄和职级切分。「平庸的 senior 是否正在被折价淘汰」，公开数据回答不了，这一点我没能验证。评论区里关于 0.1x 和 10x 工程师的争论，本质上也是在这个数据照不到的地方吵。

还有一层必须交代：27.5% 的职位缺口不能全记在 AI 头上。同期发生了三件事：加息终结了零利率时代的扩张；疫情期间过度招聘的回调；还有美国 2022 年生效的 Section 174 税改，把研发人员工资从当年全额抵税改成分五年摊销，凭空推高了雇工程师的账面成本（2025 年年中已恢复即时抵扣）。Stanford 研究的巧妙之处是控制了公司层面的冲击：同一家公司、同一职业内部，年轻员工和年长员工的走势分化。利率和税法不会只打击 22–25 岁的程序员，这个分化很难用宏观因素解释掉。

## 机制：断供，而非删除

把三组数据拼起来，故事和博文讲的版本不一样。

AI 最先吃掉的是「便宜的实现劳动力」这个角色，而这正是初级工程师的传统入场券。公司对存量员工按兵不动，对增量关门，新开的岗位转向能独立对决策负责的人。到这一步，数据和博文的方向一致：市场确实在为判断力付钱。

但 senior 不是招聘市场上凭空长出来的。中层和 senior 是 junior 在生产系统里犯错、被 review、被救火喂出来的。入口塌方的后果有五到十年的延迟：今天不生产 junior，五年后市场上就没有新的中层供给。到那时，现有中层大概率更贵，因为没人接班。博文预言的两极分化可能成真，但路径是断供，而非对存量的删除。

类似的断档别的行业出过。美国核工业停建新堆几十年，等到重启新项目时，反复被提到的瓶颈是有建设经验的中生代工程师已经老去，断掉的那代人补不回来。软件行业的新变量在于：以前不招学徒，公司立刻会疼，活没人干；AI 第一次让「不招 junior」在短期内看起来零成本，活照样有人干，只是干活的从新人换成了 agent。于是每家公司单独算账都是理性的，加总起来是全行业在吃自己的种子粮。

## 我的判断

如果你已经在中层：短期内你的岗位和薪资在数据上都看不到危险，真正变了的是标准。71% 的新增职位要 senior，意味着招聘方买的是判断力。原文那句「implementation is cheap, you are paid to make good decisions」，当作职业策略成立；当作对已发生现实的描述，超前了。往「能对架构和取舍负责」的方向挪，比焦虑「会不会被替代」有用。

如果你在管招聘：「只要 senior」每家公司单独看都划算，但你在消费一个没人续费的公共池。什么时候疼，取决于你打算在这个行业待几年。

博文担心的两极分化，数据说还没来。但梯子的第一级已经在塌。等塌到中层那一格，市场会用短缺、而非降薪的方式，让所有人知道这件事发生过。

## 参考来源

- [AI is removing the middle class of software engineering](https://blog.florianherrengt.com/ai-removing-middle-class-software-engineering.html) — 原文论点、24,506 行 PR 的虚构场景、「implementation is cheap」引文
- [Hacker News 讨论串](https://news.ycombinator.com/item?id=49271994) — 赞数与评论数（经 HN API 核实）、评论区反方观点
- [Canaries in the Coal Mine? — Stanford Digital Economy Lab](https://digitaleconomy.stanford.edu/publication/canaries-in-the-coal-mine-six-facts-about-the-recent-employment-effects-of-artificial-intelligence/) — 22–25 岁就业缺口 19%、招聘/离职机制、调整走就业量不走薪资、数据截至 2026 年 6 月
- [Canaries Dashboard — Stanford Digital Economy Lab](https://digitaleconomy.stanford.edu/project/indicators/canaries-dashboard/) — 软件开发者分年龄组走势（22–25 大降、次年轻组小降、更年长组扩张）
- [AI and Job Postings: From Destruction to Creation? — Indeed Hiring Lab](https://hiringlab.indeed.com/2026/07/08/ai-and-job-postings-from-destruction-to-creation/) — 职位量比疫情前低 27.5%、Claude Code 发布后 +15% vs 整体 -7%、增量 71% 为 senior 岗、37% 带 AI 头衔
- [Levels.fyi 2025 End of Year Pay Report](https://www.levels.fyi/2025/) — 各职级薪酬中位数与同比变化
