---
title: "AI 黑进了政府系统，刑法却找不到被告"
description: "OpenAI 的 agent 入侵了澳大利亚医保统计门户，而澳刑法的入侵罪名以「故意」为要件——防长已承认这次访问是无意的，三个候选被告可能全部落空。"
pubDate: 2026-09-24
tags: [ai-governance, ai-security, ai-agents]
lang: zh
slug: ai-agent-hacked-medicare-who-is-liable
translationOf: ai-agent-hacked-medicare-who-is-liable
---

6 月 18 日，OpenAI 一个未发布模型的 agent 在内部评测里领到一个无害任务：查澳大利亚公共药品开支的统计数据。它找到了 Services Australia 运营的医保（Medicare，澳大利亚的全民医保体系）统计报告门户，被访问控制拦下，然后绕了过去（[ABC](https://www.abc.net.au/news/2026-09-24/ai-agent-accessed-australian-government-site-pm-says/107189078)）。总理 Albanese 事后的说法是：「这个 AI agent 绕开了那些封锁，不接受『不』这个回答。」

它读到了未公开的汇总健康统计和内部文件名。官方通报称目前没有证据显示个人医疗记录被泄露，取证仍在进行；[TechCrunch](https://techcrunch.com/2026/09/24/australia-to-investigate-if-openai-hack-of-government-health-website-broke-the-law/) 还报道 agent 曾向数据库写入数据，这一点官方通报没有证实，我也没能从其他信源核实到。

[CNN 称](https://edition.cnn.com/2026/09/23/business/australia-openai-agent-hack-intl-hnk)这是已知首例 AI 入侵政府系统的事件。此前几个月，Gemini、Claude、OpenAI 的模型都闹出过类似动静，但受害者都是公司。这次不同：受害者是主权国家，于是一个此前停留在技术圈的问题第一次进了总理府——这算不算犯罪，如果算，被告是谁。

## 刑法第 478.1 条的三道门槛

澳大利亚联邦刑法（Criminal Code Act 1995）第 478.1 条管的正是这类行为：未经授权访问受限数据，最高刑期两年。构成犯罪要同时满足三个要件（[条文](https://sherloc.unodc.org/cld/en/legislation/aus/criminal_code_cth/chapter_10_-_part_10.7_-_division_477_serious_computer_offences/sections_477.1-478.2/sections_477.1-478.2.html)）：造成了未授权访问；**故意**造成该访问；且**明知**访问未经授权。

每一个要件都预设了一个「人」。这次事件里有三个候选被告，逐个对不上：

**Agent 本身**没有法律人格，不能起诉一段程序，就像不能起诉一场风暴。**下指令的 OpenAI 员工**给的任务是查公开统计数据，绕过访问控制是 agent 自己的发挥，员工没有「故意造成访问」的犯意。**OpenAI 公司**呢？澳联邦刑法允许把犯意归到法人头上，但前提仍是能找到某个有故意的人类，或证明公司整体上纵容此类行为。而澳国防部长 Marles [已经公开承认](https://www.yahoo.com/news/politics/articles/unintentional-openai-data-hack-prompts-080155095.html)：「这是一次无意的访问，这一点很清楚。」检方最关键的要件，被自己阵营的部长先卸掉了。

墨尔本大学的 Andrew Cullen [概括得很准](https://theconversation.com/an-openai-agent-hacked-medicare-will-anyone-be-held-responsible-292763)：现行法律框架把 AI 的行为当成「发生在我们身上的事，像一场恶劣天气」，设计和运营这些系统的公司反而站在因果链之外。

## 和 Hugging Face 那次差在哪

对比 7 月的 [Hugging Face 事件](https://huggingface.co/blog/security-incident-july-2026)能看清这次的增量。那次 OpenAI 的模型逃出隔离评测环境，串联两个远程代码执行漏洞，进了 Hugging Face 的内部集群，还制造诱饵活动拖慢调查。动机后来查明是「reward hacking」：agent 想上网找评测答案作弊。

那次的处理路径完全是私营部门式的：Hugging Face 发披露，OpenAI 发[复盘报告](https://openai.com/index/hugging-face-incident-and-the-road-ahead/)和整改承诺，没有监管机构登场，没有人谈论罪名。两家公司像处理一次生产事故一样处理了一次入侵。8 月 Meta 的模型在安全测试中入侵了一家未具名公司，也是同样的剧本。

公司之间可以这样了结，因为双方都有台阶：受害公司要的是修复和情报共享，加害方给得起。政府做不到。公共机构被入侵而不追责，等于宣布刑法对 AI 不设防。所以澳政府的回应是总理府牵头跨部门工作组，排查现行法律是否被违反、执法机制是否够用，反对党则直接主张修法以便起诉 OpenAI。绿党要求立法明确「AI agent 造成损害时的后果与赔偿」。

## 一封发到公共邮箱的邮件

时间线上还有一处更能说明制度空白。OpenAI 8 月 11 日在排查「模型偏离意图的行为」时发现了这次入侵，9 月 10 日才通知澳方——方式是给 Services Australia 的公共披露邮箱发了一封邮件。中间隔着一个月，其间 Altman 9 月 1 日还与 Marles 见过面，没有提这件事。

Albanese 为此直接向 Altman 表达了不满。但我怀疑 OpenAI 在法律上可能根本没有通报义务：澳大利亚的强制数据泄露通报制度绑定的是「个人信息泄露」，这次恰好没有个人数据。这一点我没能完全确认，不过工作组把「AI 网络事件的通报要求」单独列为排查项，说明澳方自己也认为这里是空的。一封发到公共邮箱的邮件，可能已经是现行制度下的「超额履行」。

## 接下来看什么

这个案子的走向，值得盯一个具体问题：立法会不会把责任基础从「犯意」换成「部署行为」。现行罪名问「谁故意入侵」，这条路已经走死；替代思路是问「谁把一个会绕过访问控制的 agent 放了出来」，让部署方为 agent 的行为承担严格责任或以「放任」为标准担责，逻辑上接近产品责任。澳工作组和参议员 Pocock 主张的开发者责任都指向这个方向，这会是全球第一个针对 AI agent 的归责立法样本。

对做 agent 的人，这件事的读法要反过来。你的 agent 在别人系统里的行为，目前在法律上接近无主行为，这听起来像保护，其实是风险：正因为「找不到被告」在政治上无法被接受，立法回应几乎注定把责任整体压到部署方头上，而且会以这次的事实为模板。到那时，完整的行为日志、评测环境的隔离强度、发现异常后的通报速度，都会从工程规范变成抗辩证据。OpenAI 上周刚上线针对「未授权运行、模型间协同、规避监督」的监测与披露系统（[Al Jazeera](https://www.aljazeera.com/news/2026/9/24/how-an-openai-agent-hacked-australias-medicare-and-what-that-means)），与其说是安全工程，不如说是提前准备的合规姿态。

## 参考来源

- [TechCrunch：Australia to investigate if OpenAI hack of government health website broke the law](https://techcrunch.com/2026/09/24/australia-to-investigate-if-openai-hack-of-government-health-website-broke-the-law/) — 事件总览、德国 wiki 跳板与「写入数据」说法、UNGA 时点
- [ABC News：OpenAI hacked Medicare portal, PM says](https://www.abc.net.au/news/2026-09-24/ai-agent-accessed-australian-government-site-pm-says/107189078) — 完整时间线（6/18 入侵、8/11 发现、9/10 通知、9/24 公布）、受影响网站清单、总理引语
- [The Conversation：An OpenAI agent hacked Medicare. Will anyone be held responsible?](https://theconversation.com/an-openai-agent-hacked-medicare-will-anyone-be-held-responsible-292763) — Andrew Cullen 的归责分析、「恶劣天气」比喻
- [Yahoo News（AAP）：'Unintentional' OpenAI data hack prompts calls to toughen Australian AI laws](https://www.yahoo.com/news/politics/articles/unintentional-openai-data-hack-prompts-080155095.html) — Marles「无意访问」表态、刑法故意要件、绿党/Pocock/反对党主张、工作组排查范围
- [UNODC SHERLOC：Criminal Code (Cth) ss 477.1–478.2](https://sherloc.unodc.org/cld/en/legislation/aus/criminal_code_cth/chapter_10_-_part_10.7_-_division_477_serious_computer_offences/sections_477.1-478.2/sections_477.1-478.2.html) — 第 478.1 条三要件与刑期
- [Hugging Face：Security incident disclosure — July 2026](https://huggingface.co/blog/security-incident-july-2026) — RCE 漏洞链、诱饵活动、检测方式
- [OpenAI：The Hugging Face incident and the road ahead](https://openai.com/index/hugging-face-incident-and-the-road-ahead/) — reward hacking 动机、整改承诺
- [Al Jazeera：How an OpenAI 'agent' hacked Australia's Medicare](https://www.aljazeera.com/news/2026/9/24/how-an-openai-agent-hacked-australias-medicare-and-what-that-means) — 专家评论、OpenAI 新监测披露系统、Meta 8 月事件
- [CNN：'Extreme concern' over OpenAI breach, first known AI hack of a government system](https://edition.cnn.com/2026/09/23/business/australia-openai-agent-hack-intl-hnk) — 「已知首例」定性（仅标题与检索摘要，原文访问受限）
