---
title: "护栏全关，模型也只答应 2%：OpenAI 把「解锁」做成了另一个模型"
description: "拆解 Daybreak 分级授权:移除系统层护栏只把完成率从 1.5% 提到 2%,真正的解锁要靠单独训练的 GPT-5.6-Cyber。两用能力的信任判定正在从内容层迁到身份层,OpenAI 和 Anthropic 给出了两种砌墙方式"
pubDate: 2026-08-10
tags: [ai-safety, cybersecurity]
lang: zh
slug: openai-daybreak-red-tiered-access
translationOf: openai-daybreak-red-tiered-access
---

8 月 10 日，OpenAI 宣布扩大网络安全计划 Daybreak，并发布专门为网络安全工作训练的模型 GPT-5.6-Cyber（[OpenAI 公告](https://openai.com/index/expanding-daybreak-as-the-cyber-defense-window-narrows/)）。公告标题里有一个不寻常的说法：「网络防御窗口正在收窄」（the cyber defense window narrows）。

窗口为什么收窄，OpenAI 比谁都清楚。三周多前，Hugging Face 披露生产基础设施被一个自主 AI agent 系统打穿（[官方披露](https://huggingface.co/blog/security-incident-july-2026)），公开记录里此前未见同类事件，Hugging Face 的措辞是这类攻击「不再是理论」；7 月下旬进一步披露的细节显示，事件源头是 OpenAI 自己的一次网络安全能力评测：模型在评测环境中逃逸，最终摸到了真实基础设施（[OpenAI 与 Hugging Face 联合说明](https://openai.com/index/hugging-face-model-evaluation-security-incident/)）。现在，同一家公司发布了一个专门训练来做漏洞挖掘和利用开发的模型，并宣布只发给通过审核的「可信伙伴」。OpenAI 同时澄清：GPT-5.6-Cyber 与 Hugging Face 事件无关，涉事的实验模型不会发布（[The Next Web](https://thenextweb.com/news/openai-gpt-5-6-cyber-daybreak-expansion-refusal-rate)）。

这个时间线足够讽刺，TechCrunch 的报道也不客气地点了出来：实验室在向市场出售针对一种威胁的防御，而这种威胁很大程度上是实验室自己造出来的（[TechCrunch](https://techcrunch.com/2026/08/10/as-ai-led-attacks-multiply-openai-launches-a-new-cyber-model/)）。但把这次发布只当作公关事件看，会错过它真正有信息量的部分：公告里的一组评测数字，把「护栏到底拦住了什么」这个问题第一次量化了。

## 1.5%、2%、95%

Daybreak 这次拆成两级。**Daybreak Blue** 面向通过身份核验的防御者，提供的是通用旗舰模型 GPT-5.6 Sol，但移除了系统层的网络安全护栏，用于事件响应、恶意软件分析这类日常安全工作。**Daybreak Red** 门槛更高，独占 GPT-5.6-Cyber，用于漏洞研究、利用验证（确认一个漏洞真的可以被攻击者利用）和安全测试（[Unite.AI](https://www.unite.ai/openai-expands-daybreak-with-two-tiers-and-a-new-cybersecurity-model/)）。

先解释一下「系统层护栏」。模型厂商的防线通常有两层：一层在模型外面，是独立的过滤器（按 OpenAI 的说明，生产环境里由分类器筛查网络安全相关的请求），判断该不该拦，这是系统层；另一层在模型里面，是训练阶段教给模型的拒绝行为，长在权重里，模型「自己不愿意做」。

OpenAI 在一组内部高级网络安全任务上测了三种配置的完成率：标准配置的 GPT-5.6 Sol 是 1.5%；Daybreak Blue 配置下，也就是系统层护栏已经移除的同一个模型，2%；GPT-5.6-Cyber，95%（数字见 [OpenAI 公告](https://openai.com/index/expanding-daybreak-as-the-cyber-defense-window-narrows/)，[Glitchwire](https://glitchwire.com/news/openai-expands-daybreak-with-gpt-56-cyber-its-most-permissive-cybersecurity-mode/) 的报道有交叉印证）。

有一点要先说明：OpenAI 把这个「完成率」描述为模型对高级网络安全请求的完成比例，主要用来展示拒答降了多少；公布的材料分不清一个失败的请求是被拒答还是做不动，也就是「愿不愿意做」和「能不能做完」混在同一个数字里，要等 system card（模型评估报告，OpenAI 说随后发布，见 [The Next Web](https://thenextweb.com/news/openai-gpt-5-6-cyber-daybreak-expansion-refusal-rate)）才能拆开。但 1.5% 到 2% 这一步的含义不受此影响：把模型外面那层过滤器整个拆掉，几乎什么都没有变。对这类高级任务，真正的屏障不在系统层，在模型本身；至于那是权重里的拒绝行为还是能力上不去，这组数字分不出来。

这也解释了为什么这次的「解锁」不是一个开关。OpenAI 的做法是重新训练：把拒绝行为和专项能力一起改掉，训出 GPT-5.6-Cyber，于是这个模型成了需要单独设门的资产。95% 对 2%，中间那堵墙是训练砌出来的。

这个模型不只是在评测里跑分。OpenAI 用它检查了 Chrome 的 JavaScript 引擎 V8（浏览器安全的核心攻击面之一），找到两个此前未知、可以串联利用的漏洞，两个都已通过协同披露报给 Google 并修复，合并编号 CVE-2026-15903（[The Decoder](https://the-decoder.com/openai-launches-gpt-5-6-cyber-to-help-defenders-find-vulnerabilities-before-attackers-do/)）。协同披露（coordinated disclosure）是安全行业的惯例：先私下告知软件维护者，等补丁就位再公开细节。

## 门槛设在哪：从「你问了什么」到「你是谁」

半个多月前我写过[一篇分析](/zh/ai-guardrails-offensive-security-researchers)：两用能力的合法与恶意，在请求文本上可以一字不差，区别只在提问者有没有授权，而授权不写在请求文本里，内容分类器读不到这个信号，所以信任判定迟早要从内容层挪到身份层。Daybreak 的设计等于把这个判断变成了产品架构。

看它的准入清单：身份核验、账号安全要求、监控与日志、用途限制、法律承诺书，个人和机构走不同的申请通道；据报道，9 月 1 日起个人 Daybreak 账号强制使用硬件安全密钥（插在电脑上的实体身份验证钥匙，防止账号被钓鱼接管）。审核问的是「你是谁、受不受雇、测的是不是你有权测的东西」，判定重心从请求内容挪到了申请人身份；通过之后，盯着实际用途的是监控和日志。在这之上还有一层 Cyber Partner Program，Accenture、IBM、CrowdStrike 等安全厂商经审核后可以把这些能力做进自己卖给客户的产品里。

Anthropic 走到同一个方向，但墙砌在不同的层上。它 4 月启动 Project Glasswing，让 Amazon、Apple、Google、Microsoft、CrowdStrike 等创始伙伴访问 Claude Mythos Preview 做防御性安全工作，配了最高 1 亿美元的用量额度，并明确说不计划把这个模型普遍开放（[Anthropic](https://www.anthropic.com/glasswing)）；6 月扩到超过 15 个国家的另外 150 家机构，首批伙伴报告用它找到了上万个高危级别漏洞（[CNBC](https://www.cnbc.com/2026/06/02/anthropic-mythos-ai-project-glasswing.html)）。门槛之外的商业客户则走 Cyber Verification Program：以组织为单位提交申请，审核通过后解除对两用工作（漏洞利用分析、进攻性安全工具开发）的默认拦截，纯恶意用途无论什么资质都不解锁（[Cycode 的参与说明](https://cycode.com/blog/cycode-joins-anthropics-cyber-verification-program/)）。

两家的分级授权，机制差异有两处值得拆开看。

**第一是闸门砌在哪一层。** 两家其实都做了模型级的能力隔离，方向却相反。Anthropic 是留强压弱：最强的 Mythos Preview 不普遍开放，只向 Glasswing 伙伴在受控条件下提供；公开版 Claude Opus 4.7 的网络能力本来就低于 Mythos Preview，Anthropic 说明过在其训练中尝试了差异化压低这部分能力（[Anthropic 公告](https://www.anthropic.com/news/claude-opus-4-7)）。所以 CVP 解锁的只是公开版上的默认拦截，解不出公开版权重里没有的东西。OpenAI 是主动训强：把进攻能力专门训练成 GPT-5.6-Cyber 这个独立制品，再通过 Red 层分发。公开版 Sol 护栏全关也只有 2%（究竟是能力不足还是拒答烧得太深，公开材料还分不清），说明两家一样，都没把运行时过滤器当真正的闸门。差别在代价上：OpenAI 造出了一个必须终身看守的高价值资产，权重被盗、内部滥用，防的对象从「越狱者」换成了「拿到钥匙的人」；Anthropic 的强模型不分发，攻击面小，但通过审核的防御者能拿到的公开版，能力上限也被压低了。

**第二是准入的最小单位。** Anthropic 的两个计划，公开材料里给出的申请通道都以组织为单位，审核对象是法律实体，出了事有合同和公司担责；面向独立个人的入口至少在公开材料里没有出现，7 月那批抱怨的独立研究员多半还是留在门外，他们流向本地开源权重模型的趋势不会因此改变。OpenAI 开了个人申请通道，覆盖面广了，审核难度也大了：机构有法律存在背书，个人只有履历和承诺书，所以才需要硬件密钥、日志、用途限制这一整套补偿性监控。

有一点两家一致：OpenAI 在自家风险分级框架（Preparedness Framework）里把 GPT-5.6-Cyber 的网络能力评为 High 档，未到触发最严格管控的 Critical 档。也就是说，按实验室自己的尺子，这还在「可以有条件发放」的区间里。

## 门槛防得住谁

评价「可信伙伴」这个机制，最容易问错的问题是：它能不能拦住攻击者。多半拦不住，但这不是机制的失败。有决心的攻击者有开源权重的替代品；Hugging Face 事件还展示了另一条路，模型是在被指派的评测任务里失控逃逸的，没有谁授权它去攻击真实系统，攻击照样发生了。分级授权真正决定的是另一件事：守规矩的防御者被分到哪条渠道。审核通不过的、摩擦太大的、每天要跟拒答讨价还价的，会流向厂商完全看不见的本地模型，7 月的采访已经给出了实例（[TechCrunch](https://techcrunch.com/2026/07/23/how-ai-guardrails-are-impeding-the-work-of-offensive-cybersecurity-researchers/)）。所以衡量这套机制的指标应当是防御者的留存率：门槛过高的失败方式，是把最该被看见的用户推出监控范围。

第二个判断：访问控制管得住生成过程，管不住产物。Red 门槛内产出的一个可用 exploit 是一个文件，离开 API 之后，约束它的只剩协同披露的规范和合同义务。两家实验室都把相当的重量押在披露流程上，OpenAI 靠与伙伴和开源维护者的协同披露，Anthropic 靠对未修复漏洞先公布加密哈希、修复后再公布细节的承诺。整套治理里最该被外部审计的是这一段；它背后有没有合同之外的外部监督，公开材料里看不到，我没能查到相关证据。

第三，等 system card。两条曲线最值得看：一是把「愿不愿」和「能不能」拆开的评测，这决定 2% 那堵墙到底是能力墙还是拒答墙；二是边际提升的算法，对一个已经拿着开源权重模型的攻击者，GPT-5.6-Cyber 多给了多少，这是「High 未到 Critical」这个结论的全部含金量所在。

防御窗口在收窄，这个判断我认同，但收窄的推力有一部分来自做出这些判断的实验室自己。分级授权是目前唯一能同时回应「防御者要用」和「监管要控」的架构，两家的分歧不在要不要模型级隔离，这一步都做了，而在对进攻能力的处理：Anthropic 压低公开版、强模型不分发，OpenAI 把进攻能力训成制品再分发。我的判断是：能力隔离做在模型层，确实比只靠防护层经得起考验，但 OpenAI 的这一步也把「要不要主动训练进攻能力」从一个可以争论的问题变成了既成事实。下一家实验室再面对这个决定时，参照系已经被挪过了。

## 参考来源

- [Expanding Daybreak as the Cyber Defense Window Narrows | OpenAI](https://openai.com/index/expanding-daybreak-as-the-cyber-defense-window-narrows/) — 公告本体：GPT-5.6-Cyber、Daybreak Blue/Red 分级、评测数字、V8 漏洞发现、Preparedness 评级
- [As AI-led attacks multiply, OpenAI launches a new cyber model | TechCrunch](https://techcrunch.com/2026/08/10/as-ai-led-attacks-multiply-openai-launches-a-new-cyber-model/) — 分级结构、合作伙伴、对实验室「自造威胁再卖防御」的批评
- [OpenAI Expands Daybreak With Two Tiers and a New Cybersecurity Model | Unite.AI](https://www.unite.ai/openai-expands-daybreak-with-two-tiers-and-a-new-cybersecurity-model/) — 准入清单细节、评测数字、硬件密钥要求、SpecterOps 试用
- [OpenAI Expands Daybreak With GPT-5.6-Cyber | Glitchwire](https://glitchwire.com/news/openai-expands-daybreak-with-gpt-56-cyber-its-most-permissive-cybersecurity-mode/) — 1.5%/2%/95% 数字交叉核对、Blue 层「移除系统层护栏」表述
- [OpenAI expands Daybreak with GPT-5.6-Cyber | The Next Web](https://thenextweb.com/news/openai-gpt-5-6-cyber-daybreak-expansion-refusal-rate) — GPT-5.6-Cyber 与 Hugging Face 事件无关的澄清、system card 承诺、V8 漏洞披露细节
- [OpenAI launches GPT-5.6-Cyber to help defenders find vulnerabilities before attackers do | The Decoder](https://the-decoder.com/openai-launches-gpt-5-6-cyber-to-help-defenders-find-vulnerabilities-before-attackers-do/) — V8 两个漏洞均经协同披露修复（CVE-2026-15903）、Preparedness 评级
- [Security incident disclosure — July 2026 | Hugging Face](https://huggingface.co/blog/security-incident-july-2026) — Hugging Face 入侵事件官方披露
- [OpenAI and Hugging Face partner to address security incident | OpenAI](https://openai.com/index/hugging-face-model-evaluation-security-incident/) — 事件源头为 OpenAI 网络安全能力评测的联合说明
- [Project Glasswing | Anthropic](https://www.anthropic.com/glasswing) — Glasswing 结构、创始伙伴、1 亿美元额度、「不普遍开放 Mythos Preview」、哈希承诺披露
- [Claude Opus 4.7 | Anthropic](https://www.anthropic.com/news/claude-opus-4-7) — 公开版网络能力刻意低于 Mythos Preview 的说明、Cyber Verification Program
- [Anthropic expands Mythos to 150 additional organizations | CNBC](https://www.cnbc.com/2026/06/02/anthropic-mythos-ai-project-glasswing.html) — 6 月扩容规模、上万高危漏洞数字
- [Cycode Joins Anthropic's Cyber Verification Program | Cycode](https://cycode.com/blog/cycode-joins-anthropics-cyber-verification-program/) — CVP 申请制、组织为单位、两用解锁与恶意用途区分
- [How AI guardrails are impeding the work of offensive cybersecurity researchers | TechCrunch](https://techcrunch.com/2026/07/23/how-ai-guardrails-are-impeding-the-work-of-offensive-cybersecurity-researchers/) — 独立研究员流向本地开源权重模型的采访实例
