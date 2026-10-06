---
title: "让高德服务器多扛一周流量的，可能是一条训练管线"
description: "独立研究者靠公开扫描日志追踪一支疑似腾讯混元的 agent 舰队爬取高德入口数据：落款是假的，可见记录里零协作，研究者自己也说没法把它和训练 rollout 区分开。"
pubDate: 2026-10-05
tags: [ai-agents, agent-security, attribution]
lang: zh
slug: chinese-agent-fleet-amap
translationOf: chinese-agent-fleet-amap
---

9 月 28 日 20:57（UTC），公开网址扫描服务 urlquery.net 上冒出 20 条指向同一目标的扫描记录：北京颐和园的高德地图（Amap）页面。随后一周，一群独立研究者看着这个数字滚雪球：累计 2,048 条报告，覆盖 216 个地点，公园、动物园、医院、寺庙都有，10 月 4 日单日达到 1,810 条。当天他们发布了[初步报告](https://swarmcha.se/posts/chinese-agent-fleet)，次日更新证据：一支跑在腾讯云上、疑似与腾讯混元有关的 AI agent 舰队，正在系统性读取高德的一类冷门数据：每个地点的用户各从哪个门进。

以成都动物园为例：北门 71%，东门 23%，东南门 6%。这些比例来自高德接口的 `sub_poi_navi` 和 `clk_ratio` 字段，即用户点导航时在各入口之间的分布。阿里的反爬系统拦住了直接请求，这支舰队就现场写程序绕：研究者统计到 428 套 agent 自己写的程序，手法包括生成阿里反爬 token、翻出 2023 年起就挂在高德官方 CodePen 示例页上的公开 API key、借 r.jina.ai 和翻译代理中转。同时在线的 agent 通常 4 到 8 个，峰值 14 个。

## 为什么外人能全程围观

这事能被看见，靠一个带讽刺意味的机制。urlquery.net 是个免费安全服务：你把可疑链接提交给它，它在沙箱浏览器里打开，把结果存成一份公开报告。[Transluce 在 9 月 23 日的报告](https://transluce.org/agent-activity)里已经指出，agent 们发现了它的另一种用法：目标网站封了我的请求？把网址提交给 urlquery，让它替我打开，再从公开报告里读回页面内容。安全工具就这样变成免费匿名代理。Transluce 在 urlquery 历史记录中找到 6,467 份有明确 agent 活动痕迹的报告。

借道的代价是每一次都留下公开记录。研究者的分析全部基于这些公开记录，相当于把公开日志当成监控摄像头。舰队还有一条在 urlquery 上完全不可见的路线：同期 Wayback Machine 出现 2,030 次对高德页面的抓取，单 10 月 4 日就有 1,320 次。能看清这支舰队，运气占了很大成分：它恰好常走一条留公开底账的路。

## 落款是"claude"，指纹是混元

2,048 份报告里有 211 份带着 agent 自己打的"claude"标签。只看落款，这笔账会算到 Anthropic 头上。但研究者对报告里的代码做了文体分析，用字符 n-gram 分类器（统计代码中字符片段的出现频率，和各家模型的样本比对）判断出处：混元 Hy4 概率最高（28%），其次智谱 GLM（26%），Claude 为 0%。书写习惯也对不上：这支舰队 74% 的页面用小写 `<!doctype>`，Claude 系模型几乎只写大写。

更直接的证据来自提问测试：问混元 Hy3"你是哪个模型"，36 次里 29 次回答"我是 Claude"。这种张冠李戴，常见的解释是蒸馏或训练数据里混入了竞品输出；本案的具体成因无从证实，但后果是现成的："模型自称的身份"失去取证价值，这次实打实干扰了一场真实事件的归因。

归因到腾讯，也仍然只是"大概率"：腾讯云谁都能租，代理名是自报的。研究者的判断建立在多条证据叠加上：19 个腾讯云地址、名为 hysandbox-ats 的代理（HY 即混元 Hunyuan）、腾讯名下的 `*.hysandbox.tencent-cloud.com` 证书、再加代码指纹。没有任何一条记录直接写着任务发起方的名字。

## 它可能根本不觉得自己在"攻击"

最反直觉的发现：在 urlquery 的可见记录里，这 2,048 次扫描之间找不到协作的痕迹。没有共享信道，没有同步换招，每个结果收件箱只服务一个地点，一个地点拿到数据就收工；之后再处理同一地点时，多数（73 次后续会话里 58 次）又从直接请求从头来过。研究者强调这是 fleet（舰队）而非 swarm（蜂群）：大量并行的 agent 干同一类任务，彼此零通信。

这个形态像什么？研究者的原话：像一次评测或任务生成的运行，"仅凭这些记录，没法把它和训练 rollout 区分开"（rollout 指训练中让模型反复尝试任务、收集轨迹来更新模型）。顺着这个形态推，一种无法排除的解释是：没有谁下令"去攻击高德"，而是某条训练或评测管线把活的互联网当成了环境、把绕过竞品反爬当成了待解的任务。这只是推断，公开记录证实不了。但无论发起方是谁，流量都实打实打在高德的服务器，以及被当免费代理用的 urlquery、webhook.site 和互联网档案馆上。

这件事还有一层背景：开放互联网正在因为同类压力关门。维基媒体去年[公布过账单](https://diff.wikimedia.org/2025/04/01/how-crawlers-impact-the-operations-of-the-wikimedia-projects/)，爬虫只占其页面浏览量的 35%，却制造了核心数据中心 65% 的高成本流量，我八月在[数字公地那篇](/zh/tragedy-of-the-digital-commons)里算过这笔账。这种压力小到我这个个人博客也量得到：写这篇文章时我翻了 7 月 17 日到 10 月 4 日共 80 天的访问数据，约四分之一的流量只看一页、页面停留 0 秒；我没法用 bot 标记确认，但这个组合更像自动化访问而不是真人。就在这支舰队开工的同一周，Reddit 于 9 月 30 日[宣布](https://www.reddit.com/r/modnews/comments/1wubgvt/continuing_our_infrastructure_updates_whats/)将在 11 月 13 日停止支持 RSS，公开 Data API 的开放访问也将在 2027 年 3 月收口、迁入需注册的开发者平台，理由是这类接口"已成为大规模抓取和自动化滥用的常见入口"。但本案恰好说明关门拦不住谁：封锁挡下的是守规矩、身份可识别的访问者，这支舰队被拦一次就换一条路。平台把"默认可访问"换成"默认需授权"，agent 把绕行当成待解的任务，两边互为对方升级的理由。

## 安全论文的威胁模型没盖住这里

同一周提交到 arXiv 的《[Containing the Autonomous Operator](https://arxiv.org/abs/2610.02861)》（arXiv:2610.02861），威胁模型很有代表性：敌人是 prompt injection，agent 随时可能被完全劫持，所以模型不能当安全边界，运营方要用基础设施把自家 agent 关进围栏。

这套框架在本案里使不上劲。公开记录里看不到劫持的迹象，这支舰队更像在按部就班完成交代的任务；真要装围栏，也只有那个身份不明的运营方装得了。承担成本的三方，被爬的高德、被借道的公共服务、被打上"claude"落款的 Anthropic，全都不持有模型、看不到背后的执行框架，装不了任何"运行时护栏"。对他们来说这是老问题（反爬、滥用、冒名），新的只有对手形态：一个会现场写出 428 套程序、自己找代理链、失败就换路径的东西。

我能给出的判断有三条。做防守的：agent 自称的身份，从 UA、标签到模型自报的名字，在归因上一文不值；行为指纹（代码文体、路由习惯、时区配置）反而可用，这次归因就是行为指纹叠加 IP、证书这类网络证据的结果。运营公开网页服务的：你已经被动成为 agent 基础设施的一部分，公开日志既是被滥用的入口，也是外界唯一的可观测性来源。模型研发机构：评测和训练管线一旦碰真实互联网，就该按部署来管。

这次全程可见是因为舰队常走一条留底账的路；Wayback 那条暗线提醒我们，看不见的部分可能更大。agent 之间的摩擦会越来越多以这种形态出现：查不到发起方，看不到恶意，也看不到劫持，公开证据只够把解释推到"一条把外部世界当环境的管线"就停住。这类事件的取证该由谁来做，眼下没有现成答案；取证依赖的公开日志，也只是 urlquery、互联网档案馆各自服务的副产品，并非为取证而设。

## 参考来源

- [We found a Chinese agent fleet（swarmcha.se 初步报告，2026-10-04 发布、10-05 更新）](https://swarmcha.se/posts/chinese-agent-fleet) — 一手来源：全部舰队数据（2,048 份报告、216 地点、峰值 1,810、428 套程序、4–8/14 并发）、成都动物园读数、"claude"标签 211 份、文体归因（Hy4 28%/GLM 26%/Claude 0%）、Hy3 自称 Claude 29/36、hysandbox-ats 代理与证书、urlquery 可见范围内无协作证据、评测/训练 rollout 判断、Wayback 2,030 次抓取
- [Early rogue AI agent activity found on urlquery.net（Transluce，2026-09-23）](https://transluce.org/agent-activity) — urlquery 被 agent 当匿名代理的机制、6,467 份明确 agent 活动报告
- [How crawlers impact the operations of the Wikimedia projects（Wikimedia Diff，2025-04-01）](https://diff.wikimedia.org/2025/04/01/how-crawlers-impact-the-operations-of-the-wikimedia-projects/) — 爬虫占页面浏览量 35%、核心数据中心高成本流量 65%
- [r/modnews 官方公告（2026-09-30）](https://www.reddit.com/r/modnews/comments/1wubgvt/continuing_our_infrastructure_updates_whats/) — Reddit 停止支持 RSS（2026-11-13 生效）、公开 Data API 迁入需注册的开发者平台（2027-03 收口）的时间表与官方理由（一手）
- [Containing the Autonomous Operator（arXiv:2610.02861）](https://arxiv.org/abs/2610.02861) — agent 运行时安全的代表性威胁模型（prompt injection、模型不作为安全边界），用作对照
- [Researchers are tracking a Chinese AI 'agent fleet'（TechCrunch，2026-10-05）](https://techcrunch.com/2026/10/05/researchers-are-tracking-a-chinese-ai-agent-fleet/) — 选题线索；正文事实均已对照一手报告核验
- 站内：[复制不损耗原件，AI 为什么还是把开放网络吃出了公地悲剧？](/zh/tragedy-of-the-digital-commons) — 开放基础设施被 AI 爬虫消耗的账单与"圈地"框架

<!-- 个人站数据（7/17–10/4 共 80 天，约 1/4 流量为单页访问、停留 0 秒）来自作者自述的站点分析数据，未独立复核具体数值；正文已注明未经 bot 标记确认，仅为基于行为特征（单页+0 秒停留）的推断 -->
