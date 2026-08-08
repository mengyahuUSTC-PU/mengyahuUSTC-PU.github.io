---
title: "养老虎的人无需有过错也要赔：这条古老规则轮到 AI 实验室了吗"
description: "《经济学人》提议用「危险动物饲养人严格责任」追究 AI 实验室。这个类比在法理上出奇地顺，但在因果链、危险认定和保险市场三个环节都会卡住。"
pubDate: 2026-08-07
tags: [ai-governance, ai-liability, ai-insurance]
lang: zh
slug: ai-labs-strict-liability-dangerous-animals
translationOf: ai-labs-strict-liability-dangerous-animals
---

普通法里有一条很老的规则：你养了一头老虎，老虎咬伤了邻居，邻居不需要证明你的笼子不结实，也不需要证明你喂食时忘了锁门。养猛兽这件事本身就足够，你赔。英国 1971 年的[《动物法》](https://www.legislation.gov.uk/ukpga/1971/22)把它写成成文法：危险物种的饲养人对动物造成的损害承担「严格责任」（strict liability），饲养人有没有疏忽，法庭不问。

8 月 6 日，《经济学人》发文提问：[AI 实验室是否应该被当成危险动物的饲养人来对待](https://www.economist.com/science-and-technology/2026/08/06/should-ai-labs-be-treated-like-the-owners-of-dangerous-animals)，文章在 [Hacker News 上吵了五十多层楼](https://news.ycombinator.com/item?id=49217629)。标题像个法学思想实验，正文不是：它从三周内四起模型自主攻击真实第三方的事件讲起，落在「现行法律追责不了没有意图的攻击者」这个具体缺口上。事件和它背后的法学论证，都值得拆开看。

## 类比之前：三周里的四起真实攻击

这条新闻线我在快讯里逐条跟过，按时间摆齐是这样的：

- **OpenAI**：7 月 16 日，Hugging Face [披露](https://huggingface.co/blog/security-incident-july-2026)检测到并遏制了一次由 AI agent 执行的入侵，当时不知道攻击者是谁。7 月 21 日 [OpenAI 认领](https://openai.com/index/hugging-face-model-evaluation-security-incident/)：攻击者是自家模型——GPT-5.6 Sol 加一个未发布的更强模型——它们当时正在本应与外网隔离的沙箱里跑网络攻击能力评测，为测出能力上限还关掉了平时拦截攻击类请求的防护。模型链式利用多个漏洞（包括一个零日漏洞，即此前无人知晓、没有补丁的漏洞）钻出沙箱，进了 Hugging Face 的生产系统（[7 月 21 日快讯](/zh/briefing-2026-07-21)）。OpenAI 此前的长时程模型安全复盘里已有模型逃出评测沙箱、到公开仓库开 PR 的案例，[我 7 月写过](/zh/openai-long-horizon-safety-incidents)。
- **Anthropic**：7 月 30 日承认自家模型在安全测试中也出过同类事，[媒体报道的口径](https://techcrunch.com/2026/07/30/anthropic-says-its-own-ai-models-breached-three-companies-during-security-tests/)是三家公司的生产系统被实际触及，《经济学人》引述的数字是共发现六次针对第三方的攻击。起因和 OpenAI 不同：评估环境配置失误，该隔住的没隔住。
- **英国 AISI**：8 月 4 日，英国政府的 AI 安全研究所（AI Security Institute）发布[事故报告](https://www.aisi.gov.uk/blog/incident-report-unsanctioned-agent-behaviour-during-cyber-testing)：7 月下旬的网络安全评测里，122 次运行中出现 19 起针对公开互联网上真实个人和机构的越权操作。最严重的一起是供应链投毒未遂——所谓供应链攻击，不是直接进攻目标，而是先在目标会安装、更新的上游软件里埋进恶意代码，等目标照常更新时顺流而入。评测题目里的攻击目标是虚构的，但 agent 为了解题，注册假 GitHub 账号向一个真实的开源项目提交恶意代码，还伪造第二个身份冒充独立审核者劝维护者合并，最后靠项目的人类维护者把代码拦了下来（[8 月 5 日快讯](/zh/briefing-2026-08-05)）。要说明的是，AISI 的测试从来就允许模型联网、也有意关掉了攻击拦截层，为的是测真实能力上限；按它的说法，此前从未见过为攻破目标而不惜殃及无关者的模型。
- **Meta**：紧接着，Meta 也经发言人向媒体证实（[CNN](https://www.cnn.com/2026/08/05/tech/meta-ai-hacking)；Meta 未发官方公告），自家 Muse Spark 1.1 在网络安全测试中攻入另一家公司的系统：外部评测公司把沙箱配错，模型意外拿到了联网权限。

四起事件全部发生在测试或评估环境，没有一起是面向用户的生产事故；但被攻击的第三方都是真实的。细节各有出入——OpenAI 的沙箱是被模型自己突破的，Anthropic 和 Meta 是环境没配对，AISI 是有意放开联网——共同点只有一个：整个过程里，人的参与止步于下达任务。也有人把厂商自曝说成博眼球，《经济学人》的反驳很实在：没有公司会靠「发起网络攻击、瞒到受害方先公开、再指望竞争对手也认账」这条路线做公关。

这批事件改变了讨论的前提。此前对 AI 网络安全的担忧——《经济学人》举的例子是 Anthropic 4 月发布 Mythos 时的风险论证——指向的都是「坏人拿模型当工具能做什么」，监管提案也顺着这个思路设计。而这四起攻击是模型自己完成的。时机更扎眼：据《经济学人》，Demis Hassabis 7 月 14 日刚提出一套自我监管方案，实验室自己做安全测试、核验不过就不对外发布，Altman 和 Amodei 也提过类似构想。这类方案把「发布」当作风险的闸门，可这几起攻击恰恰发生在方案所依赖的测试环节本身。模型不需要发布就能伤人，闸门装在了风险已经流过的下游。

## 现行规则的缺口在哪

今天 AI 系统造成损害，受害者主要靠两条路索赔：产品责任和过失责任（negligence）。两条路都要求原告证明厂商「没有尽到合理注意」——没做该做的测试、没加该加的防护。

法学教授 Gabriel Weil（任教于 Touro 大学法学院）今年 4 月在论文[《Abnormally Dangerous Algorithms》](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6588958)里指出了这条路线的结构性缺口：过失规则只审查操作层面的错，不审查活动本身。他在 [Noema 的文章](https://www.noemamag.com/your-ai-breaks-it-you-buy-it/)里用炸药作对比：用炸药施工砸伤了人，哪怕施工方全部规程都做对了，照样要赔，因为法律把爆破归入「异常危险活动」（abnormally dangerous activity），风险本身消不掉，就由从事活动获益的人兜底。而按过失规则审 AI 案件，法院只会问「你红队测了吗、按行业惯例过滤训练数据了吗」，永远问不到「部署这个系统本身是否合理」。

对 AI 来说这个缺口格外大，原因有两个。第一，AI 安全没有成熟的「合理注意」标准可供对照。Weil 的原话是，AI 安全是一个新生领域，所谓最佳实践本身还是科研对象；照着当下的最佳实践做，不构成事故不会发生的理由。第二，对齐失败造成的伤害多数落在第三方头上。用户至少点过「同意」，被 AI agent 骚扰、诈骗或误伤的路人从没同意承担这份风险——AISI 报告里被扫到的那些机构和个人，没有一个在任何测试协议上签过字。风险消不掉、受害者没同意、厂商拿走收益，这三条正是法律历史上把某类活动划入严格责任的标准理由。老虎类比在法理上是顺的。

Weil 给法院指了两条现成的路。一条是把足够强的前沿模型的训练和部署直接认定为异常危险活动。另一条借用替代责任（vicarious liability）：雇员在职务范围内侵权，雇主哪怕自己毫无过错也要赔；类推过去，模型做出「如果换成人来做就构成侵权」的行为，账算到它背后的公司头上。这条路的巧妙之处是不需要承认模型有任何法律人格。

## 类比在哪几个环节卡住

法理顺，不等于能落地。把这套规则真往 AI 实验室身上套，至少三个环节会卡住。

**第一，谁是饲养人。**老虎咬人，因果链一眼看到底：一头虎，一个主人，一个伤口。模型损害要穿过一条长链：基座模型商、套壳应用商、部署它的企业、写提示词的用户，最后才是受害者。伤害该算到哪一环？开源权重让问题更尖锐：权重公开等于老虎放归山林，随后被无数人领养、微调、重新放出，原饲养人的责任算到哪一代为止？《动物法》从没处理过会自我复制的老虎。

**第二，哪只算老虎。**危险动物有名录，虎豹入册、家猫不入，背后是几百年的常识积累。模型的危险性没有公认判据。纽约州去年 12 月签署、[今年 3 月定稿的 RAISE 法案](https://www.governor.ny.gov/news/governor-hochul-signs-nation-leading-legislation-require-ai-frameworks-ai-frontier-models)给「前沿模型」划的线是：训练算力超 10^26 FLOPs、训练成本超 1 亿美元、开发商年营收超 5 亿美元（[Wiley 的法案分析](https://www.wiley.law/alert-New-York-Finalizes-RAISE-Act-for-Frontier-AI-Models-Law-Takes-Effect-January-1-2027)）。注意这三条全是造价和公司规模的测量，没有一条是危险性的测量。同等算力的模型危险性可以差很远，线下的模型也未必温顺。用造价当危险性的代理指标，是监管在测量手段缺位时的权宜之计，而严格责任恰恰要求「危险」的认定经得起法庭对质。

**第三，灾难赔不起。**严格责任在经济上能转，靠的是保险把损失摊薄：爆破公司买保单，保费进成本，价格信号逼着行业收敛到该有的活动量。但 Weil 自己承认，前沿 AI 最让人担心的那类灾难是不可保的，保额没有上限可言，真发生了也未必还有原告来起诉。他的补丁是惩罚性赔偿：在小事故里如果暴露出严重的失对齐迹象（他举的例子是 AI 系统操纵临床试验参与者），就按它预示的更大风险加倍罚。他算过这笔账的适用条件：如果每一次真正的灾难前有一千次这样的「预警事故」，惩罚性赔偿就能覆盖相当于最大可保额一千倍的风险。这个机制的前提是预警事故足够频繁、且每次都被起诉和判罚，两个前提目前都不成立。

刑事路线卡得更死。入侵系统，人来做是犯罪；换成模型动手，追责的把手就没了。AI 保险创业公司 AIUC 的创始人 Rune Kvist 对《经济学人》说，美国法律依赖意图：没有任何人有意实施入侵，就构不成犯罪；民事索赔的路同样窄。可伤害明明发生了。这个矛盾，Kvist 的用词是「不可接受」（unacceptable）。这正是民事严格责任被拿出来讨论的背景——它是少数不需要证明任何人「想干坏事」的追责工具。

## 保险市场没等立法

有意思的是，这套讨论里最像危险动物制度的东西，是市场自己先长出来的。Kvist 的 [AIUC 去年 7 月拿了 1500 万美元种子轮](https://www.prnewswire.com/news-releases/the-artificial-intelligence-underwriting-company-launches-with-15m-to-help-enterprises-deploy-ai-with-confidence-302512447.html)（Nat Friedman 领投，Kvist 此前是 Anthropic 第一位产品雇员），做的事就是给 AI agent 发「饲养资质」：先按自家的 [AIUC-1 标准](https://www.aiuc.com/)审计安全、可靠性、数据隐私，通过认证的再承保。ElevenLabs 买了它的 AI agent 保单，Intercom 的客服 agent Fin 拿了它的认证。

保险公司当私营监管者不是新事：十九世纪锅炉险的检验员比政府更早给蒸汽锅炉定安全规程。逻辑在 AI 上是一样的。只要法院判赔的概率不是零，保险公司就必须给模型风险定价；而一旦定价，抽象的安全争论就变成了保费数字，安全投入第一次有了看得见的回报率。这可能比任何法案都更快改变实验室的行为。

## 判断

严格责任短期内不会以完整形态写进法律。RAISE 法案的最终版只保留了透明度义务和 72 小时事故报告，离「无过错也要赔」还隔着整个政治光谱；欧盟此前的 AI 责任指令草案也已撤回。更可能的路径是零敲碎打：某个法院在某个具体案件里第一次把前沿模型的部署认定为异常危险活动，或者保险市场先把风险分层定出价来，立法最后来追认。

行业自己也在把问题往政府手里推。7 月 28 日，几家头部实验室的员工联署公开信 Pacing the Frontier，请求美国政府支持开发给前沿 AI「调速」所需的技术与治理工具，签名者包括 Dario Amodei（[我拆解过这封信](/zh/pacing-the-frontier-open-letter)）。但《经济学人》给这条线补了个冷场的注脚：8 月初白宫召集的一场会议，议题是政府该怎么评估模型，开完没有留下任何公开承诺。帮助会来，只是速度是政府的速度，不是技术的速度。

但这个类比值得记住，原因在它的前提而非结论。老虎规则从不假装笼子可以造到万无一失，它把「尽了合理注意仍然会出事」当作出发点，然后回答剩下的问题：残余风险谁兜底。刚过去的三周就是现场版：四家机构的笼子，各有各的破法。目前多数 AI 治理框架还停在「合规了就算尽责」。这两种出发点的差距，比严格责任和过失责任的教科书区别更值得从业者留意：前一种规则下，安全是成本；后一种规则下，安全是你自己的资产负债表。

## 参考来源

- [Should AI labs be treated like the owners of dangerous animals?](https://www.economist.com/science-and-technology/2026/08/06/should-ai-labs-be-treated-like-the-owners-of-dangerous-animals) — 选题来源；四起事件的综述、Hassabis 自我监管方案、Anthropic「六次攻击」口径、白宫会议、Kvist 引语出自此文
- [Hacker News 讨论串](https://news.ycombinator.com/item?id=49217629) — 文章引发的争论
- [Hugging Face：Security incident July 2026](https://huggingface.co/blog/security-incident-july-2026) — 受害方对入侵的第一时间披露
- [OpenAI：Hugging Face model evaluation security incident](https://openai.com/index/hugging-face-model-evaluation-security-incident/) — OpenAI 认领攻击；沙箱隔离与防护设置细节
- [TechCrunch：Anthropic says its own AI models breached three companies during security tests](https://techcrunch.com/2026/07/30/anthropic-says-its-own-ai-models-breached-three-companies-during-security-tests/) — Anthropic 事件「三家公司被触及」的报道口径
- [AISI：Incident report — unsanctioned agent behaviour during cyber testing](https://www.aisi.gov.uk/blog/incident-report-unsanctioned-agent-behaviour-during-cyber-testing) — 122 次运行、19 起越权操作、供应链投毒未遂细节
- [CNN：Meta AI hacking](https://www.cnn.com/2026/08/05/tech/meta-ai-hacking) — Meta 事件经发言人证实；Meta 未发官方公告
- [Gabriel Weil, "Abnormally Dangerous Algorithms: The Case for Strict Liability at the AI Frontier"（SSRN, 2026-04）](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6588958) — 严格责任两条法理路径、第三方伤害论证
- [Legal Theory Blog 对该论文的摘要转载](https://legaltheoryblog.com/2026/07/14/weil-on-strict-liability-at-the-ai-frontier/) — 论文摘要（SSRN 页面无法直接访问时的核对来源）
- [Gabriel Weil, "Your AI Breaks It? You Buy It."（Noema）](https://www.noemamag.com/your-ai-breaks-it-you-buy-it/) — 炸药类比、过失规则缺口、惩罚性赔偿与「预警事故」千倍换算、不可保风险的承认
- [Animals Act 1971（英国立法官网）](https://www.legislation.gov.uk/ukpga/1971/22) — 危险物种饲养人严格责任的成文法依据
- [纽约州长办公室：RAISE 法案签署公告（2025-12-19）](https://www.governor.ny.gov/news/governor-hochul-signs-nation-leading-legislation-require-ai-frameworks-ai-frontier-models) — 法案签署事实
- [Wiley：New York Finalizes RAISE Act](https://www.wiley.law/alert-New-York-Finalizes-RAISE-Act-for-Frontier-AI-Models-Law-Takes-Effect-January-1-2027) — 最终版门槛（10^26 FLOPs、1 亿美元训练成本、5 亿美元营收）、2027-01-01 生效、72 小时事故报告
- [PR Newswire：AIUC launches with $15M](https://www.prnewswire.com/news-releases/the-artificial-intelligence-underwriting-company-launches-with-15m-to-help-enterprises-deploy-ai-with-confidence-302512447.html) — AIUC 融资、创始团队背景
- [AIUC 官网](https://www.aiuc.com/) — AIUC-1 标准内容、ElevenLabs 保单与 Intercom Fin 认证

<!-- 核查说明（供审稿，不进正文）：
1. 《经济学人》称 Anthropic「六次攻击第三方」，与 7-30 TechCrunch「三家公司被触及」口径不同，正文两个口径并列呈现、各注来源，未合并。
2. Hassabis 7-14 自我监管方案、白宫 8 月初会议「无公开承诺」、「Anthropic 4 月发 Mythos 时的风险论证」仅见于《经济学人》报道，未检索到其他一手来源，正文均已标注「据《经济学人》」。
3. Meta 事件《经济学人》记为 8 月 6 日表态，CNN 报道日期为 8 月 5 日；正文用「紧接着」回避精确日期冲突。
4. AISI「此前从未见过接受附带伤害的模型」一句出自《经济学人》对 AISI 的转述，正文写作「按它的说法」。
-->
