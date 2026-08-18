---
title: "只有 15% 的美国人信任 AI 公司：Anthropic 把这道题公开挂了出来"
description: "复盘 Anthropic 的 hard questions 计划：民调数据是实的，追踪机制还只是一块刚立起来的记分牌"
pubDate: 2026-08-17
tags: [ai-governance, public-trust, anthropic]
lang: zh
slug: anthropic-hard-questions-trust
translationOf: anthropic-hard-questions-trust
---

8 月 16 日，投资人 Gavin Baker 在播客和 X 上公开指责 Dario Amodei：你天天讲 AI 风险，助燃了美国公众对 AI 和数据中心的反弹。Amodei 的回应（[X 原帖](https://x.com/DarioAmodei/status/2088758819304443967)，另见 [TechCrunch](https://techcrunch.com/2026/08/16/anthropic-ceo-says-ai-backlash-is-fundamentally-a-crisis-of-trust/)）我在[前一天的快讯](/zh/briefing-2026-08-16)里收录过：公众的负面情绪「本质上是一场信任危机」，根子是普通人不信任公司、政府和科技行业，总怀疑他们在琢磨新的法子坑自己。

这句话其实不是临场发挥。一个月前的 7 月 9 日，Anthropic 发过一篇官方博文《[Inviting hard questions](https://www.anthropic.com/news/hard-questions)》（邀请硬问题），是这套说法的完整版。当时它没进我的视野；这场隔空争论让它有了重读的价值。我把博文和它引用的配套材料读了一遍，想回答一个问题：这是公关，还是有可核查的实质承诺。

## 博文说了什么

博文以四个问题开场：谁为 AI 制定规则？AI 能给我的孩子更好的未来吗？AI 会让世界更危险吗？AI 能帮科学家治愈疾病吗？然后逐条承认公众的顾虑：担心失业、担心创意工作贬值、担心人的自主性——AI 会不会削弱独立思考、人际连接和生活的意义感。

Anthropic 给出的回应分几层：列举了已做的调研（下文细说）；列举了在做的事，包括投入滥用防护、研究模型行为与内部机制、向科学家免费提供模型、一个叫 Claude Corps 的项目（把早期职业阶段的 Claude 用户和非营利组织配对）、一个叫 Anthropic Institute 的内部研究项目（目标是「直面 AI 将给社会带来的最重大挑战」）。最后是核心承诺：公众可以提交自己最难的问题，公司「将公开追踪并报告为回应这些问题所采取的具体行动」（原文：we'll publicly track and report the specific actions we're taking to address those questions），并表示有些目标达不成时也会如实说明。

## 拆开看：一份实的，一份软的，一句硬的

把内容按可核查程度分类，成色立刻分明。

**实的是数据。** 博文引用的 [Anthropic Public Record](https://www.anthropic.com/news/anthropic-public-record) 是公司委托英国民调机构 YouGov 做的全国性调查，2025 年 11 月 1 日至 12 月 11 日执行，样本 51,993 名美国人，结果今年 6 月 12 日公开。数字对公司相当不利：只有 15% 的美国人表示信任 AI 公司来决定 AI 如何被开发和使用；64% 担心 AI 导致失业；56% 担心认知依赖（AI 用多了让人失去独立思考的能力）；71% 认为政府应当参与 AI 的开发和监管。另有一项覆盖 159 个国家、70 种语言、81,000 名 Claude 用户的调查，加上一系列线下焦点小组。

敢把 15% 这个难看的数字自己发出来，是加分项。多数公司的公关部门会把它埋进附录。但民调本身只是测量，测出病灶和治病是两回事。

**软的是机构。** Anthropic Institute 目前只有一句目标描述，是公司内部的研究项目，没有独立地位；Claude Corps 是一个配对性质的 fellowship。两者都还没有可考核的产出指标。Anthropic 常被引用的独立监督机制是 Long-Term Benefit Trust（长期利益信托）：一个由不持公司经济利益的受托人组成的信托，持有特殊类别股份、有权任命部分董事会成员。但博文没有把 hard questions 的追踪和核查交给它，也没有交给任何第三方。

**硬的只有那一句承诺**——公开追踪、公开报告。我去看了承接它的网站：[claude.com/hard-questions](https://claude.com/hard-questions) 目前更像品牌页，我抓取时只看到一条展示中的问题（「AI 能否帮助更快的医学诊断？」）和一个「分享你的希望」入口；页面上「查看目前进展」的链接指向一个进度页，我用抓取工具访问被服务器拒绝（HTTP 403），没能核实上面到底列了什么。这一点我没验证成，只能如实记下。

## 为什么这套机制补不上信任缺口的核心

Amodei 自己的诊断是「怀疑公司在琢磨法子坑我们」。这种不信任的对象是利益结构：AI 的规则由谁定、定规则的人是否同时是商业受益者。而问答机制不改变利益结构——出题的是公众，判卷的还是公司自己。哪些问题被选中回应、什么程度算「已回应」、进度由谁核查、失败要不要写出来，目前都在 Anthropic 手里。

自我报告机制的通病都在这里：指标自定，口径自定，不利的项可以沉默。博文承诺过「达不成也透明」，这句写下来是要被将来对照的，但对照的前提是追踪页真的长成一份带时间戳、可逐条核对的行动清单，而目前它还是一页起步状态。

有意思的是，Amodei 在 8 月 16 日的回应里补了一句实在话：行业该做的是真的治愈癌症，而不是承诺治愈癌症。这句话等于给自家一个月前的博文划了上限——信任跟着可感知的成果走，不跟着承诺走。Public Record 里 48% 的受访者把治愈癌症、阿尔茨海默症列入对 AI 的前三期望，公众要的东西非常具体。

## 怎么判断它是不是公关：三个可检验信号

这篇博文比同行的常见做法多走了一步：把不利数据自己发出来，把承诺写成将来可以被打脸的句子。它是不是公关，不用现在下结论，未来一年内看三件事就够了。

第一，Public Record 是否如约复测。官方公告里承诺「定期重复」这项调查并扩展到美国以外。如果第二轮做了、且 15% 这类数字变差时照样公布，测量的诚意就成立。

第二，追踪页是否长出可核对的内容。判断标准很朴素：有没有具体行动条目、有没有日期、有没有「这件没做到」的记录。一面精选故事墙不算数。

第三，配套的两个政策框架是否落到具体立场。Public Record 发布时，Anthropic 同步提出了 Advanced AI Framework（提议对前沿模型做独立安全测试和透明度要求）和 Economic Policy Framework（政府如何应对 AI 的经济冲击）。真正的试金石是：当独立测试的立法版本出现、且测试方不由公司挑选时，它支不支持。71% 的美国人要政府参与监管，公司文件里也写了「独立测试」，两者能不能接上，一看便知。

我的综合判断：这不是一篇空洞的公关稿，数据部分经得起核查，承诺部分写法上留了被追责的接口。但截至今天，可核查的只有民调，追踪机制刚立起一块记分牌。记分牌本身不得分。

## 参考来源

- [Inviting hard questions — Anthropic](https://www.anthropic.com/news/hard-questions) — 博文全文：开场四问、公众顾虑清单、Claude Corps、Anthropic Institute、公开追踪承诺的原文
- [Results from first Anthropic Public Record — Anthropic](https://www.anthropic.com/news/anthropic-public-record) — 调研执行方（YouGov）、时间窗口、样本量 51,993、15%/64%/56%/71%/48% 各项数字、复测承诺、两个政策框架
- [There's hope in hard questions — claude.com](https://claude.com/hard-questions) — 承接博文的问题提交与展示页面现状
- [Dario Amodei 回应 Gavin Baker 的 X 原帖](https://x.com/DarioAmodei/status/2088758819304443967) — 「信任危机」与「真的治愈癌症」表态
- [Anthropic CEO says AI backlash is 'fundamentally a crisis of trust' — TechCrunch](https://techcrunch.com/2026/08/16/anthropic-ceo-says-ai-backlash-is-fundamentally-a-crisis-of-trust/) — 争论的媒体报道
- [AI 快讯 2026-08-16（本站）](/zh/briefing-2026-08-16) — 此前对该争论的快讯收录
