---
title: "Ellison 说 Oracle 的代码都是 AI 写的，OpenJDK 为什么还要禁 AI 代码？"
description: "OpenJDK 禁止一切 AI 生成的贡献，同属 Oracle 的 GraalVM 却放行。拆开这对矛盾会发现：决定开源项目 AI 政策的是权利链条和审阅带宽，不是模型能力。"
pubDate: 2026-08-07
tags: [open-source, ai-coding, ai-governance]
lang: zh
slug: openjdk-ai-code-ban
translationOf: openjdk-ai-code-ban
---

2025 年 10 月，Oracle AI World 大会的主题演讲上，Larry Ellison 对台下说：「Oracle 正在写的代码，不是 Oracle 在写，是我们的 AI 模型在写。我们只要告诉模型想让程序做什么。」（[The Register](https://www.theregister.com/ai-and-ml/2026/08/03/as-larry-ellison-bets-the-farm-oracle-says-it-loves-ai-written-code-just-not-in-openjdk/5281851)）

十个月后，这段话被人翻出来，和另一份文件摆在一起：OpenJDK，由 Oracle 主导的 Java 开源项目，在官网挂出了一份[禁止 AI 生成内容的政策](https://openjdk.org/legal/ai)。The Register 8 月 3 日的标题毫不客气：Oracle 说它爱 AI 写的代码，只是别写进 OpenJDK。[Hacker News 上两百多条评论](https://news.ycombinator.com/item?id=49213754)，大半在笑这个矛盾。

但这件事比「双标」有意思得多。

## 禁令到底禁了什么

这份政策 2026 年 4 月初就发布了，标注为「临时政策」，8 月才因为 Ellison 的对照进入热榜（[InfoQ](https://www.infoq.com/news/2026/06/oracle-genai-policies/)）。条文很干脆：贡献不得包含由大语言模型、扩散模型或类似深度学习系统部分或全部生成的内容。覆盖范围包括源代码、文本、图片，从 Git 仓库、pull request 一直到邮件列表、wiki 和 bug 系统。AI 生成一百行、你改掉几行再提交，同样不行。

但它明确不是「禁用 AI」：私下用 AI 理解、调试、审阅代码，政策原文写的是「鼓励」。禁的只是把生成物提交上来。

给出的理由有三条。一是审阅负担：AI 能批量产出看着可信、配着看着可信的测试、实则错误或难以维护的代码，耗尽本就稀缺的审阅时间。二是安全：JDK 托着全球大量关键系统，这类代码直接构成风险。三是知识产权：向 OpenJDK 提交代码要先签 OCA（Oracle Contributor Agreement，Oracle 贡献者协议），它要求贡献者对自己的贡献拥有完整权利，而「AI 生成的产出归谁所有」眼下还在诉讼中没有定论。

执行方式说出来有点泄气：在 Skara（OpenJDK 的 PR 流程工具）勾一个合规选框。政策自己承认检测 AI 代码不可能，只给审阅者列了些迹象：啰嗦的注释、层层小标题、emoji（[JVM Weekly](https://www.jvm-weekly.com/p/whats-coming-in-jdk-27-and-why-openjdk)）。

真正的看点在隔壁。GraalVM，Oracle 旗下另一个开源项目（做高性能 Java 虚拟机和多语言运行时），几乎同期发布的政策方向完全相反：允许用 AI 编码助手，人对提交负全责，披露用了 AI「鼓励但可选」。两个项目都要求签 OCA（[InfoQ](https://www.infoq.com/news/2026/06/oracle-genai-policies/)）。同一家公司、同一份贡献者协议，两个极端。这说明决定政策的变量，不在「AI 写的代码行不行」。

## 权利链条：OpenJDK 特有的那道题

给不熟悉 Java 生态的读者补两句背景。OpenJDK 是 Java 标准的「参考实现」，也就是 Java 规范的官方落地版本，几十亿台设备上跑的 Java 最终都源自它或它的衍生版。它的代码走两条路：一条以开源许可证（GPLv2 附例外条款）发布为 OpenJDK；另一条由 Oracle 打包成 Oracle JDK，按商业条款卖给企业客户。Oracle 能这么做，正是因为 OCA 让它对每份贡献拿到了共同所有权。

这条商业化路径成立的前提，是每一行代码的权利链条干净：贡献者真的拥有权利，才谈得上授予 Oracle。而美国版权局 2025 年 1 月的报告重申，没有人类作者参与表达的纯 AI 生成内容不受版权保护（[copyright.gov/ai](https://www.copyright.gov/ai/)）。没有版权，就没有可转让的权利，贡献者在 OCA 上签的字对这部分代码就是空头支票。还有反向的风险：如果 AI 输出复现了训练数据里别人的受版权代码，Oracle 等于把侵权代码再授权卖了出去。对一个靠再授权赚钱的项目，这是直接的商业风险。HN 评论区的主流判断也在这里：这份禁令首先是法务动作。

对照 Linux 内核就更清楚。内核只有一个许可证 GPL-2.0，没有商业再授权，贡献靠 DCO（Developer Certificate of Origin，开发者原创声明）：提交者自己声明有权提交，出了问题责任落在提交者头上。所以内核 2026 年 4 月合并的[官方文档](https://docs.kernel.org/process/coding-assistants.html)选了另一条路：AI 可以辅助写代码，但 AI 不得添加 Signed-off-by 签名，因为只有人能做这个法律声明；建议加 Assisted-by 标签披露用了什么模型；人对每一行负全责。风险本来就压在提交者身上，项目层面用不着一刀切。

不过要说明一点：GraalVM 的贡献者同样签 OCA，法律暴露和 OpenJDK 相同，政策却是放行。所以法律结构只解释了 OpenJDK「为什么有理由怕」，解释不了「为什么必须禁」。同样的不确定性面前，禁与不禁是风险偏好的选择。OpenJDK 是参考实现，出问题波及面最大，治理层拧到了最保守的一档，同时把政策标为临时、留了修订的口子。

## 光谱上的位置

OpenJDK 不是第一个禁 AI 代码的项目，只是其中分量最重的项目之一。开源世界的政策已经排成一条光谱。

禁令一端：Gentoo 2024 年 4 月理事会投票禁止 AI 辅助的贡献，NetBSD 同年把 AI 代码默认视为「受污染」（[Tom's Hardware](https://www.tomshardware.com/software/linux/linux-distros-ban-tainted-ai-generated-code)）；QEMU 的[政策原文](https://www.qemu.org/docs/master/devel/code-provenance.html)用大写的 DECLINE 拒绝一切疑似 AI 生成的贡献，理由同样落在 DCO 无法核证权利上。

披露一端：Apache 软件基金会早在 2023 年 6 月就[允许 AI 生成的贡献](https://www.apache.org/legal/generative-tooling.html)，条件是工具条款兼容开源定义、确认产出没有裹挟第三方受版权材料，并在提交信息里加 Generated-by 标记；Linux 内核的 Assisted-by 同属此类。

两端共享一条底线：人对代码负全责，AI 不能签字。走禁令路线的项目还有个共同画像：基础设施、审阅者稀缺、权利链条要求苛刻。政策的松紧映射的是项目的法律结构和审阅人手，没有一家给出的理由是「模型写不好代码」。

## 判断

这份禁令能执行到什么程度？约束力有限，它防的层面在法律和流程，技术上拦不住人。实际功能有两个：其一，贡献者勾了合规选框还提交 AI 代码，违约责任清晰，知识产权风险被显式转回贡献者；其二，审阅者拿到了直接拒收的依据，不用再逐行论证一份可疑 patch 哪里不好。挡的正是政策第一条抱怨的东西：批量涌来、看着可信、审不过来的生成代码。

会被效仿吗？我的判断：纯禁令不会成为主流，「人负全责加披露」会。OpenJDK 自己都称临时政策；大多数项目不具备它那种风险集中度，禁令挡住正常贡献者的成本高于收益；而且禁令的两条根基都在松动，版权诉讼迟早给出边界，工具链也在补产出溯源的能力。一旦「这段代码从哪来」可以核证，禁令就没有理由不退回披露制。

对做 AI coding agent 的人，这件事标出了落地阻力的真实位置：权利链条能不能核证，审阅带宽够不够消化，模型能力反而不是瓶颈。Ellison 的话和 OpenJDK 的禁令也并不真的矛盾：自家产品代码，权利风险自己兜底，AI 随便写；开源社区的代码要再授权给全世界，每一行都得有主。同一家公司在两边各自算了账，得出不同的答案，仅此而已。

## 参考来源

- [OpenJDK Interim Policy on Generative AI](https://openjdk.org/legal/ai) — 政策原文：禁令条文、三条理由、允许范围
- [InfoQ: Oracle's OpenJDK Bans Generative AI Contributions While Oracle's GraalVM Allows Them](https://www.infoq.com/news/2026/06/oracle-genai-policies/) — 政策发布时间、GraalVM 对比、两项目同用 OCA
- [The Register: As Larry Ellison bets the farm…](https://www.theregister.com/ai-and-ml/2026/08/03/as-larry-ellison-bets-the-farm-oracle-says-it-loves-ai-written-code-just-not-in-openjdk/5281851) — Ellison 在 Oracle AI World 2025 的引语、事件成为新闻的时间点
- [JVM Weekly vol. 171](https://www.jvm-weekly.com/p/whats-coming-in-jdk-27-and-why-openjdk) — Skara 选框、检测迹象等政策细节
- [Linux kernel: AI Coding Assistants 文档](https://docs.kernel.org/process/coding-assistants.html) — 内核 Assisted-by / Signed-off-by 规则（已直接核对原文）
- [QEMU: Code Provenance 文档](https://www.qemu.org/docs/master/devel/code-provenance.html) — QEMU 拒收政策及 DCO 理由（已直接核对原文）
- [ASF Generative Tooling Guidance](https://www.apache.org/legal/generative-tooling.html) — Apache 2023 年起的披露制政策（已直接核对原文）
- [Tom's Hardware: Linux distros ban 'tainted' AI-generated code](https://www.tomshardware.com/software/linux/linux-distros-ban-tainted-ai-generated-code) — Gentoo、NetBSD 禁令
- [US Copyright Office: Copyright and Artificial Intelligence](https://www.copyright.gov/ai/) — 纯 AI 生成内容不受版权保护
- [Hacker News 讨论](https://news.ycombinator.com/item?id=49213754) — 社区对动机与可执行性的反应
