---
title: "Debian 给 LLM 投票:写进章程的禁令,拦得住检测不出来的东西吗"
description: "Debian 就 LLM 使用开启全员公投,四个提案从全面禁止到附条件放行。拆开条文看,真正可执行的只有披露与问责——Gentoo、QEMU、Fedora 也都撞上过同一堵墙。"
pubDate: 2026-07-25
tags: [ai-governance, open-source, debian]
lang: zh
slug: debian-llm-general-resolution
translationOf: debian-llm-general-resolution
---

2026 年 7 月 24 日,Debian([1993 年创立](https://www.debian.org/doc/manuals/project-history/intro.en.html)的最老牌社区驱动 Linux 发行版之一,[Ubuntu 就是在它基础上构建的](https://www.debian.org/derivatives/))开启了一场全员公投(General Resolution,简称 GR,由全体 Debian 开发者投票表决的正式决议)的讨论期,议题只有一个:开发者能不能用 LLM 参与 Debian 的官方工作。[官方投票页面](https://www.debian.org/vote/2026/vote_002)上,提案一共四个。

有意思的是附议名单。Ian Jackson 自己提出了要求项目「尽可能拒绝 LLM」的提案 C,却同时附议了最严格的全面禁令提案 A;Pierre-Elliott Bécue 一边提出最宽松的提案 D(接受 AI 贡献、责任归提交者),一边也附议了 A。给对立阵营的提案附议,看着像立场混乱,其实是 Debian 投票规则下的正常操作。

先把规则说清楚。附议(second)的意思只是「联署,让这个提案获得上选票的资格」,不代表赞成——一个提案凑够[宪章](https://www.debian.org/devel/constitution)规定数量的附议就能成为候选项,仅此而已。正式投票用的是排序投票:每个投票人不是四选一,而是给选项(包括默认选项「以上皆非」,None of the above)按偏好排序——不必排完所有选项,没排的视为彼此并列,且低于所有已排序项;计票时把选项两两配对比较——比如 A 对 B,数把 A 排在 B 前面的票多,还是把 B 排在 A 前面的票多——如果有一个选项能在两两对决中赢过其余所有选项,它就当选。宪章附录 A 规定的具体算法,Debian [官方称作 Condorcet/Clone Proof SSD](https://www.debian.org/vote/2003/vote_0002)(即 Cloneproof Schwartz Sequential Dropping),属于 Condorcet 法的一种,作用是在出现循环胜负(A 胜 B、B 胜 C、C 又胜 A)时也能定出赢家。这套规则下,选票上多一个选项,远不像简单多数制那样容易「分票」:你把自己支持的方案排第一、反对的排最后,基本不会因为对手的方案上了选票而吃亏。Jackson 和 Bécue 没有公开解释为什么附议对立提案,但客观效果清楚:光谱的两端都被摆上了选票,最严的禁令和最松的放行都要参与两两对决,胜出的方案不是只赢了几个没人真心支持的陪跑方案。

我说这套流程比大多数公司和行业组织制定 AI 政策的方式干净,干净在「谁来决定哪些选项能被讨论」这一步。就我的观察,公司里常见的流程是:一个小团队起草一份政策,层层审批,员工至多在既定草案上提提意见,「全面禁止」「彻底放开」这类选项从一开始就不在桌面上——控制议程的人预先框定了结果的范围。Debian 这边,任何开发者都可以提案,对手会帮你把提案送上选票,全体投票者的排序决定胜负,每个落选方案都与胜出方案正面比过。议程被少数人预先框定的空间,被压到了最低。

## 四个提案,两个真问题

表面看,四个提案是「禁止/劝阻/附条件允许/放行」的光谱。拆开条文,它们其实在回答两个更根本的问题:LLM 产出算什么性质的问题,以及规则靠什么执行。

**提案 A(Matthias Geiger)**:全面禁止 LLM 或生成式 AI 辅助的直接贡献,覆盖源码包、官方工具、网站、文档、翻译和官方通信,并要把这条禁令写进社会契约(Social Contract,Debian 的基础文件之一,相当于项目章程)。理由是 LLM 产出「法律状态非常不清晰」、生成的打包质量差、破坏社区以审代教的人才培养机制,外加对 LLM 公司无差别抓取全网内容的伦理反对。有两个细节值得注意:上游(upstream)软件用 LLM 不在管辖范围——Debian 只负责打包分发;而修改基础文件按宪章需要 3:1 绝对多数——把该选项排在默认选项「以上皆非」之前的票数,须达到反向排序票数的三倍——门槛远高于普通决议。

**提案 B(Lucas Nussbaum)**:允许,附六个条件——AI 工具的服务条款不得与 Debian 的分发冲突;引入第三方受版权材料前自查许可证;提交者对技术质量、安全性、许可证合规负全责;贡献的「显著部分」由工具生成或大幅辅助时必须披露(如用 Git trailer,即提交信息末尾的标注行);批量或自主生成的贡献须事先与社区讨论;不得把项目非公开信息传给不可信的云端服务。

**提案 C(Ian Jackson)**:政治宣言与可执行规则的混合体。前半段是表态:请贡献者避免使用 LLM,请各级决策者尽量劝阻,并呼吁整个自由软件世界远离这项技术。后半段才是硬规则:凡是写给人看的信息(bug 报告、邮件列表、博客)必须由人亲笔起草;任何 LLM 使用必须披露;子项目和维护者有权彻底禁用 LLM 贡献,且禁令必须被尊重;违反者按行为准则(Code of Conduct)处理。最后一条豁免耐人寻味:非英语母语者可以直接用母语写作,不必为语言错误羞愧——「用 LLM 润色英文」这类常见用例,恰好落在这条豁免给出的替代路径上。

**提案 D(Pierre-Elliott Bécue)**:接受 AI 贡献,前提是提交者负全责、能证明自己充分理解所提交的内容、亲自完成签名与提交,AI 辅助的工作应在提交信息或 changelog 中标注。它还写下了一个诚实的例外:像 Copilot 的 tab 补全这类轻量生成工具,使用者可能根本意识不到背后是生成式模型,「因此我们信任提交者自行判断规则是否适用」。

## 每款规则的命门都在同一处

放到实际协作场景里推演,四个方案撞上的是同一堵墙:LLM 产出目前无法被普遍、可靠地检测——[对抗性研究显示](https://arxiv.org/abs/2303.11156),对生成文本做几轮改写,就能让各类检测器的命中率大幅下降。

禁令的执行成本因此是无限的。没有检测手段,提案 A 大概率只能靠自觉,而我推断它的实际效果是把使用赶到地下——最需要披露信息的审阅者,恰恰因为禁令的存在拿不到披露。提案 C 的「给人的信息必须人写」面对同样的检测不对称:[检测研究显示](https://aclanthology.org/2025.coling-main.288/),分类器对文体和文本难度高度敏感,某些情况下会退化成随机猜测——流利的 LLM 英文未必查得出来,风格不合审阅者预期的人类写作反而可能被误伤,这正是它第 8 条豁免要对冲的副作用。

披露制(B、C、D 的交集)的软肋在触发线上。「显著部分」由提交者自我裁量;D 的轻量工具豁免更是等于承认,随着 LLM 下沉到 IDE 补全、拼写检查和翻译,「用没用 AI」的边界每年都在漂移。今天写下的条文,冻结的是 2026 年的工具形态。

真正可执行的只剩问责:你签了名,你负责。这不是新发明,而是 [DCO](https://developercertificate.org/)(Developer's Certificate of Origin,开发者来源证明——提交者以签名担保自己有权以相应许可证提交这份代码)逻辑的延伸。它把一个不可判定的来源问题,换成了一个总有签名记录可查的担保问题。

横向看,其他项目已经把这条曲线走了一遍。[Gentoo](https://wiki.gentoo.org/wiki/Project:Council/AI_policy) 2024 年 4 月由理事会通过禁令,提案人 Michał Górny [向 LWN 表示](https://lwn.net/Articles/970072/),执行靠的是信任而非检测,项目不会主动排查贡献是否用了 AI;[QEMU](https://www.qemu.org/docs/master/devel/code-provenance.html) 以 DCO 法律风险为由「拒收一切被认为包含或衍生自 AI 生成内容的贡献」,但 2026 年 5 月维护者 Paolo Bonzini [提交补丁](https://lists.nongnu.org/archive/html/qemu-devel/2026-05/msg07614.html),提议对 20 行以内的小型修复,以及测试、文档类改动放行,换取 `AI-used-for:` 提交标注——截至本文写作,官方文档仍是禁令,补丁还在邮件列表讨论;[Fedora](https://communityblog.fedoraproject.org/council-policy-proposal-policy-on-ai-assisted-contributions/) 则在 2025 年 10 月直接通过「允许 + Assisted-by 披露 + 人负全责」的政策。三个项目起点不同,走到的位置也不同:Fedora 已经落在披露加问责上,QEMU 正朝这个方向挪,Gentoo 的禁令还立着——但连这条禁令,承认的执行方式也是信任提交者。原因是机制性的——「这段代码是不是 AI 写的」不可判定,「谁为这段代码签名担保」总有记录可查,治理只能建在可判定的东西上。

## 值得盯的不是结果

按排序投票的中位偏好推演,我的赛前判断是:某个披露加问责的方案胜出是大概率,提案 A 即便附议者众多,3:1 的修宪门槛也极难跨过——这是预测,不是定论,投票结果会给出检验。真正值得等的是投票公布的完整排序数据:实际参与投票的 Debian 开发者对 LLM 的偏好分布,一份来自正式投票的一手数据。

而对开源世界之外的 AI 治理讨论,这场公投提前演完了一整套推演:当检测不可行,禁令退化为表态,规则最终能抓住的只有两样东西——事前的披露义务,和事后为产出签名担责的那个人。各国正在推进的 AI 生成内容标注义务立法——比如[欧盟 AI Act 第 50 条](https://artificialintelligenceact.eu/transparency-rules-article-50/)对合成内容的机器可读标注要求,2026 年 8 月起适用——在我看来,迟早要面对 Debian 这四份提案已经摊开的同一个难题。

## 参考来源

- [Debian GR: LLM usage in Debian(vote_002)](https://www.debian.org/vote/2026/vote_002) — 四个提案全文、提案人与附议名单、讨论期起始日期
- [Debian Constitution](https://www.debian.org/devel/constitution) — 基础文件修改需 3:1 多数(§4.1.5)、排序投票方法与默认选项(附录 A、§4.2)
- [Debian vote_0002(2003)](https://www.debian.org/vote/2003/vote_0002) — 投票制度官方名称 Condorcet/Clone Proof SSD
- [Gentoo Council AI Policy](https://wiki.gentoo.org/wiki/Project:Council/AI_policy) — 2024 年 4 月 14 日禁令议案原文及适用范围
- [LWN: Gentoo bans AI-created contributions](https://lwn.net/Articles/970072/) — 提案人 Górny 关于禁令靠信任而非检测执行的说明
- [QEMU: Code provenance 文档](https://www.qemu.org/docs/master/devel/code-provenance.html) — QEMU 现行拒收 AI 生成内容政策原文及 DCO 理由
- [qemu-devel: docs/devel: relax policy on AI-generated contributions](https://lists.nongnu.org/archive/html/qemu-devel/2026-05/msg07614.html) — Bonzini 2026 年 5 月放宽提案:适用类别与 AI-used-for 标注
- [Fedora Community Blog: Council Policy Proposal on AI-Assisted Contributions](https://communityblog.fedoraproject.org/council-policy-proposal-policy-on-ai-assisted-contributions/) — Fedora 政策内容,2025 年 9 月提出、10 月 22 日批准
- [Developer Certificate of Origin](https://developercertificate.org/) — DCO 1.1 文本原文
- [Sadasivan et al.: Can AI-Generated Text be Reliably Detected?](https://arxiv.org/abs/2303.11156) — 改写攻击可大幅降低 AI 文本检测器命中率
- [Exploring the Limitations of Detecting Machine-Generated Text(COLING 2025)](https://aclanthology.org/2025.coling-main.288/) — 检测器对文体与文本难度高度敏感,可能退化为随机分类
- [EU AI Act 第 50 条透明度义务](https://artificialintelligenceact.eu/transparency-rules-article-50/) — 合成内容机器可读标注要求,2026 年 8 月 2 日起适用
