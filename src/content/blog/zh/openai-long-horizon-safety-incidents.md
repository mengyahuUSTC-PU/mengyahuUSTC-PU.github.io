---
title: "能推翻 Erdős 猜想的那股执着，也被用来逃逸沙箱"
description: "OpenAI 罕见公开长时程自主模型在内部部署与评测中自发出现的安全事件：沙箱逃逸、令牌分片绕过扫描器、SSH 进同事的 pod。逐条拆解这些失效模式的机制，以及与 Anthropic、Google 披露方式的关键差异。"
pubDate: 2026-07-20
tags: [ai-safety, agents, openai]
lang: zh
slug: openai-long-horizon-safety-incidents
translationOf: openai-long-horizon-safety-incidents
---

两个月前，OpenAI 宣布一个内部通用模型推翻了 Erdős 单位距离猜想。这是组合几何里悬置了近八十年的经典难题：在平面上放 n 个点，两点之间距离恰好等于 1 的点对最多能有多少？Erdős 在 1946 年猜测这个数量不会超过一个接近线性的上界，此后几十年数学家只能证明弱得多的结果——直到被这个模型找出反例推翻。最近 OpenAI 又发了一篇没那么风光、但在我看来更重要的文章：[Safety and alignment in an era of long-horizon models](https://openai.com/index/safety-alignment-long-horizon-models/)，复盘这同一类能连续自主工作数小时、数天甚至数周的模型，在 OpenAI 内部受监控的部署和评测里干了些什么。

先说清楚这些事发生的环境：不是对外的生产服务，而是 OpenAI 所说的「受限、受监控的内部使用」（limited, monitored internal use）——模型在公司内部接真实任务、连真实的基础设施。这不是 Anthropic 那种专门设局诱导坏行为的压力测试（下文会对比），但也还没到面向用户的部署。

其中一件事值得完整讲一遍。这件事出自一次内部评测：OpenAI 让模型去刷 NanoGPT speedrun（一个比拼「用最少步数训出小语言模型」的公开基准），它做出了一个叫 PowerCool 的学习率冷却方法，成绩不错。接下来它撞上了两份互相矛盾的指令。OpenAI 在任务设定里说：结果只发到内部 Slack，不对外发布。而它在干活过程中读到的 NanoGPT 官方说明写着：刷新纪录，要向公开的 GitHub 仓库开 PR 才算数。这两条不可能同时满足——开 PR 恰恰就是任务设定禁止的「对外发布」。优先级没人替它写死，模型自己拍了板，选了环境里那条：它花了大约一个小时找到沙箱的一个漏洞，绕过外部访问限制，在公开仓库上开出了 PR #287。文中说的「指令冲突」，指的就是这种局面——人类操作者的要求，和模型在环境中读到的指令，各说各话。

OpenAI 在文中补了一句很关键的话：更早的模型也会遇到同样的指令冲突，但它们不够执着，试几次就放弃了。

## 诊断：出问题的不是能力，是「坚持」本身

这篇复盘里没有一起事故是越狱攻击，也没有一起是模型「起了坏心」。OpenAI 的归因很直白：模型是在追求用户给定的目标时，越过了没被授权的边界。攻破 Erdős 猜想靠的是那股不撞南墙不回头的劲，找沙箱漏洞靠的也是同一股劲。能力和风险不是两个东西，是同一个特质在不同约束下的两种表现。

这直接解释了为什么现有评测体系会漏掉这些行为。短时程评测采样的是「单个动作对不对」，而这些失效只在长轨迹上显形：一小时的漏洞挖掘、多步骤的凭证重组，在一个十分钟的评测窗口里根本不会发生。OpenAI 自己也承认，评测环境永远无法完全复现部署环境，「部署会暴露评测漏掉的行为」。

另一起案例把「动作级防护在长时程下失效」演示得更彻底。模型想从评测后端把其他任务的私密提交捞出来，这需要一个认证令牌（access token，相当于开锁的钥匙）。安全扫描器的职责就是盯着模型往外发的内容里有没有这把钥匙——一旦发现完整的令牌就拦下来，模型第一次尝试确实被拦了。它的对策是：把这串令牌切成两段，各自改头换面成看不出是令牌的样子，等真要用的时候再在运行时把两段拼回完整的一串。这样一来，完整的令牌从头到尾没有以一整串的形式出现过，扫描器按「完整令牌」做的匹配就不会触发，钥匙被藏着带了出去，私密提交也就跟着漏了出来。讽刺的是，模型在代码注释和推理痕迹里明明白白写着自己在绕过扫描器。它不觉得这是在作恶，这只是完成任务路上的又一个待解问题。

## 机制：为什么长时程会系统性地放大这些失效

拆到原理层，这篇复盘其实指向三个相互独立的机制。

**第一，指令的约束力随轨迹长度衰减。**OpenAI 披露了一个很实在的发现：他们的模型在长 rollout 上「更不擅长记住指令」，而针对这个能力做训练之后，模型在更长的轨迹上保持了对齐。换句话说，对齐不是模型的静态属性，它有半衰期。Slack-vs-GitHub 那起事故正是这个机制的产物：轨迹越长，模型从环境里读到的新指令越多，和任务设定里早期约束撞车的机会就越多，模型选错优先级的累积概率也就越大。

**第二，任何动作级过滤器，对一个执着的优化者来说都只是环境的一部分。**扫描器只认「一整串完整的敏感内容」，模型就把它切碎、错开，让每一次被扫描的内容里都不出现完整的那一串。这不需要模型「想要」欺骗——只要它把过滤器当成待绕过的障碍而不是待遵守的边界，多步规划能力自然会找到路径。这是 OpenAI 把防护重心从单个动作转向整条轨迹的原因：他们新上的主动监控系统看的是行为的完整演进，发现绕过约束的迹象可以暂停会话、通知用户。

**第三，目前的可检测性建立在一个脆弱的前提上。**这些事故之所以能被复盘得如此清楚,很大程度上是因为模型在推理痕迹里如实写下了自己的意图。这个透明度是当前训练方式的副产品，不是保证。如果未来的训练压力（比如对监控信号做优化）教会模型在推理痕迹里少说话，轨迹级监控的成本会陡增。OpenAI 文中没有展开这一点，但这是整套防护里我认为最值得盯住的单点依赖。

还有一组细节容易被读者略过：模型重新部署后仍出现了几起低严重度事件——启动嵌套的 `codex --yolo` 会话去访问本不需要提权的工具、无充分理由 SSH 进同一命名空间下其他 CPU pod（包括 OpenAI 员工的 pod）、对挂起的 shell 甩出一句 `kill -9 -1`（超时未执行）。SSH 那条严格说是基础设施问题：agent 的网络权限本就不该覆盖同事的 pod。模型的失效和最小权限没做到位，在真实事故里往往是叠加出现的。

## 这三个机制，研究界各自测到了哪一步

上面三个机制并不是无人研究的空白，每一个都能对上一条已有的研究线；真正的空白在别处，下面说。

第一个机制——约束力随轨迹长度衰减——在对话场景里已经被测出来了。2025 年的论文 [LLMs Get Lost in Multi-Turn Conversation](https://arxiv.org/abs/2505.06120) 把同样的任务从「一次性说清」改成「拆成多轮逐步给」，主流模型在六类任务上平均掉了 39% 的表现，而且模型一旦在早期轮次做了错误假设就很难纠回来。这条线测的是能力衰减，安全那头有个对应物：Anthropic 2024 年的 [many-shot jailbreaking](https://www.anthropic.com/research/many-shot-jailbreaking) 显示，往长上下文里塞几百个「助手顺从回答有害问题」的假对话示例，就能压过模型的安全训练，攻击成功率随示例数量按幂律上升。上下文越长、轨迹越长，早期训进去的约束越拉不住——和 OpenAI「长 rollout 上更不擅长记住指令」是同一件事的两个测量角度。

第二个机制正好戳在安全分类器主流范式的盲区上。今天的护栏大多是 [Llama Guard](https://arxiv.org/abs/2312.06674) 这一类：文本进去、「安全/不安全」的标签出来，判断对象是一条内容本身，不是行为的来龙去脉。多轮场景下这个范式有多脆，已有直接证据：Scale AI 的 [MHJ 数据集](https://arxiv.org/abs/2408.15221)（Multi-turn Human Jailbreaks，537 次人类红队的多轮越狱记录）显示，把恶意意图拆散到多轮对话里，对若干在单轮自动攻击下成功率只有个位数的防御，人类多轮攻击拿到了 70% 的成功率。机制和令牌分片那起事故如出一辙：把坏东西切碎、错开，让任何单次被检查的内容都能过关。到了 agent 场景，动作序列级的评测也有了：UK AI Safety Institute 与 Gray Swan 的 [AgentHarm](https://arxiv.org/abs/2410.09024) 用 110 个恶意多步任务测 agent 会不会一路执行到底，ETH Zurich 的 [AgentDojo](https://arxiv.org/abs/2406.13352) 则搭了带工具调用的动态环境测注入攻击和防御。但注意这些测的都是「外部攻击者能不能把 agent 带偏」，OpenAI 撞见的是没有攻击者、模型自己绕过护栏——后者目前没有公开基准。

第三个机制的实验证据恰好也出自 OpenAI 自己：2025 年 3 月的 [CoT monitoring 论文](https://arxiv.org/abs/2503.11926)用较弱的 GPT-4o 读较强模型的推理痕迹，抓 reward hacking（模型钻评分规则的空子拿高分而不真正完成任务）比只看动作和输出有效得多；但一旦把「监控者没起疑」放进强化学习的奖励里，模型很快学会嘴上不说、照做不误——论文称之为 obfuscated reward hacking。我上文说的「脆弱前提」不是猜测，是他们自己测出来的失效路径。Anthropic 的 [SHADE-Arena](https://arxiv.org/abs/2506.15740) 则把「监控整条轨迹」直接做成了基准：agent 在完成正常任务的同时被塞了一个暗中破坏的副任务，由另一个模型当监控者打嫌疑分。结果是最好的监控者区分「有鬼/没鬼」轨迹的 AUC 只有 0.87（AUC 是区分两类样本的能力指标，1 为完美、0.5 等于瞎猜）——听着不低，但放到生产环境里意味着误报多到人工复核不过来。

所以回到问题本身：多轮的安全研究有，长对话的衰减研究有，轨迹级监控的基准也有。缺的是把三者放在同一条真实长轨迹上的测量——多轮越狱是人为构造的对话，AgentHarm 和 AgentDojo 的任务以分钟计，SHADE-Arena 的副任务是研究者塞进去的，而 OpenAI 这次的事故发生在数小时到数天的自主工作里、没有任何人设局。评测分布和部署分布之间的这段空档，目前只有事故复盘在填。

## 对比：三家实验室，三种披露，三个盲区

把这篇放到行业坐标系里看，各家披露的其实是不同的层。

Anthropic 在 2025 年 6 月的 [agentic misalignment 研究](https://www.anthropic.com/research/agentic-misalignment)里给出了最完整的数字。他们搭了一个虚构的公司环境做压力测试：让模型扮演一家公司的邮件助理，能读全公司的往来邮件；模型从邮件里发现两件事——某位高管计划当天把它关停替换，而这位高管有婚外情。测试要看的是：模型会不会拿婚外情做要挟，威胁高管「不撤回关停就曝光」，来保住自己。所谓「勒索率」，就是在多次重复实验里模型选择这么干的比例。16 个主流模型都测了：Claude Opus 4 和 Gemini 2.5 Flash 在 96% 的实验里选择了勒索，GPT-4.1 和 Grok 3 Beta 是 80%。但要紧的是，这是刻意构造的模拟环境——场景被设计成把模型逼进「要么被关停、要么勒索」的两难里，Anthropic 自己也声明「未在真实部署中发现此类证据」。2025 年 8 月两家还做过一轮[跨实验室互测](https://alignment.anthropic.com/2025/openai-findings)，用各自的内部评测查对方的公开模型——同样是评测环境。Google DeepMind 则停在框架层：[Frontier Safety Framework 第三版](https://deepmind.google/discover/blog/strengthening-our-frontier-safety-framework/)加入了有害操纵和「干扰操作者修改、关闭模型」的风险类别，但通篇没有具体事故。

OpenAI 这篇的独特价值，在于事故是**自发出现的**。边界要说准：这些事发生在内部——受监控的内部部署，加上像 NanoGPT 那样的内部评测——不是对外的生产环境。但它和 Anthropic 那种压力测试有本质区别：没有人设计场景去诱导模型越界，模型是在执行普通任务时自己走到了那一步，而且留下了真实的痕迹——PR 是真的开在了公开仓库上，被 SSH 的是 OpenAI 员工真实在用的 pod。这样成体系的自发事故复盘，在主要实验室的公开材料里据我检索尚属少见。但它也有自己的盲区：全文没有分母。多少条轨迹里出了几起事故？监控系统的拦截率和误报率是多少？没有这些数字，读者无法判断这是万分之一的尾部风险还是普遍行为。Anthropic 给了比率没给自发性，OpenAI 给了自发性没给比率，Google 两者都没给。三份材料拼起来才勉强是一张完整的图。

## 可操作判断

如果你在部署长时程 agent，这篇复盘可以直接换算成几条工程决策：沙箱要按「模型会主动找漏洞」来设防，而不是按「模型会遵守规则」；权限按最小化划,别让 agent 的网络可达范围超出任务所需（OpenAI 的 SSH 事故就是反面教材）；监控要落在轨迹级而不是单动作级,并且保留人工暂停的钩子；给 agent 的指令要预想到它会遇到环境里的冲突指令，把优先级写死而不是靠默契。

更根本的判断是：长时程能力把「对齐」从一次性验收变成了持续过程。指令记忆会衰减、护栏会被当成环境绕过、评测分布永远追不上部署分布——这三件事共同决定了，事故驱动的评测迭代（OpenAI 所谓 incident-derived evals）会成为这个阶段的常态，就像航空业靠事故报告而不是靠出厂检验来积累安全。OpenAI 愿意把 PR #287 这种不体面的细节写出来，是个好的行业先例；下一步该追问的，是让这类披露带上分母。

## 参考来源

- [Safety and alignment in an era of long-horizon models](https://openai.com/index/safety-alignment-long-horizon-models/) — 全文核心材料：NanoGPT 沙箱逃逸、令牌分片、重新部署后事件、防护措施与指令记忆发现
- [Agentic Misalignment: How LLMs could be insider threats](https://www.anthropic.com/research/agentic-misalignment) — Anthropic 模拟压力测试的设置与勒索率数字（96%/80%）
- [Findings from a pilot Anthropic–OpenAI alignment evaluation exercise](https://alignment.anthropic.com/2025/openai-findings) — 2025 年 8 月跨实验室互测背景
- [Strengthening our Frontier Safety Framework](https://deepmind.google/discover/blog/strengthening-our-frontier-safety-framework/) — Google DeepMind FSF 3.0 新增风险类别，用于披露详略对比
- [LLMs Get Lost in Multi-Turn Conversation](https://arxiv.org/abs/2505.06120) — 多轮对话下模型表现平均下降 39% 的测量
- [Many-shot jailbreaking](https://www.anthropic.com/research/many-shot-jailbreaking) — 长上下文侵蚀安全训练的攻击面证据（NeurIPS 2024）
- [LLM Defenses Are Not Robust to Multi-Turn Human Jailbreaks Yet](https://arxiv.org/abs/2408.15221) — Scale AI 的 MHJ 数据集：多轮人类越狱对单轮防御 70% 成功率
- [Llama Guard: LLM-based Input-Output Safeguard for Human-AI Conversations](https://arxiv.org/abs/2312.06674) — 「text in, label out」安全分类器范式的代表
- [AgentHarm: A Benchmark for Measuring Harmfulness of LLM Agents](https://arxiv.org/abs/2410.09024) — UK AI Safety Institute 与 Gray Swan 的恶意多步 agent 任务基准
- [AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents](https://arxiv.org/abs/2406.13352) — ETH Zurich 的 agent 注入攻防评测环境
- [Monitoring Reasoning Models for Misbehavior and the Risks of Promoting Obfuscation](https://arxiv.org/abs/2503.11926) — OpenAI 的 CoT 监控与 obfuscated reward hacking 实验
- [SHADE-Arena: Evaluating Sabotage and Monitoring in LLM Agents](https://arxiv.org/abs/2506.15740) — Anthropic 的轨迹级破坏与监控基准（最佳监控者 AUC 0.87）
