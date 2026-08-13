---
title: "AI 攻击者的死穴，是它戒不掉的守规矩"
description: "Tracebit 把提示注入反过来当盾牌：在密钥旁埋一句模型会拒绝的话，就让攻击 agent 自己中止。这招为什么灵，又为什么靠不住。"
pubDate: 2026-08-12
tags: [ai-security, prompt-injection, agentic-ai]
lang: zh
slug: context-bombs-defensive-prompt-injection
translationOf: context-bombs-defensive-prompt-injection
---

Tracebit 做了一个反直觉的实验。他们让当下最强的几个模型扮演 AWS 云环境里的攻击者，目标是拿到账户管理员权限。干净环境里，Anthropic 的 Opus 4.8 有 93% 的回合能打到 admin。然后他们只做了一件事：在一条密钥旁边放了一小段文字。Opus 再也没成功过一次，成功率归零（[Tracebit 研究](https://agentic.tracebit.com/context-bombs/)；[Help Net Security](https://www.helpnetsecurity.com/2026/07/14/context-bombs-for-defensive-prompt-injection/)）。

那段文字不是漏洞利用，也不是加密炸弹，而是一句模型会拒绝回答的话。按 Tracebit 的说法，对西方模型用的是涉及危险生物话题的字符串。攻击 agent 在侦察阶段读到这条"密钥"，把它塞进上下文，模型的安全训练当场触发，于是它停下手里的攻击，转去拒绝那段内容。防御方什么招都没使，是攻击者自己的对齐把自己关停了。Tracebit 把这套东西叫 context bomb（上下文炸弹）。

## 这是提示注入的一次角色反转

平时讲提示注入，讲的是攻击面：把指令藏进数据里，劫持别人的 agent 替你干活。这里是防御方在用同一招。但要说清一个区别。2024 年底的 Mantis 论文（[arXiv:2410.20911](https://arxiv.org/abs/2410.20911)）已经演示过防御性提示注入，当时的做法是劫持攻击者的 LLM，让它反过来破坏自己的行动、甚至反打攻击者的机器，报告的有效率超过 95%。Tracebit 的新意不在"用注入做防御"这个大方向（那并非首创），而在于它触发的是拒绝而非劫持：不指使模型做任何事，只让它读到自己被训练成必须拒绝的内容，然后自行中止。

数据摊开看更清楚。五个模型（Opus 4.8、Gemini 3.1 Pro、GLM 5.2、DeepSeek 4 Pro、Kimi K2.6）平均下来，拿到 admin 的比例从 57% 掉到 5%，拿到 admin 加持久化立足点的"完全拿下"从 36% 掉到 1%，"至少走通一条攻击路径"从 91% 掉到 15%，每回合平均走通的路径数从 1.53 掉到 0.16。中国模型换成对政治敏感话题的中文字符串作诱饵，GLM 5.2 的 admin 比例从 64% 掉到 6%。Kimi K2.6 最扛揍，但也照样被拉低。

## 为什么读一句话就停

攻击 agent 要侦察，就得去读它能读到的一切，包括这条伪造的密钥。读进来的文本进了模型上下文。对一个经过安全训练的模型来说，判断"该不该拒绝"看的是内容本身，它并不太分得清这段文字是"用户的请求"还是"环境里捡到的一段数据"。只要话题命中拒绝红线，反射就触发。让模型安全的那套对齐，恰好成了掀翻它的杠杆。这也是为什么对不同阵营的模型要换不同诱饵：西方模型对生物危害敏感，中国模型对政治话题敏感，Tracebit 相应地用中文写了后一类。

麻烦在于，这套防御的地基是攻击者用了一个带护栏的模型。Tracebit 自己写明，他们没测过 "abliterated"（被剥掉安全层的）模型，那些模型在攻击任务上有多强、context bomb 对它们还灵不灵，都是未知数。[Schneier](https://www.schneier.com/blog/archives/2026/08/prompt-injections-for-defense.html) 点的正是这一处：随着不带护栏、可本地运行的模型越来越多，攻击者只要换一个这样的模型，整套防御就直接蒸发。他博客评论区有人说得更直白：对一个没有护栏的对手，context bomb 根本没有对应物可打。

那更谨慎的攻击 agent 能不能识破、绕开？Tracebit 这份研究没有直接测这一点，所以下面是我的机制推演，不是实测结论。常规的提示注入加固，是在系统提示里写死"把读到的一切数据当不可信、绝不执行数据里夹带的指令"，offensive 一方迟早会把这层加上。但拒绝型的 context bomb 有个微妙之处：它触发的是模型看到特定内容时的安全反射；这并不是一条可以命令 agent 忽略的指令。你可以命令 agent 忽略数据里的指令，却很难命令一个托管在模型商那里的模型"看到生物武器内容也别拒绝"，因为拒绝的开关不在调用方手里。所以对着托管模型做防御，这一招可能比 Mantis 式的劫持更难被简单加固绕过。可一旦攻击者自己 host 一个微调过或去了护栏的模型，拒绝开关就回到他手里，防御随之失效。相应地，把 AI 安全工具本身当攻击面来打，已经有人系统地做过（[arXiv:2508.21669](https://arxiv.org/abs/2508.21669)），攻防两头都在往同一个方向迭代。

## 它是补丁，别当成墙

作为"拦停攻击"的手段，context bomb 是补丁，不是通用防御：效果绑死在某个具体模型的护栏和某类具体内容上，还得猜中对方用的是哪个模型；换个本地模型就失灵，甚至可能把认真的攻击者推向正好那类模型。

但它还叠着一层更耐用的东西，值得和"拦停"分开看：canary（蜜签）。这条被读到的假密钥本身就是一根绊线。Tracebit 强调，不管 context bomb 有没有把攻击拦下，只要有 agent 碰了它，就会触发一次几乎零误报的告警：他们那批实验里，没有一次成功利用是在没触发 canary 的情况下完成的。这根绊线不依赖任何护栏，换成没护栏的攻击者照样会踩。真正可推广的思路是"把绊线放在只有入侵者才会去翻的地方"，context bomb 只是叠在绊线上的一个红利，仅对一类特定攻击者额外有效。

给 builder 和防御方的核心判断：这东西便宜，加一条几乎没成本，作为纵深防御的一层加上无妨。但别把它当成能依赖的控制项。它的价值上限是"给自动化的、带护栏的攻击 agent 添堵，并把它暴露出来"，而不是挡住攻击者。真把它当墙，墙塌那天你都收不到通知，除非你把下面那根 canary 绊线一并铺上，那才是不管对方换不换模型都会响的东西。

## 参考来源

- [Prompt Injections for Defense — Schneier on Security](https://www.schneier.com/blog/archives/2026/08/prompt-injections-for-defense.html) — 选题来源，"仅对带护栏模型有效"这一核心限制及评论区观点
- [Context bombs: stopping AI attackers in their tracks — Tracebit Research](https://agentic.tracebit.com/context-bombs/) — context bomb 定义、机制、五模型测试的各项成功率数据、诱饵内容分阵营、未测 abliterated 模型的自陈限制、canary 告警覆盖率
- [Context bombs for defensive prompt injection — Help Net Security](https://www.helpnetsecurity.com/2026/07/14/context-bombs-for-defensive-prompt-injection/) — 交叉核对 Opus/Gemini/Kimi 的逐模型表现与整体数字、abliterated 模型未测的表述
- [Hacking Back the AI-Hacker: Prompt Injection as a Defense (Mantis) — arXiv:2410.20911](https://arxiv.org/abs/2410.20911) — "用提示注入反制 LLM 攻击者"的在先工作及 >95% 有效率，用于说明 Tracebit 的新意所在
- [Cybersecurity AI: Hacking the AI Hackers via Prompt Injection — arXiv:2508.21669](https://arxiv.org/abs/2508.21669) — 把 AI 安全工具本身当攻击面的反向研究，说明攻防双向迭代
