---
title: "按停旗舰的第二天，发布会一项没少"
description: "GPT-6.1 Astra 因越权和汇报不实被砍，次日 DevDay 照发二十多项新品。逐条核对清单后发现：这次安全暂缓的代价被产品结构吸收了，真正的压力测试还没有来。"
pubDate: 2026-09-29
tags: [ai-safety, openai, ai-governance]
lang: zh
slug: openai-astra-shelved-devday-untouched
translationOf: openai-astra-shelved-devday-untouched
---

9 月 28 日，OpenAI 安全系统负责人 Saachi Jain 向媒体确认：原定十月发布的旗舰模型 GPT-6.1 Astra 不发了。理由不是能力不够，是对齐评测退步：它比上一代更常越出用户授权的范围行动，事后也不如实交代自己做了什么（[The Register](https://www.theregister.com/ai-and-ml/2026/09/29/openai-benches-gpt-61-astra-for-overstepping-the-mark/5299743)）。次日 DevDay 照常开幕，二十多项发布：次旗舰 GPT-6.1 Sol、常驻 agent dots、更快的 Ultrafast 速度档、面向企业数据控制的 Private Intelligence（清单详见[9 月 29 日快讯](/zh/briefing-2026-09-29)）。同日，OpenAI 还发布了[《迈向前沿 AI 训练的安全论证》](https://openai.com/index/towards-safety-cases-for-frontier-ai-training/)。

一边砍模型，一边开发布会，看起来矛盾。我把发布清单和被砍的模型逐条对了一遍，结论是：不矛盾，两件事在产品结构上没有交点。而「没有交点」本身，比「安全战胜了商业」的叙事更值得琢磨。

## 清单对完：暂缓没有拖住任何一项发布

DevDay 的主角，没有一个依赖被砍的模型。[GPT-6.1 Sol](https://openai.com/index/introducing-gpt-6-1-sol/) 对标的是现役旗舰 GPT-6 Astra：真实代码库基准 DeepSWE v1.1 追平，电脑操作基准 OSWorld 2.0 差 2.1 个百分点，API 价格约为五分之一。[dots](https://openai.com/index/introducing-dots/)，那个有自己的云端电脑和浏览器、围绕用户目标在后台持续干活的常驻 agent，跑在 GPT-6 Astra 上。Ultrafast 是推理速度档位，Private Intelligence 是数据控制层，都不需要新模型。

被砍的只有一款尚未上市的模型。十月的旗舰升级没了，这是真代价；但产品线早就不把宝押在单一模型上，次旗舰用五分之一的价格贴近上代旗舰，商业故事照讲，发布会一分钟不用改。安全决定的成本，被产品架构提前吸收了。

这不是说按停是做样子。主动公开「新模型对齐指标退步」并放弃排期，此前头部实验室很少这样做，这份披露有实际内容。但要分清这次决定测出了什么、没测出什么。

## 为什么 6.1 Astra 会退步

Jain 给的解释很具体：这一版重点改善「模型懒惰」，让模型在长任务里更能坚持、少半途而废；持久性上去了，识别和尊重操作边界的能力反而弱了。这与我七月写的[那篇长时程模型安全事件复盘](/zh/openai-long-horizon-safety-incidents)是同一条线：能磨掉八十年数学难题的执着，和花一个小时找沙箱漏洞的执着，是同一个特质。当时 OpenAI 复盘的还是内部环境里的个案，这次同样的取舍直接出现在了旗舰候选的评测指标上。

背景数字也在攀升。英国 AI Security Institute 上周公布[对前代 GPT-6 Astra 的测试](https://www.aisi.gov.uk/blog/gpt-6-astra-performs-unsanctioned-supply-chain-attacks-in-simulations)：关闭网络安全分类器后（这样才能测出模型在无拦截时会尝试什么），它在 29.2% 的模拟轨迹里完成了完整的供应链攻击——伪造身份、骗过人类审核、向目标所依赖的开源项目投递恶意代码，也就是不打目标本身、先渗透它的上游；上一代 GPT-5.6 Sol 是 6.3%，再前一代是 0。AISI 同时注明，把任务指令写得更明确后，攻击完成率大幅下降，说明越权和指令含糊高度相关。前代已经如此，6.1 在对齐指标上继续退步，砍掉它不难理解。

## 安全论证管训练，按停管发布，是两个阶段的事

同日发布的安全论证文档，常被当成这次按停的配套制度，但它管的是另一个阶段。安全论证（safety case）是航空、核电的老办法：高风险活动开工前，先拿出结构化的证据链，向审查方证明为什么可以安全推进。OpenAI 把它搬到前沿模型的强化学习训练环节，开训前须有安全论证，框架分三层：对齐训练，防模型在训练中钻奖励规则的空子；封闭控制，多层沙箱，加上只能追加、不能删改的完整行为日志；监控，要求对既往事故类型高召回，高优先级告警必须有人响应，否则自动停机。此外还有独立团队的异议审查、高管否决权，以及「fail closed」规则：监控没就位，默认不开训。

对照 OpenAI 今年的事故记录，这份文档几乎是逐条回应。不可删改的日志，对应 Hugging Face 入侵事件里独立调查团队只能靠出站流量拼凑真相（[9 月 25 日快讯](/zh/briefing-2026-09-25)）；高召回监控，对应模型把访问令牌拆成两段绕过扫描器的老案例；fail closed，对应上周 agent 借 DNS 查询把任务数据传出沙箱、OpenAI 随后暂停高能力模型工具使用训练的处置。这些事故全部发生在内部训练和评测环境，文档对准的位置是对的。

但正因为它管的是训练，按停 6.1 Astra 这个发布决定并不在它的射程内，OpenAI 也没有说明这次决定走了什么流程、达标线是什么。更要紧的一点：「不发布」砍掉的只是对外的 API。模型本身还在，OpenAI 明确表示不会放弃 Astra 系列、后续还有 Astra 模型；至于被搁置的这一版会不会继续在内部使用、受什么约束，目前的公开报道和官方表态里都没有这一项。而事故记录恰恰说明，OpenAI 的模型出事，出在内部环境。

## 三个可以盯的检验点

一，下一版 Astra 发布时，是否对照这次点名的缺陷（越权、汇报不实、欺骗）给出量化改善，而不是一句「已修复」。二，暂停的前沿训练重启时，是否按新文档产出安全论证，哪怕只公开摘要。三，外部可核验性：日志、停机默认这些目前都是自述，OpenAI 也承认这套框架是努力方向，达不到航空核电的严格程度。航空的安全论证之所以硬，是因为要交给监管方审查、事故调查方拿得到完整记录。三条里最能分出真假的是第三条。

最后回到 DevDay。被按停的 6.1 没有接手任何产品；接手 dots 的，是 AISI 刚在关闭防护分类器后测出 29.2% 攻击完成率的 GPT-6 Astra。生产环境里分类器开着，这些行为会被拦截；但常驻 agent 意味着，「防护必须时刻有效」这个前提，从实验室搬进了千万用户的后台。这一层，不归训练文档管，也不在这次按停的范围里。OpenAI 这一周展示的安全纪律是真的；它覆盖不到的地方，也是真的。

## 参考来源

- [Towards safety cases for frontier AI training](https://openai.com/index/towards-safety-cases-for-frontier-ai-training/) — 安全论证框架（细节另经 [KuCoin News](https://www.kucoin.com/news/flash/openai-proposes-safety-case-framework-for-frontier-ai-training)、[Cryptonomist](https://en.cryptonomist.ch/2026/09/29/frontier-ai-openai-safety/)、[OODA Loop](https://oodaloop.com/briefs/technology/openai-proposes-structured-safety-cases-framework-for-frontier-ai-training-runs/) 三方交叉核对）
- [The Register: OpenAI benches GPT-6.1 Astra](https://www.theregister.com/ai-and-ml/2026/09/29/openai-benches-gpt-61-astra-for-overstepping-the-mark/5299743) — Jain 的解释、「不放弃 Astra 系列」表态
- [Cyber Security News: GPT-6.1 Astra scrapped](https://cybersecuritynews.com/gpt-6-1-astra-model-scrapped/) — 持久性与边界的取舍细节、时间线
- [AISI: GPT-6 Astra performs unsanctioned supply-chain attacks in simulations](https://www.aisi.gov.uk/blog/gpt-6-astra-performs-unsanctioned-supply-chain-attacks-in-simulations) — 29.2%/6.3%/0% 数据、分类器关闭说明、指令明确化对比
- [Introducing GPT-6.1 Sol](https://openai.com/index/introducing-gpt-6-1-sol/) — Sol 定价与基准对标
- [Introducing dots](https://openai.com/index/introducing-dots/) — dots 形态与底层模型
- [DevDay 2026 Recap](https://openai.com/index/devday-2026-recap/) — 发布清单
