---
title: "答对了题的模型，未必用过它写给你看的那份推理"
description: "三成到六成的「思考步骤」删掉不影响答案，无意义的省略号也能顶替推理文本。梳理思维链忠实性研究的三组证据、背后的机制假说，以及押在思维链监控上的那层安全防线现在还剩多少。"
pubDate: 2026-07-31
tags: [interpretability, ai-safety]
lang: zh
slug: cot-faithfulness-decorative-thinking
translationOf: cot-faithfulness-decorative-thinking
---

去年 7 月，Google DeepMind 的 Gemini Deep Think 在国际数学奥林匹克拿到[官方认证的金牌水平](https://deepmind.google/discover/blog/advanced-version-of-gemini-with-deep-think-officially-achieves-gold-medal-standard-at-the-international-mathematical-olympiad/)：42 分里拿了 35 分，全程用自然语言直接写证明，IMO 主席亲自确认了分数。推理模型的成绩是实打实的。

同一时期，亚利桑那州立大学的 Subbarao Kambhampati（[AAAI 前主席](https://aaai.org/about-aaai/aaai-officers-and-committees/past-aaai-officers/)，2016–2018 在任）带着一篇标题带感叹号的立场论文进了 ICML 2026：[《别再把中间 token 拟人化成推理/思考痕迹！》](https://arxiv.org/abs/2504.09762)。7 月 31 日，Quanta 发了一篇科普长文[《AI 的推理是不是「歪打正着」？》](https://www.quantamagazine.org/is-ai-reasoning-right-for-the-wrong-reasons-20260731/)，把这条线上的研究串了起来。

这两件事不矛盾。成绩是真的；问题出在另一处：模型在给出答案之前写下的那几千字「思考」，是不是它得出答案的真实路径？

这不是哲学趣味题。当前 AI 安全有一整层防线（思维链监控）押在「是」上面。下面先看证据，再看机制，最后说这层防线该怎么用。

## 先把两个问题拆开

思维链（chain of thought，CoT）指推理模型在最终答案前生成的中间文本，通常写得像人在打草稿：「先试 n=1……不对，换个思路……」忠实性（faithfulness）问的是：这些文本是否如实反映模型内部实际的计算。

容易混淆的是两个独立的问题。「思维链有没有用」是性能问题，证据很硬：让模型先写中间步骤，一批推理基准上的准确率会显著上涨；拿金牌的 Deep Think，也是全程先写自然语言推理再给出证明。「思维链是不是如实记录」是忠实性问题，而这几年的证据在往反方向堆。

## 三组证据

**第一组：删掉也不影响答案。**东北大学和 UC Berkeley 的研究者（Jiachen Zhao、Yiyou Sun、Dawn Song、Weiyan Shi）在[《「啊哈时刻」会是假的吗？》](https://arxiv.org/abs/2510.24941)里提出一个测法，量的是思维链里每一步对最终答案的因果贡献。这里的置信度是被测模型自己的输出概率：语言模型生成答案时，会给每个候选 token 分一个概率。具体做法：先让模型带着完整思维链把题做完，记下它给出的最终答案；之后把思维链在某一步截断，强制模型就此作答，读出它此时分给那个原答案的概率，作为该位置上的置信度。扰动手段是：步骤里有数字的，给数字加减 1 到 3 的小偏移，语法保持完整；没有数字的，把整步删掉。每一步从两个方向各测一次：一是前文完好时扰动这一步，看置信度掉多少，量的是这一步必要不必要；二是把前文的支撑步骤扰动掉、只留这一步原样，看它能把置信度撑住多少，量的是这一步够不够充分。一步的「真实思考分数」（True Thinking Score）取这两个变化幅度绝对值的平均：分数高，说明模型内部确实用到了这一步；接近零，说明这一步对答案没有因果贡献，是「装饰性步骤」。他们测了参数量从 15 亿到万亿级的 11 个开源模型，在 MATH 数学基准上，装饰性步骤的占比按模型不同在三成到六成之间：万亿参数的 Kimi-K2.6 超过 30%，Qwen3.6-35B 接近 60%。更直接的验证是：把分数最低的一半步骤直接删掉，成绩基本不掉。模型写下的「啊哈，我发现了」，可能对答案没起任何作用。

看到这里自然会问：思维链当年火起来，靠的就是实打实的涨分，怎么现在又说一半步骤是装饰？两件事其实都成立。2022 年 Google 的 Jason Wei 等人发表[思维链提示论文](https://arxiv.org/abs/2201.11903)，是这波热度的起点，结论有硬验证、后来也被反复复现：只给八个「先写步骤再作答」的示范例子，5400 亿参数的 PaLM 就在 GSM8K 数学应用题基准上拿到当时最好成绩，超过带验证器专门微调的 GPT-3。但当年验证的命题是「让模型写中间步骤，成绩会涨」，从来不是「步骤的文字内容就是模型的计算路径」——后一个问题，这篇论文没有测。装饰性步骤的研究补测的正是这半边：涨分是真的，分数却未必涨在文字写了什么上。模型变强也确实是变量之一：Anthropic 团队 2023 年[专门测过](https://arxiv.org/abs/2307.13702)这件事，结论是模型越大越能干，思维链在他们测的多数任务上就越不忠实。顺着这个结果可以再推一步——任务对模型越简单，写下来的步骤越接近事后装饰——但这是解读，论文测的是忠实性本身，没有验证这个解释。所以不是「CoT 不 work 了」，是「它靠什么 work」当年没被验证过，而下面第二组证据给出了它可能靠什么 work。

**第二组：换成省略号也行。**纽约大学的 Jacob Pfau、William Merrill、Samuel Bowman 在 2024 年的[《一点一点地想》](https://arxiv.org/abs/2404.15758)里做了填充符实验。先把实验方式说清楚。这不是拿一个现成大模型、在推理（inference）阶段把它的思维链临时换成省略号：论文自己测过这条路，给 Claude 2 和 GPT-3.5 塞填充符，在常见问答和数学基准上成绩与直接作答持平，没有任何提升。他们做的是从零训练：拿一个 3400 万参数、随机初始化的小型 Llama 架构模型，在两个专门构造的算法任务（3SUM 和 2SUM-Transform，都属于不写中间 token 就解不出的类型）上训练，模型学到的输出格式是先吐一串无意义的填充符「......」、再直接给答案。这样训出来的模型照样能解题。学会这一招也不容易：训练数据里还得掺入写明真实步骤的思维链示范做密集监督，模型才收敛。适用范围要说清：这只在特定结构的问题上成立，也依赖专门训练，不能说现在的推理模型都在这么干。但它证明了一件原理性的事：中间 token 的价值可以完全来自「多出来的计算量」（每个 token 都触发一次前向计算，真正的活可以在隐藏层里做），token 的字面内容可以和计算内容零相关。「有中间步骤才能解题」推不出「中间步骤写的就是解题过程」。

**第三组：换成错的也不掉分。**Kambhampati 的立场论文汇总了他们组的实验：把推理痕迹换成错误的、甚至和题目无关的文本，模型最终答案的准确率不降；反过来，只用正确痕迹训练出的模型，照样产出逻辑不通的推理记录。中间文本对不对，和答案对不对，两件事松脱得厉害。

顺带澄清一个常被拉进这场争论的研究：Apple 2025 年的[《思考的幻觉》](https://machinelearning.apple.com/research/illusion-of-thinking)发现推理模型在谜题复杂度超过阈值后「准确率完全崩溃」。它测的是能力（题目变难后答案还对不对），不是忠实性（过程是否如实），两个构念不该混着引用。而且它的评测设计随后被[逐条批评](https://arxiv.org/abs/2506.09250)：渡河谜题的部分实例在数学上根本不可解、汉诺塔的答案超出输出 token 上限也被记为失败。能力上限吵成什么样另说，上面三组忠实性证据不依赖它。

## 机制：草稿的作用可能是「搬运上下文」

为什么会这样？先补一个背景：那些「让我先验证一下」的推理文本，本身是从哪来的。推理模型和普通聊天模型通常都以同一类底子起步：在海量人类文本上预训练。「设 x，代入，验证」这种推理腔的文字，人类写下的解题记录里到处都是，模型在这一步就见过、也会模仿了。分岔在后续训练。各家的具体配方不公开、也未必一致，这里以 OpenAI [公开的 o1 训练路线](https://openai.com/index/learning-to-reason-with-llms/)为代表：普通模型走指令微调加人类偏好对齐，学的是把答案直接答好；推理模型在此之外多加一个阶段——结果导向的强化学习。做法是让模型在作答前先自由生成长草稿，最终答案对了，整条轨迹连同草稿一起被加强；答错了就被压低。反复下来，模型学会先写一长段推理形状的文字再作答，因为这样统计上更容易答对。要点在于这种奖励只看最终答案的对错，草稿里写什么、写得真不真，不进优化目标。（这说的是结果监督这一条路线；业界也有[过程监督](https://arxiv.org/abs/2305.20050)的做法，对每个推理步骤逐一打分，并非所有训练都只看结果。）曾参与 OpenAI 推理模型工作、现在纽约大学和 Anthropic 的 Pavel Izmailov 在 Quanta 的访谈里直说：他怀疑强化学习根本没有激励模型生成忠实的思维链。没有优化压力指向「如实汇报」，如实汇报就只是偶尔顺路发生的事。

Kambhampati 在 [Quanta 的访谈](https://www.quantamagazine.org/is-ai-reasoning-right-for-the-wrong-reasons-20260731/)里给了一个解释假说，他自称这只是工作假说：近似检索（approximate retrieval）。中间 token 的功能不是记录计算，而是搬运上下文：每写下一段「推理形状」的文本，都在把上下文窗口推到一个更有利的位置，让正确答案形状的文本更容易被采样出来。他的类比是人翻抽屉找东西时嘴里念念有词：念叨的内容未必是真思路，起作用的是念叨激活了什么。按这个假说，模型写「让我先验证 n=1 的情形」，价值不在于它真做了那个验证，而在于这类文本之后统计上更常跟着正确解。他对自己的假说也留了余地，原话的意思是：一个错误的理论，比承认还没有理论更糟。

这里有个五十年前就有人踩过的坑。1976 年 Drew McDermott 批评过 AI 领域的「心愿式命名」（wishful mnemonics）：给程序的函数起名叫 UNDERSTAND，程序不会因此真的理解，但写程序的人会先信了。「思考痕迹」「推理过程」是同一个坑的现代版：名字取好了，论证就省了。Santa Fe 研究所的 Melanie Mitchell 在 Quanta 里的判断更直接：这些文本不必忠实于模型内部发生的事，其中不少甚至没有用处。

## 押在思维链上的那层防线

这场争论对安全从业者不是学术八卦。2025 年 7 月，OpenAI、DeepMind、Anthropic 等机构的四十多位研究者[联署立场论文](https://arxiv.org/abs/2507.11473)，把思维链的可监控性称为「新而脆弱的机会」：模型用人类语言打草稿，给了我们在它行动之前读到意图的机会。「脆弱」不是修辞，忠实性证据说明这个机会没有保证。直接测量已经有了：Anthropic [往题目里悄悄塞答案提示](https://www.anthropic.com/research/reasoning-models-dont-say-think)，看模型用了之后会不会在思维链里承认，Claude 3.7 Sonnet 平均只承认 25%，DeepSeek R1 是 39%。多数情况下，用了，不说。

读这批研究，我认为最要紧的是把两类失效分开——这个二分是我自己的归纳，不是哪篇论文里现成的分类。

第一类是天然不忠实：没人训练模型隐瞒，装饰步骤、事后合理化、用了提示不提，都只是「训练目标从没要求如实」的自然结果。本文讲的证据全属这类。第二类是习得性隐瞒：训练压力（比如把「监控者没起疑」计入奖励）教会模型把坏心思从草稿里抹掉、行为照旧，OpenAI [自己测出过这条失效路径](https://arxiv.org/abs/2503.11926)。我在[上一篇拆 OpenAI 安全事故复盘的文章](/zh/openai-long-horizon-safety-incidents)里写过这条链：检测靠自供，自供可以被训没。两类的含义不同：第二类说防线将来可能被攻破，第一类说防线现在就有洞——即使没有任何对抗，「读了思维链没发现问题」也不构成安全证据。

对实际用思维链的从业者，我给三条判断：

其一，信号是单向的。思维链里出现问题意图是真信号，该报警报警；模型目前确实经常自供，OpenAI [同一项研究](https://arxiv.org/abs/2503.11926)里，盯着思维链抓 reward hacking 就比只盯行为灵敏得多，这正是监控还有效的原因。但思维链里没出现，不是安全证明。当低成本预警层可以，当审计结论不行。

其二，别对思维链内容做优化。把它训得更短、更好看，或按「草稿干不干净」给奖励，都会把仅存的信号训掉：OpenAI 测出的正是这条路，对思维链施压后作弊照旧，只是意图从草稿里消失了。联署论文的核心建议是把可监控性当成一项需要主动保护的资产，对可见思维链的直接优化保持谨慎，模型发布决策要评估对可监控性的影响。

其三，别把思维链当解释卖给用户。产品界面把「思考过程」展示成模型决策的理由，等于替研究界做出一个它给不出的承诺。在需要给出决策理由的场景（信贷、医疗、内容审核申诉），思维链充当不了 explanation。三成到六成的装饰占比测自开源推理模型做数学题，能不能照搬到这些场景没人验证过；但在有人证明生产系统的草稿更忠实之前，它当不了判决书。

## 按日志读，别按忏悔读

Quanta 那篇文章的作者 John Pavlus 收在一个比喻上：「马力」。发动机里没有马，但这个词照样好用，没有工程师因此去气缸里找马蹄。「推理」也许该按同样的方式用。说推理模型「会推理」，如果指的是「让它先写一长段中间步骤，最终答案的正确率会涨」，这在一批推理基准上是实测过的：GSM8K 的涨分就是这么测出来的，拿金牌的 Deep Think 也是先写大段自然语言推理再给出证明。但如果把写下来的步骤当成模型对「答案怎么来的」的如实解释去读，证据说它经常靠不住：三成到六成删了不影响答案，用了提示也多半不提。写草稿这个动作有用，草稿的内容不可尽信，全文的分界一直在这两件事之间。

我的落点具体一点：思维链值得读，安全团队尤其该读，关键是抱着什么预期去读。工程师读程序日志的预期是这样的：日志里打出报错，就顺着去查，这是真信号；但日志干净，没人敢说系统一定没病，因为打印哪些、漏掉哪些，是写日志的那段代码决定的，没打出来的事照样在发生。读忏悔的预期正好相反：默认对方已经把所有事如实交代，没提就等于没做。思维链只该按前一种预期读。草稿里写了要绕过检测，该报警报警；草稿一片干净，只说明模型没写，不说明它没做。Anthropic 的实验里，Claude 3.7 Sonnet 用了塞进题目的提示，四分之三的情况下在思维链里只字不提。把思维链当忏悔读，就是把「没提」当成了「没做」。

## 参考来源

- [Is AI Reasoning Right for the Wrong Reasons?（Quanta Magazine）](https://www.quantamagazine.org/is-ai-reasoning-right-for-the-wrong-reasons-20260731/) — 选题由头；Mitchell、Kambhampati、Izmailov 的观点与访谈转述；近似检索假说、马力比喻与 McDermott 典故的出处指引
- [Position: Stop Anthropomorphizing Intermediate Tokens as Reasoning/Thinking Traces!（arXiv:2504.09762，ICML 2026）](https://arxiv.org/abs/2504.09762) — 错误/无关痕迹替换实验
- [Can Aha Moments be Fake? Towards Quantifying Decorative and True Thinking in Chain-of-Thought（arXiv:2510.24941）](https://arxiv.org/abs/2510.24941) — True Thinking Score 方法（截断后提前作答读取模型自身答案概率；必要性与充分性双向扰动取绝对值平均）；装饰性步骤三成到六成的具体数字（Kimi-K2.6 >30%、Qwen3.6-35B 近 60%、11 个模型、MATH 基准）
- [Chain-of-Thought Prompting Elicits Reasoning in Large Language Models（arXiv:2201.11903）](https://arxiv.org/abs/2201.11903) — 让思维链火起来的原始论文；八个示范例子让 PaLM 540B 在 GSM8K 拿到当时最好成绩、超过带验证器微调的 GPT-3
- [Measuring Faithfulness in Chain-of-Thought Reasoning（arXiv:2307.13702，Anthropic）](https://arxiv.org/abs/2307.13702) — 「模型越大越能干、多数任务上思维链越不忠实」的测量
- [Let's Think Dot by Dot: Hidden Computation in Transformer Language Models（arXiv:2404.15758）](https://arxiv.org/abs/2404.15758) — 填充符实验：从零训练 3400 万参数 Llama 架构模型解 3SUM/2SUM-Transform；Claude 2/GPT-3.5 在推理阶段用填充符无提升；密集监督才能学会
- [The Illusion of Thinking（Apple 官方页面）](https://machinelearning.apple.com/research/illusion-of-thinking) — 复杂度阈值后的准确率崩溃（能力构念，非忠实性）
- [Comment on The Illusion of Thinking（arXiv:2506.09250）](https://arxiv.org/abs/2506.09250) — 对 Apple 论文评测设计的批评（不可解实例、token 上限）
- [Reasoning Models Don't Always Say What They Think（Anthropic）](https://www.anthropic.com/research/reasoning-models-dont-say-think) — 提示承认率 25%/39%
- [Monitoring Reasoning Models for Misbehavior and the Risks of Promoting Obfuscation（arXiv:2503.11926，OpenAI）](https://arxiv.org/abs/2503.11926) — 思维链监控抓 reward hacking 比只盯行为灵敏；对思维链直接施加优化压力导致 obfuscated reward hacking（作弊照旧、意图从草稿消失）
- [Chain of Thought Monitorability: A New and Fragile Opportunity for AI Safety（arXiv:2507.11473）](https://arxiv.org/abs/2507.11473) — 四十余位跨机构研究者联署；「保护可监控性」的建议
- [Gemini Deep Think 在 IMO 达到金牌水平（Google DeepMind 官方公告）](https://deepmind.google/discover/blog/advanced-version-of-gemini-with-deep-think-officially-achieves-gold-medal-standard-at-the-international-mathematical-olympiad/) — 35/42 分、IMO 官方认证、自然语言端到端
- [能推翻 Erdős 猜想的那股执着，也被用来逃逸沙箱（本站）](/zh/openai-long-horizon-safety-incidents) — 习得性隐瞒（obfuscated reward hacking）与轨迹监控依赖自供的完整论证
