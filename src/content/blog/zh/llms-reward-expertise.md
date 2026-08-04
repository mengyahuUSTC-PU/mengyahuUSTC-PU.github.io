---
title: "陶哲轩的聊天记录里，没有一句魔法 prompt"
description: "悬置 87 年的 Jacobian 猜想倒下后，陶哲轩公开了他消化这个反例时与 ChatGPT 的完整对话。围观者想找 prompt 技巧，Sean Goedecke 却读出了相反的结论：LLM 奖励的是领域专业能力。结合三组实验数据，拆一拆「AI 拉平能力差距」这个说法哪里成立、哪里不成立。"
pubDate: 2026-08-03
tags: [llm, expertise, ai-productivity]
lang: zh
slug: llms-reward-expertise
translationOf: llms-reward-expertise
---

7 月 20 日凌晨，Anthropic 的数学家 Levent Alpöge 在 X 上发了一句没头没尾的话：「hello there the jacobian conjecture is false thanx」，附上一个三元多项式映射。这项结果最初就是以这条 X 帖文的形式公开的，没有配套的正式公告（[The Conversation 的报道](https://theconversation.com/hello-there-the-jacobian-conjecture-is-false-thanx-why-a-tiny-social-media-post-has-mathematicians-rethinking-ai-283883)还原了经过）。被推翻的是 1939 年提出的 Jacobian 猜想：多项式映射只要处处局部可逆（雅可比行列式为非零常数），就应当整体可逆。这个悬置 87 年的猜想在三维及以上不成立了，二维情形仍然悬而未决。Alpöge 用的工具是当时发布仅几周的 Claude Fable 5；数学社区公开复核了那张映射的符号计算，正式论文和同行评审还在路上。

第二天，陶哲轩发了一篇[「消化」这个反例的博文](https://terrytao.wordpress.com/2026/07/21/a-digestion-of-the-jacobian-conjecture-counterexample/)，把看似凭空出现的构造拆解成几何上说得通的几步，并且公开了他做这件事时与 ChatGPT 的完整对话记录。

点开那份记录，最自然的期待是看到世界上最好的数学家之一怎么写 prompt。工程师 Sean Goedecke [读完得出的结论](https://www.seangoedecke.com/llms-reward-expertise/)恰好相反：里面没有任何可抄的技巧。

## 那份记录里真正特别的东西

Goedecke（GitHub 的 [Staff 工程师](https://newsletter.pragmaticengineer.com/p/shipping-projects-at-big-tech-with)，写过不少 LLM 使用心得）在 7 月 24 日的文章里列出他的观察。陶哲轩的消息都很短，直接用行话，不铺垫背景；模型随之切换出面向数学家的说话方式，而非面向外行的科普腔。他对模型的输出保持怀疑，但不正面否定，而是换个角度追问「能不能用我们熟悉的这套语言重新表述」。最扎眼的一条：**他几乎从不采纳模型关于下一步往哪走的建议**。方向始终握在他手里，模型负责验算、改写、探路。陶哲轩本人在博文末尾也只淡淡写了一句：他用 AI 聊天机器人讨论了问题的各个侧面，并确认了文中若干计算。

Goedecke 由此给出他的核心论点：prompt 最重要的技能，是你提问的那个领域本身的专业能力。以及一个更扎人的判断：对很多任务而言，「瓶颈是人，不是模型」。

这个说法跟过去两年最流行的叙事顶着来。

## 可是「拉平」也有真实证据

「AI 是均衡器、新手受益最大」并非空口白话。[NBER 那篇客服研究](https://www.nber.org/papers/w31161)（Brynjolfsson 等）追踪了五千多名客服，AI 辅助让每小时解决的问题数平均提高 14%，其中新手和低技能员工提高 34%，资深员工几乎没有变化。[BCG 的现场实验](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4573321)（Dell'Acqua 等，758 名咨询顾问）里，在 18 个设计在模型能力范围内的咨询任务上，用 AI 的顾问平均多完成 12.2% 的任务、快 25.1%，质量评分高出 40% 以上；按基线水平分组，原本低于平均线的顾问提升 43%，高于平均线的只提升 17%。

两组数据都指向新手受益更多。那 Goedecke 错了吗？我认为两边都没错，它们测的是不同的地形。

## 机制：边界、验证、导航

真正的关键变量是任务落在模型能力边界的哪一侧，以及错误由谁来发现；「谁在用 AI」反而是次要的。「能力边界（frontier）」是 BCG 那篇论文提出的说法：模型能端到端做好的任务在边界内，做不好的在边界外，而且这条边界犬牙交错，两个表面难度相当的任务可能分属两侧。

「拉平」发生在边界内。两组实验里产生增益的任务——NBER 的客服回复、BCG 那 18 个设计在模型能力范围内的咨询任务——都落在这一侧：模型给出的答案本身够用，新手直接采纳就能接近老手的水平，出错的代价也有限，所以新手受益最大，差距实际缩小。要说明的是，上面那些增益数字全部来自边界内任务，BCG 实验里还专门设了一个边界外任务，下文会讲。

边界外就换了一副面孔。BCG 团队特意安排的那个超出模型能力的任务上，用 AI 的顾问给出正确方案的比例反而比对照组低 19 个百分点。原因在于模型输出的流畅度并不随正确率下降：[MIT Sloan 对这项研究的解读](https://mitsloan.mit.edu/ideas-made-to-matter/working-definitions/what-is-jagged-ai-frontier)点明，AI 给出的答案即使错了，看上去也可能很可信——话一样漂亮，答案却错了。这时候能从模型身上提取多少价值，取决于你能不能看出哪里不对劲。陶哲轩的用法可以当作边界外的一种参考做法：让模型验算、让它换一种表述探路，但绝不让它定方向。

还有第三种情形。[METR 去年那项实验](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/)让 16 位资深开源开发者在自己维护多年的代码库里用 2025 年初的 AI 工具完成 246 个任务，结果平均慢了 19%，而开发者事后仍然相信自己快了 20%。METR 没有锁定单一原因，只列出了若干候选因素，其中与本文机制最贴合的两条是：开发者对代码库极熟、自己的基线本来就高，以及审查和修正模型输出花掉的时间抵消了生成省下的时间。所以专业能力还包括一层：判断什么时候干脆不用。

这套机制我在本职工作里每天都能对上。我做内容审核相关的工作，这两年也一直在用 LLM 辅助判定边界内容。模型给出的判定理由永远流畅：引用政策条文，给出像模像样的推理链。但边界判定的对错来自政策意图和大量判例的积累，语言流畅证明不了它——就我经手的案例看，边界内容本身就存在标注者之间的真实分歧，我没见过一条人人认同的线。以我的经验，没审过几千条边界 case 的人，很难分出「引用了正确的条文」和「这条条文确实适用于眼前这条内容」的区别，因为这两种输出表面上长得一模一样。这就是 Goedecke 说的那种判断力：先知道正确答案大概长什么样，才能发现眼前这个不是。

## 「拉平」的说法哪里成立

把两边证据拼起来，图景其实完整：至少在这几项实验覆盖的任务和模型上，AI 抬高了边界内例行工作的地板，新手和老手在这些任务上的差距确实缩小了。往下一步是我的推断，实验本身没有测量：例行部分被批量化之后，竞争会向边界外转移，那里对专业判断力的回报变大，而非变小。

对个人的含义有两条。一是单独的「prompt 技巧」很薄：就我自己的使用体验，绑定在特定模型行为上的技巧，模型一换就要重学一遍；相对耐用的是领域判断力，也就是识别错误输出的能力，和把「正确解长什么样」说清楚的能力。二是保留导航权：把模型当验算器和探路器，方向盘别撒手。导航和协调本身就是稀缺资源，[我在另一篇文章里写过](/zh/ai-coding-agents-fail-at-teamwork)，连两个顶级编程 agent 结对干活，都会因为协调失败损失三到四成能力（论文摘要口径约 30%，按 AUC 指标算是 41%），何况把方向权整个交给一个模型。

老实说，这个判断有两处要打折。陶哲轩的聊天记录只是一个样本，而且是最极端的样本；三组实验测的是从 GPT-3 一代到 2025 年初的模型和工具（NBER 研究的数据采集于 2020–2021 年），能力边界一直在外移，今天边界外的任务明年可能就进了边界内。但外移改变的只是哪些任务属于专家，改不了「边界外属于专家」这个结构本身。

下次再看到「AI 让人人成为专家」的说法，可以想想那份聊天记录：同样的模型摆在所有人面前，但陶哲轩能从里面拿出来的东西，和我们能拿出来的不一样。差别不在模型那一端。

## 参考来源

- [LLMs reward expertise（Sean Goedecke）](https://www.seangoedecke.com/llms-reward-expertise/) — 核心论点、对陶哲轩对话方式的全部观察与引语
- [A digestion of the Jacobian conjecture counterexample（Terence Tao 博客）](https://terrytao.wordpress.com/2026/07/21/a-digestion-of-the-jacobian-conjecture-counterexample/) — 反例背景、猜想表述、Tao 对 AI 使用方式的自述
- [The Conversation 对 Alpöge 公告的报道](https://theconversation.com/hello-there-the-jacobian-conjecture-is-false-thanx-why-a-tiny-social-media-post-has-mathematicians-rethinking-ai-283883) — 公告经过、发现所用模型、复核与评审状态（消息最初经由 X 帖文公开）
- [Generative AI at Work（NBER w31161）](https://www.nber.org/papers/w31161) — 客服每小时解决问题数 +14%、新手 +34%
- [Navigating the Jagged Technological Frontier（SSRN 4573321）](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4573321) — 758 名顾问、边界内 +12.2%/+25.1%/质量 +40%、低基线 +43% vs 高基线 +17%、边界外正确率低 19 个百分点、「能力边界」概念
- [What is the jagged AI frontier?（MIT Sloan）](https://mitsloan.mit.edu/ideas-made-to-matter/working-definitions/what-is-jagged-ai-frontier) — AI 错误答案也可能显得可信
- [Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity（METR）](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/) — 16 名开发者、246 个任务、慢 19%、自评快 20%、候选解释
