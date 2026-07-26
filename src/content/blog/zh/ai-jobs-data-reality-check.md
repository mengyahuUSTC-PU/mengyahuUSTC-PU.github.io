---
title: "裁员公告里的 AI，和失业数据里的 AI，不是同一个 AI"
description: "斯坦福 SIEPR 用五套数据核查『AI 失业潮』：总量上几乎看不到，真正的信号窄而具体——集中在高暴露职业的入口岗位。"
pubDate: 2026-07-25
tags: [ai-economy, labor-market]
lang: zh
slug: ai-jobs-data-reality-check
translationOf: ai-jobs-data-reality-check
---

2025 年 10 月 28 日，亚马逊宣布裁减约 1.4 万个办公室岗位。媒体标题几乎众口一词：[「亚马逊裁员 1.4 万，拥抱 AI」](https://www.cbsnews.com/news/amazon-layoffs-14000-job-cuts-ai/)。但去读[官方备忘录原文](https://www.aboutamazon.com/news/company-news/amazon-workforce-reduction)，措辞比标题谨慎：备忘录把这轮裁员本身归因于组织结构——层级太多、要更精简；AI 是精简的理由，不是裁员的直接归因：「这一代 AI 是自互联网以来最具变革性的技术」，组织必须更精简才能跟上它的节奏。至于「未来几年 AI 带来的效率提升会缩减办公室岗位总量」这句预告，出自 CEO Andy Jassy [2025 年 6 月的另一份备忘录](https://www.aboutamazon.com/news/company-news/amazon-ceo-andy-jassy-on-generative-ai)，并不在这份裁员公告里。

裁员是现在时，归因是组织结构；「AI 缩减岗位」是将来时，还写在另一份备忘录里。大多数标题把它们合并成了一句。

而且裁员还在继续：就在本文发稿这一周（2026 年 7 月 22 日），[据 CNBC 报道](https://www.cnbc.com/2026/07/22/amazon-lays-off-some-employees-in-its-agi-unit.html)，亚马逊又在其 AGI（通用人工智能）部门——负责研发亚马逊自家大模型的团队——裁掉一批员工，这次被裁的恰恰是做 AI 的人。这类新闻这两年接连不断，很自然让人想问：这么多被裁的人，都找到下一份工作了吗？为什么就业数据里看不出裁员潮？这个问题下文会专门拆。

这种「现在裁员、将来归因」的错位，正是斯坦福经济政策研究所（SIEPR）2026 年 7 月一份政策简报（[原文](https://siepr.stanford.edu/publications/policy-brief/what-really-happening-jobs-separating-ai-hype-reality)）要拆解的问题。作者阵容值得注意：SIEPR 主任 Neale Mahoney、前美国劳工统计局局长 Erika McEntarfer、研究员 Karsen Wahal——其中 McEntarfer 直到 2025 年 8 月还在主管美国官方就业数据的编制。

## 总量数据里没有失业潮

简报的核心方法是「按暴露度分组对比」：给每个职业打一个 AI 暴露度分数，衡量该职业的任务与现有 AI 能力的重合程度。分数不是简报作者自己打的，用的是经济学家 Felten、Raj 和 Seamans 2021 年发表的 [AI 职业暴露指数（AIOE）](https://sms.onlinelibrary.wiley.com/doi/full/10.1002/smj.3286)——该指数把 O*NET 职业数据库里各职业依赖的能力，与各类 AI 应用的进展逐项对应起来算分。把所有职业按分数分成五档，再用 IPUMS-CPS 微观数据（2015–2026 年，按季度）比较各档的失业率走势。两头的职业大致长这样：暴露度最高一档是遗传咨询师、金融审查员这类核心工作是标准化处理文本信息的岗位，最低一档是舞蹈演员、建筑辅助工这类依赖现场肢体劳动的岗位。

结果是全文最硬的一组数字：2022 年以来，暴露度最高一档的失业率上升了 0.77 个百分点，暴露度最低一档上升了 0.85 个百分点。最该被 AI 冲击的人群，失业率涨得反而比最不该被冲击的人群略慢。作者的结论是：这是一个整体走软的劳动力市场，而不是一个被 AI 驱动失业的劳动力市场——真正拖慢招聘的，更像是[美联储 2022 年 3 月开始的加息](https://www.federalreserve.gov/newsevents/pressreleases/monetary20220316a.htm)和疫情期间超额招聘的回调这类作用于整个市场、而不只是高暴露职业的宏观因素。

企业侧数据同样平淡。人口普查局的企业调查里，已采用 AI 的企业中只有 5% 报告 AI 影响了用工人数——而且这 5% 里增员和减员各占一半。亚特兰大联储的高管调查里，约 80% 的高管承认 AI 投资尚未改变公司的人员规模或生产率。

回到开头那个问题：这两年裁员新闻此起彼伏，为什么总量数据里看不到？答案主要在规模和流量上。失业率是一个净值：美国[就业人口约 1.6 亿](https://www.bls.gov/news.release/empsit.nr0.htm)，按[劳工统计局的 JOLTS 数据](https://www.bls.gov/news.release/jolts.nr0.htm)（最新一期为 2026 年 5 月数据），即便在当下，每月被裁员和解雇的也有约 170 万人（月度裁员率约 1.1%，处于历史低位），同时每月新招聘约 520 万人。单个公司裁掉一两万人，放进这个流量里连零头都算不上——裁员新闻上头条，靠的是公司名字，不是人数。同时要看到，眼下是一个「低招聘、低裁员」的市场：公司不太裁人，也不太招人。这与失业率在各个暴露度分组都缓慢上行的图景相吻合，也是简报所说「整体走软」的具体含义。还要说明简报的时间边界：它的数据止于 2026 年中，7 月下旬这轮 AGI 部门裁员发生在简报发布之后，不在其覆盖范围内。

那为什么裁员公告言必称 AI？简报作者对企业自报的归因明确持保留态度，并提出两种可能：企业在用 AI 叙事解释疫情期招聘过度后的收缩，或是借裁员腾出现金投入 AI 资本开支。在我看来，激励也确实不对称：把裁员说成「为 AI 转型」，比承认「疫情期间招多了」体面得多，也更符合投资者想听的故事。裁员公告首先是写给资本市场的文本，其次才是对劳动力市场的描述。

## 真正的信号：窄，但真实

简报没有停在「虚惊一场」。它承认有一个信号是真的：入口岗位。

2026 年一季度，美国新毕业生失业率达到 5.6%，比三年前高 1.6 个百分点。更细的证据来自 Brynjolfsson 团队的「煤矿里的金丝雀」研究（[Stanford Digital Economy Lab](https://digitaleconomy.stanford.edu/publication/canaries-in-the-coal-mine-six-facts-about-the-recent-employment-effects-of-artificial-intelligence/)，用 ADP 工资单数据）：在 AI 暴露度最高的职业里，22–25 岁年轻人的就业相对下滑了约 16%，而同职业的资深员工基本稳定——最典型的是软件开发：22–25 岁开发者的就业从 2022 年底的峰值到 2025 年 7 月下滑近 20%。而且下滑集中在 AI 更可能「替代」人类任务（直接接手活儿）而非「辅助」人类（帮人把活干得更快）的职业里。同一职业、只有新人受冲击、且冲击集中在替代型职业——这个模式看起来确实像 AI 的指纹。

但简报提醒：先别急着把账全记在 AI 头上，因为时间线有个疑点。年轻人就业的下滑从 2022 年底就开始了，而 [ChatGPT 也是 2022 年 11 月底才发布](https://openai.com/index/chatgpt/)——很难想象企业在它刚发布时就已经用它替代掉了员工。那段时间真正在发生的是另外两件事：美联储 2022 年 3 月开始加息，科技行业招聘应声收缩；疫情后的远程办公让新人失去了在办公室里边干边学的机会，企业招新人的意愿本来就在下降。针对这类质疑，Brynjolfsson 团队后来做了修订分析，把这些混杂因素当作控制变量剔除，结果是：剔除之后，入门岗位的明显下滑要到 2024 年才出现。换句话说，2022–2023 年那段下滑，加息、远程办公这类 AI 之外的解释看起来更说得通；AI 如果真的在压缩入门岗位，可辨认的影响要到 2024 年才开始显现。

所以准确的读法是：入口岗位的困境是真的，AI 是嫌疑人之一，但目前的证据不足以让它单独定罪。

## 量尺问题：同一个问题，四个答案

简报最有方法论价值的部分，是把「AI 采用率」的各种口径摆在一起：问企业（人口普查局调查），约两成在用；问员工（家庭调查），超四成说工作中用 AI；问高管，声称超八成员工在用；看企业实际付费（Ramp 平台数据，样本不具代表性），超半数客户在为 AI 工具花钱。同一个问题，答案从 20% 到 80%,取决于问谁、怎么问。任何一篇拿单一口径下结论的报道，都值得先打个问号。

生产率证据同样撕裂。实验室一侧：呼叫中心研究测得整体生产率提升 15%、新手提升约 30%（[Brynjolfsson、Li 和 Raymond 的原始研究，QJE 2025](https://academic.oup.com/qje/article/140/2/889/7990658)）；[GitHub Copilot 实验](https://arxiv.org/abs/2302.06590)中开发者完成任务快约 56%——增益集中在经验较浅的人身上。但 [METR 的随机对照实验](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/)给了反例。这个实验的设计值得细说：16 名资深开源开发者，在自己维护多年的大型代码库（平均超 2.2 万 star、上百万行代码）上，拿出 246 个真实任务——修 bug、加功能、重构，都是他们本来就要干的活，平均每个约两小时。每个任务被随机分到「可用 AI」或「禁用 AI」两组之一，每个任务只做一遍——不是同一个任务做两遍再比时间，所以不存在「第二遍已经熟悉了所以更快」的学习效应；对比发生在两组任务之间，随机分配让两组任务的难度分布大体可比。结果：允许用 AI 的那组任务，平均完成时间反而长了 19%——而开发者自己事后仍感觉 AI 让他们快了 20%。感知与实测的落差高达约 40 个百分点，这也为高管调查和实测数据为什么经常对不上提供了一条线索：所有人都「感觉」AI 提效了。

这不是新故事。1987 年，经济学家 Robert Solow [说过一句著名的话](https://standupeconomist.com/solows-computer-age-quote-a-definitive-citation/)：「计算机时代处处可见，唯独在生产率统计里看不见」——当时美国企业已经大量购入电脑，但宏观生产率增速多年毫无起色，直到 1990 年代中后期才明显加速。原因不是电脑没用，而是企业要把新技术真正转化为产出，得先重组工作流程、重新培训员工、配齐周边投资，这些动辄以年、甚至十年计。简报用这段历史类比 AI：模型能力的突破可以一年一个台阶，但它渗透进企业日常运营、进而在经济数据里留下痕迹的速度要慢得多。换句话说，不是 AI 对经济没有影响，而是影响的显形可能有很长的时滞。

## 给行业观测者的三个判断

**一、读任何「AI 导致 X」的就业论断，先查三个口径。** 数据来自谁（企业自报、工资单、还是家庭调查）、时间窗多长（是否覆盖了加息和疫情回调这两个混杂因素）、暴露度怎么定义。口径不亮出来的结论，一律当观点而非事实。

**二、把裁员归因当叙事读，不当证据读。** 亚马逊的例子是标准样本：裁员备忘录把裁员归因于组织结构，「AI 缩减岗位」的预告写在另一份备忘录里、用的是将来时，标题把两者合并成了现在时。企业有充分动机把结构调整包装成技术转型，数据（5% 报告影响、增减各半）目前不支持这些公告的字面含义。

**三、盯窄信号，别盯宽叙事。** 总量失业率短期内不会给出 AI 信号；值得持续跟踪的是高暴露职业里的入口岗位——年轻软件开发者、客服、初级文书分析岗的招聘量和失业率（Stanford Digital Economy Lab 有[持续更新的仪表盘](https://digitaleconomy.stanford.edu/project/indicators/canaries-dashboard/)）。同时记住这份简报的边界：它的核心就业数据只覆盖美国、止于 2026 年中，而 agent 类工具进入企业日常工作流的时间还很短——按「扩散慢于突破」的逻辑，现在的数据本来就照不到它们。这不是简报的漏洞，而是它自己反复强调的不确定性。

我的综合判断：AI 对就业的影响目前「真实但窄」——总量数据里几乎看不出影响；高暴露职业入口岗位的压力是真实存在的，AI 很可能是推手之一。舆论场上两种声音都在失真：失业潮叙事把窄信号放大成了海啸，企业公告把宏观回调包装成了技术必然。技术跑得快、扩散走得慢，这个时间差恰恰是留给政策和个人调整的窗口——前提是我们盯着数据本身，而不是盯着标题。

## 参考来源

- [What is really happening to jobs? Separating AI hype from reality（SIEPR 政策简报）](https://siepr.stanford.edu/publications/policy-brief/what-really-happening-jobs-separating-ai-hype-reality) — 核心数据与结论：0.77/0.85 个百分点、新毕业生 5.6%、采用率各口径、5% 企业报告用工影响、80% 高管称未改变人员规模、呼叫中心与 Copilot 生产率研究转引
- [Occupational, industry, and geographic exposure to artificial intelligence（Felten, Raj & Seamans, 2021）](https://sms.onlinelibrary.wiley.com/doi/full/10.1002/smj.3286) — 简报所用 AI 职业暴露指数（AIOE）的原始论文；最高/最低暴露职业例子（遗传咨询师、金融审查员 vs 舞蹈演员、建筑辅助工）出自该指数
- [An update from SVP Beth Galetti on Amazon workforce reduction（亚马逊官方备忘录，2025-10-28）](https://www.aboutamazon.com/news/company-news/amazon-workforce-reduction) — 开篇案例：1.4 万岗位裁减的官方归因原文（归因于组织结构调整）
- [Amazon CEO Andy Jassy on Generative AI（亚马逊官方备忘录，2025 年 6 月）](https://www.aboutamazon.com/news/company-news/amazon-ceo-andy-jassy-on-generative-ai) — 「未来几年 AI 效率提升将缩减办公室岗位总量」预告的实际出处
- [Amazon lays off some employees in its AGI unit（CNBC，2026-07-22）](https://www.cnbc.com/2026/07/22/amazon-lays-off-some-employees-in-its-agi-unit.html) — 开篇补充案例：亚马逊 AGI 部门新一轮裁员（亚马逊未发官方公告，此为原始报道）
- [Job Openings and Labor Turnover Summary（美国劳工统计局 JOLTS，2026 年 5 月数据）](https://www.bls.gov/news.release/jolts.nr0.htm) — 月度裁员和解雇约 170 万人、裁员率约 1.1%（历史低位）、每月新招聘约 520 万人；「低招聘、低裁员」市场的判断依据
- [Canaries in the Coal Mine?（Stanford Digital Economy Lab）](https://digitaleconomy.stanford.edu/publication/canaries-in-the-coal-mine-six-facts-about-the-recent-employment-effects-of-artificial-intelligence/) — 22–25 岁高暴露职业就业相对下滑约 16%（修订后数字）、年轻软件开发者下滑近 20%、替代型与辅助型职业的区分、修订分析中下滑推迟到 2024 年才显现
- [Generative AI at Work（Brynjolfsson, Li & Raymond，QJE 2025）](https://academic.oup.com/qje/article/140/2/889/7990658) — 呼叫中心整体生产率 +15%、新手约 +30% 的原始研究
- [The Impact of AI on Developer Productivity: Evidence from GitHub Copilot（Peng et al., 2023）](https://arxiv.org/abs/2302.06590) — 开发者完成任务快 55.8% 的原始实验
- [Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity（METR）](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/) — 16 名资深开发者、246 个真实任务随机分组的实验设计；实测慢 19%、自感快 20% 的感知落差
