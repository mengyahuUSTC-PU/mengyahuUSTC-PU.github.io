---
title: "造一家假智库，AI 到底出了哪份力？"
description: "OpenAI 封禁了一场伪造以色列智库、炮制「主权指数」的俄罗斯影响力行动。拆开操作链条看：文章靠抄袭，AI 负责的是更值钱的环节。"
pubDate: 2026-08-25
tags: [influence-operations, ai-safety, openai]
lang: zh
slug: fake-think-tank-sovereignty-index
translationOf: fake-think-tank-sovereignty-index
---

一家自称设在以色列的「专家社区」，名叫国际伯克研究所（International Burke Institute，下称 IBI）。它有官网，有挂名专家，有几十篇署名文章，还有一个招牌产品「主权指数」：给各国的「主权程度」打分。打分结果很稳定：俄罗斯体面，法国、德国、美国和欧盟一律难看。

8 月 25 日，OpenAI 披露封禁了运营这场行动的一批 ChatGPT 账号（[官方公告](https://openai.com/index/disrupting-malicious-uses-of-ai-influence-campaign-russia/)，本文细节经 [The Register](https://www.theregister.com/ai-and-ml/2026/08/25/slop-factory-bans-russians-for-using-slop-factory-to-create-slop/5292297)、[The Decoder](https://the-decoder.com/russia-used-chatgpt-to-run-a-covert-influence-campaign-pushing-pro-kremlin-narratives-across-the-west/)、[StartupHub](https://www.startuphub.ai/ai-news/artificial-intelligence/2026/openai-disrupts-russian-influence-ops) 三家报道交叉核实）。账号从俄罗斯经 VPN 连入，绕开 OpenAI 在俄罗斯的服务限制。这家「智库」从上到下都是假的。

## 这场行动具体做了什么

身份层。OpenAI 抽查了 IBI 网站 2025 年 9 月到 2026 年 5 月发布的 36 篇挂名专家文章，其中 34 篇抄自网上其他地方，有的把多年前的旧文安上新作者，政治学者福山（Francis Fukuyama）和语言学家乔姆斯基（Noam Chomsky）都被冒名。The Register 还查出一个细节：一篇移民政策文章的挂名「专家」，真实身份是澳大利亚一位食品科学教授。

内容层。操作者用俄语给 ChatGPT 下指令，让它生成英语和德语的社媒帖子、评论和回复，并明确要求抹掉一切会暴露俄语母语者身份的语言痕迹。

分发层。内容铺到五个平台：Substack（订阅通讯平台）、Telegram、X、Facebook、LinkedIn。一个叫 Lahme Ente（德语「跛脚鸭」）的德语 Telegram 频道专攻德国受众，批乌克兰、批欧盟、批德国联邦政府。另一名操作者用 ChatGPT 给十几个 Telegram 频道批量生成 logo 和头像，频道分别面向德国、美国、法国、波兰和土耳其。

## AI 出力的环节，和想象的不一样

流行的想象是「AI 批量造谣」：模型日夜不停生成假新闻。这场行动里恰恰相反：文章主体靠抄，AI 几乎没参与「写观点」。它被用在三件事上。

抹口音。俄语下指令，产出地道的英语德语，再加一层「隐藏语言痕迹」的指令。跨语言伪装过去要靠母语写手，是影响力行动里实打实的人力成本；现在是一句 prompt。

装门面。机构 logo、频道头像、挂名专家的包装文案。这些东西单看都不值钱，合起来构成「一家正规机构」的视觉可信度。

维持人格。十几个频道、五个平台、多种语言的日常发帖回帖。这种跨平台身份维护过去需要一个班子轮班，现在一两个人就能撑起来。

换句话说，AI 降低的门槛不在内容生产，在权威包装。谣言从来不难写，难的是让它看起来出自一家有专家、有方法论的研究机构。

## 为什么是「指数」

这场行动里最有心思的设计是主权指数。为什么不直接发文章，要做一个指数？

因为数字比文章传播得远。文章要人读完，指数只要一张排名图：可截图，可转发，可以被别的文章当「数据来源」引用，还能年年更新、按国别拆报告，是天然的内容流水线。真实的智库生态里，指数就是权威的硬通货——自由指数、民主指数、清廉指数。假智库抄的正是这个格式。

至于这个指数怎么算的？OpenAI 的说法是，它依据某种「IBI 内部计算」，对反对俄罗斯入侵乌克兰的西方国家一律打低分，各国报告的行文「带着论战腔」。指数在这里的功能，是把立场洗成看起来中立的数据。

## 露馅的地方，和检测的边界

伪装没有做满。行动的德语内容里出现了「Svetofor 联盟」这样的写法：德国上一届执政联盟通称「红绿灯联盟」（Ampelkoalition），svetofor 是俄语「红绿灯」的音译。模型按指令抹掉了语法层面的痕迹，却在专有名词的长尾上露了底。

OpenAI 能抓到这场行动，靠的是一种只有模型服务商才有的可见性：它看得见提示词。操作者用什么语言下指令、要求隐藏什么、同一批账号在批量生成什么，这些信号在发出来的内容上完全看不到，只存在于模型这一层。

但这套检测思路的边界也很清楚。第一，它只对托管模型有效。操作者换用开放权重模型（权重文件公开、可下载到自己服务器上运行的模型，如 Llama、DeepSeek 系列），模型层的可见性就归零，检测压力全部回到分发平台。第二，封号不等于拆掉行动。OpenAI 能处置的只有自家账号；IBI 的网站、Telegram 频道、社媒账号都在别人的地盘上，OpenAI 能做的是公开线索，等其他平台和研究者接手。

## 该担心什么，不该担心什么

OpenAI 用 Breakout Scale 给这场行动定级。这是布鲁金斯学会研究员 Ben Nimmo 2020 年提出的六级量表（[原文](https://www.brookings.edu/wp-content/uploads/2020/09/Nimmo_influence_operations_PDF.pdf)），衡量影响力行动的破圈程度：一级是困在单一平台的单一社群里，四级是被主流媒体放大，六级是引发政策后果或出现暴力号召。IBI 被放在第三级的低端：铺开了多个平台、触及多个社群，但典型帖子浏览量很低，官方账号订阅者寥寥。

这符合 OpenAI 两年多来历次披露的共同模式：AI 让行动更便宜，没有让它更有效。从 2024 年在 Telegram 批量刷评论、目标覆盖乌克兰和美国的 Bad Grammar（[Time 报道](https://time.com/6983903/openai-foreign-influence-campaigns-artificial-intelligence/)），到 2025 年针对德国联邦选举的 Helgoland Bite（[OpenAI 2025 年 6 月报告](https://cdn.openai.com/threat-intelligence-reports/5f73af09-a3a3-4a55-992e-069237681620/disrupting-malicious-uses-of-ai-june-2025.pdf)），再到这次，瓶颈始终在分发，不在内容。粉丝还是要一个一个骗，注意力还是要一点一点买。

但这次有一处实质升级：以前是喷子农场，这次搭的是可复用的基础设施。假智库和指数做好之后，边际成本极低，可以一年一年发下去；而它只需要被一家正规媒体或一个有影响力的账号不加核实地引用一次，就能从第三级跳到第四级。它现在的流量不值得担心，值得担心的是那一次引用发生的概率。

给做防御和做平台的人两个具体判断。一，内容层的 AI 检测器在这类行动面前基本无效：IBI 的文章是抄的，不是生成的，检测器给不出信号。有效的信号在身份层和行为层，比如挂名专家查无此人或身份对不上、机构没有可追溯的注册和资助信息、跨平台账号呈现同步的行为聚类。二，模型层的检测红利是真实的，但它依赖操作者继续使用托管模型；这个前提正随开放权重模型的能力提升而变弱，不能当作长期防线来规划。

这场行动里，AI 没有让谣言更有说服力，而是让一个没有专家、没有研究能力的团队，以极低的成本穿上了权威的外衣。这次缝线还露在外面：抄来的文章、对不上的专家、没翻译干净的「Svetofor 联盟」。下一个班子会缝得更仔细。核实一家「智库」是否真的存在，正在从记者的基本功，变成每个转发者的基本功。

## 参考来源

- [Disrupting a new covert influence campaign from Russia — OpenAI](https://openai.com/index/disrupting-malicious-uses-of-ai-influence-campaign-russia/) — 事件一手披露；全部行动细节的原始出处
- [The Register 报道](https://www.theregister.com/ai-and-ml/2026/08/25/slop-factory-bans-russians-for-using-slop-factory-to-create-slop/5292297) — 36 篇抽查 34 篇抄袭、误署名细节（含食品科学教授）、「Svetofor 联盟」、指数「内部计算」及「论战腔」措辞、低触达数据
- [The Decoder 报道](https://the-decoder.com/russia-used-chatgpt-to-run-a-covert-influence-campaign-pushing-pro-kremlin-narratives-across-the-west/) — VPN 接入、五个平台清单、Lahme Ente 频道、十几个国别频道、与既往俄罗斯行动的对比
- [StartupHub.ai 报道](https://www.startuphub.ai/ai-news/artificial-intelligence/2026/openai-disrupts-russian-influence-ops) — 俄语提示词与隐藏语言痕迹指令、logo/头像生成、Breakout Scale 第三级低端评级
- [The Breakout Scale — Ben Nimmo, Brookings](https://www.brookings.edu/wp-content/uploads/2020/09/Nimmo_influence_operations_PDF.pdf) — 六级量表的定义
- [Disrupting malicious uses of AI: June 2025 — OpenAI](https://cdn.openai.com/threat-intelligence-reports/5f73af09-a3a3-4a55-992e-069237681620/disrupting-malicious-uses-of-ai-june-2025.pdf) — Helgoland Bite 行动背景
- [Time 报道（2024 年 5 月）](https://time.com/6983903/openai-foreign-influence-campaigns-artificial-intelligence/) — Bad Grammar 行动背景
