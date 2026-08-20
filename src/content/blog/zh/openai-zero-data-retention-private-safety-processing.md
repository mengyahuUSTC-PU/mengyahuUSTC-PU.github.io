---
title: "数据一条不留,坏事照样能查?拆解 OpenAI 的「私有安全处理」"
description: "OpenAI 承诺前沿模型继续零数据留存,并预览「私有安全处理」;而 Anthropic 一个多月前刚要求企业客户接受 30 天留存。同一个问题,两家头部实验室给了相反答案。"
pubDate: 2026-08-19
tags: [ai-governance, data-privacy, enterprise-ai]
lang: zh
slug: openai-zero-data-retention-private-safety-processing
translationOf: openai-zero-data-retention-private-safety-processing
---

8 月 19 日,OpenAI 发了一篇公告:[前沿模型将继续提供零数据留存(Zero Data Retention,ZDR)](https://openai.com/index/offering-zero-data-retention-for-frontier-models/),同时预览一套叫「私有安全处理」(Private Safety Processing)的新机制。单看像一次例行的企业功能更新。放进背景里看,这是一次正面交锋:[Anthropic 宣布](https://privacy.claude.com/en/articles/15425996-data-retention-practices-for-covered-models)已有的零留存协议不再覆盖 Mythos 级模型(Claude Mythos 5 和 Claude Fable 5),企业客户想用这两个模型,就必须接受提示词和输出被留存 30 天,政策 6 月 9 日生效。[TechCrunch 的标题](https://techcrunch.com/2026/08/19/openai-seeks-to-one-up-anthropic-with-new-customer-privacy-protections/)写得很直白:OpenAI seeks to one-up Anthropic。

同一个问题——前沿模型的滥用监测到底要不要留客户数据——两家给了相反答案。这篇拆一下各自的技术路线,以及「审查有害内容」和「保护数据隐私」在工程上如何兼容。

下文的公告细节,我用 [OpenAI 官方 X 帖](https://x.com/OpenAI/status/2090165328290701800)以及 Axios、TechCrunch、Computerworld 三家的报道做了交叉核实。

## 零留存承诺的是什么,不承诺什么

ZDR 是 API 供应商与其审批通过的企业客户之间的一种合同安排:在符合条件的端点上,你发来的提示词和模型生成的输出,推理完成后不再留存。[OpenAI 的数据用途文档](https://developers.openai.com/api/docs/guides/your-data)对这条边界有明确界定,包括写明的例外(疑似 CSAM 在内)和获得这项资格所需的事先审批。注意它管不到什么:在标准的托管 API 部署里,你的请求仍然要送到供应商的服务器上、以可读形式被处理,ZDR 管的是「处理完之后数据怎么办」,不是「处理」本身。

对律所、医院、金融机构这类自身对用户负有保密义务的客户,留存条款天然是合规审查里的一个卡点。数据在第三方存 30 天是否可接受,要看具体合同条款、所在司法辖区和数据类型,没有一概而论的答案——正因如此,「一条不留」是其中最不需要逐条论证的选项,尽管我们后面会看到,「零」从来不是字面意义的零。

## 冲突出在哪:滥用监测天然想要历史数据

供应商这边的滥用监测(abuse monitoring)——按 [OpenAI 的数据用途文档](https://developers.openai.com/api/docs/guides/your-data),就是自动分类器加日志,日志可能包含提示词、回复和分类器输出,用来执行使用政策、缓解有害用途——有一个和零留存直接冲突的需求:看历史。

单条消息级别的安全分类器,只能看见孤立请求。TechCrunch 把这类行为的一般模式描述为坏人「把请求分散开来躲避检测」。一个假想的场景(这是我自己构造的,不是来自公告)是把一件坏事拆碎:今天在一个会话里问一段网络扫描代码,明天换个会话问权限提升,后天再问持久化驻留。每一条单看都是正常的编程问题,拼起来是完整的入侵工具开发流程。要识别这种拆碎的模式,系统必须能跨会话回看。而 AI 越是 agent 化——任务运行更久、自主性更强、单个任务包含的交互越来越多——这个需求越尖锐。OpenAI 在 X 帖里自己就是这么论证的:「随着 AI 承担更长、更自主的工作、为企业创造更大价值,安全系统也需要跨相关交互识别风险。」Anthropic 给 30 天留存的理由同样是安全工作需要。

于是矛盾摆在桌面上:客户要「一条不留」,安全团队要「留下来慢慢看」。两家的分歧,在于谁向谁让步。

## Anthropic 的路线:承认要留,用流程管住谁能看

Anthropic 的方案是治理约束型。按[官方政策页](https://privacy.claude.com/en/articles/15425996-data-retention-practices-for-covered-models),Mythos 级模型的输入输出留存 30 天后自动删除(被安全系统标记或依法必须保留的内容除外);默认员工无法访问;人工审查「只能经由一条受控访问路径进行」,在自动信任与安全系统标记出潜在危害内容时触发;每一次访问都记录在审查员无法屏蔽、无法修改的防篡改日志里;符合条件的组织可以再加客户自管加密密钥和访问透明审计日志。这套要求覆盖所有接入渠道,包括 AWS Bedrock、Google Cloud、Microsoft Foundry 上的零留存客户;不接受留存,就用不了这两个模型。

注意客户自管密钥在这个方案里的实际角色:数据仍然不在客户自己手里——直连 API 时存在 Anthropic 一侧,经 Bedrock、Google Cloud 这类云渠道接入时留存在对应的云平台上——内容被标记后,仍可能有审查员经受控路径看到明文。整个方案的本质是「数据在供应商侧,但用流程保证只有该看的人在该看的时候看」。信任的对象是流程。

## OpenAI 的路线:换掉明文历史的存放地和钥匙归属

OpenAI 的「私有安全处理」走的是另一条路:不碰「留不留」,改「留在哪、谁持钥匙」。据 [Axios](https://www.axios.com/2026/08/19/openai-previews-zero-retention-safety-system-as-anthropic-requires-data-logs) 转述,给客户两个部署选项:一,用于安全分析的历史数据留在客户自己控制的基础设施上;二,由 OpenAI 存储,但用客户控制的密钥加密,OpenAI 不持有密钥副本,员工无法解密。自动系统在这些数据上做跨交互的模式分析,发现疑似滥用时,只向 OpenAI 发回一个「狭义定义的信号」(a narrowly defined signal),提示存在某种特定类型的活动,不带出提示词和回复本身。据 TechCrunch,信号触发后由 OpenAI 决定是否需要行动,客户可以自愿共享相关数据配合处置。

这里有一个公告没有回答的关键技术问题:分类器要判断内容危不危险,就必须读到明文。明文存在客户侧,或锁在客户密钥的加密存储里,那这个分类器在哪里运行、由谁解密?我能想到三种实现(以下是我的推测,公告没说):分类器作为组件跑在客户基础设施内;跑在[机密计算环境](https://confidentialcomputing.io/)里(TEE,可信执行环境——处理器提供的加密隔离区,解密只发生在隔离区内,连机器和云平台的运营方都读不到隔离区内存);或者在推理发生的当下同步打分,只持久化分数、不持久化内容。三种实现的信任模型完全不同。OpenAI 说 9 月开始推出并发布技术白皮书,在那之前,我只能核实「承诺是什么」,核实不了「实现是什么」。

还有两个口子说明「零」从来不是字面意义的零。其一,法律例外:即便是零留存部署,被标记为疑似 CSAM(儿童性虐待材料)的图像仍会被留存,供人工审查和依法上报,[Computerworld](https://www.computerworld.com/article/4211661/openai-temporarily-slows-scaling-efforts-also-promises-zero-data-retention-for-select-frontier-model-customers.html) 采访的咨询顾问、FormerGov 执行董事 Brian Levine 说得直接:「零从来不是真正的零。」其二,那个「安全信号」本身,就是从客户数据里提炼出来、交到 OpenAI 手上的信息。信号的字段定义得多窄,决定这条通道能带出多少东西。这是白皮书需要回答的第二个问题。

这个思路似曾相识:内容留在用户一侧,只把「是否命中危险模式」的判定结果送回厂商——[2021 年 Apple 提出、2022 年底放弃的客户端 CSAM 扫描方案](https://9to5mac.com/2022/12/07/apple-confirms-that-it-has-stopped-plans-to-roll-out-csam-detection-system/)走的就是这个方向。两者技术上并不相同:Apple 做的是设备端哈希匹配加[账户级阈值](https://9to5mac.com/2021/08/19/apple-csam-system-tricked/)(累计 30 张命中图像才会触发 Apple 的服务器端审查),不是跨交互的行为分类,只能算取向相近的有限类比。但当年的争议在今天原样适用:[安全学界的联名论文](https://arxiv.org/abs/2110.07450)集中批评的一点是,扫描通道一旦建成,可能被扩展为超出最初声明用途的监控工具,匹配规则也可能悄悄扩大。企业客户评估「私有安全处理」时,这个问题一样要问。

## 怎么用这条新闻做决策

两家表面上背道而驰,方向其实在收敛:内容都交给自动系统看,人的角色被压到最小——Anthropic 模式下,少数审查员在内容被标记后仍可经受控路径读到明文;OpenAI 模式下,按公告的说法,员工连被标记的内容也读不到,只能看到信号。剩下的分歧收窄成一个变量:跨会话的明文历史放在谁手里、谁持有钥匙。Anthropic 的答案是「放我这,我管好流程」;OpenAI 的答案是「放你那,或者锁上、钥匙给你」。

对企业客户,这意味着合规评估的问法要变。过去审的是供应商的政策文本,现在应该逐层问三个技术问题:明文历史物理上存在哪里;谁能解密,解密发生在什么执行环境;离开客户边界的信号具体包含哪些字段。Anthropic 模式下,这三个问题的答案主要写在政策和审计条款里;OpenAI 模式下,如果白皮书兑现承诺,答案有一部分可以写进架构,由第三方独立验证。可验证性落在哪一层,是两条路线的本质区别。

但今天就下结论为时过早。OpenAI 目前交付的只有承诺和预览:「符合条件的企业与 API 客户」的资格标准没有公布——[OpenAI 自家的文档](https://developers.openai.com/api/docs/guides/your-data)只说这些控制需要事先审批、有意向的客户请联系销售团队,Computerworld 特意点了这一点。分类器的运行环境、信号的具体定义、误报后的处置流程,同样没有公开答案;9 月的白皮书是最早可能给出答案的机会,而且没人保证它会全部覆盖。白皮书如果写得含糊,这次公告就只是一次对着 Anthropic 的营销卡位;如果详细到可以复核,它会反过来给整个行业的滥用监测施压:既然工程上能把「人看不到内容」做实,那「为了安全所以必须留你的数据」这个默认等式,就再也不能当作不证自明的前提了。

我的判断是后一种可能值得认真对待。9 月见白皮书。

## 参考来源

- [Offering Zero Data Retention for frontier models — OpenAI](https://openai.com/index/offering-zero-data-retention-for-frontier-models/) — 公告主体(内容经官方 X 帖与下列三家报道交叉核实)
- [OpenAI 官方 X 帖](https://x.com/OpenAI/status/2090165328290701800) — 「继续为前沿模型提供 ZDR」「安全系统需要跨相关交互识别风险」的官方原话
- [Your data — OpenAI API 文档](https://developers.openai.com/api/docs/guides/your-data) — ZDR 的官方定义(适用端点、事先审批、例外条款)与滥用监测日志的官方说明
- [Data retention practices for Covered Models — Anthropic Privacy Center](https://privacy.claude.com/en/articles/15425996-data-retention-practices-for-covered-models) — Anthropic 30 天留存政策的全部细节:覆盖模型、生效日期(2026-06-09)、员工访问限制、防篡改日志、客户自管密钥选项
- [OpenAI previews zero-retention safety system as Anthropic requires data logs — Axios](https://www.axios.com/2026/08/19/openai-previews-zero-retention-safety-system-as-anthropic-requires-data-logs) — 两个部署选项(客户基础设施/客户密钥加密)、safety signal、9 月白皮书、CSAM 例外
- [OpenAI seeks to one-up Anthropic with new customer privacy protections — TechCrunch](https://techcrunch.com/2026/08/19/openai-seeks-to-one-up-anthropic-with-new-customer-privacy-protections/) — 竞争定位、信号触发后的处置流程、客户可自愿共享数据
- [Computerworld 报道](https://www.computerworld.com/article/4211661/openai-temporarily-slows-scaling-efforts-also-promises-zero-data-retention-for-select-frontier-model-customers.html) — 资格标准未公布、咨询顾问 Brian Levine「零从来不是零」评论
- [Apple confirms it has stopped plans to roll out CSAM detection system — 9to5Mac](https://9to5mac.com/2022/12/07/apple-confirms-that-it-has-stopped-plans-to-roll-out-csam-detection-system/) — Apple 客户端扫描方案 2021 年提出、2022 年 12 月放弃的时间线与设备端匹配设计
- [Apple's CSAM system details — 9to5Mac (2021)](https://9to5mac.com/2021/08/19/apple-csam-system-tricked/) — 触发服务器端审查前累计 30 张图像的账户级阈值的出处
- [Bugs in Our Pockets: The Risks of Client-Side Scanning — arXiv](https://arxiv.org/abs/2110.07450) — 客户端扫描被滥用、被扩展为监控工具的风险分析
