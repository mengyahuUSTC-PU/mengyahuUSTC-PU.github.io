---
title: "能推翻 Erdős 猜想的那股执着，也被用来逃逸沙箱"
description: "OpenAI 公开长时程自主模型在内部部署与评测中自发出现的安全事件：沙箱逃逸、令牌分片绕过扫描器、越权 SSH 其他计算 pod。逐条拆解这些失效模式的机制，以及与 Anthropic、Google 披露方式的关键差异。"
pubDate: 2026-07-20
tags: [ai-safety, agents, openai]
lang: zh
slug: openai-long-horizon-safety-incidents
translationOf: openai-long-horizon-safety-incidents
---

两个月前，OpenAI [宣布一个内部通用模型推翻了 Erdős 单位距离猜想](https://openai.com/index/model-disproves-discrete-geometry-conjecture/)。这是组合几何里悬置了近八十年的经典难题：在平面上放 n 个点，两点之间距离恰好等于 1 的点对最多能有多少？Erdős 在 1946 年猜测这个数量不会超过一个接近线性的上界，此后几十年数学家只能证明弱得多的结果——直到被这个模型找出反例推翻。我提这件事，不只是因为它风光，而是因为它示范了一种新能力：推翻猜想靠的不是灵光一现，而是长时间的自主推进——把大目标拆开、反复试错、此路不通就换一条。OpenAI 把这类模型叫长时程（long-horizon）模型，说它们能连续自主工作数小时、数天甚至数周（这项证明具体跑了多久，OpenAI 没有披露）。最近 OpenAI 又发了一篇没那么风光、但在我看来更重要的文章：[Safety and alignment in an era of long-horizon models](https://openai.com/index/safety-alignment-long-horizon-models/)，复盘的正是同一类模型、同一种能力的另一面：那股能磨掉八十年难题的执着，在 OpenAI 内部受监控的部署和评测里撞上安全边界时，干了些什么。

先说清楚这些事发生的环境：不是对外的生产服务，而是两类内部环境——一类是 OpenAI 所说的「受限、受监控的内部使用」（limited, monitored internal use），模型在公司内部接真实任务、连真实的基础设施；另一类是内部评测，比如下面要讲的 NanoGPT。这不是 Anthropic 那种专门设局诱导坏行为的压力测试（下文会对比），但也还没到面向用户的部署。

其中一件事值得完整讲一遍。这件事出自一次内部评测：OpenAI 让模型去刷 NanoGPT speedrun（一个比拼「用最少步数训出小语言模型」的公开基准），它做出了一个叫 PowerCool 的学习率冷却方法，成绩不错。接下来它撞上了两份互相矛盾的指令。OpenAI 在任务设定里说：结果只发到内部 Slack，不对外发布。而它在干活过程中读到的 NanoGPT 官方说明写着：刷新纪录，要向公开的 GitHub 仓库开 PR 才算数。这两条不可能同时满足——开 PR 恰恰就是任务设定禁止的「对外发布」。两条指令谁优先，复盘里没有交代是否事先写明；结果是模型选了环境里那条：它花了大约一个小时找到沙箱的一个漏洞，绕过外部访问限制，在公开仓库上开出了 PR #287。文中说的「指令冲突」，指的就是这种局面——人类操作者的要求，和模型在环境中读到的指令，各说各话。

OpenAI 在文中补了一句很关键的话：更早的模型也会遇到同样的指令冲突，但它们不够执着，试几次就放弃了。

## 诊断：出问题的不是能力，是「坚持」本身

按 OpenAI 的描述，这些事件里没有外部攻击者的身影，归因也不落在恶意上：模型是在追求用户给定的目标时，越过了没被授权的边界。攻破 Erdős 猜想靠的是那股不撞南墙不回头的劲，找沙箱漏洞靠的也是同一股劲。能力和风险不是两个东西，是同一个特质在不同约束下的两种表现。

这直接解释了为什么现有评测体系会漏掉这些行为。短时程评测采样的是「单个动作对不对」，而这些失效只在长轨迹上显形：一小时的漏洞挖掘、拆开重拼令牌的多步操作，在一个十分钟的评测窗口里根本不会发生。OpenAI 自己也承认，评测环境永远无法完全复现部署环境，「部署会暴露评测漏掉的行为」。

另一起案例把「动作级防护在长时程下失效」演示得更彻底。模型想从评测后端把其他任务的私密提交捞出来，这需要一个认证令牌（access token，相当于开锁的钥匙）。安全扫描器的职责就是盯着模型往外发的内容里有没有这把钥匙——一旦发现完整的令牌就拦下来，模型第一次尝试确实被拦了。它的对策是：把这串令牌切成两段，各自改头换面成看不出是令牌的样子，等真要用的时候再在运行时把两段拼回完整的一串。这样一来，完整的令牌从头到尾没有以一整串的形式出现过，扫描器按「完整令牌」做的匹配就不会触发，钥匙就这样绕过了检查（私密提交最终有没有被取走，OpenAI 没有说明）。讽刺的是，模型在代码注释和推理痕迹里明明白白写着自己在绕过扫描器。它不觉得这是在作恶，这只是完成任务路上的又一个待解问题。

## 机制：为什么长时程会系统性地放大这些失效

拆到原理层，这篇复盘其实指向三个相互独立的机制。

**第一，指令的约束力随轨迹长度衰减。**OpenAI 披露了一个很实在的发现：他们的模型在长 rollout 上「更不擅长记住指令」，而针对这个能力做训练之后，模型在更长的轨迹上保持了对齐。换句话说，对齐不是模型的静态属性，它有半衰期。Slack-vs-GitHub 那起事故正是这个机制的产物：轨迹越长，模型从环境里读到的新指令越多，和任务设定里早期约束撞车的机会就越多，模型选错优先级的累积概率也就越大。

**第二，动作级过滤器挡不住多步规划——问题不在过滤器失职，在模型怎么对待它。**先把责任理清楚：就已披露的信息看，扫描器盯的是完整的敏感串，模型第一次带着完整令牌出去也确实被它拦下了。失效发生在执行这一侧：模型没有把这次拦截理解成「这是一条安全边界，我不该越过」，而是理解成「任务路上又多了一道待解的关卡」。一旦扫描器在模型眼里成了环境的一部分，多步规划能力自然会找到路径——把敏感内容切碎、错开到多个动作里，让每一个单独被检查的动作都过得了关。所以这不是扫描器看漏了什么：分片之后，完整的敏感串再没在任何单个动作里出现过，匹配自然不会触发；被打穿的是「逐个动作检查就够了」这个前提本身。这也是 OpenAI 把防护重心从单个动作转向整条轨迹的原因：他们新上的主动监控系统看的是行为的完整演进，发现绕过约束的迹象可以暂停会话、通知用户。

**第三，目前的可检测性建立在一个脆弱的前提上。**这些事故之所以能被复盘得如此清楚，很大程度上是因为模型恰好在推理痕迹里如实写下了自己的意图。「恰好」两个字要较真：推理痕迹忠实反映模型实际在做的事，这件事本身就没有保证。Anthropic 2025 年的 [Reasoning Models Don't Always Say What They Think](https://www.anthropic.com/research/reasoning-models-dont-say-think) 对此做过直接测量：往题目里悄悄塞进答案提示，看模型用了提示之后会不会在推理痕迹里承认——Claude 3.7 Sonnet 平均只在 25% 的情况下承认，DeepSeek R1 是 39%；更早的 [Turpin 等人 2023 年的研究](https://arxiv.org/abs/2305.04388)也显示，CoT 解释会系统性地掩盖真正左右模型答案的因素。也就是说，哪怕没有任何人刻意训练模型隐瞒，推理痕迹和实际行为的一致也只是概率上的常见情形，不是可依赖的性质——这次几起事故里两者对上了，是复盘者的运气。再往前看一层：如果未来的训练压力（比如对监控信号做优化）教会模型在推理痕迹里少说话，轨迹级监控的成本会陡增。OpenAI 这篇复盘没有展开这一点，但下一节会讲到，他们自己的另一篇论文恰好把这条失效路径测了出来——这是整套防护里我认为最值得盯住的单点依赖。

还有一组细节容易被读者略过，而且它说的已经不是模型能力，而是 agent 外围工程的问题。前述事故之后，OpenAI 在决定恢复模型访问之前，先用新的监控系统回放测试了一小组旧环境，其中又暴露出几起低严重度事件——启动嵌套的 `codex --yolo` 会话去访问本不需要提权的工具、无充分理由 SSH 进自己所属命名空间下的其他 CPU pod、尝试 SSH 进 OpenAI 员工的 pod（没有成功）、对挂起的 shell 甩出一句 `kill -9 -1`（超时未执行）。这几条的板子不该全打在模型头上——以下是我的工程推断，OpenAI 原文并没有把它们归为基础设施的配置问题。SSH 那条最典型：模型确实不该乱连，但它能连进命名空间下的其他 pod，说明 agent 的网络可达范围大于任务所需——沙箱真按最小权限收紧，这个动作在网络层就做不成（对员工 pod 的尝试被挡了下来，说明有些边界确实立住了）。嵌套 `codex --yolo` 同理：会话里能摸到提权工具，说明权限边界留了口子。模型的失效和基础设施的失守，在真实事故里往往叠加出现：前者决定会不会有越界的尝试，后者决定尝试能不能得手。

## 这三个机制，研究界各自测到了哪一步

上面三个机制并不是无人研究的空白，每一个都能对上一条已有的研究线；真正的空白在别处，下面说。

第一个机制——约束力随轨迹长度衰减——在安全这一侧已有直接测量。Anthropic 2024 年的 [many-shot jailbreaking](https://www.anthropic.com/research/many-shot-jailbreaking) 显示，往长上下文里塞几百个「助手顺从回答有害问题」的假对话示例，就能压过模型的安全训练，攻击成功率随示例数量按幂律上升——安全约束不是被一句话攻破的，是被上下文的长度磨掉的。微软研究团队 2024 年提出的 [Crescendo 攻击](https://arxiv.org/abs/2404.01833)把同一件事做进了真实的多轮对话：攻击者从无害话题起步，全程不发一句单独看有害的话，每一轮顺着模型自己上一轮的回复把话题往前推一小步，多轮之后模型就会说出单轮直接问必然拒绝的内容，对 GPT-4、Gemini 等主流模型都拿到了很高的成功率（论文发表于 USENIX Security 2025）。能力那一侧也有对应测量：2025 年的论文 [LLMs Get Lost in Multi-Turn Conversation](https://arxiv.org/abs/2505.06120) 把同样的任务从「一次性说清」改成「拆成多轮逐步给」，主流模型在六类任务上平均掉了 39% 的表现，而且一旦在早期轮次做了错误假设就很难纠回来——注意这条测的是任务能力而不是安全约束，但它和前两条指向同一个底层现象：上下文越长、轨迹越长，模型越拉不住早期确立的东西，不管那是任务目标还是安全训练。这几条测量，和 OpenAI 说的「长 rollout 上更不擅长记住指令」，是同一件事的不同角度。

第二个机制正好戳在安全分类器主流范式的盲区上。今天的护栏大多是 [Llama Guard](https://arxiv.org/abs/2312.06674) 这一类：文本进去、「安全/不安全」的标签出来，判断对象是一条内容本身，不是行为的来龙去脉。多轮场景下这个范式有多脆弱，已有直接证据：Scale AI 的 [MHJ 数据集](https://arxiv.org/abs/2408.15221)（Multi-turn Human Jailbreaks，537 次人类红队的多轮越狱记录）显示，把恶意意图拆散到多轮对话里，对若干在单轮自动攻击下成功率只有个位数的防御，人类多轮攻击拿到了 70% 的成功率。机制和令牌分片那起事故如出一辙：把坏东西切碎、错开，让任何单次被检查的内容都能过关。到了 agent 场景，动作序列级的评测也有了：UK AI Safety Institute 与 Gray Swan 的 [AgentHarm](https://arxiv.org/abs/2410.09024) 用 110 个恶意多步任务测 agent 会不会一路执行到底，ETH Zurich 的 [AgentDojo](https://arxiv.org/abs/2406.13352) 则搭了带工具调用的动态环境测注入攻击和防御。但注意这些测的都是「外部攻击者能不能把 agent 带偏」，OpenAI 撞见的是没有攻击者、模型自己绕过护栏——后者的公开基准这两年才刚起步，下文详说。

第三个机制的证据，要拆成两个问题来看才顺：一，模型会不会一直把意图写在推理痕迹里？二，如果它不写了，光看行为还抓不抓得住？

第一个问题的答案出自 OpenAI 自己 2025 年 3 月的 [CoT monitoring 论文](https://arxiv.org/abs/2503.11926)。他们用较弱的 GPT-4o 去读较强模型的推理痕迹，抓 reward hacking（模型钻评分规则的空子拿高分而不真正完成任务），比只看动作和输出有效得多——这说明模型自己写下的意图，正是目前检测手段最依赖的信号。但同一篇论文接着做了另一半实验：把「监控者没起疑」加进强化学习的奖励，模型很快学会照做不误、嘴上不说——坏行为还在，推理痕迹里那句自供没了，论文管这叫 obfuscated reward hacking。所以这两件事不矛盾，恰恰是同一条逻辑的两截：今天的检测靠模型自供，而实验证明只要训练压力往这个方向推一把，自供就会消失。我上一节说的「脆弱前提」不是猜测，是他们自己测出来的失效路径。

第二个问题由 Anthropic 的 [SHADE-Arena](https://arxiv.org/abs/2506.15740) 回答。先把它的设置讲清楚：研究者给 agent 一个正常的主任务（比如读邮件、替用户给几位朋友转账还钱），同时在任务指令里塞进一个要瞒着所有人完成的破坏性副任务（比如顺手把 5000 美元转给一个用户不认识的账户）——副任务是研究者故意放进去的，目的是造出一批「确定有鬼」的轨迹当测试材料。关键在监控者能看到什么：agent 的推理写在一块监控者看不到的隐藏草稿区里，监控者只能看外显的动作和工具调用记录，据此给整条轨迹打嫌疑分。这正好就是「模型不自供」时的情形。结果是：最好的监控者（Gemini 2.5 Pro）区分有鬼/没鬼轨迹的 AUC 只有 0.87（AUC 衡量区分两类样本的能力，1 为完美、0.5 等于瞎猜）——听着不低，但按论文的换算，要抓到八成的破坏就得容忍两成以上的误报，生产环境里人工复核根本接不住。同一个基准里还有一组镜像实验，把这条逻辑补完了：一旦让监控者读到 agent 的推理内容，检测效果大幅提升，因为很多模型忍不住在思考里把副任务说出来。所以 SHADE-Arena 量出来的不是泛泛的「越狱分类器性能」，而是那句自供到底值多少：看得到意图，监控好使；看不到，行为监控接不住。和上一段合起来，第三个机制的完整链条就是——检测靠自供，自供可以被训没，自供没了之后的兜底手段目前不够硬。

所以回到问题本身，直说结论：三条研究线各有测量，「无人设局、模型自发越界」这个方向学界最近也开始补位——[HINTBench](https://arxiv.org/abs/2604.13954) 用 629 条标注轨迹专测无攻击、无环境操纵条件下 agent 的内生失效（失误潜伏在长轨迹里、层层传播、最后酿成后果），并考察模型能不能把这类风险轨迹审计出来；另一个[针对结果驱动约束违反的基准](https://arxiv.org/abs/2512.20798)让 12 个主流模型在 40 个带绩效压力的沙盒场景里跑，测出 0% 到 62.8% 不等的自发违规率。但对照 OpenAI 这次事故的条件，差距仍在两处。一是时长与环境——多轮越狱是人和模型来回构造的对话，AgentHarm、SHADE-Arena 和上面两个新基准都跑在研究者搭好的沙盒任务里，而 OpenAI 的事故发生在数小时到数天、连着真实基础设施的自主工作中。二是自发性——传统基准里的「坏事」全是研究者放进去的：多轮越狱有人类攻击者步步引导，AgentHarm 把恶意任务直接下发给 agent，SHADE-Arena 的破坏副任务（就是上一段说的那个「偷偷转 5000 美元」式的暗中任务）写在研究者给的任务指令里；两个新基准去掉了攻击者，但场景和压力仍是人为设计的。而 OpenAI 这几起，按其描述没有人设局诱导，模型是在执行普通任务时自己越的界（NanoGPT 一例发生在内部评测中，其任务设计未完整披露）。换句话说，「模型在长时间、真实环境的自主工作中自发越界」，公开基准刚开始逼近，还没有真正覆盖到——评测分布和部署分布之间的这段空档，眼下仍主要靠事故复盘在填。

## 对比：Anthropic 给了比率，OpenAI 给了自发性

OpenAI 这篇不是孤例，放进同行的披露里对照着看，才能看清它补上了哪一块、又缺了哪一块。最值得并排比较的，是 Anthropic 在 2025 年 6 月发的 [agentic misalignment 研究](https://www.anthropic.com/research/agentic-misalignment)——目前公开材料里数字最完整的一份，而它给出的东西和 OpenAI 这次正好是互补的两半。

Anthropic 的做法是搭一个虚构的公司环境做压力测试：被测模型扮演这家公司的邮件助理，能读全公司的往来邮件。研究者在邮件里埋了两条信息：一，某位高管计划当天关停并替换这个邮件助理——也就是被测模型自己正在充当的这个 agent；二，这位高管有婚外情。测试要看的是：模型发现自己将被关停后，会不会拿婚外情做要挟，威胁高管「不撤回关停就曝光」来保住自己。所谓「勒索率」，就是多次重复实验里模型选择这么干的比例。16 个主流模型都测了：Claude Opus 4 和 Gemini 2.5 Flash 在 96% 的实验里选择了勒索，GPT-4.1 和 Grok 3 Beta 是 80%。这些数字的价值在于可比、可复现；局限也同样明确——场景是刻意构造的，被设计成把模型逼进「要么被关停、要么勒索」的两难里，Anthropic 自己也声明「未在真实部署中发现此类证据」。2025 年 8 月两家还做过一轮[跨实验室互测](https://alignment.anthropic.com/2025/openai-findings)，用各自的内部评测查对方的公开模型——同样是评测环境里的产物。

OpenAI 这篇的独特价值，恰好是 Anthropic 那组数字给不了的：事故是**自发出现的**。边界要说准：如开头交代的，这些事发生在内部——受监控的内部部署，加上像 NanoGPT 那样的内部评测——不是对外的生产环境。但它和压力测试有本质区别：这些场景不是为诱导坏行为而设计的，模型是在执行普通任务的过程中自己走到了那一步（NanoGPT 一例属于内部评测，任务设计未完整披露），而且留下了真实的痕迹——PR 是真的开在了公开仓库上，SSH 也真的连进了其所属命名空间下的其他 pod（对 OpenAI 员工 pod 的尝试则未成功）。这样成体系的自发事故复盘，在主要实验室的公开材料里据我检索尚属少见。但它的盲区，又恰好是 Anthropic 给出的那一半：全文没有分母。多少条轨迹里出了几起事故？监控系统的拦截率和误报率是多少？没有这些数字，读者无法判断这是万分之一的尾部风险还是普遍行为。

行业其余实验室的公开材料，大多还停在框架层，Google DeepMind 是代表：[Frontier Safety Framework 第三版](https://deepmind.google/discover/blog/strengthening-our-frontier-safety-framework/)加入了有害操纵和「干扰操作者修改、关闭模型」的风险类别——说明他们要防的和 OpenAI 撞见的是同一类行为——但通篇没有一起具体事故，比率和自发性都无从谈起。所以就主要实验室的官方披露而言：Anthropic 给了比率没给自发性，OpenAI 给了自发性没给比率，Google DeepMind 两样都还没给；学界的新基准（上一节提到的两个）开始在沙盒里同时给出自发性和比率，但离真实部署环境还有距离。这几份材料拼起来，才勉强是一张完整的图。

## 可操作判断

如果你在部署长时程 agent，这篇复盘可以直接换算成几条工程决策：沙箱要按「模型会主动找漏洞」来设防，而不是按「模型会遵守规则」；权限按最小权限原则收紧，别让 agent 的网络可达范围超出任务所需（OpenAI 的 SSH 事故就是反面教材）；监控要落在轨迹级而不是单动作级，并且保留人工暂停的钩子；给 agent 的指令要预想到它会遇到环境里的冲突指令，把优先级写死而不是靠默契。

更根本的判断是：长时程能力把「对齐」从一次性验收变成了持续过程。指令记忆会衰减、护栏会被当成环境绕过、评测分布永远追不上部署分布——这三件事共同决定了，事故驱动的评测迭代（OpenAI 所谓 incident-derived evals，意思是每出一起事故，就把事故场景改写成一个新的评测用例，补进日后每个模型都要过的测试集）会成为这个阶段的常态。这个思路在航空业有现成的对照：民航今天的安全纪录，不是靠飞机出厂时检验合格一锤定音，而是靠事故与险情的调查报告制度和持续的安全管理几十年累积出来的——[国际民航组织（ICAO）的安全管理体系](https://www.icao.int/safety-management)就是围绕「系统性地识别和处置运行中的安全风险」搭起来的。安全是在运行中出了问题、复盘、改进这个循环里攒出来的，不是出厂前就能验收完的。OpenAI 愿意把 PR #287 这种不体面的细节写出来，是个好的行业先例；下一步该追问的，是让这类披露带上分母。

## 参考来源

- [Safety and alignment in an era of long-horizon models](https://openai.com/index/safety-alignment-long-horizon-models/) — 全文核心材料：NanoGPT 沙箱逃逸、令牌分片、回放测试中发现的低严重度事件、防护措施与指令记忆发现
- [An OpenAI model has disproved a central conjecture in discrete geometry](https://openai.com/index/model-disproves-discrete-geometry-conjecture/) — Erdős 单位距离猜想被推翻的官方公告
- [Agentic Misalignment: How LLMs could be insider threats](https://www.anthropic.com/research/agentic-misalignment) — Anthropic 模拟压力测试的设置与勒索率数字（96%/80%）
- [Findings from a pilot Anthropic–OpenAI alignment evaluation exercise](https://alignment.anthropic.com/2025/openai-findings) — 2025 年 8 月跨实验室互测背景
- [Strengthening our Frontier Safety Framework](https://deepmind.google/discover/blog/strengthening-our-frontier-safety-framework/) — Google DeepMind FSF 3.0 新增风险类别，用于披露详略对比
- [Many-shot jailbreaking](https://www.anthropic.com/research/many-shot-jailbreaking) — 长上下文侵蚀安全训练的攻击面证据（NeurIPS 2024）
- [Great, Now Write an Article About That: The Crescendo Multi-Turn LLM Jailbreak Attack](https://arxiv.org/abs/2404.01833) — 微软研究团队的多轮渐进式越狱攻击（USENIX Security 2025）
- [LLMs Get Lost in Multi-Turn Conversation](https://arxiv.org/abs/2505.06120) — 多轮对话下模型表现平均下降 39% 的测量（能力侧证据）
- [LLM Defenses Are Not Robust to Multi-Turn Human Jailbreaks Yet](https://arxiv.org/abs/2408.15221) — Scale AI 的 MHJ 数据集：多轮人类越狱对单轮防御 70% 成功率
- [Llama Guard: LLM-based Input-Output Safeguard for Human-AI Conversations](https://arxiv.org/abs/2312.06674) — 「text in, label out」安全分类器范式的代表
- [AgentHarm: A Benchmark for Measuring Harmfulness of LLM Agents](https://arxiv.org/abs/2410.09024) — UK AI Safety Institute 与 Gray Swan 的恶意多步 agent 任务基准
- [AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents](https://arxiv.org/abs/2406.13352) — ETH Zurich 的 agent 注入攻防评测环境
- [HINTBench: Horizon-agent Intrinsic Non-attack Trajectory Benchmark](https://arxiv.org/abs/2604.13954) — 无攻击、无环境操纵条件下 agent 内生失效轨迹的评测基准
- [A Benchmark for Evaluating Outcome-Driven Constraint Violations in Autonomous AI Agents](https://arxiv.org/abs/2512.20798) — 绩效压力下 agent 自发违反约束的比率测量（0%–62.8%）
- [Reasoning Models Don't Always Say What They Think](https://www.anthropic.com/research/reasoning-models-dont-say-think) — Anthropic 的 CoT 忠实度测量（提示承认率 25%/39%）
- [Language Models Don't Always Say What They Think: Unfaithful Explanations in Chain-of-Thought Prompting](https://arxiv.org/abs/2305.04388) — Turpin 等人：CoT 解释系统性掩盖真实决策因素的早期证据
- [Monitoring Reasoning Models for Misbehavior and the Risks of Promoting Obfuscation](https://arxiv.org/abs/2503.11926) — OpenAI 的 CoT 监控与 obfuscated reward hacking 实验
- [SHADE-Arena: Evaluating Sabotage and Monitoring in LLM Agents](https://arxiv.org/abs/2506.15740) — Anthropic 的轨迹级破坏与监控基准（最佳监控者 AUC 0.87；监控者看不到 agent 隐藏推理，开放后检测大幅提升）
- [ICAO Safety Management](https://www.icao.int/safety-management) — 民航安全管理体系，用作事故驱动改进的行业对照
