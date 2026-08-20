---
title: "权重不是源代码：这个夏天的开源大论战吵错了轴"
description: "开放权重回答「我能不能跑它」，开源回答「我能不能信它、改它」。出口管制、公开信、制裁威胁全在前一个问题上吵，而科研需要的开放在另一条轴上，那条轴上几乎没人交货。"
pubDate: 2026-08-19
tags: [open-source, ai-governance, ai-research]
lang: zh
slug: open-weights-are-not-open-source
translationOf: open-weights-are-not-open-source
---

美东时间 6 月 12 日下午 5 点 21 分，Anthropic 收到美国政府一纸出口管制指令：暂停任何外国国籍人士访问 Fable 5 和 Mythos 5，包括公司自己的外籍员工（[Anthropic 官方声明](https://www.anthropic.com/news/fable-mythos-access)）。两款旗舰模型公开上线才三天，起因是一种据称能绕开安全护栏的越狱手法（[NBC News](https://www.nbcnews.com/business/business-news/commerce-department-gives-green-light-anthropic-bring-back-fable-5-rcna352501)）。Anthropic 在声明里写得很硬——「我们不同意把一个窄面的潜在越狱，当作召回一个数亿人在用的商业模型的理由」——但还是照办了。6 月 30 日，商务部解除限制，模型重新上线（[CNBC](https://www.cnbc.com/2026/06/30/anthropic-says-trump-admin-has-lifted-export-controls-on-claude-fable-5-and-mythos-5.html)）。

不到一个月后的 7 月 27 日，Moonshot 把 2.8 万亿参数的 Kimi K3 全量权重放上 Hugging Face（[moonshotai/Kimi-K3](https://huggingface.co/moonshotai/Kimi-K3)）。同一件事在这边是反着的：权重文件一旦被下载，世界上不存在能让它下线的指令。7 月 24 日，Nvidia、Microsoft、Meta 等 25 家公司发表公开信《Open Weights and American AI Leadership》，警告华盛顿不要对开放权重模型施加「过早限制」（[CNBC](https://www.cnbc.com/2026/07/24/nvidia-microsoft-meta-open-weight-ai-models.html)）；一天之内签名翻倍到 50 家，OpenAI 和 Google 补了名，Anthropic 没签（[Forbes](https://www.forbes.com/sites/sandycarter/2026/07/25/huangs-open-weights-letter-doubled-to-50-without-amazon-and-anthropic/)）。

这个夏天所有关于开源 AI 的争吵，压的都是同一条轴：模型收得回，还是收不回。8 月 4 日，斯坦福 HAI 官网刊文转述联合创始人 James Landay 的主张（[Stanford HAI](https://hai.stanford.edu/news/open-weight-models-arent-enough-we-need-truly-open-source-ai-models-for-science-and-society)）：这条轴上根本没有科学关心的问题——开放权重模型不够，科学和社会需要真正开源的 AI。他的核心论点只有两问：「开放权重回答的是『我能跑它吗』，开源回答的是『我能信它、改进它、在它上面盖下一层吗』。」

## 权重这一档开放，给了你什么

先把「权重」说清楚：一个大模型训练结束后，产出是几千亿到几万亿个数值参数，这堆数就是权重，相当于成品本身。厂商把这个文件放出来任人下载，就叫开放权重。

拿到权重能做的事不少：在自己的机器上跑推理，数据全程不出内网；照自己的任务微调；蒸馏出小模型；最重要的是不怕断供——上面 Anthropic 的例子刚演示过，闭源 API 的总阀门握在别人手里，一纸指令就能拧上。对企业和对主权国家，这一档开放解决的都是真问题。我 7 月写[制裁话题](/zh/sanctioning-open-weight-models)时查过，Hugging Face 文本生成模型下载榜前 30 里中国权重占 18 席，这个生态是真实需求堆出来的。

但从科研的账本上数一数没给的东西：训练数据没有，训练代码没有，中间 checkpoint（训练过程中定期存档的模型快照）没有，训练日志没有。写这篇文章时我把 Kimi-K3 的 Hugging Face 仓库翻了一遍：权重有，技术报告有，上面四样一样都没有。DeepSeek、Qwen 的主力模型也是同一个配置。

Linux 基金会 2024 年提出的 Model Openness Framework 给开放程度做了分级（[arXiv:2403.13784](https://arxiv.org/abs/2403.13784)，[LF AI & Data](https://lfaidata.foundation/blog/2024/04/17/introducing-the-model-openness-framework-promoting-completeness-and-openness-for-reproducibility-transparency-and-usability-in-ai/)）：Class III 叫「开放模型」，放出架构、权重和基础文档；Class II 叫「开放工具」，加上全套训练与评估代码和关键数据集；Class I 叫「开放科学」，再加上原始训练数据、完整技术报告、中间 checkpoint 和日志。当红的开放权重模型基本都停在 Class III。Landay 管这一档叫「开放分发」：开的是发行渠道，源头还锁着。他主张科研和公共利益场景需要的是 Class I。

## 隔着玻璃，有三件事做不了

第一件，审计。不知道训练语料的构成，一串问题就永远只能猜：benchmark 高分是真能力还是背过题（训练集混入测试题的「污染」问题，只有对着语料查才能排除）；模型对不同人群的刻画偏差从哪来；哪些文化假设被写进了默认答案。外部研究者能做的只剩行为测试——隔着玻璃观察一台机器，记录它对各种输入的反应，再推测内部构造。Landay 的说法是，研究者「只能从外部观察成品系统，猜测它为什么这样行为」。

行为测试的天花板有多低，有现成的参照。我 7 月[写过 Kimi K2.5 的第三方安全评估](/zh/kimi-k3-open-weight-audit-gap)：十家机构、38 个行为维度、两万多条评委打分，是公开检索范围内对此类模型最认真的一次独立评估——而它从头到尾都在行为侧，能告诉你模型对隐蔽破坏指令的服从率是 65%，回答不了这个倾向是哪部分训练带出来的。

这个缺口有多现实，7 月下旬正好出了一个地缘政治级别的例子。白宫科技政策办公室主任 Michael Kratsios 公开指认：Moonshot 是靠大规模蒸馏 Anthropic 的 Fable 5 造出 Kimi K3 的（[SCMP](https://www.scmp.com/news/us/diplomacy/article/3361510/trump-tech-official-accuses-chinas-moonshot-ai-stealing-anthropic)）。蒸馏，指拿别家模型的输出当自己的训练数据，把能力「抽」过来。这项指控没有附带公开可查证的证据。然后呢？没有然后——K3 的训练数据不公开，第三方既证实不了指控，也还不了 Moonshot 清白。一场牵动制裁威胁的争端，落在一个结构上无法查证的问题上。

第二件，复现。科学的基本单位是可复现的实验。现代 AI 的几次架构跃迁——transformer、注意力机制、专家混合路由——全部出自其他实验室能质疑、能复现、能改进的公开研究，这是 Landay 文中特意点出的历史。开放权重让你研究「这个模型」，但研究不了「怎么造出这样的模型」：数据配比怎么影响能力，某项能力在训练的哪个阶段冒出来（这需要中间 checkpoint），换一种数据清洗方式结果差多少。这些问题的答案锁在训练过程里，权重文件里没有。

第三件，对照。真正做到 Class I 的模型存在：Ai2 的 OLMo 3，权重、Dolma 3 预训练数据、OLMoCore 训练代码、中间 checkpoint、技术报告全部公开（[Ai2](https://allenai.org/olmo)）。但它最大的版本是 32B，和 Kimi K3 的 2.8T 差着接近两个数量级。当下的真实格局一句话可以说完：**可审计的不前沿，前沿的不可审计。**

顺带把一条此前理过的线接上：开放深度这条轴，和「中国还是美国」那条轴是垂直的。下载榜由中国权重占大头，而目前把开放做到最深的 OLMo 出自美国非营利机构。「开放权重强国」推不出「开放科学强国」，反过来也一样。

## 停在权重档不是过渡期，是稳态

为什么厂商都停在 Class III？把激励摆开就清楚了。开放权重的收益——生态采用、开发者心智、行业标准话语权、对冲闭源对手——在权重这一档就几乎全部兑现。继续往深开，收益骤减，成本陡增：原始语料一公开，版权诉讼的证据开示等于自动完成；数据配比和清洗流程被业内当作核心竞争资产；抓取来源里的灰色地带全部见光。开数据的账算不平，所以没人开。

这意味着 Class III 不该被理解成通往 Class I 的中间站。它是激励结构算出来的停靠点，没有外力不会自己往深处滑。

Landay 由此把担子指向大学：只有不被产品周期追着跑的机构，才会为验证而发表、为长线问题投入。方向我同意，但他轻描淡写了硬约束：算力。OLMo 3 停在 32B，大体就是非营利机构算力现状的写照，而前沿规模还在涨。指望公共机构把 Class I 做到 2.8T 不现实；现实一点的读法是双轨——前沿能力由商业公司以权重档开放，科学基线由公共机构以全开模型维护，研究者先在小而全透明的模型上回答机制问题，再到大模型上验证结论是否外推。这条双轨能走多宽，取决于公共算力投入的力度。而这个夏天的政策辩论——出口管制、公开信、制裁威胁——没有一分钟花在这上面。

回到那两个问题。「谁能拿到模型」吵了一整个夏天，从华盛顿吵到 Hugging Face；「谁能理解模型」没排上议程。Landay 的收尾我照原意译一下：如果「开源」的意思被压缩成「可下载」，那我们只是把一个封闭实验室换成了另一个，换了面旗子而已。下次看到「开源模型」四个字，先别问它是谁家的，先问它开到第几级——权重、代码，还是数据。前一个问题决定你能不能用它，后一个问题决定所有人能不能看懂它。

## 参考来源

- [Open-weight models aren't enough — we need truly open source AI models for science and society（Stanford HAI）](https://hai.stanford.edu/news/open-weight-models-arent-enough-we-need-truly-open-source-ai-models-for-science-and-society) — 本文主要讨论对象；Landay 的「两问」、「开放分发」提法、transformer 等架构史论证
- [Statement on the US government directive to suspend access to Fable 5 and Mythos 5（Anthropic）](https://www.anthropic.com/news/fable-mythos-access) — 出口管制指令的时间、范围与 Anthropic 回应原文
- [U.S. lifts ban on Anthropic's powerful Fable 5 AI model（NBC News）](https://www.nbcnews.com/business/business-news/commerce-department-gives-green-light-anthropic-bring-back-fable-5-rcna352501) — 上线三天被下线的时间线、解禁经过
- [Anthropic says Trump admin has lifted export controls（CNBC）](https://www.cnbc.com/2026/06/30/anthropic-says-trump-admin-has-lifted-export-controls-on-claude-fable-5-and-mythos-5.html) — 解禁日期
- [moonshotai/Kimi-K3（Hugging Face）](https://huggingface.co/moonshotai/Kimi-K3) — 亲自核对仓库内容：有权重和技术报告，无训练数据、训练代码、中间 checkpoint
- [Nvidia, Microsoft, Meta warn against 'premature restrictions' of open-weight models（CNBC）](https://www.cnbc.com/2026/07/24/nvidia-microsoft-meta-open-weight-ai-models.html) — 公开信内容与首批 25 家签署方
- [Huang's Open Weights Letter Doubled To 50 Without Amazon And Anthropic（Forbes）](https://www.forbes.com/sites/sandycarter/2026/07/25/huangs-open-weights-letter-doubled-to-50-without-amazon-and-anthropic/) — 签名一天翻倍至 50 家、OpenAI/Google 补签、Anthropic 缺席
- [The Model Openness Framework（arXiv:2403.13784）](https://arxiv.org/abs/2403.13784) — Class I/II/III 三级定义
- [Introducing the Model Openness Framework（LF AI & Data）](https://lfaidata.foundation/blog/2024/04/17/introducing-the-model-openness-framework-promoting-completeness-and-openness-for-reproducibility-transparency-and-usability-in-ai/) — 分级官方说明
- [Trump tech official accuses China's Moonshot AI of stealing from Anthropic（SCMP）](https://www.scmp.com/news/us/diplomacy/article/3361510/trump-tech-official-accuses-chinas-moonshot-ai-stealing-anthropic) — Kratsios 蒸馏指控
- [OLMo（Ai2）](https://allenai.org/olmo) — OLMo 3 的开放范围（数据/代码/checkpoint/报告）与 7B/32B 规模
- 站内：[制裁挡不住模型，只能决定谁用它](/zh/sanctioning-open-weight-models)、[3万亿参数开源了，安全评估还在路上](/zh/kimi-k3-open-weight-audit-gap) — HF 下载榜数据、K2.5 第三方评估细节的原始出处
