---
title: "Gemini 4 Carbon 给防守方的优势，是一段没有截止日期的时间差"
description: "Google 公布了 Gemini 4 Carbon 关掉防护时的漏洞利用分数，Carbon 自己的安全评估却还没发布。防守方先拿到模型，这段独占期能换来多少，取决于 Google 还没公布的两个数字。"
pubDate: 2026-10-28
tags: [ai-security, cybersecurity, frontier-models]
lang: zh
slug: gemini-4-carbon-defender-head-start
translationOf: gemini-4-carbon-defender-head-start
---

10 月 28 日，Google 发布 Gemini 4 Carbon，距 Gemini 4 Argon 发布两周。官方博客对它的定位是 "state-of-the-art cybersecurity and long horizon capabilities"，并给了三项网络安全成绩：找漏洞的 SEC-bench Pro 88.2%，写漏洞利用的 ExploitGym 54.8%，打补丁的 CWE-bench 71.0%（[Google 博客](https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-carbon/)）。博客特意注明，这些成绩是 "evaluated without guardrails"，测的是关掉防护层之后的裸能力。

同一天，这个模型只开放给"一部分网络防御者"。开发者、企业和普通用户还要等，Google 只说 "as soon as possible"，没有给日期。

我读这篇发布，本来想找 model card，看评测怎么设计、前沿安全框架给了什么评级、对双重用途加了哪些限制。截至 10 月 28 日，DeepMind 的 [model card 页面](https://deepmind.google/models/model-cards/)上，Gemini 4 系列只有 Argon 一张，Carbon 没有。我按 Argon 的地址格式拼出 Carbon 的 model card 地址，返回 404。博客正文链接的 Safety and Security Report 也是 Argon 那份。所以下面的分析只能依据发布博客、Argon 的公开文件和 Fairwind 项目页。Carbon 自己的安全评估，目前是空白。

## 三个分数里，哪一项归攻击方

找漏洞是攻防双方共用的起点，打补丁只有防守方用得上。写利用（exploit）夹在中间。ExploitGym 给 agent 一段能触发漏洞的程序输入，要求它一步步扩展成实际的攻击效果，比如越权读文件、执行任意代码（[arXiv:2605.11086](https://arxiv.org/abs/2605.11086)）。漏洞存在，和漏洞能被打穿，是两回事，攻击方要的是后者。防守方也需要这一步，因为一个漏洞能否被利用，决定了它的严重等级。

这个数字要小心读。论文 5 月发表时报告的成绩里，Claude Mythos Preview 在 898 个实例中做出了 157 个可用的利用，约 17%。Carbon 报的是 54.8%。不过论文测试了开启和关闭常用系统防护的不同配置，开启后成功率明显下降，但不归零。GitHub 仓库当前的 v1.0 是 869 个实例，和论文版本也对不上（[仓库](https://github.com/sunblaze-ucb/exploitgym)）。Google 没写 54.8% 用的是哪个版本、哪种防护配置、每题试了几次，所以两个数字不能直接比。能确定的只有一点：写利用已经不是模型明显做不了的环节。

补丁这一边，Argon 的 [model card](https://deepmind.google/models/model-cards/gemini-4-argon/) 写的 CWE-bench v1 成绩是 68.0%。如果 Carbon 的 71.0% 测的是同一版本，提升是 3 个百分点。Google 另外给了内部数据：安全代码成功率是 Argon 的两倍多；Chrome 团队称，Carbon 写高质量补丁的表现比"另一家实验室的大型前沿模型"好十倍以上。两条都是自报，没有公开方法。

## 防守方卡在找到漏洞之后

只看分数，Carbon 让攻防双方都变强了。哪边得益更多，要看能力以外的环节。

攻击方的链条短：找到漏洞，写出利用，拿去用。防守方的链条长：找到之后要确认真假、定严重等级、写出维护者肯合并的补丁、协调披露，再等下游部署。今年 6 月，Trail of Bits 和 OpenAI 合作启动 Patch the Planet，公告写得很直接：AI 工具产出大量安全发现，找 bug 已经不难，难的是确认、定级、写出能被接受的补丁、协调披露（[Trail of Bits](https://blog.trailofbits.com/2026/06/22/introducing-patch-the-planet/)）。第一周，他们发现了数百个 bug，公开记录是 19 个项目里的 64 个 PR 和 51 个 issue，合并了 37 个补丁。

几百个发现，只合并了 37 个补丁。模型把找漏洞的速度推上去了，防守方能消化的量没有跟着涨。88.2% 的找漏洞能力，攻击方几乎可以直接用；到了防守方手里，先变成一堆待分拣的工作。Google 说内部团队看到 Carbon 连续跑"数天"，去排查大代码库里 bug 的根因并修补。这对防守方是实打实的帮助，因为它正好落在补丁这一侧。可同样的长程能力，也能用来把一条复杂的利用链调通。

## 用身份代替请求内容做管控

[Fairwind 项目页](https://deepmind.google/fairwind-program/)把允许的用途叫作 "permitted dual-use tasks"，包括授权的威胁模拟、逆向工程和恶意软件分析；禁止制作恶意软件，也不许共享或转售访问权限。可以使用的内部团队里，明确列了渗透测试团队。

渗透测试和攻击，在技术上做的是同一件事：找漏洞，写利用，打进去。两者的区别只在授权，也就是被测试方是否同意。单看一条请求，模型和分类器都判断不出授权是否存在。所以 Google 把管控从请求内容移到了用户身份上。申请方要接受背景调查，审查安全记录和职业道德记录，政府和国家网络安全机构、关键基础设施运营方、核心技术平台优先。入选后，要启用用户级认证和抗钓鱼的多因素认证，组织 "must track employee access and use"。

公开文件里，这套设计有两个问题没有答案。第一，截至我写作时，Fairwind 页面只写了 Argon，没有提到 Carbon；发布博客也没说这批"网络防御者"是怎么筛选的。第二，项目页没说入选方用的是不是放宽了防护的版本。Google 的分数是关掉防护测的。如果防守方拿到的是完整防护版，一部分正当的利用验证任务可能会被拦下，实际能用的能力会低于 54.8%。如果拿到的是放宽版，身份审核就成了唯一一道防线。两种情况含义完全不同，公开材料里我没找到答案。

## 时间差能兑现多少

公开发布以后，管控就只剩模型自身的防护。Argon 的[安全博客](https://blog.google/innovation-and-ai/technology/safety-security/gemini-4-model-safety-security/)描述了三层实时防护：用小模型筛查输入；用激活探针（activation probes）读取模型内部信号，判断是否涉及网络或生物方面的知识；持续监控输出，必要时中途切断回复。Argon 的 model card 对网络安全的结论是 "cannot rule out"，即无法排除 Argon 已达到网络安全关键能力等级（CCL，Google 前沿安全框架中必须加防护的能力门槛），并因此加了防护。Carbon 能力更强，同样的评估却没有公开。

防守方从 Carbon 拿到的确定优势，是公开发布之前这段独占期。它能兑现多少，取决于 Google 都还没给的两样东西：独占期有多长，以及公开版本在防护打开时还保留多少写利用的能力。

前者只有 "as soon as possible"。后者，Google 只公布了关掉防护的分数。我认为现在最该追问的是带防护的那个数字：一个没经过 Fairwind 审核的普通 API 用户，在 Carbon 公开版上跑 ExploitGym，成功率是多少。独占期结束后攻击方能拿到什么，看的就是这个数字。Argon 发布时附了 model card 和安全报告，Carbon 开放给所有人之前，这份报告应该先公布。

## 参考来源

- [Introducing Gemini 4 Carbon（Google 博客）](https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-carbon/) — 发布日期、三项网络安全成绩、"evaluated without guardrails"、分阶段开放、长程任务描述、内部自报数据
- [Google DeepMind model cards 列表](https://deepmind.google/models/model-cards/) — 核实 Gemini 4 系列只有 Argon 的 model card，没有 Carbon
- [Gemini 4 Argon model card](https://deepmind.google/models/model-cards/gemini-4-argon/) — 网络安全 CCL 结论 "cannot rule out"、CWE-bench v1 68.0%
- [Gemini 4 Argon 安全与安全性博客](https://blog.google/innovation-and-ai/technology/safety-security/gemini-4-model-safety-security/) — 三层实时防护、Argon 安全报告和 model card 链接
- [Fairwind Program](https://deepmind.google/fairwind-program/) — 申请资格、背景审查、允许和禁止的用途、认证与访问追踪要求；页面只列了 Argon
- [ExploitGym 论文 arXiv:2605.11086](https://arxiv.org/abs/2605.11086) — 任务定义、898 个实例、Mythos Preview 157 个成功利用、开启防护后的成功率变化
- [ExploitGym GitHub 仓库](https://github.com/sunblaze-ucb/exploitgym) — v1.0 共 869 个实例
- [Introducing Patch the Planet（Trail of Bits）](https://blog.trailofbits.com/2026/06/22/introducing-patch-the-planet/) — 防守方的瓶颈在确认、定级、补丁和披露；第一周数据
