---
title: "被水印吓到之前，先让老板和老师回答：到底什么算违规"
description: "Anthropic 给 Claude 输出加隐形水印，用户在 Reddit 上炸了锅。拆解这类水印在技术上能检测什么、什么时候失灵，以及「被抓」的恐慌为什么该由规则缺位的雇主和学校来回答。"
pubDate: 2026-08-12
tags: [ai-governance, watermarking, trust-and-safety]
lang: zh
slug: claude-watermark-backlash
translationOf: claude-watermark-backlash
---

8 月 11 日，Anthropic 宣布给 Claude 生成的文本嵌入隐形水印（[我在当天的快讯里报过](/zh/briefing-2026-08-11)）。第二天，TechCrunch 发了一篇标题很直白的后续：[部分 Claude 用户很愤怒，因为水印会让他们在工作和课堂上用 AI 的事被抓包](https://techcrunch.com/2026/08/12/some-claude-users-are-mad-that-anthropics-new-watermarks-will-catch-them-cheating-at-their-jobs-classes/)。

据 TechCrunch 引述，Reddit 上一位用户这样写：「谁会被抓？是你。那个用 Claude 重新组织了一段话的学生……这些人走完流程，脑门上就多了一个数字纹身。」另一位说这个方向「非常阴险」，并把讽刺指向行业自己的老账：给用户的产出加水印，「考虑到这些前沿模型的训练数据是怎么来的，讽刺得吓人」。支持的声音同样不少，最典型的一句是：「实在找不出反对它的理由。你不想要它的唯一原因，就是想骗人。」

两边吵的其实不是同一件事。要看清争议，得先回答两个问题：这个水印在技术上到底能检测出什么？以及「被抓」这件事，责任该算在谁头上？

## 先摆事实：这是合规动作

直接动因是欧盟《AI 法案》第 50 条：生成式 AI 的提供方必须给合成内容打上机器可读的标记，这条义务 2026 年 8 月 2 日起生效（[EUR-Lex 法案原文](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32024R1689)），违反最高可罚 1500 万欧元或全球年营收的 3%，取高者（[Euronews](https://www.euronews.com/next/2026/08/11/eu-compliance-delivered-globally-anthropic-to-watermark-claudes-output-worldwide)）。配套还有一份自愿性的[《AI 生成内容标记与标注行为准则》](https://digital-strategy.ec.europa.eu/en/news/commission-publishes-first-draft-code-practice-marking-and-labelling-ai-generated-content)，由独立专家起草、欧盟委员会促成，2025 年 12 月出初稿、2026 年 6 月定稿；Anthropic 在[官方帮助页](https://support.claude.com/en/articles/16266773-how-claude-marks-ai-generated-content)确认自己是这份准则的签署方。

具体做法上，我能找到的最详细的一手说明是 [Anthropic 的官方帮助页](https://support.claude.com/en/articles/16266773-how-claude-marks-ai-generated-content)：文本嵌入一个肉眼不可见、不改变含义和可读性的水印，复制粘贴后仍在，部分编辑后可能保留；生成受支持的文件类型（如 .png、.jpg、.svg）时，附上 C2PA 标准的签名元数据——[C2PA](https://c2pa.org/) 是内容溯源的开放标准（[规范全文](https://spec.c2pa.org/specifications/specifications/2.2/specs/C2PA_Specification.html)），相当于给文件配一张防篡改的出处证明。范围是全球生效，不限欧盟用户，覆盖 API、claude.ai、Claude Code 等全部入口，以及经 AWS、Google Cloud、Microsoft Foundry 调用的版本。8 月 2 日之后发布的新模型出厂即带；之前的旧模型「正在补加」，Anthropic 自己没给完成日期，法规层面倒有一条线：欧盟今年 7 月通过的过渡条款要求 8 月 2 日前已上市的系统最迟在 2026 年 12 月 2 日前完成合规（[Regulation (EU) 2026/1744](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=OJ%3AL_202601744)；[欧盟委员会 FAQ](https://digital-strategy.ec.europa.eu/en/faqs/code-practice-transparency-ai-generated-content)）。也就是说，取决于你用的具体是哪个模型，你此刻在用的那一个未必已经带上了。

最值得较真的一句写在这份官方说明里：检测到水印，只能说明内容「可能被 Claude 处理过」，官方明确说这「并非完全定论」。这句话是理解全部争议的钥匙，下文回来收它。

## 机制：水印怎么藏进普通的字里

Anthropic 没公开具体算法，检测机制的技术文档也说是后续发布。但文本水印在学界和同行那里已有成熟的公开做法（欧盟委员会为行为准则委托了[三份关于标记与检测技术的研究](https://digital-strategy.ec.europa.eu/en/library/three-studies-technical-solutions-mark-and-detect-ai-generated-content)作为依据），可以拿来对照。

公开文献里最有名的一族是统计采样水印。模型生成文字的方式是一个词一个词往外挑：每写下一个词之前，它手里有一串候选词，各带一个概率。水印算法用一把只有厂商掌握的密钥，在每一步从候选词里划出一部分「偏好词」，悄悄给它们加一点概率。单看任何一句话都毫无异常，因为被加分的词本来就是合理选项；但文本积累到足够长，拿同一把密钥重新核对，「偏好词」出现的频率会明显高出自然写作的水平，统计检验就能判定这段文字带水印。这套方法 2023 年就公开发表了（[Kirchenbauer 等人的论文](https://arxiv.org/abs/2301.10226)）；「足够长」没有固定门槛，因为论文的检验统计量随词元数量和采样偏置的强度增长，能不能检出取决于算法参数和文本本身。Google DeepMind 的 [SynthID](https://deepmind.google/science/synthid/) 走的是同一条在生成阶段调整候选词概率的路线（[官方技术说明](https://deepmind.google/blog/watermarking-ai-generated-text-and-video-with-synthid/)），具体算法不同，已在 Gemini 上线。

这个原理恰好解释了官方帮助页列出的每一条特性：复制粘贴不掉，因为词还是那些词；重度改写、翻译、混入自己的文字后可能失效，因为词被换掉，统计信号被稀释；太短的段落往往难以可靠检出，因为统计检验需要样本量。另一族技术是往字符层塞特殊字符，比如宽度为零、肉眼看不见的「[零宽空格](https://en.wikipedia.org/wiki/Zero-width_space)」，但那种记号用 Unicode 归一化或简单的字符过滤就能程序化地查出并剥掉，透明度价值很低。从公开特性看，Claude 的水印更像统计采样一族——这是我的推断，不是已证实的事实：Anthropic 没有说，公开信息也排除不了字符层或混合方案。下文凡是依赖这个推断的部分，都带着同样的不确定性。

## 能检测什么，什么时候失灵

把上面的边界连起来看。按官方列出的特性，能留下记录的是足够长、基本原样使用的 Claude 输出。整段粘贴进作业、报告、邮件，水印跟着走。

很可能检不出的：重度改写过的文本，翻译成另一种语言的文本，短句和只言片语。官方把这些列为水印可能失效的情形，Google 对 SynthID 的说明也一样——信号被大幅削弱，漏检概率变大，但两边都没把话说死。还有最关键的一条：它区分不了「Claude 写的」和「Claude 碰过的」。你自己写完一整篇，丢给 Claude 修错别字，出来的文字也可能带上记号。水印的语义是「处理过」，不含「代写」的意思。

再看绕过的路径，得一条条分开算——仍然以「Claude 用的是统计采样」这个未经证实的推断为前提。照着屏幕重新打一遍，听上去最彻底，其实对这一族水印无效：记号藏在「选了哪些词」里，不在文件或字符层（[Kirchenbauer 等人](https://arxiv.org/abs/2301.10226)的检测就是直接对选词本身重新打分），你一字不差地重新敲出来，词还是那些词，记号原样带走；重打能洗掉的只有零宽字符那类藏在字符里的标记。让另一家的模型转写一遍，确实可能稀释 Claude 的统计信号——改写和翻译会大幅削弱这类水印，Kirchenbauer 团队和 Google 都承认，不过[同一团队的后续研究](https://arxiv.org/abs/2306.04634)发现，即使经过人工重度改写，观察到大约 800 个词元后信号仍然可以检出；而且如果那家也部署了水印（Gemini 的 SynthID 已经上线），转写出来的文字又可能带上对方的记号，最终能不能被检出，取决于文本长度和各家检测器的门槛，并不是稳赚的洗白。这样数下来，不需要技术能力的出路是两条：自己动手重度改写，或者一开始就换一个不加水印的模型。攻击研究的文献里还列了更多花哨的办法，但没有一种能保证漏检。这两条简单出路要的只是多花功夫，或者换个工具。

如果上面这幅图景成立，它指向的方向和愤怒正相反。我的判断是——这是对激励结构的推断，没有部署数据支撑——水印筛出的不是最想作弊的人，而是最不设防的人。蓄意隐瞒的人有现成的出路；会被留下记录的，是那些没想过要防备的用法。「数字纹身」那句话里，真实的部分是这个。

还有一个决定走向的细节：检测器在谁手里。Anthropic 目前没有公开检测工具；Google 的 SynthID 检测门户正向早期测试者开放，等候名单面向记者、媒体从业者和研究人员（[官方公告](https://blog.google/innovation-and-ai/products/google-synthid-ai-content-detector/)）。如果检测能力只发放给平台和机构，普通人连「我这段文字带没带记号」都无从自查。检测者和被检测者之间的信息差，比水印本身更值得盯。

## 「被抓」的责任在谁

欧盟的义务分配写得清楚：给内容打标记是模型厂商的法定义务（[第 50(2) 条](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32024R1689)）；「用 AI 算不算违规」的日常边界，主要握在学校和雇主手里，法律和行业监管划的是外圈底线。前一项从 8 月 2 日起有法律和罚款盯着；后一项有多少组织写成了文，我没见到统计，只能说就我个人接触到的范围，没有一家写了。「重新组织一段话的学生」会恐慌，正因为从没有人说清这算不算违规。

水印的出现把这个空白从「可以拖」变成「拖不下去」。我担心的是——这是预测，不是我能拿出证据的事实——没有成文规则的组织会倾向于直接拿检测结果当规则用。概率性的检测信号一旦接入执行流程，置信度的细节容易被丢掉，「可能处理过」到了一线执行环节被按「违规」处理，举证的成本落到被标记的人身上。官方帮助页写明检测结果并非定论，但处罚流程不读帮助页。

回头看那句「你不想要水印的唯一原因就是想骗人」——它成立的前提，是「什么算骗」有共识。眼下恰恰没有：同一个「用 Claude 重新组织段落」，在一家公司可能是被鼓励的效率工具，在一门课上可能被按学术不端处理。水印测得出「机器碰过」，测不出这些边界。边界只能由规则给出。

## 我的判断

对个人，主线只有一条：别在技术层面对抗，去把规则问出来。研究怎么洗掉水印没有意义——会失效的情形官方等于已经列给你了，但水印证明力的模糊是双向的：它定不了你作弊，也还不了你清白。真正能保护你的是一句成文的「这类任务允许用 AI」。在规则落地之前，把假设调成「凡是新模型产出的文字都可能被识别」，比赌检测器测不出来可靠。

对行业：第 50 条的标记义务覆盖欧盟市场上的生成式 AI 提供方，但给只提供常规编辑辅助、或不实质改变输入内容的系统留了豁免（[第 50(2) 条](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32024R1689)）。Google 有现成技术在生产环境运行，合规的方向是给定的。照这个趋势，我判断文字水印会逐渐成为主流模型的出厂默认——这是预测，不是既成事实。真到那一步，「用没用 AI」也不会变成一测便知的铁证——水印给出的是绑定单一厂商密钥的概率信号（今天公开的方案都是这么工作的），短文本和重度改写照旧漏检（[Google 自己的定性](https://deepmind.google/blog/watermarking-ai-generated-text-and-video-with-synthid/)）——但对足够长、原样使用的输出，这件事会比今天可测得多。而「被允许怎么用 AI」有没有成文规则，还是要一家一家组织自己回答的问题。水印真正逼出来的，是这个回答。

## 参考来源

- [Some Claude users are mad that Anthropic's new watermarks will catch them cheating（TechCrunch, 2026-08-12）](https://techcrunch.com/2026/08/12/some-claude-users-are-mad-that-anthropics-new-watermarks-will-catch-them-cheating-at-their-jobs-classes/) — 用户反弹与全部 Reddit 引语
- [Anthropic says it will watermark text generated by its AI models（TechCrunch, 2026-08-11）](https://techcrunch.com/2026/08/11/anthropic-says-it-will-watermark-text-generated-by-its-ai-models/) — 发布报道，及「删除水印需要多少编辑量尚不清楚」的未答问题
- [How Claude marks AI-generated content（Anthropic 官方帮助中心）](https://support.claude.com/en/articles/16266773-how-claude-marks-ai-generated-content) — 一手来源：技术方式、覆盖范围、时间线、行为准则签署确认、「处理过≠作者」的官方定性
- [Commission publishes first draft Code of Practice on marking and labelling of AI-generated content（欧盟委员会）](https://digital-strategy.ec.europa.eu/en/news/commission-publishes-first-draft-code-practice-marking-and-labelling-ai-generated-content) — 行为准则的起草方式（独立专家起草、委员会促成）、时间线与第 50 条生效日期
- [Commission FAQ on the Code of Practice for transparency of AI-generated content（欧盟委员会）](https://digital-strategy.ec.europa.eu/en/faqs/code-practice-transparency-ai-generated-content) — 已上市系统的 2026 年 12 月 2 日过渡期限
- [EU AI Act 法案原文（EUR-Lex）](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32024R1689) — 第 50 条机器可读标记义务及其豁免条款
- [Regulation (EU) 2026/1744（EUR-Lex）](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=OJ%3AL_202601744) — 给 2026 年 8 月 2 日前已上市系统的四个月标记义务过渡期
- [EU compliance, delivered globally（Euronews, 2026-08-11）](https://www.euronews.com/next/2026/08/11/eu-compliance-delivered-globally-anthropic-to-watermark-claudes-output-worldwide) — 全球生效范围、罚款数额（1500 万欧元或全球年营收 3%）
- [A Watermark for Large Language Models（Kirchenbauer et al., arXiv:2301.10226）](https://arxiv.org/abs/2301.10226) — 统计采样水印（绿名单偏置 + 统计检验）的公开方法
- [On the Reliability of Watermarks for Large Language Models（Kirchenbauer et al., arXiv:2306.04634）](https://arxiv.org/abs/2306.04634) — 改写会削弱但不能可靠抹掉统计水印；人工重度改写后约 800 词元仍可检出
- [SynthID（Google DeepMind）](https://deepmind.google/science/synthid/) — 同路线技术已在 Gemini 部署
- [SynthID Detector 公告（Google, blog.google）](https://blog.google/innovation-and-ai/products/google-synthid-ai-content-detector/) — 检测门户的开放安排：先面向早期测试者，等候名单面向记者、媒体从业者与研究人员
- [Watermarking AI-generated text and video with SynthID（Google DeepMind Blog）](https://deepmind.google/blog/watermarking-ai-generated-text-and-video-with-synthid/) — 文本水印的候选词概率机制、失效情形与「不是万能方案」的官方定性
- [本站快讯 2026-08-11](/zh/briefing-2026-08-11) — 水印上线的首次报道
