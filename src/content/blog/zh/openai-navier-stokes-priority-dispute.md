---
title: "数学家还在改写证明，OpenAI 先发布了：一场围绕千禧年难题的抢跑风波"
description: "OpenAI 称内部模型解决了 Navier-Stokes 爆破问题，数学家 Buckmaster 公开了完整时间线。真正被改变的是数学界的优先权制度本身。"
pubDate: 2026-09-08
tags: [ai-research, open-science, mathematics]
lang: zh
slug: openai-navier-stokes-priority-dispute
translationOf: openai-navier-stokes-priority-dispute
---

9 月 6 日是个周日。中午 12 点 45 分，纽约大学数学家 [Tristan Buckmaster](https://cims.nyu.edu/~tristanb/) 被问到「今天任何时候」能不能通话。当天下午的两通电话里，OpenAI 研究员 Sébastien Bubeck 告诉他：一个未发布的内部模型拿出了约一百页的证明，解决了带外力的 Navier-Stokes 爆破问题。这是克雷数学研究所悬赏一百万美元的[七个千禧年难题](https://www.claymath.org/millennium-problems/)之一，也是 Buckmaster 和合作者 Levent Alpöge 悄悄攻了一年、刚刚取得突破的方向。

按 Buckmaster 的记录，他在电话里说，如果 OpenAI 按提议的方式发布结果，他会把整件事公开。得到的回答是：「你为什么要毁掉自己的职业生涯？」他答自己是学者，反问公开为什么会毁掉职业生涯。对方说：「如果你不想让我客气，那我也不必客气。」（[Buckmaster 公开声明](https://cims.nyu.edu/~tristanb/statement.pdf)）

三篇预印本和 Lean 形式化证明先行上线——陶哲轩 9 月 7 日已在博客里逐篇评述；9 月 8 日，Buckmaster 公开这份四页声明。同一天，OpenAI 发布公告[《On the Navier–Stokes Millennium Prize Problem》](https://openai.com/index/navier-stokes-solution/)。Bubeck 称社交平台上流传的指控「不实且具煽动性」（[OfficeChai](https://officechai.com/ai/openais-sebastien-bubeck-calls-tristan-buckmasters-claims-of-trying-to-take-credit-for-fluid-dynamics-proofs-false-and-inflammatory/)），否认要求过除名（[OfficeChai](https://officechai.com/ai/openais-sebastien-bubeck-says-he-tried-to-coordinate-release-of-navier-stokes-related-proofs-with-buckmaster-alpoge-but-was-rebuffed/)），OpenAI 并表示「我们（研究员和 agent）在他们公开之前，没有通过任何渠道看到他们的任何工作」（[OfficeChai](https://officechai.com/ai/openai-says-it-didnt-see-any-of-buckmaster-and-alpoges-work-while-resolving-navier-stokes/)）。

这不只是一桩罗生门。把时间线摊开看，它暴露的是一个更结构性的问题：AI 把解题速度压缩到以天计之后，数学界沿用了几百年的优先权制度，漏洞在哪里。

## 先讲清楚：他们在争的到底是什么

[Navier-Stokes 方程](https://www.claymath.org/millennium/navier-stokes-equation/)描述有粘性的流体怎么运动，天气预报、机翼气流的模拟底层都是它。千禧年难题问的是：给定光滑的初始状态，这套方程的解是否永远保持光滑，还是会在有限时间内「爆破」，即流速在有限时间内失去任何上界，光滑的解无法延续，方程作为物理模型随之失效。

一个常被忽略的细节：官方题面比大众印象宽。Clay 研究所的正式问题描述由 Charles Fefferman 撰写（[官方 PDF](https://www.claymath.org/wp-content/uploads/2022/06/navierstokes.pdf)），列了四个命题 (A)–(D)，证出任何一个即算解决。(A)(B) 是证明解永远光滑，要求不带外力；但 (C)(D) 是证明解会崩溃，且明确允许构造一个光滑的外力项（方程里代表外部施力的那一项）去逼出爆破。也就是说，「带外力的爆破」并非取巧，是官方认可的解法路径。这一点我直接查了 Fefferman 的原文。争议在于，不少数学家习惯把这个问题理解成无外力版本，所以就算带外力的证明成立，「算不算真正解决了 Navier-Stokes」在共同体内部也会继续吵。

这条外力路线是西班牙数学家 [Diego Córdoba](https://www.icmat.es/people/dcordoba/) 和 Luis Martínez-Zoroa 花数年开出来的。Buckmaster 在声明里说得很直白：基本思想的功劳全归他们两人，「我认为 Luis Martínez-Zoroa 配得上菲尔兹奖」。他和 Alpöge 做的，是用大语言模型把这条路从「粗糙外力」推进到「光滑外力」：两人以纯私人合作的方式（Alpöge 在 Anthropic 工作，但双方雇主均无机构参与，Buckmaster 用自己的科研经费付 OpenAI 的账单），用 Claude、Codex、GPT-5.6 Sol 等模型干了一年。8 月 15 日，他们拿到 Boussinesq 和三维 Euler 方程（Navier-Stokes 去掉粘性的近亲）的光滑外力爆破；8 月 22 日在 [Lean](https://github.com/tristanbuckmaster/fluid_lean) 里完成验证。Lean 是一种证明助手：把证明翻译成计算机可逐行检查的代码，机器验证通过，推理层面出错的风险就被压得很低。

然后他们做了一件按旧规范天经地义、按新规则却致命的事：不急着发。Buckmaster 说模型生成的第一版证明是「我读过的最不堪入目的」，两人围着这份证明连轴转改写，想先把它变成人类读者能看懂的论文再公开。这一改就是近三周。窗口就是这段时间。

## 谣言本身就是情报

因为 Alpöge 的雇主，风声在圈内变形为「Anthropic 解决了一个大问题」。按 OpenAI 自己的说法，它 9 月 1 日听到谣言后启动攻关，9 月 6 日完成。9 月 3 日，Buckmaster 听说自己工作的信息已传到 OpenAI，主动写邮件澄清；三天后就是开头那两通电话。

电话里的细节值得记下来。Buckmaster 说，对方最初的说法是模型「只拿到了问题陈述」、「几乎没有人类输入」，但随着 OpenAI 团队成员在内部聊天里不断给 Bubeck 发来更正，图景当场变了样：整个团队在攻关，试了多个方向，先让模型练手更容易的方程（包括 Euler），展示给他看的那条 prompt 本身也是用 Codex 写的，用掉的算力「多到疯狂」（[TechCrunch](https://techcrunch.com/2026/09/08/openai-fought-dirty-on-career-making-math-problem-says-nyu-mathematician/) 报道称约三千亿个输出 token）。他问第一条 prompt 是什么时候发出的，对方拖了许久才承认：就在过去几天，在他们的工作信息传到 OpenAI 之后。

注意 OpenAI 否认的和承认的分别是什么。它否认看过两人的任何具体工作，事后也承认了两人在带外力 Euler 结果上的优先权、表示不会申领克雷奖金；但它不否认是听到谣言才动手的。在旧的学术伦理里，「我没看你的手稿」就算清白。问题是，优先权制度隐含一个前提：从「知道某条路走得通」到「写出完整证明」隔着以年计的人力，所以光知道别人接近答案没有太大用处。AI 恰好废掉了这个前提。当执行只需要一个周末和一笔算力预算，「哪个问题熟了、哪条路可行」这条信息就成了全部稀缺所在。Buckmaster 说，听到「forced」这个词他立刻警觉，因为这条路上几乎没有别人，「这不是把问题陈述丢给模型几天就能自己找到的方向」。坐标一旦泄露，搜索空间瞬间塌缩。谣言不需要附带任何一个引理，它本身就是载荷。

还有一层更不舒服的结构。两人整个项目的草稿都放在 Codex 的工作会话里，那是 OpenAI 自家的产品。Buckmaster 问：模型是否访问过、或用我们的会话训练过？访问的答复是「模型不查用户数据」；训练的问题，他说自己没有得到回答。OpenAI 事后补充：不能排除去标识化的使用数据在总体上改进了其系统（[OpenAI 公告](https://openai.com/index/navier-stokes-solution/)）。我没有任何证据表明数据被不当使用，Buckmaster 自己也在声明里说「我不指控任何人任何事，我只陈述我被告知了什么、何时、以及向我提议了什么」。但结构性的事实摆在那里：你的基础设施供应商同时是你的竞争对手，而「模型不查用户数据」这样的答复，外部无从验证。理性的研究者只有一种反应，就是不再把未发表的想法放进对手的云工具。

## 陶哲轩的「不可再生资源」

风波爆发前六天，陶哲轩在[个人页面](https://teorth.github.io/tao-web/ai-views.html)写下一个判断：人类积累的开放数学问题，第一次变成了「类似不可再生资源的东西」。问题本身无穷无尽，但经过长期领域浸泡才能识别出的「好问题」是稀缺的；一个好问题一旦被公开解掉，就永久失去了训练和评估价值。他推演的最坏情形几乎是预言：仅仅一条「有人在攻某问题」的谣言，就可能引来大规模算力抢先收割，而激励会随之反转，研究者不再分享有前景的方向，「逆转几个世纪的开放科学传统，对这个领域的未来造成严重的长期伤害」。[Fortune](https://fortune.com/2026/09/08/openai-says-it-cracked-navier-stokes-math-grand-challenge-buckmaster-accusation-cheating-intimidation-tao-lament/) 引用他的话说，对开放问题不加区分的露天开采，可能摧毁下一代数学技术、问题和从业者赖以成长的生态。

要说清楚的是，陶哲轩并不反对 AI 做数学。他在 [9 月 7 日的博客](https://terrytao.wordpress.com/2026/09/07/finite-time-blowup-with-smooth-forcing-term-for-the-incompressible-porous-medium-boussinesq-and-incompressible-euler-equations/)里正面、细致地讨论了 Buckmaster 和 Alpöge 的数学内容，认为照此推进，无外力情形「在不远的将来看起来非常可行」。两位当事人自己在这项工作里就大量使用 LLM。冲突不在人与 AI 之间，而在两种用法之间：数学家用模型延长自己的手，和实验室用算力集群收割别人标记出的矿脉。

## 关键结论

这件事给所有做研究、也给所有做 AI 的人留下三条具体判断。

第一，优先权的证据标准变了。Buckmaster 手里最硬的东西，是 8 月 22 日完成 Lean 验证的记录（日期出自他的声明）和公开的 GitHub 仓库；OpenAI 也在公告里同步放出了证明全文和 Lean 形式化，供外界复验（[TechCrunch](https://techcrunch.com/2026/09/08/openai-fought-dirty-on-career-making-math-problem-says-nyu-mathematician/)）。双方都拿得出机器可验证的证明，真正要争的只剩时间戳。形式化验证本来是给证明上保险的，现在多了一个用途：给优先权上时间戳。「我先做出来的」以后要靠机器可验证的存证来主张，靠不了君子协定。

第二，「写好再发」的质量规范成了战略脆弱点。两人多等了近三周是为了对得起读者和共同体，代价是给了别人一个周末的窗口。这个两难没有干净解法：抢时间就得发布连作者自己都称为「AI slop」的写作，讲质量就得承担被抢跑的风险。学术共同体需要一种新的存证发布方式，让「我到了这里」和「这是可读的论文」两件事解耦。

第三，对 AI 实验室，这暴露的是治理短板。OpenAI 事后的姿态是体面的：祝贺、承认两人在带外力 Euler 上的优先权、不申领奖金。但按 Buckmaster 的单方记录，谈判桌上先出现的是「把 Alpöge 从作者里去掉」的提议和「你为什么要毁掉自己的职业生涯」。哪怕这些对话细节最终各执一词，一个行业若想让科学界把最好的问题交给它的模型，先得让科学界相信它不会顺手把问题收走。

如果这样的进展持续，剩下的千禧年难题或许真会在几年内被逐个解开——这一点我说不准。悬而未决的是另一件事：解完之后，还有没有人愿意把下一个好问题说出口。

## 参考来源

- [Tristan Buckmaster 公开声明（PDF）](https://cims.nyu.edu/~tristanb/statement.pdf) — 完整时间线、通话内容、两项提议、全部引语的一手来源
- [Fefferman：Navier-Stokes 官方问题描述（Clay 研究所 PDF）](https://www.claymath.org/wp-content/uploads/2022/06/navierstokes.pdf) — 核实命题 (A)–(D) 四选一、(C)(D) 允许光滑外力
- [Terence Tao：AI 观点页](https://teorth.github.io/tao-web/ai-views.html) — 「不可再生资源」「污染」「激励反转」的原始出处（9 月 2 日）
- [Terence Tao：三篇爆破预印本的数学评述](https://terrytao.wordpress.com/2026/09/07/finite-time-blowup-with-smooth-forcing-term-for-the-incompressible-porous-medium-boussinesq-and-incompressible-euler-equations/) — Córdoba–Martínez-Zoroa 路线沿革、结果评价、无外力前景
- [OpenAI 公告](https://openai.com/index/navier-stokes-solution/) — 时间线（9/1 启动）、否认看过两人工作、「不能排除去标识化数据」表述、证明全文与 Lean 形式化的发布入口
- [TechCrunch](https://techcrunch.com/2026/09/08/openai-fought-dirty-on-career-making-math-problem-says-nyu-mathematician/) — 三千亿输出 token、OpenAI 公开证明全文、OpenAI 回应
- [Scientific American](https://www.scientificamerican.com/article/openai-claims-blockbuster-math-breakthrough-amid-swirl-of-controversy/) — OpenAI 称证明经 Lean 验证
- [Engadget](https://www.engadget.com/2253393/whats-going-on-with-openai-and-the-navier-stokes-controversy/) — OpenAI 不申领奖金的表态
- [Fortune](https://fortune.com/2026/09/08/openai-says-it-cracked-navier-stokes-math-grand-challenge-buckmaster-accusation-cheating-intimidation-tao-lament/) — 陶哲轩「露天开采」引语、9 月 3/6/8 日时间线
- [OfficeChai](https://officechai.com/ai/openai-says-it-didnt-see-any-of-buckmaster-and-alpoges-work-while-resolving-navier-stokes/) — OpenAI「未通过任何渠道看到」声明引语
- [OfficeChai](https://officechai.com/ai/openais-sebastien-bubeck-calls-tristan-buckmasters-claims-of-trying-to-take-credit-for-fluid-dynamics-proofs-false-and-inflammatory/) — Bubeck「不实且具煽动性」引语
- [OfficeChai](https://officechai.com/ai/openais-sebastien-bubeck-says-he-tried-to-coordinate-release-of-navier-stokes-related-proofs-with-buckmaster-alpoge-but-was-rebuffed/) — Bubeck 否认要求除名、短信记录
- [Unite.AI](https://www.unite.ai/buckmaster-and-alpoge-post-ai-fluid-blowup-proofs-dispute-openai-contact/) — 三篇预印本细节、8 月 15/22 日期、Lean 仓库地址
