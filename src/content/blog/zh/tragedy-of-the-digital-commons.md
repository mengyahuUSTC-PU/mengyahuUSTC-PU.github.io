---
title: "复制不损耗原件，AI 为什么还是把开放网络吃出了公地悲剧？"
description: "维基媒体的带宽账单、curl 的假漏洞报告、跌回 2009 年的 Stack Overflow 提问量：AI 抓取消耗的是数字公地的再生能力，而正在成型的解药叫圈地。"
pubDate: 2026-08-09
tags: [ai-governance, open-web, digital-commons]
lang: zh
slug: tragedy-of-the-digital-commons
translationOf: tragedy-of-the-digital-commons
---

《经济学人》8 月 6 日发了一篇[《The tragedy of the commons, AI edition》](https://www.economist.com/britain/2026/08/06/the-tragedy-of-the-commons-ai-edition)，讲英国的就业仲裁庭。按文中的说法，AI 把写申诉状的成本压到接近零，任何人十分钟就能生成一份看起来专业的法律文书，于是申诉量暴涨、积压越拖越长，今天立案的案子可能要等到 2030 年才开庭。免费的法律援助本该是好事，结果是所有人排更长的队。这篇文章在付费墙后面，我没能读到全文，以上概括来自公开流传的原句和 [Hacker News 上的讨论](https://news.ycombinator.com/item?id=49235011)。

仲裁庭是个标准的公地：处理能力有限，先到先得，每个人多占用一点，代价摊给所有排队的人。《经济学人》把这个框架用在法律系统上，但它真正的主场是开放网络本身。过去一年半，「AI 消耗数字公地」已经用不着比喻，运维报告里全是数字。

## 四份账单

维基媒体基金会 2025 年 4 月[公布过一组数据](https://diff.wikimedia.org/2025/04/01/how-crawlers-impact-the-operations-of-the-wikimedia-projects/)：自 2024 年 1 月起，多媒体内容的带宽消耗涨了 50%，增量几乎全部来自抓训练数据的爬虫。更能说明问题的是结构：机器人只占页面浏览量的 35%，却制造了核心数据中心 65% 的高成本流量。原因在缓存。人类读者扎堆在热门条目上，前端缓存就能挡下大部分请求；爬虫是地毯式扫库，专读没人看的冷门页面，每一次都得穿透到源站。基金会的原话：「我们的内容是免费的，我们的基础设施不是。」

代码托管平台 SourceHut 的创始人 Drew DeVault 在 2025 年 3 月的博文[《请别再把你的成本直接甩到我脸上》](https://drewdevault.com/blog/Stop-externalizing-your-costs-on-me/)里给出第二份账单：那几个月他每周 20% 到 100% 的工作时间花在对付 LLM 爬虫上，网站每周出现几十次短暂宕机。爬虫专挑计算上最贵的端点：git blame（逐行追溯代码作者，服务器要翻整个仓库历史）、每个仓库每一页提交记录。拦截几乎无效：请求来自数万个住宅 IP（看上去和普通家庭宽带用户没有区别），User-Agent 伪装成日常浏览器，每个 IP 在任何统计窗口里只发一个请求。同期 KDE 的 GitLab 也被爬到开发者一度无法访问（[LibreNews 的汇总报道](https://thelibre.news/foss-infrastructure-is-under-attack-by-ai-companies/)）。

curl 的维护者 Daniel Stenberg 在 2025 年 7 月给出第三份：当年 curl 在 HackerOne 上收到的安全漏洞报告里，[约 20% 是 AI 生成的垃圾](https://daniel.haxx.se/blog/2025/07/14/death-by-a-thousand-slops/)，编造的漏洞、幻觉出来的函数调用，写得有模有样；报告的真实率跌到 5%。每份报告要 3 到 4 名维护者各花半小时到三小时排查。资深维护者的审查注意力本来就稀缺，现在它被成批倒进了假报告。

第四份最直观。据 Gergely Orosz [对 Stack Exchange 公开数据的统计](https://blog.pragmaticengineer.com/stack-overflow-is-almost-dead/)，2025 年 5 月 Stack Overflow 的月度新提问量跌回了 2009 年的水平，那是网站上线后的第一个完整年头。

## 悲剧发生在哪一层

经济学教科书里的公地悲剧有个前提：资源是竞争性的，你多吃一口，我就少一口。数字内容恰恰不满足这个前提：一篇维基条目被复制一万次，原文一个字都不会少。单看这一点，「AI 版公地悲剧」像个用错的比喻。

但把四份账单摆在一起就清楚了：被消耗的都不是内容存量，而是让内容再生的资源。这样的资源有三种。

第一种是钱。带宽和服务器是真金白银，维基媒体的捐款、SourceHut 的订阅费，本来该花在人类读者身上。

第二种是注意力。curl 的例子比带宽更糟：假报告除了占用审查时间，还掺假。往草场倒垃圾和过度放牧是两种伤害，AI 同时干了这两件事。

第三种最要命：贡献回路。开放网络运转三十年靠一份隐性契约，抓取换流量。搜索引擎抓你的页面，作为交换，把搜到的读者送回你的网站；读者来了，广告费、捐款、新注册的编辑和回答者也跟着来，公地由此自我补给。这份契约还剩多少，Cloudflare 提出过一个直白的指标：crawl-to-refer 比值，平台每给你送回一个访客，抓走了多少个页面。[2025 年 6 月下旬的 Radar 数据](https://blog.cloudflare.com/ai-search-crawl-refer-ratio-on-radar/)里，Anthropic 的这个比值约为 70,900 比 1。按 [Cloudflare 自己的换算](https://blog.cloudflare.com/content-independence-day-no-ai-crawl-without-compensation/)：内容创作者想从 OpenAI 换到旧日谷歌同等的回流量，难 750 倍；从 Anthropic，难 30,000 倍。连谷歌自己送回的流量也比过去难挣了近 10 倍，因为越来越多搜索止步于结果页本身：先是答案框，如今是 AI 摘要。

AI 助手把答案直接说给用户听，用户就不再拜访答案的出处。对问答社区这是双重打击：读者不来，提问的人也不来。没有新提问就没有新回答，语料从此停更。再往下推一步，就是公地悲剧的标准结构：每家 AI 公司单独看都理性，抓得越多模型越好；合在一起，它们在吃掉训练自己的管线。下一代模型面对明年发布的新框架、新 API，去哪里找人类写下的答案？

自愿规范为什么拦不住，也能用同一个框架解释。网站表达「别抓我」的传统手段是 robots.txt：放在网站根目录的一个纯文本文件，写明哪些路径不欢迎爬虫。它没有任何强制力，全靠爬虫自觉，是 1994 年由 Martijn Koster 定下的君子协定，后来的标准文档 [RFC 9309](https://www.rfc-editor.org/rfc/rfc9309.html) 也明说「这些规则不是访问授权机制」（这个机制我在几天前[写 Claude 分享链接的文章](/zh/claude-share-links-google-indexed)里拆过）。它在搜索时代大体有效，因为搜索引擎要和网站维持长期关系，守规矩符合自身利益。训练数据的博弈不一样：抓一次就够，不需要关系；你克制，竞争对手不克制，落后的是你的模型。数万个住宅 IP 和伪装 User-Agent 的军备竞赛由此而来。Garrett Hardin [1968 年发表在《科学》的那篇论文](https://www.science.org/doi/10.1126/science.162.3859.1243)，开篇画的正是一片「对所有人开放的草场」；开放网络把「对所有人开放」写进了自己的设计。

## 围栏正在立起来

公地悲剧并非宿命。Elinor Ostrom 靠这个拿了 [2009 年的诺贝尔经济学奖](https://www.nobelprize.org/prizes/economic-sciences/2009/ostrom/facts/)：她研究的真实公地（灌溉系统、渔场、山地牧场）能长期维持下去，条件是边界清晰、监督可行、违规有代价。开放网络正在急补这三样，眼下能看到三种围栏。

技术围栏。开发者 Xe Iaso 在 [2025 年 1 月发布](https://xeiaso.net/blog/2025/anubis/)的 [Anubis](https://github.com/TecharoHQ/anubis)，在网站前面加一道工作量证明：浏览器要先算一道小的哈希题才能拿到页面，单个人类用户几乎无感，按百万次计的抓取就要付出实打实的算力成本。GNOME 的 GitLab、WINE、UNESCO 等一批站点已经部署（[The Register 的报道](https://www.theregister.com/2025/07/09/anubis_fighting_the_llm_hordes/)）。它不是终局：据 [Codeberg 报告](https://www.theregister.com/2025/08/15/codeberg_beset_by_ai_bots/)，2025 年 8 月已有爬虫学会了解题，军备竞赛还在继续。

市场围栏。Cloudflare 从 [2025 年 7 月 1 日起](https://blog.cloudflare.com/content-independence-day-no-ai-crawl-without-compensation/)把新接入网站的默认设置改为拦截 AI 爬虫，并推出 pay-per-crawl：想抓，先谈价。抓取从默认许可变成默认拒绝，这是基础设施层面对「默认开放」的一次明确掉头。

制度围栏。维基媒体把「降低爬虫流量」写进了 [2025-2026 年度计划](https://meta.wikimedia.org/wiki/Wikimedia_Foundation_Annual_Plan/2025-2026/Product_&_Technology_OKRs)，目标是请求量降 20%、带宽降 30%；基金会同时[把商业公司引向付费的 Wikimedia Enterprise 接口](https://wikimediafoundation.org/news/2026/07/16/wikimedia-enterprise-protecting-wikipedia-ai/)：数据照样给，走正门，付成本。

三种围栏指向同一个结局。英国的草场公地，大部分正是在 18、19 世纪的[圈地运动](https://www.parliament.uk/about/living-heritage/transformingsociety/towncountry/landscape/overview/enclosingland/)里收的场：草保住了，公地没了。数字公地眼下走的正是这条路，而围栏的代价分配得很不均匀。AI 大厂付得起过路费，Cloudflare 和维基媒体收得到钱；被夹在中间的，是没有议价渠道的小站和志愿者项目，以及不以训练为目的的合法抓取，学术研究、网页存档、无障碍工具。围栏不分来意。

落到可操作的判断上。如果你维护公开的基础设施，「爬虫是对抗性的」应该成为默认假设：给计算上贵的端点（搜索、diff、历史记录）单独限流，把 Anubis 或它的等价物当成和 HTTPS 一样的标配，别指望 robots.txt。如果你在 AI 公司做数据或政策，crawl-to-refer 比值大概率会从博客图表变成谈判桌上的筹码和监管指标，早于同行把它做小是便宜的保险。如果你两者都不是，只是个读者，那你会更早感受到围栏：更多登录墙，更多「请验证你是人类」。

草场没有枯死，它在被围起来。围栏保得住草，保不住「公地」这个词的本义：任何人不问来意、不付费都进得来。开放网络花三十年攒下的语料把这一代 AI 养大；等围栏合拢，下一个想白手起家读遍整个网络的人，无论是学生、研究者还是创业者，会发现那个网络已经不在了。

## 参考来源

- [The tragedy of the commons, AI edition — The Economist](https://www.economist.com/britain/2026/08/06/the-tragedy-of-the-commons-ai-edition) — 选题来源与开篇的仲裁庭案例（付费墙，仅读到公开流传的原句）
- [Hacker News 讨论串](https://news.ycombinator.com/item?id=49235011) — 《经济学人》原文引句及 Ostrom 相关讨论
- [How crawlers impact the operations of the Wikimedia projects — Wikimedia Diff](https://diff.wikimedia.org/2025/04/01/how-crawlers-impact-the-operations-of-the-wikimedia-projects/) — 带宽增长 50%、机器人占 35% 浏览量/65% 高成本流量、「内容免费基础设施不免费」
- [Please stop externalizing your costs directly into my face — Drew DeVault](https://drewdevault.com/blog/Stop-externalizing-your-costs-on-me/) — SourceHut 的时间成本、宕机频率、爬虫伪装手法
- [FOSS infrastructure is under attack by AI companies — LibreNews](https://thelibre.news/foss-infrastructure-is-under-attack-by-ai-companies/) — KDE GitLab 宕机等开源基础设施案例汇总
- [Death by a thousand slops — Daniel Stenberg](https://daniel.haxx.se/blog/2025/07/14/death-by-a-thousand-slops/) — curl 安全报告中 AI 垃圾占比 20%、真实率 5%、每份报告 3–4 人排查
- [Stack Overflow is almost dead — The Pragmatic Engineer (Gergely Orosz)](https://blog.pragmaticengineer.com/stack-overflow-is-almost-dead/) — 提问量跌回 2009 年水平（基于 Stack Exchange Data Explorer）
- [The crawl before the fall… of referrals — Cloudflare Blog](https://blog.cloudflare.com/ai-search-crawl-refer-ratio-on-radar/) — crawl-to-refer 比值定义与 Anthropic 约 70,900:1（2025 年 6 月 19–26 日）
- [Content Independence Day — Cloudflare Blog](https://blog.cloudflare.com/content-independence-day-no-ai-crawl-without-compensation/) — 750 倍/30,000 倍换算、谷歌回流难 10 倍、默认拦截与 pay-per-crawl（2025-07-01）
- [RFC 9309: Robots Exclusion Protocol — IETF](https://www.rfc-editor.org/rfc/rfc9309.html) — robots.txt 的标准化文档，1994 年由 Martijn Koster 提出，明确「不是访问授权机制」
- [The Tragedy of the Commons — Garrett Hardin, Science（1968）](https://www.science.org/doi/10.1126/science.162.3859.1243) — 「对所有人开放的草场」原始模型
- [Elinor Ostrom — Facts, NobelPrize.org](https://www.nobelprize.org/prizes/economic-sciences/2009/ostrom/facts/) — 2009 年诺贝尔经济学奖，公地治理研究
- [Anubis — TecharoHQ (GitHub)](https://github.com/TecharoHQ/anubis) — 工作量证明机制
- [Anubis 发布公告 — Xe Iaso](https://xeiaso.net/blog/2025/anubis/) — 发布日期 2025-01-19 与工作原理
- [Anubis: Fighting off the hordes of LLM bot crawlers — The Register](https://www.theregister.com/2025/07/09/anubis_fighting_the_llm_hordes/) — GNOME/WINE/UNESCO 等部署情况
- [Codeberg beset by AI bots — The Register](https://www.theregister.com/2025/08/15/codeberg_beset_by_ai_bots/) — 爬虫学会解 Anubis 挑战（2025-08）
- [Wikimedia Foundation Annual Plan 2025-2026 Product & Technology OKRs — Meta-Wiki](https://meta.wikimedia.org/wiki/Wikimedia_Foundation_Annual_Plan/2025-2026/Product_&_Technology_OKRs) — WE5.4：爬虫请求量降 20%、带宽降 30%
- [Wikimedia Enterprise: protecting Wikipedia in the age of AI — Wikimedia Foundation](https://wikimediafoundation.org/news/2026/07/16/wikimedia-enterprise-protecting-wikipedia-ai/) — 引导商业公司走付费接口
- [Enclosing the land — UK Parliament](https://www.parliament.uk/about/living-heritage/transformingsociety/towncountry/landscape/overview/enclosingland/) — 18、19 世纪圈地运动背景
