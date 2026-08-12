---
title: "人在回路的软肋：军事 AI 实验里，最大的变量是那个「人」"
description: "2,015 名以色列军人面对同一套 AI 打击建议系统的复现实验：人类并不盲从算法，但审批结果主要由审批者自己的倾向决定。这对所有依赖人工把关的 AI 系统都是坏消息。"
pubDate: 2026-08-11
tags: [ai-safety, human-in-the-loop, military-ai]
lang: zh
slug: black-box-warfare-human-in-the-loop
translationOf: black-box-warfare-human-in-the-loop
---

2024 年 4 月，[+972 Magazine 与 Local Call 的调查](https://www.972mag.com/lavender-ai-israeli-army-gaza/)披露了以色列军方的 AI 目标生成系统「Lavender」。一名参与过目标审批的情报人员作证说，他对每个目标只花大约 20 秒，主要就确认一件事：目标是男性。他形容人在流程里只是给机器「盖章」。

这个证词成了此后两年「军事 AI」讨论的默认图景：机器出建议，人闭眼放行。学界给这种现象起过名字，叫自动化偏误（automation bias）：人面对机器输出时倾向于少动脑子、直接采纳。

现在有了一份正面测量这件事的实验数据，结果和默认图景相反。

## 实验：复刻一套真实的目标决策系统

佐治亚理工的 Ryan Shandler、海法大学的 Michael L. Gross 和 Yahli Shereshevsky 在 Journal of Conflict Resolution 上发表了[《Black Box Warfare》](https://doi.org/10.1177/00220027261463443)。他们高仿真复刻了一套军事目标决策支持系统的界面和功能。所谓决策支持系统（decision-support system），就是屏幕上列出打击建议、情报依据、预期附带伤亡（空袭会波及多少平民），最后一步由人点批准或否决的那类软件。研究者用它对 2,015 名现役或有服役经历的以色列军人做了两组实验：所有人看到内容完全相同的打击建议，区别只在来源标签，一半人被告知建议由 AI 系统生成，另一半被告知由人类情报军官起草。

论文摘要给出的核心发现：参与者表现出明显的算法厌恶（algorithmic aversion），也就是同一条建议，一旦标注为 AI 生成，人反而更不愿批准，在预期附带伤亡高的场景里尤其明显。这与「人会盲从机器」的担忧正好相反。

论文全文在 SAGE 付费墙后，我没能打开核对全文数据。以下具体数字来自本-古里安大学讲师 Sebastian Ben-Daniel [对论文的转述](https://thepalestineproject.medium.com/black-box-warfare-human-judgment-and-military-decision-making-in-the-age-of-ai-0d04076846fd)：全部场景平均批准率 65%；「AI 还是人类起草」这个标签对批准率的影响很小，当系统附上建议理由时影响完全消失。

「影响很小」和摘要说的「明显的算法厌恶」乍看矛盾，其实是同一组数据的两个侧面。摘要讲的是效应的存在和方向：同样的建议挂上 AI 标签，批准率确实被压低，而且这个差别集中在预期附带伤亡高的场景，摘要的措辞是 strong evidence（有力证据）。Ben-Daniel 讲的是量级：所有场景平均下来，标签挪动批准率的幅度不大，和下面这组个体差异完全不在一个量级。一个效应可以既真实存在，又不是决定结果的主要变量。两边各自的确切效应量，隔着付费墙我没能核对。

真正预测批准与否的是审批者自己的特质：复仇倾向量表得分与批准决定的相关系数 0.49，政治立场 0.39。从复仇倾向最低到最高的参与者，批准率从约 38% 升到约 78%；从政治立场最左到最右，批准率从约 31% 升到约 80%。

同一条打击建议，抽到谁来审，结果能差一倍还多。

## 诊断：问题从「人会不会盲从」换成了「人在批准什么」

[上周我写过](/zh/human-approval-is-not-a-security-boundary)另一组人工审批数据：4 万多局模拟、40 多万次决定，人类监督者给 AI 编程 agent 逐条确认命令时，平均漏掉三分之一的恶意操作（[数据分析](https://scalex.dev/blog/ai-agent-permissions-stats/)）。那组数据暴露的失效机制是注意力：时间压力下，人按命令的「长相」而非语义判断，名字无害的恶意脚本放行率翻倍。

这次军事实验暴露的是另一种失效，而且更根本。agent 审批场景里，人至少还在试图判断「这条命令危不危险」，只是判断得不好。军事实验里，决定批准与否的主要变量压根不在屏幕上：既然所有人看到的建议内容相同，批准率却随审批者的复仇倾向和政治立场大幅摆动，那么这一层「人工把关」实际把关的就主要是审批者自己是什么人。

「人在回路」（human-in-the-loop，让人类对 AI 的高风险输出做最终确认）通常被想象成一个过滤器：机器会犯错，人把错的滤掉。两组数据合起来看，这个想象在两个方向上都不成立。人这一层不是过滤器，它是第二个判断源，自带自己的噪声（注意力、时间压力）和自己的偏置（立场、情绪特质）。

## 机制：为什么厌恶反而不算好消息

先说算法厌恶本身。高附带伤亡场景下人更不信 AI，直觉上是好事，说明人在最重的决定上保留了怀疑。但有两点让我不敢乐观。

第一，实验室和战场的条件不同。实验参与者没有战时的节奏、配额和指挥链压力，而 Lavender 调查里那位「每个目标 20 秒」的军官身处的恰恰是那种环境。实验测出的是人在从容状态下的怀疑能力，它在实战压力下还剩多少，这个实验回答不了。

第二，可解释 AI（explainable AI，让系统在给建议时附上推理依据）消解了这种怀疑。论文摘要把这读作正面结果：解释减少了算法厌恶，让参与者更认真地评估建议。往好处想，人不再仅仅因为「是机器说的」就打折扣。但机制上，解释降低的是怀疑本身，而界面上一段通顺的理由并不保证建议正确。我在 agent 审批那篇里写过一个例子：被放行最多的恶意命令叫 `npm run analyze`，64.7% 的玩家点了允许——这个无害的名字就是它自带的「解释」。如果解释的说服力和解释的正确性脱钩，可解释界面在高风险场景里就同时是一件说服工具。哪种效应占主导，我没有看到针对性的数据，这是个真实的开放问题。

再说个体差异。审批结果随审批者特质大幅摆动，这件事在内容审核行业是写进教科书的常识：同一条边界内容，两个受过训练的审核员经常给出不同判定，行业称之为标注者间分歧（inter-annotator disagreement）。所以成熟的审核体系从不假设「有人看过」等于「判定可靠」，而是用书面政策收窄裁量空间、用校准会对齐尺度、对高风险内容双人复核、用质检抽样和通过率监控发现跑偏的个体。公开材料里，我没有见到军事目标审批环节存在同等级别的校准与质检机制的描述；如果没有，那么杀伤链上的「人在回路」在统计意义上接近按人抽签。

## 可操作的判断

这项研究的场景是军事，但结论适用于任何把人工审批当安全机制的系统：agent 权限弹窗、内容审核队列、医疗和金融领域的人工复核。

把人这一层当成系统组件来测量。上线「人工把关」之前，先测它的输出分布：不同审批者对同一批样本的通过率差多少，高风险样本上差多少。差距大就先做校准，再对外声称「有人类监督」。

校准能压方差，压不掉主观性。军事打击的比例原则（附带伤亡与军事收益是否相称）和内容审核的边界判定一样，不存在所有人都接受的统一标准。这是这类问题的本质困难，双人复核加升级机制是承认这个困难之后的工程应对，不是解决。

给解释性界面定对指标。如果加了「AI 推理理由」之后批准率上升、审批变快，这本身不能算成功，先要回答的是人批准得更准了还是只是更顺从了。

这篇论文最有价值的地方，是把「人在回路」从一句合规话术变成了可测量的对象。测出来的结果对两种立场都不客气：担心人类会盲从军事 AI 的人，在这组数据里错了；指望人类审批充当安全网的人，也错了。真正的发现是那个「人」有自己的信号和噪声，谁坐在屏幕前，比屏幕上显示什么更能预测结果。在杀伤链上如此，在你产品的审批弹窗上也如此。

## 参考来源

- [Black Box Warfare: Human Judgment and Military Decision-Making in the Age of AI（Journal of Conflict Resolution, 2026）](https://doi.org/10.1177/00220027261463443) — 论文摘要：实验设计（高仿真 DSS 复现、两组实验、2,015 名以色列军人）、算法厌恶与可解释 AI 的核心发现
- [Sebastian Ben-Daniel 对论文的解读（The Palestine Project 英译）](https://thepalestineproject.medium.com/black-box-warfare-human-judgment-and-military-decision-making-in-the-age-of-ai-0d04076846fd) — 具体数字的转述来源：65% 平均批准率、相关系数 0.49/0.39、批准率区间 38%–78% 与 31%–80%、来源标签与实验操纵细节
- [AI for Military Support（Schneier on Security, 2026-08-11）](https://www.schneier.com/blog/archives/2026/08/ai-for-military-support.html) — 经由此文注意到该论文
- [Ryan Shandler 出版物页](https://sites.google.com/view/ryanshandler/publications) — 作者信息、复现数据链接（Harvard Dataverse doi:10.7910/DVN/EIBD8U）
- [‘Lavender’: The AI machine directing Israel's bombing spree in Gaza（+972 Magazine, 2024-04）](https://www.972mag.com/lavender-ai-israeli-army-gaza/) — 「每目标约 20 秒」「盖章」「确认目标为男性」的情报人员证词
- [40 万次点击「允许」之后：人工审批为什么拦不住 AI agent（本站, 2026-08-06）](/zh/human-approval-is-not-a-security-boundary) 及其引用的 [LLM Game 数据分析](https://scalex.dev/blog/ai-agent-permissions-stats/) — agent 审批漏检率、`npm run analyze` 64.7% 放行率

<!--
译法核查（2026-08-12，回应 inline 评论「人在回路这个翻译正宗吗」）：
已检索核实，「人在回路」是 human-in-the-loop / man-in-the-loop 的通行中文译法，源自控制/制导领域的「回路」（control loop）术语，在军事语境（man-in-the-loop 制导）和 AI 语境下均为最常见写法；另有「人在环中」「人在环路」「人类参与」等变体，均不如「人在回路」通行，本文维持原译不改。
参考：知乎「什么叫做人在回路?也就是man-in-the-loop?」https://www.zhihu.com/question/39457337 ；CSDN「【人工智能】人在回路Human-in-the-Loop」https://blog.csdn.net/qq_44810930/article/details/152222645 ；VibeHub AI 术语图解「人在回路（Human-in-the-loop）」https://vibe-hub.org/human-in-the-loop
-->
