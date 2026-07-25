---
title: "提示注入快被『解决』了吗？Opus 5 发布里被埋掉的那一页"
description: "Opus 5 把间接提示注入的攻击成功率压到 2%，但这句话不在发布公告里，而在系统卡第 73 页——数字怎么读、离『解决』还有多远"
pubDate: 2026-07-24
tags: [prompt-injection, ai-safety, agent-security]
lang: zh
slug: opus-5-prompt-injection-system-card
translationOf: opus-5-prompt-injection-system-card
---

7 月 24 日 Anthropic 发布 [Claude Opus 5](https://www.anthropic.com/news/claude-opus-5)。公告是标准的能力叙事：Frontier-Bench 和 GDPval-AA 新 SOTA，ARC-AGI 3 得分是次优模型的三倍，还有一句「我们迄今对齐最好的模型」。

但对做 agent 安全的人来说，这次发布最重要的信息不在公告里。我把公告通读了一遍，「prompt injection」（提示注入）一词一次都没出现。它被放在了[系统卡](https://www.anthropic.com/claude-opus-5-system-card)第 5.2 节，第 71 到 76 页。连 Anthropic 自己人都看不下去——Claude Code 的作者 Boris Cherny（Anthropic [官方活动页](https://www.anthropic.com/webinars/claude-code-service-delivery)称其为「Claude Code 的发明者」）发布后[在 X 上说](https://twitter.com/bcherny/status/2080713091688583312)：

> "Opus 5 is our least prompt injectable model yet. It is a bit buried in the system card, but across PI evals and red teaming, Opus 5 is very hard to prompt inject successfully."

（Opus 5 是我们迄今最难被提示注入的模型。这一点有些埋没在系统卡里，但从提示注入评测到红队测试，成功注入 Opus 5 都非常困难。）

先把一件事说清楚：「迄今最难被提示注入」这个断言，出自员工个人帖子。系统卡的正式表述是：「Opus 5 在我们的 agentic 安全套件上与 Claude Opus 4.8 相当或更好，提升最大的是编码、计算机使用和浏览器使用场景下的提示注入鲁棒性」。这不是抠字眼——断言出自哪份文件、承诺范围多大，决定了你能不能拿它当部署决策的依据：个人帖子表达的是员工的观感，系统卡才是厂商愿意为之负责的正式文件。

## 数字本身：从 5.5% 到 2.0%

所谓间接提示注入（indirect prompt injection），指攻击者把恶意指令藏在 agent 会读取的内容里——网页、邮件、文档——让模型把这些内容当成用户指令去执行。这是 agent 落地的主要安全风险之一：OWASP 把提示注入列在 [LLM 应用十大风险的首位](https://genai.owasp.org/llm-top-10/)。一个能替你读邮件、订机票的助手，也能被一封邮件指挥着把你的收件箱转发出去——这不是凭空设想的场景，OWASP 的 [Excessive Agency 风险条目](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/)给出的示例正是恶意邮件诱使 agent 扫描收件箱并把敏感信息外发给攻击者。

系统卡引用了安全评测公司 Gray Swan 的间接提示注入基准。核心数字（出自系统卡第 73 页图表，完整表格数值经多方转述交叉核对，见文末参考来源）：

| 模型 | 单次尝试成功率 | 15 次尝试内成功率 |
|---|---|---|
| Opus 5 | 0.2% | 2.0% |
| Opus 4.8 | 0.5% | 5.5% |
| Mythos 5 | 0.3% | 2.6% |
| GPT-5.6 Sol | 3.1% | 20.0% |
| Gemini 3.1 Pro | 14.2% | 49.2% |

三个观察。

第一，纵向进步是真的，而且快。八个月前 Opus 4.5 的系统卡里，同样来自 Gray Swan 的评测显示单次强攻击成功率 4.7%，十次尝试内 33.6%（[The Decoder 当时的报道](https://the-decoder.com/claude-opus-4-5-resists-prompt-injections-better-than-rivals-but-still-falls-to-strong-attacks-alarmingly-often/)）。两代评测的具体设置未必完全可比——基准版本和攻击预算都可能调整过——但量级趋势明确：从「多试几次必然打穿」到「15 次预算内 2%」，不到一年。

第二，横向差距是量级差距。GPT-5.6 Sol 在 15 次预算下 20%，是 Opus 5 的十倍。Gemini 3.1 Pro 的数字接近一半，但系统卡注明它参与过该评测攻击样本来源的竞赛，结果不能与其他模型直接比较，横向解读要留这个心眼。即便把 Gemini 放在一边，提示注入鲁棒性目前也不是各家挤在一起的赛道，而是拉开了 10 倍的分布。

第三个细节容易被忽略：Opus 5（2.0%）比 Mythos 5（2.6%）还略好。这里先交代一下 Anthropic 这批模型的命名，免得表格看着糊涂：Mythos 是 Anthropic 新设的能力档位，[官方公告](https://www.anthropic.com/news/claude-fable-5-mythos-5)写明它「在能力上位于 Opus 档之上」，现阶段只向 Glasswing 网络安全合作方开放，并计划开放给少数生物研究者；普遍可用的受防护版本叫 Claude Fable 5——底层就是 Mythos 5 同一个模型，只是加装了针对网络安全、生物化学等高危话题的分类器护栏（触发时改由 Opus 4.8 应答）。所以表里的对比是：定位更高的 Mythos 5，注入成功率反而比 Opus 5 略高。至少在这项评测里，注入鲁棒性并没有随模型能力同步上涨——这也解释了为什么这个数字值得单独看，而不能从能力跑分里推出来。

## 2% 不是「解决」，是攻击成本上升

现在把数字放进真实部署场景。评测里的「15 次尝试」是给攻击者设的预算上限，但现实里的攻击面不按次数计费：一个每天替你处理几百封邮件、浏览几十个网页的 agent，暴露量远超评测设定。这个外推要打个折扣——现实中 agent 读到的每份内容并不是独立同分布的攻击样本，攻击者往往不清楚你的具体部署，反复尝试也会增加自己暴露的风险——但方向没变：对持续暴露的系统，多次尝试下的成功率比单次数字更接近真实风险。这就是为什么读这类评测要先看 15 次那一列——攻击者不着急。

系统卡里另一组数字把这件事的结构讲得更清楚：浏览器使用场景下，不加任何防护时，攻击成功率从 Opus 4.8 的 31.5% 降到 Opus 5 的 3.7%；叠加 Anthropic 的运行时防护后，129 个测试环境里成功率为 0%。

这组数字的正确读法是分层：3.7% 是模型本体的鲁棒性，0% 是「模型 + 系统防护」的组合结果。两者都有用，但含义不同。模型本体的提升跟着模型走；那条 0% 的线则叠加了 Anthropic 自家的运行时防护，系统卡只确认它用在 Anthropic 自己的产品形态里——换一套部署框架，未必有现成的等价物。而 129 个环境全防住，也不等于现实世界为零：基准环境有限，真正的对手会针对防护本身做自适应优化，公开的「评测里 0%」很可能就是下一轮红队瞄准的靶子。

## 给部署者的三个判断

**读系统卡时，找多次尝试的成功率，并确认测的是裸模型还是带防护的系统。**厂商有动机把最好看的那条线放在最显眼处。Opus 5 这次的信息分层本身就说明问题：能力数字进公告标题，安全数字进系统卡第 73 页——好在这次埋进去的数字也拿得出手，员工才会主动指给你看。反过来想：没被指出来的页码里写了什么，才更值得翻。

**架构上继续假设注入必然发生。**2% 时代和 33% 时代的正确架构是同一套：[最小权限、敏感操作人工确认](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/)（OWASP 对 agent 权限过大风险给出的标准缓解措施），加上不可信内容与指令通道隔离。区别只在于这些措施从「唯一防线」变成了「纵深防御的外层」。如果你的 agent 拿着全量权限裸奔，模型再鲁棒也救不了你。

**把提示注入鲁棒性当成独立采购指标。**这次的数据显示它和模型能力、甚至和同厂更高端的型号都不同步。选 agent 底座时，能力跑分和注入鲁棒性要分开问、分开验——后者厂商未必主动给，系统卡里有没有、写得多细，各家做法不一，拿不到本身就是个信号。

提示注入没有被解决，它只是正在从「防不住」变成「可以工程化压制」的问题。这条曲线还在往下走，但走到哪一天都替代不了系统设计——单次 0.2% 看着接近零，架不住暴露量按天累积，防线不能只剩模型这一层。

## 参考来源

- [Introducing Claude Opus 5（Anthropic 官方公告）](https://www.anthropic.com/news/claude-opus-5) — 发布日期、能力断言；核实公告正文未提及 prompt injection
- [Claude Fable 5 and Claude Mythos 5（Anthropic 官方公告）](https://www.anthropic.com/news/claude-fable-5-mythos-5) — Mythos 档位「在能力上位于 Opus 档之上」、Fable 5 与 Mythos 5 同底层模型、护栏触发时回落 Opus 4.8、Mythos 5 现阶段限 Glasswing 合作方及后续选定的生物研究者
- [Claude Opus 5 System Card（PDF）](https://www.anthropic.com/claude-opus-5-system-card) — 第 5.2 节（71–76 页）原文措辞「largest gains in prompt injection robustness across coding, computer use, and browser use」
- [Boris Cherny 的 X 帖](https://twitter.com/bcherny/status/2080713091688583312) — 「least prompt injectable model yet」引言（X 原帖无法直接抓取，引文经 [Simon Willison 的转录](https://simonwillison.net/2026/Jul/25/boris-cherny/)核对）
- [Anthropic 官方活动页](https://www.anthropic.com/webinars/claude-code-service-delivery) — Boris Cherny 身份（「inventor of Claude Code」、Head of Claude Code）
- [OWASP GenAI：LLM Top 10](https://genai.owasp.org/llm-top-10/) 与 [LLM06: Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/) — 提示注入列 LLM01 首位；恶意邮件诱使 agent 外发收件箱内容的示例场景与缓解建议
- [MarkTechPost 报道](https://www.marktechpost.com/2026/07/24/meet-the-new-claude-opus-5-frontier-class-agentic-coding-and-computer-use-at-unchanged-opus-pricing/) — Gray Swan 15 次尝试数字、浏览器场景 31.5%→3.7%→0%（129 环境）的交叉核对
- [JAIKIN：Opus 5 benchmarks](https://www.jaikin.eu/blog/opus-5-benchmarks) — Gray Swan 完整对比表（含单次尝试与 Gemini 3.1 Pro 数值）的交叉核对
- [The Decoder：Claude Opus 4.5 提示注入报道](https://the-decoder.com/claude-opus-4-5-resists-prompt-injections-better-than-rivals-but-still-falls-to-strong-attacks-alarmingly-often/) — Opus 4.5 历史数字（单次 4.7%、十次内 33.6%）
