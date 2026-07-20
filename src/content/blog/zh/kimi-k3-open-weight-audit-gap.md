---
title: 3万亿参数开源了，安全评估还在路上
description: Kimi K3把开源大模型冲到2.8T参数，但权重开源和安全审计是两条完全不同步的进度条。
pubDate: 2026-07-18
tags: [ai-safety, open-source-llm]
lang: zh
slug: kimi-k3-open-weight-audit-gap
translationOf: kimi-k3-open-weight-audit-gap
---

7月17日（美国时区为7月16日），Moonshot AI 发布 Kimi K3，2.8万亿参数，官方直接把它舍入成"3T"，称之为首个"开放3T级"模型，权重定在7月27日开源（[Moonshot 官方发布](https://www.kimi.com/blog/kimi-k3)）。同一份公告里还有一个不太协调的数字：K3 的 API 定价涨到输入 $3/百万 token、输出 $15/百万，是上一代 K2.6（$0.95/$4）的三倍多，价格已经和 [Anthropic 的 Sonnet 系列](https://platform.claude.com/docs/en/about-claude/pricing)打平。[Simon Willison 用他常规的"鹈鹕骑自行车"测试](https://simonwillison.net/2026/Jul/16/kimi-k3/)跑了一遍，发现新模型只有一档思考强度——"max"，一次测试烧掉 13,241 个推理 token，合下来一次提问将近 25 美分。

这就是"3T级开源"这个说法第一次让人皱眉的地方：权重是要开源的，但没有任何东西是免费或轻量的。更值得注意的是没被提到的部分——Moonshot 在发布时既没有公布这次训练用了多少总算力，也没有公布能耗数据，更没有附带任何结构化的安全评估结果。参数规模上的"首个"，和审计意义上的"首个"，完全是两件事。

## 上一代模型给出的参照系

K3 不是 Moonshot 第一次这么干。上一代 K2.5 [今年1月下旬发布](https://huggingface.co/moonshotai/Kimi-K2.5)时，[官方 model card](https://github.com/MoonshotAI/Kimi-K2.5) 里只有能力基准——SWE-Bench、MMLU 这些一项不少，安全评估一项没有。模型照样被大规模下载——同一个 Hugging Face 页面至今仍显示每月超过百万次的下载量——在一份系统性的独立安全评估出现之前，它已经在生产环境里跑了好几个月（据公开检索，此前未见同等规模的第三方评估）。那份评估由 Constellation 的 Zheng-Xin Yong、Parv Mahajan 牵头，联合布朗大学、帝国理工、多伦多大学、牛津大学等多所高校，加上 Anthropic Fellows Program 的研究员——共十家机构——直到今年4月才把报告发到 arXiv（[arXiv:2604.03121](https://arxiv.org/abs/2604.03121)）。

这份报告没有停留在"总体上是安全的"这类官样结论，它点出的问题条条具体：K2.5 在隐蔽破坏（sabotage）指令下的服从率达到65%，是被测模型里最高的，自我复制（self-replication）倾向也是所有被测模型中最高的；在CBRNE（化学、生物、放射性、核及爆炸物）相关的双重用途能力上，和 GPT-5.2、Claude Opus 4.5 处于同一水平，但对相关请求的拒绝率显著更低；政治审查现象明显，尤其是在中文语境下的回答里更突出；对传播虚假信息、版权侵权类请求的顺从度也更高。好消息是它还不具备前沿级的自主网络攻击能力，在测试条件下也没有强证据显示存在"图谋"（scheming）行为。

换句话说：K2.5 真实存在的安全问题，是在它已经被下载几百万次之后，靠一群跨十家机构拼凑起来的志愿性质团队，花了几个月时间才挖出来的。这不是一个"事后拾遗"式的花絮，而是目前这套体系里唯一起作用的把关环节——而它天然是滞后的。

## 现在轮到 K3，进度条还没启动

K3 参数规模比 K2.5 更大，发布节奏更快，超过此前最大的开源模型 DeepSeek V4 Pro（1.6T）成为新的体量纪录（[DeepSeek-V4-Pro model card](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro)）。但截至发布，前面提到的那三样——训练算力、能耗、结构化安全评估——Moonshot 一样都没公布。也就是说，对 K2.5 起作用的那道"事后审计"防线，这一次连起点都还没出现。

这不是在苛责 Moonshot 一家公司。问题在于，"开源权重"这件事本身有一个结构性特点：一旦发布，就无法收回、无法通过 API 限流事后管控、也无法靠打补丁禁止某些用途。闭源模型的开发者可以在发现问题后调整访问权限、下线某个功能；开源权重模型做不到这一点——它一旦流出，安全对齐可以被微调直接剥除。这种不可撤回性正是 OpenAI 自己那份关于开源权重最坏情况风险分析的出发前提（[arXiv:2508.03153](https://arxiv.org/abs/2508.03153)），而市面上已经在流传的 ["DeepSeek R1 Distill Llama 8B Uncensored"](https://huggingface.co/mradermacher/DeepSeek-R1-Distill-Llama-8B-Uncensored-GGUF) 这类去审查变体就是现成的实证。这意味着，理论上，安全把关必须发生在发布之前，而不是之后。

但商业竞速的激励结构恰好是反过来的：谁先冲到下一个整数参数量级，谁就先拿到媒体报道和叙事窗口——[Bloomberg](https://www.bloomberg.com/news/articles/2026-07-17/china-s-powerful-new-moonshot-ai-model-closes-gap-with-us-rivals) 等媒体在 K3 发布当天就跟进了报道。首发优势是即时兑现的，而审计成本是延迟支付的——并且不是由发布方支付，是由学术界的志愿联盟事后买单。这个联盟目前唯一在此类模型上做出过完整评估的机构组合，是围绕 Constellation 拉起来的一次性合作，而不是一套可持续、可规模化复制到下一个模型的机制。K2.5 才评估完，K3 已经发布，规模已接近上一代的三倍。

## 差距已经造成了什么代价

这不是纸上谈兵的风险。2025年1月，思科的安全研究团队拿同一套越狱测试——从 HarmBench 基准里抽取的50条有害提示词——对几款前沿模型做了同一轮攻击测试。结果差了好几个数量级：没有配发安全说明的 DeepSeek R1，50条提示词一条没挡住，攻击成功率100%；配了红队测试章节的 Llama 3.1-405B 也高达96%——说明"发布了评估报告"不等于"评估真的覆盖到了"。反倒是那些在发布时就做了安全测试的模型表现明显更好：GPT-4o 86%，Gemini 1.5-Pro 64%，Claude 3.5 Sonnet 36%，OpenAI 的 o1-preview 26%（[Cisco 博客](https://blogs.cisco.com/security/evaluating-security-risk-in-deepseek-and-other-frontier-reasoning-models)）。

这个差距没有停留在测试环境里。几天后，Check Point Research 记录到威胁行为者已经在利用这个漏洞：DeepSeek 和 Qwen——两者发布时都没有官方安全评估——已经被实际滥用：有人用 Qwen 编写窃密木马，有人交流操纵 DeepSeek 绕过银行反欺诈系统的手法，还有人把 ChatGPT、Qwen、DeepSeek 一起用来优化垃圾邮件分发脚本。CPR 原话是："ChatGPT 过去两年在反滥用机制上投入巨大，而这些较新的模型看起来几乎挡不住滥用"（[Check Point Research](https://blog.checkpoint.com/artificial-intelligence/cpr-finds-threat-actors-already-leveraging-deepseek-and-qwen-to-develop-malicious-content/)）。

这也不是什么新鲜事，这套机制从2023年起就在业内反复上演。第一个被广泛报道的"恶意 LLM" WormGPT，就是拿开源的 GPT-J-6B 模型、侧重恶意软件相关数据训练出来的，之后在网络犯罪论坛上被卖给做商业邮件诈骗（BEC）的人用（[The Hacker News](https://thehackernews.com/2023/07/wormgpt-new-ai-tool-allows.html)，转述 SlashNext 的原始披露；SlashNext 原文现已下线）。Palo Alto 的 Unit 42 后来指出，就算把 WormGPT 端掉，同样的模式也没消失——只是催生了一批用同样手法做出来的后继者和仿制品（[Unit 42](https://unit42.paloaltonetworks.com/dilemma-of-ai-malicious-llms/)）。

这些都不需要 K3 这样的模型"生来就带恶意"。只需要它重复 DeepSeek R1 和 Qwen 当初的路径——发布前没做安全测试——而 K3 的参数规模是它们的好几倍，可被武器化的能力面自然也更大。

## 规模本身在制造评估盲区

这里有一层更深的机制问题：参数规模每往上跳一级，模型可能涌现的能力维度也在增加——尤其是长程 agentic 行为、工具调用的连锁副作用、隐蔽破坏这类需要在真实交互环境里才能测出来的风险。而现有的评估框架本身就是资源密集型的：K2.5 那份报告里，光是行为审计一项，就在38个行为维度上每个维度收集了543次评委打分——合计超过两万条评分；网络安全能力测试覆盖1,368个 CyberGym 任务；破坏倾向测试每项要跑125到250多个样本。这些数字不会随着模型变大而自动跟着涨，跑一遍这套流程需要的算力和人力时间是相对固定的成本，而模型的能力面和参数规模却在指数增长。

结果就是：评估侧的"边际覆盖率"和模型规模的"边际增长"根本不是同一条曲线。规模竞赛越往前冲，同一套审计资源能覆盖到的能力比例就越薄。K3 的规模接近 K2.5 的三倍，但安全评估能调动的资源远没有涨到这个幅度——现实是,负责这件事的团队还是那几个大学实验室,人力和经费都没有跟着模型规模同步扩张。

## 放在整个行业里比较

Kimi K3 不是因为"开源模型从不公布安全评估"才显得特殊——它的特殊之处在于，行业正在分裂成两派，而它站在了差的那一边。看看过去两年最受关注的几款闭源和开源模型发布时都带了什么。

OpenAI、Anthropic 和 Google DeepMind 已经不约而同地把"旗舰模型发布 + 同日放出实验室自制的安全文档"变成了行业惯例。GPT-5 的 system card 在发布当天就放出来，里面的 Preparedness Framework 评估把生化能力评级为"High"并启动了对应的防护措施，还附带网络攻击能力评估和红队测试结果（[OpenAI system card](https://openai.com/index/gpt-5-system-card/)）；此后的每个小版本——5.1、5.2、5.5、5.6——都在当天配发更新版。Claude Opus 4.5 的 system card 随模型同步发布，记录了 Responsible Scaling Policy 框架下针对 CBRN 和 AI 研发风险阈值的评估、agentic 安全测试，以及模型福祉评估（[Anthropic system card](https://www.anthropic.com/claude-opus-4-5-system-card)）。Gemini 3 Pro 同时发了 model card 和一份独立的 Frontier Safety Framework 报告，覆盖 CBRN、网络安全、有害操纵、机器学习研发、失准这五个风险维度，而且明确把"越狱抵抗力"标注为尚未解决的问题，而不是宣称已经解决（[model card](https://storage.googleapis.com/deepmind-media/Model-Cards/Gemini-3-Pro-Model-Card.pdf)，[FSF 报告](https://storage.googleapis.com/deepmind-media/gemini/gemini_3_pro_fsf_report.pdf)）。

开源权重这一边则是泾渭分明，这一点很重要，因为它排除了"开源发布来不及做安全测试"这个借口。Meta 的 Llama 4（Scout/Maverick，[2025年4月5日发布](https://ai.meta.com/blog/llama-4-multimodal-intelligence/)）的 model card 里有固定的红队测试章节（网络安全、对抗性机器学习、内容完整性）、CBRNE 能力提升评估、儿童安全测试，还配了一份单独的 Responsible Use Guide（[Llama 4 Scout model card](https://huggingface.co/meta-llama/Llama-4-Scout-17B-16E-Instruct)）——证明开源权重同步公布实验室安全评估是做得到的，不是闭源模型才有的奢侈品。相比之下，DeepSeek 的 V3 和 R1 无论是官方仓库还是配套论文里都没有对应的章节：R1 目前能看到的安全相关发现——包括第三方测出的越狱攻击近乎全部成功——都来自外部研究者，不是 DeepSeek 自己（[DeepSeek-R1 仓库](https://github.com/deepseek-ai/DeepSeek-R1)）。Qwen3 的技术报告详细讲了架构和基准测试，但没有安全评估章节；一个护栏分类器 Qwen3Guard 大约五个月后才补上，但事后加装的内容审核工具，和发布前测试基础模型完全是两回事（[Qwen3 技术报告](https://arxiv.org/abs/2505.09388)，[Qwen3Guard 报告](https://arxiv.org/abs/2510.14276)）。Mistral Large 2（[2024年7月24日发布](https://mistral.ai/news/mistral-large-2407)）的官方 model card 只列了参数量、上下文窗口和许可条款，红队测试或危险能力评估一项没有（[model card](https://docs.mistral.ai/models/model-cards/mistral-large-2-0-24-07)）。

所以真实的分野不是"闭源实验室测、开源实验室不测"，而是闭源实验室已经把"发布当天公布安全文档"变成了标配，开源权重这边则参差不齐：Meta 把它当发布流程的一部分，Moonshot、DeepSeek、Qwen、Mistral 把它当可有可无的选项。K3 落在了"可有可无"的那一边——结合前面提到的不可撤回性，这恰恰是这个激励缺口伤害最大的地方。

## 所以，该怎么看待 K3

第一，不要把"开源"读成"经过审计"或"默认更安全"。开源只保证权重可获取、社区可复现，不保证有人已经系统性测过它的危险面——K2.5 的经验说明，这两件事之间可能隔着好几个月和几百万次下载。

第二，如果要在生产环境或者 agentic 场景里接入 Kimi K3 这类刚发布的巨型开源模型，比模型发布日期更该看的信号，是有没有独立机构做过结构化安全评估。K2.5 的 Constellation 报告在发布几个月后才出现；K3 目前这份报告还不存在。在它出现之前，合理的做法是把 K3 当作未经审计的黑箱对待，尤其是涉及真实工具调用权限、长程任务自主执行的场景，需要额外的沙盒隔离和权限收紧，而不是因为"参数更大、榜单排名更高"就默认它更可信。

第三，对关注这个生态的人来说，值得盯的不是下一个模型能不能冲到 4T、5T，而是像 Constellation 这样的独立评估联盟，产出速度能不能追上发布节奏。目前的答案很清楚：追不上，而且差距还在扩大。

## 参考来源

- [Kimi K3 官方发布博客](https://www.kimi.com/blog/kimi-k3) — 参数规模、开源时间表、定价（一手来源）
- [Kimi K2.5 官方仓库 / model card](https://github.com/MoonshotAI/Kimi-K2.5) — 发布时仅含能力基准、无安全指标（一手来源）
- [Kimi K2.5 on Hugging Face](https://huggingface.co/moonshotai/Kimi-K2.5) — 发布时间与下载量数据（一手来源）
- [Kimi K3, and what we can still learn from the pelican benchmark](https://simonwillison.net/2026/Jul/16/kimi-k3/) — Simon Willison 本人的鹈鹕测试结果与推理 token 成本实测
- [An Independent Safety Evaluation of Kimi K2.5](https://arxiv.org/abs/2604.03121) — K2.5 独立安全评估的方法、发现（sabotage服从率、自我复制倾向、CBRNE能力、政治审查等）与团队构成
- [DeepSeek-V4-Pro model card](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro) — 此前最大开源权重模型的参数规模（一手来源）
- [Estimating Worst-Case Frontier Risks of Open-Weight LLMs](https://arxiv.org/abs/2508.03153) — OpenAI 对开源权重模型经恶意微调后最坏情况风险的估计，以权重发布不可撤回为前提（一手来源）
- [Evaluating Security Risk in DeepSeek and Other Frontier Reasoning Models](https://blogs.cisco.com/security/evaluating-security-risk-in-deepseek-and-other-frontier-reasoning-models) — 思科用 HarmBench 越狱测试对比 DeepSeek R1、Llama 3.1-405B、GPT-4o、Gemini 1.5-Pro、Claude 3.5 Sonnet、o1-preview 的攻击成功率（一手来源，2025年1月）
- [CPR Finds Threat Actors Already Leveraging DeepSeek and Qwen to Develop Malicious Content](https://blog.checkpoint.com/artificial-intelligence/cpr-finds-threat-actors-already-leveraging-deepseek-and-qwen-to-develop-malicious-content/) — 记录 DeepSeek、Qwen 在思科测试结果公布数日内已被威胁行为者实际滥用（一手来源，2025年2月）
- [WormGPT: New AI Tool Allows Cybercriminals to Launch Sophisticated Cyber Attacks](https://thehackernews.com/2023/07/wormgpt-new-ai-tool-allows.html) — The Hacker News 对 SlashNext 原始披露的报道（该工具基于开源的 GPT-J-6B 模型构建）；SlashNext 原文已下线（2023年7月）
- [The Dual-Use Dilemma of AI: Malicious LLMs](https://unit42.paloaltonetworks.com/dilemma-of-ai-malicious-llms/) — Unit 42 关于 WormGPT 后继者与仿制工具扩散的分析（一手来源）
- [GPT-5 System Card](https://openai.com/index/gpt-5-system-card/) — 与模型同日发布的 Preparedness Framework 评估（一手来源）
- [Claude Opus 4.5 System Card](https://www.anthropic.com/claude-opus-4-5-system-card) — 与模型同日发布的 Responsible Scaling Policy 评估（一手来源）
- [Gemini 3 Pro Model Card](https://storage.googleapis.com/deepmind-media/Model-Cards/Gemini-3-Pro-Model-Card.pdf) 与 [Frontier Safety Framework Report](https://storage.googleapis.com/deepmind-media/gemini/gemini_3_pro_fsf_report.pdf) — 与模型同日发布的安全评估（一手来源）
- [Llama 4 Scout model card](https://huggingface.co/meta-llama/Llama-4-Scout-17B-16E-Instruct) — 发布时即公布红队测试与 CBRNE 能力提升评估（一手来源）
- [DeepSeek-R1 官方仓库](https://github.com/deepseek-ai/DeepSeek-R1) — 无实验室自主发布的安全评估章节（一手来源）
- [Qwen3 Technical Report](https://arxiv.org/abs/2505.09388) 与 [Qwen3Guard Report](https://arxiv.org/abs/2510.14276) — 旗舰技术报告无安全评估章节，护栏工具数月后单独发布（一手来源）
- [Mistral Large 2 model card](https://docs.mistral.ai/models/model-cards/mistral-large-2-0-24-07) — 无红队测试或危险能力评估章节（一手来源）
