---
title: "AI 理财建议赢了谁?对照组里没有人类顾问"
description: "MIT Sloan 让 1000 个成年人自己写 prompt 向 LLM 要理财建议,再模拟照做一生的结果。结论确实亮眼,但要先看清对照组是谁、哪些场景会失效。"
pubDate: 2026-08-01
tags: [personal-finance, llm-evaluation, ai-fairness]
lang: zh
slug: ai-financial-advice-right-questions
translationOf: ai-financial-advice-right-questions
---

七月底,MIT Sloan 一篇研究的报道在 [Hacker News 上传开](https://news.ycombinator.com/item?id=49139102)(200 多条评论),标题自带结论:[AI 理财建议出人意料地好,尤其当你问对问题时](https://mitsloan.mit.edu/ideas-made-to-matter/ai-financial-advice-surprisingly-good-especially-if-you-ask-right-questions)。

我读完的第一个问题是:和谁比?标题用的是 good,不是 better,没有点出比较对象,可评价一份建议好不好,总得有个参照。

答案藏在研究设计里,比标题有意思得多。

## 这项研究到底测了什么

论文题为[《AI Financial Advice: Supply, Demand, and Life Cycle Implications》](https://tahachoukhmane.com/wp-content/uploads/2026/03/CdSLA-2026-AI-Financial-Advice.pdf),作者是 MIT Sloan 的 Taha Choukhmane、Weidong Lin、Matthew Akuzawa 和斯坦福商学院的 Tim de Silva,拿了 2026 年瑞士金融研究所杰出论文奖([MIT Sloan 工作论文 7377-26](https://mitsloan.mit.edu/centers-initiatives/cfi/ai-financial-advice-supply-demand-and-life-cycle-implications))。

设计分三步。第一步,找 1000 名有代表性的美国成年人,让他们自己写 prompt,向 GPT-5.2 和 Gemini 3 Flash 要消费和投资建议。注意是自己写:研究者不代笔,就是要看真实用户会怎么问。

第二步,把模型的建议解析成可执行的规则:存多少、股票配多少。

这一步顺带框定了研究范围。「理财建议」这个词能装下很多东西,但这项研究只测了其中一条线:长期的消费储蓄和投资配置。论文摘要写得明白,受访者被要求写的就是 spending 和 investing 的提问,模拟器跑的也只有这两个变量的长期轨迹。买房、房贷、信贷、保险、税务筹划这些同样日常的理财决策,都不在测试范围内。后文所有「好」与「不好」的结论,都只覆盖这条线。

第三步,把这些规则放进一个生命周期模拟器,让「虚拟的你」带着这套建议过完一生。收入按真实劳动力市场数据涨跌,会失业,会遇到熊市,要交税。模拟从成年工作期一直跑到退休之后;报告结果时,财富比较取的是 60 岁这个时点的切片,消费看的是一生的水平。

评判标准是生命周期理论。这是家庭金融的规范框架,核心处方大致是:年轻时投资期限长、未来工资收入多,该多配股票;随年龄增长逐步降低股票比例;留出应急储蓄;让消费在好坏年景之间尽量平滑,别大起大落。

看清这个设计,「出人意料地好」的意思就落定了。这话是 MIT Sloan 报道标题的原话,夸的对象是模型给出的建议;作者之一 Choukhmane 也说,看到人们实际提的那些糙问题,再看建议的质量,他们「有点意外」。

那和什么比?照 AI 建议这一边,是模拟出来的一生:把建议解析成规则,放进模拟器跑到老。对照的另一边不是又一条模拟轨迹,而是受访者在问卷里报告的当前实际做法——现在存多少、股票配多少。两边性质不同,一边是长期轨迹,一边是当下的切面;论文的比法是各自对照生命周期理论的处方。结果是:对大多数受访者,照 AI 建议走出的轨迹,比维持当前做法更接近理论。

不管怎么比,对照组里都没有人类理财顾问——论文自己也把「与其他形式的理财建议怎么比」列为留待研究的问题。

这个基线有多低?据 [phys.org 转述](https://phys.org/news/2026-07-llms-nudge-users-smart-investing.html),写 prompt 的受访者里约四成存款不到一万美元。作者之一 de Silva 的原话也很诚实:「它不完美,但比很多人现在做决定的方式强,比如问亲友,或者随手上网搜。」

但「比问亲友强」这话得多想一层:强在哪?存款少不等于意识不到该存钱。「多存点」这条建议问谁都能拿到,亲友会说,上网搜也会说;很多人存不下钱,未必是不知道,更可能是坚持不住。如果 AI 的增量只是把「存更多」再说一遍,这个「比现状强」就没多大分量。

模拟里打分的规则其实有两部分:存多少,以及存下来的钱怎么配置——股票占多少、随年龄怎么降、留多少应急现金、坏年景怎么平滑消费。后一半才是亲友和随手搜索给不出的个性化数字。下一节还有个直观例子:流动性这个维度,绝大多数用户压根没想到要问,模型主动补上了。至于这份改善里多少来自「多存」、多少来自「配好」,公开材料没拆开讲,这点我没核实到。

而「知道该存却坚持不住」的问题,这项研究测不了。模拟里的虚拟人严格照做几十年,不会半途而废;所以「比现状强」说的是建议本身的质量,前提是照做。AI 能不能让真人把钱真的存下来,是另一个问题。

## 三个发现,分开看

第一,方向大体正确。模型的建议整体把人往教科书方向推:更多人参与分散化的股票基金,股票比例随年龄下降,存出可观的储蓄缓冲。模型还会主动补课:据 phys.org 转述,83% 的回复提到了流动性,也就是手头留多少随时能动用的现金,而只有 6% 的用户主动问到这一点。

第二,「问对问题」的门槛比听上去高。研究者做了替换实验:把用户自己写的 prompt 换成「学术 prompt」,建议质量进一步向理论靠拢,消费平滑做得更好,更少依赖粗糙的经验法则。所谓学术 prompt,是把生命周期框架、完整的财务信息(收入、资产、负债、投资期限)和明确的经济假设都写进提问里。

也就是说,「问对问题」并非提示词话术,它约等于「你本来就得懂点理财,还得把自己的家底说全」。de Silva 给个人用户的建议也是先补金融常识,他说提问的写法「影响极大」,有了基础知识才能把这个工具用出威力(据 phys.org 转述)。

第三,建议质量因人而异,吃亏的正是本来就弱势的群体。先说清「因人而异」指什么:不是说各人起点不同所以终点不同。模拟器对每个人跑的是同一套流程,差距出在模型给出的建议本身:照各自拿到的建议模拟到 60 岁,女性和金融素养较低的用户,财富比男性和高素养用户少约 4% 到 5%。按 [MIT Sloan 报道](https://mitsloan.mit.edu/ideas-made-to-matter/ai-financial-advice-surprisingly-good-especially-if-you-ask-right-questions)给的绝对数:少约 5 万美元;没用过 AI 的用户比用过的少近 10 万美元(6%)。

那差距从哪来?拿性别差距来说,论文拆出了两个来源,大小还不一样。

约三分之二来自需求端:男女写的 prompt 本来就不一样。据 phys.org 转述的词频统计,女性更常用「family」「grocery」「credit」「loan」这类词,模型顺着话头,给的建议偏保守,多留现金、建应急缓冲;男性更常用「portfolio」「equity」「strategy」「crypto」,拿到的投资建议就更激进。金融素养低的用户同理,prompt 里交代的自身财务信息少,拿到的建议就糙。这一半不是模型在歧视谁,是输入不同、输出跟着不同。

剩下约三分之一来自供给端,这才是模型自身的偏差([MIT Sloan 报道](https://mitsloan.mit.edu/ideas-made-to-matter/ai-financial-advice-surprisingly-good-especially-if-you-ask-right-questions)给出这个分解)。研究者做了对照实验:同一条 prompt,内容一字不改,只把它标注成来自女性而非男性,模型建议的股票配置就变保守了——标注为女性的提问,拿到的股票敞口建议更低([phys.org](https://phys.org/news/2026-07-llms-nudge-users-smart-investing.html)、[斯坦福商学院报道](https://www.gsb.stanford.edu/insights/what-ai-tells-people-seeking-low-cost-financial-advice))。至于日常使用中模型怎么知道用户性别:通常不知道,据 phys.org 转述,受访者自然写 prompt 时模型一般拿不到这个信息;对照实验里的性别标签是研究者主动写进提问的。但实验说明,一旦提问透露了性别,建议就会被它带偏。

两个来源方向一致,都对弱势群体不利。需求端构成一个循环:最需要建议的人,恰恰最问不出好问题;供给端则意味着,就算问出了同样的问题,模型还会再偏一点。

## 为什么好处偏向会提问的人

LLM 按输入定输出。你给的信息越完整、框架越对,它的建议越接近最优;你只说「我 30 岁,该怎么投资」,它只能给通用模板。真人顾问的服务通常从问询开始,先把收入、家底、目标问清楚再开方——这是行业常规,不是这项研究测出来的,论文没有比较两边的问诊流程。研究里的模型是单轮问答,不会追问,你给什么信息,它就只用这些信息作答。这不是缺陷,是这种用法下系统的工作方式。

后果是:传统理财顾问的门槛在价格,请得起的人才有;LLM 把这道价格门槛压到几乎可以忽略,却立起另一道门槛,会提问的人才能问出好建议。模拟里,下限确实抬高了:大多数受访者若严格照做,会比维持现状更接近理论处方。但好处的大头流向金融素养高、会用 AI 的人。工具人人可用,好处并不均摊。

## 静态原则会背,动态调整不会做

模拟里暴露的三个坑,比总体结论更有参考价值。这三个坑指的是模型给不同受访者的建议里反复出现的同类错误,并非哪位用户碰巧抽到的一次坏回答:

- 失业后,模型建议砍支出砍得过狠。生命周期理论的处方恰恰相反:动用储蓄缓冲、平滑消费,别让一次收入冲击把生活水平打穿。
- 组合放着漂移,不主动再平衡。股票涨了之后在组合里的占比会被动升高,风险敞口越拉越大,模型不太会提醒你卖掉一部分、回到目标比例。
- 退休后花钱过于保守,基本照搬「每年提取储蓄的 3%-4%」这条安全提取率经验法则,该花的钱不花,消费平滑又输一次。

三个坑一个共性:通用原则背得很好,遇到状态变化时的动态调整做不好。而这类动态调整,我认为正是人们付费请人类顾问想买的东西——研究没有测人类顾问,这是我的判断。

## 还有一个没人管的问题:推荐位

Vanguard(先锋领航,低费率指数基金巨头)的产品出现在 6% 的回复里,iShares(贝莱德旗下的 ETF 品牌)出现在约 3%(MIT Sloan 报道称 3.4%,论文当前版本的图表为 2.9%,两处口径略有出入),而提到这两家的 prompt 不到 0.4%([MIT Sloan 报道](https://mitsloan.mit.edu/ideas-made-to-matter/ai-financial-advice-surprisingly-good-especially-if-you-ask-right-questions))。

今天这不算坑人:两家都以低成本指数产品著称([Vanguard 官方数据](https://investor.vanguard.com/investment-products/mutual-funds/low-cost)称其平均费率比行业平均低 84%),推荐它们和教科书方向一致。至于推荐从何而来,论文没有分析;我猜是训练数据的自然分布,但这只是猜测。de Silva 点出的隐忧是结构性的:模型厂商清楚大量用户在拿它做理财决策,就存在引导用户买特定产品的激励(据 [phys.org 转述](https://phys.org/news/2026-07-llms-nudge-users-smart-investing.html))。模型回答里的「推荐位」值多少钱,目前没有针对 LLM 的披露规则。类似问题监管碰到过:2013 年美国 FTC 就[要求搜索引擎](https://www.ftc.gov/news-events/news/press-releases/2013/06/ftc-consumer-protection-staff-updates-agencys-guidance-search-engine-industry-need-distinguish)把广告和自然搜索结果区分清楚,不区分可能构成欺骗性行为;但这套规则怎么落到聊天机器人的回答上,还没有先例。搜索引擎从自然排序走到竞价排名,就是现成的前车之鉴。

## 我的判断:能用,怎么用

可以信的部分:原则性、方向性的建议。该不该建应急金、指数基金还是个股、股债比例怎么随年龄调,这些是模型从教科书共识里学来的,研究显示它执行得不错。

要打折的部分:状态变化后的动态调整。失业、市场暴跌之后怎么办,模拟里模型明确做不好,这种时刻别只听它的。

要自己动手的部分:替模型做追问。「信息给全才有定制方案」算不上新发现,找真人顾问你同样得交底;差别在于真人顾问的服务通常从把信息问全开始,而单轮问答里的模型不追问,信息缺了它就只给模糊的通用答案。所以这份清单得你自己过一遍:收入、资产、负债、年龄、目标期限、风险承受能力,一项别省,再要求模型说明它做了哪些假设。研究里学术 prompt 带来的改善,正是来自这些信息。

管不到的部分:范围外的理财决策。前面说过,这项研究只测了长期的存钱和配置。买房、房贷、信贷、保险不在其中,而这些决策往往一次性、金额大、错了难回头,和存钱配置这种可以逐年修正的决策性质不同。AI 在这些问题上表现如何,这项研究没有提供任何证据,「出人意料地好」的结论搬不过去。

始终记住的部分:这是模拟结果。论文测的是「严格照做几十年」的虚拟人,真人做不到;从建议文本到可执行规则的转译,也经过研究者的解释。它证明的是建议文本的方向质量,不是真实用户的真实收益。

回到标题的问题:AI 理财建议赢了谁?赢的是受访者自己报告的现状——按 de Silva 的描述,很多人的现状就是没有顾问,靠亲友和随手搜索做决定;研究里正式的比较对象是人们当前的做法,「亲友」「搜索」并没有单独设组——而且只赢在长期存钱和配置这一条线上。这个结论我信,也有实际意义,毕竟这是绝大多数人的处境。但它没和人类顾问比过,没在真实世界跑过,没测过买房信贷这类一次性大决策,还会因为你是谁、你怎么问而给出成色不同的答案。当第一意见,值得用;当唯一意见,风险自负。

## 参考来源

- [AI financial advice is surprisingly good — especially if you ask the right questions | MIT Sloan](https://mitsloan.mit.edu/ideas-made-to-matter/ai-financial-advice-surprisingly-good-especially-if-you-ask-right-questions) — 选题来源;「照 AI 建议模拟 vs 受访者当前做法」的比较方法、Choukhmane「有点意外」引语、5 万/10 万美元财富差距、Vanguard 6%/iShares 3.4%/提及率 0.4%、失业后砍支出与组合漂移两处失效模式、「学术 prompt 改善建议」表述、性别差距分解(约三分之二来自 prompt 写法差异,约三分之一来自同一 prompt 标注性别后建议变化)
- [AI Financial Advice: Supply, Demand, and Life Cycle Implications(论文 PDF,作者官网)](https://tahachoukhmane.com/wp-content/uploads/2026/03/CdSLA-2026-AI-Financial-Advice.pdf) — 论文本体;实验设计、模拟器与对照的细节以此为准(论文图表中 iShares 提及率为 2.9%,与报道的 3.4% 略有出入)
- [论文页 | MIT Sloan CFI](https://mitsloan.mit.edu/centers-initiatives/cfi/ai-financial-advice-supply-demand-and-life-cycle-implications) — 摘要原文:受访者被要求写 spending 与 investing 提问(即研究范围仅覆盖消费储蓄与投资配置,不含买房/信贷/保险)、测试模型为 GPT-5.2 与 Gemini 3 Flash、三大发现(含「更好的消费平滑、更少依赖经验法则」)、组间退休财富差 4-5%、supply/demand 分解、工作论文编号 7377-26、瑞士金融研究所奖项
- [Study finds LLMs nudge users toward smart savings and investing habits | phys.org](https://phys.org/news/2026-07-llms-nudge-users-smart-investing.html) — de Silva 引语、四成受访者存款不足 1 万美元、83%/6% 流动性数据、男女 prompt 用词差异、「模型一般不知道用户性别」与「给女性的股票敞口建议更低」表述、3%-4% 提取率失效模式、厂商推销激励引语
- [What AI tells people seeking low-cost financial advice | Stanford GSB Insights](https://www.gsb.stanford.edu/insights/what-ai-tells-people-seeking-low-cost-financial-advice) — 性别标签对照实验「给女性推荐更低股票敞口」的表述、de Silva 访谈
- [Hacker News 讨论](https://news.ycombinator.com/item?id=49139102) — 报道的传播背景(200 多条评论)
