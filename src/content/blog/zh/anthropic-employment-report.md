---
title: "初级新聘从 27% 跌到 9%：AI 公司自己先被 AI 改组了"
description: "Anthropic 公布自家就业数据：agent 工时今年 3 月起超过全员，初级技术新聘占比从 27% 降到 9%，会议时长反涨 20%。这两个数字是同一个机制的两面，但有些归因要打折。"
pubDate: 2026-10-17
tags: [ai-adoption, labor-market, anthropic]
lang: zh
slug: anthropic-employment-report
translationOf: anthropic-employment-report
---

10 月 16 日，Anthropic 旗下的 Anthropic Institute 发了一份报告《[How employment is changing at Anthropic](https://www.anthropic.com/research/employment-at-anthropic)》，研究对象是自己的雇主：这家公司的内部雇佣记录、Claude 使用日志、代码产出、员工日历、招聘评分卡，外加 17 场员工访谈。

两个数字放在一起最扎眼。初级技术岗在新聘员工中的占比，从 2025 年初的 27% 跌到 9%；同期，员工日历上的会议时长中位数同比涨了 20%。AI 厂商向客户讲的故事是把人从琐事里解放出来，而把工作流围绕 AI 重组得最彻底的公司，自己的员工在开更多的会。

## 先交代这是谁的数据

这是 Anthropic 研究自己、发布自己，性质和 OpenAI 八月那份 ChatGPT Enterprise 使用报告相同（[我拆过那份数据](/zh/how-organizations-use-chatgpt)）：厂商有动机把「AI 重塑工作」的叙事讲足，所有数字出自内部口径，外人无法复核。报告自己承认了两处硬伤。一是选择偏差：生产力对比用的是 192 名先用上 coding agent 的工程师和 74 名没用的，采用与否并非随机分配，先用的人可能本来就更高产。二是可推广性：全员持股、优先内部转岗这些做法「无法在整个经济中复制」。

把折扣打完，剩下的数字仍然值得看，因为这个颗粒度外部研究拿不到。2026 年 3 月，公司内 agent 的工作时长第一次超过全体员工的工作时长；到 8 月，员工指挥下的交互式 agent 工时已是员工本人的 6 倍。用上 coding agent 的工程师，人均代码提交量涨到半年前的约 5 倍。

## 入口层为什么先缩

招聘端的变化有迹可循。报告称初级技术岗的职位发布从 2025 年 12 月起急剧减少；初级员工在技术部门的存量占比从 21% 降到 14%。同时，招聘评分卡（面试官给候选人打分的记录）里提到候选人会不会用 AI 工具的比例，技术岗从 2024 年的 5% 涨到 2026 年的 15%，非技术岗从 7% 涨到 28%；对技术候选人的评语里，涨得最多的是「自主性与判断力」，领域专业知识的讨论占比在降。

机制不复杂：agent 接走的是把方案落成代码的执行层，这恰好是初级工程师的主要产出，也是他们攒经验的途径；留给人的是决定做什么、验收对不对，这又是初级员工最缺的。两头一夹，入口就窄了。

## 会议为什么变多

报告给的解释是，人的注意力成了新瓶颈。交互式会话里 agent 大约 80% 的时间在空转等人回复。一位工程师把同时带多个 agent 比作看孩子：「每个孩子都觉得自己的事最急：我的果汁盒打不开了，这是紧急事件。」于是长出一层报告称为 meta-work 的工作，内容已不是业务本身：给 agent 排任务、盯输出、搭监控面板。这类工作的占比从 2025 年秋的 10% 涨到 2026 年春的 22%。

另一半解释是，有些东西 agent 接不走。报告反复提到：跨团队的技术债需要人当面拍板，大的战略问题需要辩论，为结果负责、彼此信任只能在人与人之间生产。执行变便宜之后，剩下的稀缺品都是会议形状的。

不过这 20% 不能全记在 AI 头上。报告自己写了，销售、财务、招聘这些职能在密集扩张，增速超过技术团队，技术团队占全员比例一年内从 61% 降到 56%。组织快速变大，协调成本本来就会涨。报告把会议增长归因于 agent 带来的协调需求，却没有把「公司在膨胀」这个混杂因素从日历数据里拆出来，这部分归因读的时候要打折。

## 和外部数据对得上的部分

斯坦福团队用 ADP 工资单数据做的[「煤矿里的金丝雀」研究](https://digitaleconomy.stanford.edu/publication/canaries-in-the-coal-mine-six-facts-about-the-recent-employment-effects-of-artificial-intelligence/)发现，AI 暴露度最高的职业里，22 到 25 岁年轻人的就业在下滑，同职业的资深员工稳定（[七月我拆过这批数据](/zh/ai-jobs-data-reality-check)）。Anthropic 等于给这个宏观模式提供了一个公司内部的切片：公司总人数还在涨，缩掉的只是岗位结构里的入口层。

## 梯队问题没有答案

真正悬着的问题是：判断力从哪来。它靠亲手做执行层工作攒出来，Anthropic 自己的[随机对照试验](https://www.anthropic.com/research/AI-assistance-coding-skills)测过：把任务整个交给 AI 的初级工程师，理解测验低 17 个百分点（[我八月写过这份试验](/zh/ai-coding-and-expertise-formation)）。如今执行层给了 agent，Anthropic 的对策是按判断力招人、让老员工内部转岗，在职满一年的员工 2026 年跨部门流动的月度概率比 2025 年高 50%。但这默认市场上存在已经练出判断力的人。一家公司可以搭全行业培养梯队的便车；全行业没有便车可搭。报告把这个问题交给「前瞻性的政府政策」去做再培训和收入支持，等于承认公司层面无解。

对读者的两个实际参考。如果你的组织正在铺 agent：会议变多不是实施失败的信号，是执行成本降下来之后协调成本显性化，预算里应提前留出这块。如果你在规划自己的技能：面试评分卡的变化比任何趋势文都硬，「判断力」已经是被单独打分的考察项。

## 参考来源

- [How employment is changing at Anthropic（官方报告页）](https://www.anthropic.com/research/employment-at-anthropic) — 全部核心数据：初级新聘 27%→9%、存量 21%→14%、会议 +20%/+16%、agent 工时 6:1 与 3 月反超、commit 约 5 倍、meta-work 10%→22%、agent 空转 80%、评分卡 5%→15% 与 7%→28%、内部转岗 +50%、局限性自述与员工引语
- [报告 PDF（Wilmers, Catipon, Massenkoff, McCrory）](https://www-cdn.anthropic.com/72628f1863c53432195db83279252dfd2cb53158/Employment%20at%20Anthropic.pdf) — 作者与方法（17 场访谈、192 vs 74 工程师对比）
- [TechCrunch 报道](https://techcrunch.com/2026/10/17/anthropic-says-its-workforce-has-become-less-junior-and-is-spending-more-time-in-meetings/) — 选题来源，事实均已核对回官方报告
- [Canaries in the Coal Mine（Stanford Digital Economy Lab）](https://digitaleconomy.stanford.edu/publication/canaries-in-the-coal-mine-six-facts-about-the-recent-employment-effects-of-artificial-intelligence/) — 入口岗位下滑的外部对照
- [How AI assistance affects the formation of coding skills（Anthropic RCT）](https://www.anthropic.com/research/AI-assistance-coding-skills) — 17 个百分点理解测验差距
