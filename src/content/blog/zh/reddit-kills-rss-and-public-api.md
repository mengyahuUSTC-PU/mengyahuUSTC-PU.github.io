---
title: "挡不住爬虫,就把免费关掉:Reddit 杀死 RSS 和公开 API"
description: "Reddit 自己的诉状承认,工业级抓取早已绕开正门。关闭 RSS 和公开 API 拦住的是守规矩的人,换来的是授权生意的稀缺性和 DMCA 诉由。"
pubDate: 2026-09-30
tags: [open-web, data-licensing, ai-governance]
lang: zh
slug: reddit-kills-rss-and-public-api
translationOf: reddit-kills-rss-and-public-api
---

9 月 30 日,Reddit 在面向版主和开发者的两个官方帖子里宣布([r/modnews](https://www.reddit.com/r/modnews/comments/1wubgvt/continuing_our_infrastructure_updates_whats/)、[r/redditdev](https://www.reddit.com/r/redditdev/comments/1wubcvf/moving_data_api_apps_to_the_developer_platform/)):11 月 13 日起停止支持 RSS;公开 Data API 在 2027 年 3 月前全部关闭,今年 10 月 31 日后不再受理新接入申请,现有第三方应用须在 2027 年 1 月 12 日前迁入其开发者平台并通过审批([TechCrunch](https://techcrunch.com/2026/09/30/reddit-is-killing-rss-feeds-ending-public-api-access-because-of-ai-bots/))。旧版界面 Old Reddit 也加了门槛:只对登录的版主和近 90 天用过旧版的登录用户开放([Engadget](https://www.engadget.com/2273661/reddit-imposes-new-restrictions-on-old-reddit/))。理由是一句话:RSS「已成为大规模抓取和自动化滥用的常见入口」。

替代方案的分配很能说明优先级:版主的审核告警可以迁去官方的 Discord Relay 应用;至于把 RSS 用在社区审核之外的普通订阅者,官方直说没有替代品。

抓取的负担是真的。我八月在[写数字公地那篇](/zh/tragedy-of-the-digital-commons)里算过维基媒体、SourceHut 这些开放基础设施被 AI 爬虫吃掉的账单,Reddit 面对的压力不会更小。但「防滥用」解释不了这次关门的方式。

## 正门外面没有爬虫

最有力的反证来自 Reddit 自己的诉状。2025 年 10 月它起诉 Perplexity 和三家数据中介(SerpApi、Oxylabs,以及由前俄罗斯僵尸网络运营的 AWM Proxy)时,描述过工业级抓取如今长什么样:被 Reddit 封锁后,这些中介不碰 RSS 也不碰 API,改从 Google 搜索结果里成规模地抓取 Reddit 内容的副本,同时伪装身份躲避封锁([SiliconANGLE](https://siliconangle.com/2025/10/22/reddit-suing-perplexity-ai-data-scraping-firms-using-data-without-permission/))。

也就是说,按 Reddit 自己的描述,决心抓取的人早就不走正门了。RSS 和公开 API 是只读、结构化、最容易限流和计量的接口,真要对付滥用,限流比拆除更对症。拆除之后断粮的,是用 RSS 订阅版面的用户、做研究的学者、社交聆听工具和依赖告警的审核流程,恰恰是守规矩、身份可识别的那部分流量。

## 关门图什么:一条商业线,一条法律线

把 Reddit 近三年的动作连起来,方向只有一个:

- 2023 年 6 月,API 从免费转收费,Apollo 等第三方客户端关停,数千社区以关闭版面抗议([Wikipedia](https://en.wikipedia.org/wiki/Reddit_API_controversy))
- 2024 年 2 月,与 Google 签内容授权协议,双方公开确认,金额未官宣,媒体援引知情人士估算约每年 6000 万美元;公告与 IPO 申报同日([The Register](https://www.theregister.com/2024/02/22/reddit_google_license_ipo_altman/))
- 2024 年 5 月,与 OpenAI 签类似协议([CNBC](https://www.cnbc.com/2024/05/16/reddit-soars-after-announcing-openai-deal-on-ai-training-models.html))
- 2024 年 7 月,robots.txt 改为封禁所有爬虫、只给 Google 留口([Waxy](https://waxy.org/2024/07/reddit-blocks-all-crawlers-in-robots-txt-gives-exclusive-access-to-google-with-ai-deal/));当时承诺 Internet Archive 这类「善意行为者」不受影响([TechCrunch](https://techcrunch.com/2024/06/25/reddits-upcoming-changes-attempt-to-safeguard-the-platform-against-ai-crawlers))
- 2025 年 6 月,起诉 Anthropic 抓取数据训练模型
- 2025 年 8 月,收回上述承诺,Wayback Machine 从此只能存档 Reddit 首页([Gizmodo](https://gizmodo.com/reddit-is-blocking-the-wayback-machine-from-archiving-posts-2000641546))
- 2025 年 10 月,起诉 Perplexity 与三家中介
- 2026 年 9 月,关闭 RSS 与公开 API

每一步都在把「默认可访问」换成「默认需授权」。为什么值得做,有两条线。

商业线:2026 年二季度,Reddit 的「其他收入」(数据授权是大头)为 4300 万美元,同比增 24%([SEC 8-K](https://www.sec.gov/Archives/edgar/data/0001713445/000171344526000098/exhibit992q226.htm)),只占 8.05 亿美元总营收的 5%,但这是它对资本市场讲的第二增长曲线,已披露的买家里最大的是 Google 和 OpenAI。授权生意需要稀缺性:只要还存在免费且合法的程序化通道,付费方买到的就只是「省事」;免费通道拆光之后,买到的才是「唯一合法入口」。

法律线更关键。公开接口还在时,「未经授权的抓取」在法律上是模糊的:内容公开、接口由官方提供,平台很难主张对方绕过了什么。把一切程序化访问收进注册审批的闸口之后,任何绕行都可以被描述成「规避技术保护措施」。Perplexity 诉状正是这个用法:Reddit 主张的重点不是对方复制了内容,而是对方绕过了封锁,触发 DMCA 反规避条款,这与普通版权侵权是两个独立诉由。关闭公开接口在技术上拦不住抓取,但它改写了每一次抓取的法律性质:围栏的功能,是让「翻墙」这个动作在法律上成立。

所以选题里那个问题,「保护数据资产,还是把访问权转卖给付费方」,答案是这两件事本来就是同一件:圈地的意思,就是把无主的通行变成可出售的通行权。只有一层值得点破:被保护的物件并非内容本身。内容由用户无偿写成,复制也不损耗原件;这轮操作真正制造出来、也真正值钱的,是「合法访问」这个此前不存在的稀缺品。

## 对从业者意味着什么

一,数据管线的合规风险变了。经搜索结果页、代理中介间接获取 Reddit 数据,已从灰色地带变成被点名的诉由;采购第三方网络数据集时,来源链里是否经过被诉中介(SerpApi、Oxylabs 都在名单上),值得专门查一遍。

二,「平台公开接口默认存在」不能再当架构假设。X 在 2023 年初关掉免费 API 是前例,Reddit 这次进一步证明了关门的成本有多低:广告收入 7.62 亿美元不受影响,授权收入反而因稀缺性更值钱。同样坐拥大量用户对话数据的平台,没有理由不跟进。

三,没有议价能力的那部分使用者会直接消失。官方列出的受影响方包括研究工具,而公共存档去年已被先行关在门外。付得起钱的进围栏,付不起的离场,「关于互联网的研究」所依赖的数据底座会被系统性收窄。

接下来我会盯两处:2027 年 3 月闸口合拢后,Reddit 是否为学术研究留出可负担的通道;以及哪家 UGC 平台第一个复制这套「诉讼加价目表」的组合。围栏一旦被证明无成本,就不会只有一道。

## 参考来源

- [TechCrunch: Reddit is killing RSS feeds and ending public API access because of AI bots](https://techcrunch.com/2026/09/30/reddit-is-killing-rss-feeds-ending-public-api-access-because-of-ai-bots/) — 主事件:各项截止日期、官方引语、$43M 背景
- [r/modnews 官方公告](https://www.reddit.com/r/modnews/comments/1wubgvt/continuing_our_infrastructure_updates_whats/) — RSS 关闭、Old Reddit 限制、Discord Relay(一手)
- [r/redditdev 官方公告](https://www.reddit.com/r/redditdev/comments/1wubcvf/moving_data_api_apps_to_the_developer_platform/) — Data API 迁移与注册截止日(一手)
- [Reddit Q2 2026 股东信(SEC 8-K Exhibit 99.2)](https://www.sec.gov/Archives/edgar/data/0001713445/000171344526000098/exhibit992q226.htm) — 总营收 $804.9M、广告 $762M、其他收入 $43M(+24%)
- [Social Media Today](https://www.socialmediatoday.com/news/reddit-ends-support-for-rss-feeds/831844/)、[Engadget](https://www.engadget.com/2273661/reddit-imposes-new-restrictions-on-old-reddit/) — 官方引语与 Old Reddit 90 天限制的交叉核实
- [The Register: Google-Reddit 授权协议](https://www.theregister.com/2024/02/22/reddit_google_license_ipo_altman/) — 约 $60M/年(知情人士估算)、与 IPO 申报同日
- [CNBC: Reddit-OpenAI 协议](https://www.cnbc.com/2024/05/16/reddit-soars-after-announcing-openai-deal-on-ai-training-models.html) — 2024 年 5 月 16 日公告
- [Waxy.org: robots.txt 封禁](https://waxy.org/2024/07/reddit-blocks-all-crawlers-in-robots-txt-gives-exclusive-access-to-google-with-ai-deal/)、[TechCrunch 2024-06-25](https://techcrunch.com/2024/06/25/reddits-upcoming-changes-attempt-to-safeguard-the-platform-against-ai-crawlers) — 封禁全部爬虫、「善意行为者」承诺
- [Gizmodo: Reddit 封锁 Wayback Machine](https://gizmodo.com/reddit-is-blocking-the-wayback-machine-from-archiving-posts-2000641546) — 2025 年 8 月 12 日起仅可存档首页
- [SiliconANGLE: Reddit 诉 Perplexity 等](https://siliconangle.com/2025/10/22/reddit-suing-perplexity-ai-data-scraping-firms-using-data-without-permission/) — 诉讼对象、经 Google 搜索结果抓取、DMCA 反规避诉由;并提及 6 月诉 Anthropic
- [Wikipedia: Reddit API controversy](https://en.wikipedia.org/wiki/Reddit_API_controversy) — 2023 年 API 收费与第三方客户端关停
- 站内:[复制不损耗原件,AI 为什么还是把开放网络吃出了公地悲剧?](/zh/tragedy-of-the-digital-commons) — 抓取成本账单与「圈地」框架的前文
