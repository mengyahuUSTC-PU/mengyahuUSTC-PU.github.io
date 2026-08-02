---
title: "AI 理财建议赢了谁?对照组里没有人类顾问"
description: "MIT Sloan 让 1000 个成年人自己写 prompt 向 LLM 要理财建议,再模拟照做一生的结果。结论确实亮眼,但要先看清对照组是谁、哪些场景会失效。"
pubDate: 2026-08-01
tags: [personal-finance, llm-evaluation, ai-fairness]
lang: zh
slug: ai-financial-advice-right-questions
translationOf: ai-financial-advice-right-questions
---

七月底,MIT Sloan 一篇研究的报道在 Hacker News 上传开,标题自带结论:[AI 理财建议出人意料地好,尤其当你问对问题时](https://mitsloan.mit.edu/ideas-made-to-matter/ai-financial-advice-surprisingly-good-especially-if-you-ask-right-questions)。

我读完的第一个问题是:「好」是个比较级,和谁比?

答案藏在研究设计里,比标题有意思得多。

## 这项研究到底测了什么

论文题为[《AI Financial Advice: Supply, Demand, and Life Cycle Implications》](https://tahachoukhmane.com/wp-content/uploads/2026/03/CdSLA-2026-AI-Financial-Advice.pdf),作者是 MIT Sloan 的 Taha Choukhmane、Weidong Lin、Matthew Akuzawa 和斯坦福商学院的 Tim de Silva,拿了 2026 年瑞士金融研究所杰出论文奖([MIT Sloan 工作论文 7377-26](https://mitsloan.mit.edu/centers-initiatives/cfi/ai-financial-advice-supply-demand-and-life-cycle-implications))。

设计分三步。第一步,找 1000 名有代表性的美国成年人,让他们自己写 prompt,向 GPT-5.2 和 Gemini 3 Flash 要消费和投资建议。注意是自己写:研究者不代笔,就是要看真实用户会怎么问。

第二步,把模型的建议解析成可执行的规则:存多少、股票配多少。

第三步,把这些规则放进一个生命周期模拟器,让「虚拟的你」带着这套建议过完一生。收入按真实劳动力市场数据涨跌,会失业,会遇到熊市,要交税。最后看 60 岁时的财富和一生的消费水平。

评判标准是生命周期理论。这是家庭金融的规范框架,核心处方大致是:年轻时投资期限长、未来工资收入多,该多配股票;随年龄增长逐步降低股票比例;留出应急储蓄;让消费在好坏年景之间尽量平滑,别大起大落。

看清这个设计,「出人意料地好」的确切含义就出来了:照 AI 的建议做,大多数受访者会比他们现在的实际做法更接近生命周期理论的处方。

对照组是受访者自己的现状。不是人类理财顾问。

这个基线有多低?据 [phys.org 转述](https://phys.org/news/2026-07-llms-nudge-users-smart-investing.html),写 prompt 的受访者里约四成存款不到一万美元。作者之一 de Silva 的原话也很诚实:「它不完美,但比很多人现在做决定的方式强,比如问亲友,或者随手上网搜。」

## 三个发现,分开看

第一,方向大体正确。模型的建议整体把人往教科书方向推:更多人参与分散化的股票基金,股票比例随年龄下降,存出可观的储蓄缓冲。模型还会主动补课:据 phys.org 转述,83% 的回复提到了流动性,也就是手头留多少随时能动用的现金,而只有 6% 的用户主动问到这一点(此数据仅见转述,待核实,见文末)。

第二,「问对问题」的门槛比听上去高。研究者做了替换实验:把用户自己写的 prompt 换成「学术 prompt」,建议质量进一步向理论靠拢,消费平滑做得更好,更少依赖粗糙的经验法则。所谓学术 prompt,是把生命周期框架、完整的财务信息(收入、资产、负债、投资期限)和明确的经济假设都写进提问里。

也就是说,「问对问题」并非提示词话术,它约等于「你本来就得懂点理财,还得把自己的家底说全」。de Silva 给个人用户的建议也是先补金融常识,他说提问的写法「影响极大」,有了基础知识才能把这个工具用出威力(据 phys.org 转述)。

第三,建议质量因人而异,而且偏差的方向很糟糕。建议随性别和金融素养系统性变化,几十年累积下来,组间退休财富差 4% 到 5%。按 [MIT Sloan 报道](https://mitsloan.mit.edu/ideas-made-to-matter/ai-financial-advice-surprisingly-good-especially-if-you-ask-right-questions)给的绝对数:女性和金融素养较低的用户,60 岁时财富少约 5 万美元;没用过 AI 的用户少近 10 万美元(6%)。

论文把差异拆成两半。需求端:不同人写的 prompt 不同,素养低的人给的信息少,拿到的建议就糙。供给端:同样的 prompt,模型给的建议也不同,这一点论文摘要明确写了;据 phys.org 转述,即便 prompt 内容相同,模型给女性的股票配置建议也更保守(具体实验做法待核实,见文末)。供给端这半是模型自身的问题;需求端那半构成一个循环:最需要建议的人,恰恰最问不出好问题。

## 为什么增益分布是这样

LLM 按输入定输出。你给的信息越完整、框架越对,它的建议越接近最优;你只说「我 30 岁,该怎么投资」,它只能给通用模板。这不是缺陷,是这类系统的工作方式。

后果是:传统理财顾问的门槛在价格,请得起的人才有;LLM 把价格降到零,却立起另一道门槛,会提问的人才能问出好建议。下限确实抬高了,大多数人照做都比现状强。但增益向高金融素养、高 AI 熟练度的人倾斜。工具普惠,增益不均。

## 静态原则会背,动态调整不会做

模拟里暴露的三个具体的坑,比总体结论更有参考价值:

- 失业后,模型建议砍支出砍得过狠。生命周期理论的处方恰恰相反:动用储蓄缓冲、平滑消费,别让一次收入冲击把生活水平打穿。
- 组合放着漂移,不主动再平衡。股票涨了之后在组合里的占比会被动升高,风险敞口越拉越大,模型不太会提醒你卖掉一部分、回到目标比例。
- 退休后花钱过于保守,基本照搬「每年提取储蓄的 3%-4%」这条安全提取率经验法则,该花的钱不花,消费平滑又输一次。

三个坑一个共性:通用原则背得很好,遇到状态变化时的动态调整做不好。而后者恰恰是人类顾问收费的核心部分。

## 还有一个没人管的问题:推荐位

Vanguard(先锋领航,低费率指数基金巨头)的产品出现在 6% 的回复里,iShares(贝莱德旗下的 ETF 品牌)出现在 3.4%,而提到这两家的 prompt 不到 0.4%([MIT Sloan 报道](https://mitsloan.mit.edu/ideas-made-to-matter/ai-financial-advice-surprisingly-good-especially-if-you-ask-right-questions))。

今天这不算坑人:两家都以低费率著称,推荐它们和教科书方向一致,大概率来自训练数据的自然分布。但 de Silva 点出的隐忧是结构性的:模型厂商清楚大量用户在拿它做理财决策,就存在引导用户买特定产品的激励。模型回答里的「推荐位」值多少钱,目前没有任何披露或监管机制。搜索引擎从自然排序走到竞价排名,是现成的前车之鉴。

## 我的判断:能用,怎么用

可以信的部分:原则性、方向性的建议。该不该建应急金、指数基金还是个股、股债比例怎么随年龄调,这些是模型从教科书共识里学来的,研究显示它执行得不错。

要打折的部分:状态变化后的动态调整。失业、市场暴跌之后怎么办,模拟里模型明确做不好,这种时刻别只听它的。

要自己动手的部分:把 prompt 写全。收入、资产、负债、年龄、目标期限、风险承受能力,一项别省,再要求模型说明它做了哪些假设。研究里学术 prompt 的增益,正是来自这些信息。

始终记住的部分:这是模拟结果。论文测的是「严格照做几十年」的虚拟人,真人做不到;从建议文本到可执行规则的转译,也经过研究者的解释。它证明的是建议文本的方向质量,不是真实用户的真实收益。

回到标题的问题:AI 理财建议赢了谁?赢的是「没有顾问、靠亲友和搜索做决定」的现状。这个结论我信,也有实际意义,毕竟这是绝大多数人的处境。但它没和人类顾问比过,没在真实世界跑过,还会因为你是谁、你怎么问而给出成色不同的答案。当第一意见,值得用;当唯一意见,风险自负。

## 参考来源

- [AI financial advice is surprisingly good — especially if you ask the right questions | MIT Sloan](https://mitsloan.mit.edu/ideas-made-to-matter/ai-financial-advice-surprisingly-good-especially-if-you-ask-right-questions) — 选题来源;5 万/10 万美元财富差距、Vanguard 6%/iShares 3.4%/提及率 0.4%、失业后砍支出与组合漂移两处失效模式、「学术 prompt 改善建议」表述
- [AI Financial Advice: Supply, Demand, and Life Cycle Implications(论文 PDF,作者官网)](https://tahachoukhmane.com/wp-content/uploads/2026/03/CdSLA-2026-AI-Financial-Advice.pdf) — 论文本体(本环境无法解析 PDF 文本,细节核对见下方核查点)
- [论文页 | MIT Sloan CFI](https://mitsloan.mit.edu/centers-initiatives/cfi/ai-financial-advice-supply-demand-and-life-cycle-implications) — 摘要原文:测试模型为 GPT-5.2 与 Gemini 3 Flash、三大发现、组间退休财富差 4-5%、supply/demand 分解、工作论文编号 7377-26、瑞士金融研究所奖项
- [Study finds LLMs nudge users toward smart savings and investing habits | phys.org](https://phys.org/news/2026-07-llms-nudge-users-smart-investing.html) — de Silva 引语、四成受访者存款不足 1 万美元、83%/6% 流动性数据、相同 prompt 下对女性更保守、3%-4% 提取率失效模式
