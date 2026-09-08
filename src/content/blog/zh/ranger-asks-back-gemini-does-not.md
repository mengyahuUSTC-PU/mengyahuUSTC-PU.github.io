---
title: "护林员会反问你，Gemini 不会"
description: "三名徒步者按 Gemini 的规划爬 Mount Shasta，8 小时的登顶计划变成两天一夜的救援。拆一拆模型为什么在最需要保守估计的场景里给出乐观答案，以及普通人还能不能用 AI 做行程规划。"
pubDate: 2026-09-05
tags: [ai-safety, consumer-ai]
lang: zh
slug: ranger-asks-back-gemini-does-not
translationOf: ranger-asks-back-gemini-does-not
---

8 月 29 日周六，三个来自加州 Roseville 的年轻人在 Mount Shasta（沙斯塔山，[据 USGS 海拔 14,162 英尺](https://www.usgs.gov/volcanoes/mount-shasta/science/geology-and-history-mount-shasta)，约 4,300 米）8,400 英尺处扎了营。周日凌晨 3 点，他们背着轻便小包出发冲顶。按计划，登顶来回 8 小时。

实际情况是：晚上 7 点才登顶，比这座山约定俗成的正午折返线晚了 7 个小时。摸黑下撤一小时后迷路，打电话给县警局问路，随后偏出 Clear Creek 路线、误入 Mud Creek 峡谷，一人膝盖受伤，露天熬过一夜。周一早晨，林务局的登山护林员和搜救志愿者把他们带了下来（时间线综合自 [CBS Sacramento](https://www.cbsnews.com/sacramento/news/mount-shasta-hikers-rescued-california-ai-incorrect-instructions/) 与 [KRCR](https://krcrtv.com/news/local/sheriff-discusses-mount-shasta-rescue-after-hikers-relied-on-ai-to-plan-trip) 的报道）。

获救后，三人告诉现场警员：路线怎么走、装备带什么，他们主要问的 Gemini。Siskiyou 县警长办公室[在 Facebook 声明里](https://www.facebook.com/SiskiyouCountySheriff/posts/pfbid02D23TtBRnd8FKorvr4DXKQt57zFRJu6GQGEf5uKS9RXt9pvnEp5QJD4jBdNYwGXLKl)把这称为「关键性失误」（critical misstep）：Gemini 建议携带的食物和水「远少于这组人的实际所需」，尤其当计划中 8 小时的攀登变成多日困局之后。截至 [ABC News 发稿](https://abcnews.com/US/3-hikers-ai-plan-trip-rescued-after-becoming/story?id=136176177)，Google 没有回应置评请求。

我在[本周六的快讯](/zh/briefing-2026-09-05)里收录了这条新闻。这里想把它拆开：错的不是某个事实，而是整个估计的方向。

## 诊断：8 小时错得有多离谱

Mount Shasta 官方雪崩中心（由 USFS Shasta-Trinity 国家森林与国家气象局合作运营）对 Clear Creek 路线的[描述](https://www.shastaavalanche.org/general-route-description/clear-creek)是：体力很强的人可以一天往返，「大多数人应该按两到三天规划」。晚季的路况是松散的火山灰和碎石，8,600 英尺营地附近有泉水，再往上补水就没有着落了。

也就是说，这三位新手（[ABC News](https://abcnews.com/US/3-hikers-ai-plan-trip-rescued-after-becoming/story?id=136176177) 的说法是 novice）拿到的计划，对应的是官方描述里最强壮那一档人的用时。计划错了，挂在计划上的一切跟着错：食物和水按 8 小时备，白昼按 8 小时算，折返时间形同虚设。警长办公室声明里那句「尤其当 8 小时变成多日」点得很准——补给量本身也许配得上那个 8 小时的问题，配不上的是真实的山。

这不是孤例。加拿大 BC 省的 Lions Bay 搜救队今年也[公开警告过](https://thenarwhal.ca/bc-hiking-avoid-google-maps/)：7 月他们救的一组人，用 Google Maps 规划 Howe Sound Crest Trail，应用给出的步行时间是 5 小时 13 分，实际需要 8 到 14 小时——那条路线有 1,300 米以上的爬升和需要手脚并用的攀爬段。Google 对此的回应是，Maps 的步行导航按街道的标准步速设计，建议登山者用专门的登山地图。搜救经理 Maria Masiar 对 AI 规划工具的评价更直接：「它给出虚假的信息、虚假的方向，它从来历不明的地方抽数据。」

## 机制：为什么模型在最需要保守的地方最乐观

先说清一个边界：三人具体问了 Gemini 什么、Gemini 原话答了什么，都没有公开，我没能验证。「建议少带食物和水」是当事人向警方的转述。但无论他们的 prompt 写得好不好，都指向同一组结构性问题。

**第一，模型的反问不是关卡。** 你可能会说：我用 AI 的时候，它明明会追问。确实会——现在的 Gemini、ChatGPT 遇到规划类问题，常常先问几句日期、人数、目的地。但标题说护林员会反问、Gemini 不会，准确的说法是：护林站的反问是流程，模型的反问是概率。你打电话给护林站，对方先问你们几个人、爬过什么山、哪天出发，问不清楚，建议不往下给；这套问题本身就是安全机制的一部分，它逼你面对自己没想过的变量。模型这边，问不问取决于你的措辞和模型的具体表现：你直接问「Clear Creek 来回几小时、要带多少水」，它多半跳过追问直接报数字；就算它问了、你含糊带过，它也照样作答，不会因为关键信息缺失而扣住答案。[8 月初我写过 MIT Sloan 那篇 AI 理财建议研究](/zh/ai-financial-advice-right-questions)，测的正是这一点：模型只按你给的信息作答，信息缺了，它给的是通用模板。而这次最要命的几个变量——当天的山况（晚季碎石还是残雪）、这组人的体能、以及海拔适应——恰恰是新手自己想不到要说的。人体适应高海拔低氧环境需要好几天，头天睡在 8,400 英尺、第二天直接冲上 14,000 英尺的新手，速度会比任何攻略数字慢得多，这正是 8 小时变 16 小时的最可能路径。这些信息用户不主动给，模型不坚持要，答案照样产出。

**第二，网上的用时数字来自不能代表你的人。** 会把登山用时写上网的，多半是常爬山、爬得快的人；攻略和游记里的「一天往返」，默认读者也是这类人。模型从这些文本里学来数字，但它不知道提问的你属于哪一档。Gemini 当时怎么得出 8 小时的，无法回放；可查的是它的原料长什么样——官方描述里「强者一天、多数人两三天」的分布，压缩成一个数字时，留下来的往往是前者。Google Maps 那个 5 小时 13 分是同一族错误的更纯粹版本：一个按平地步速算路的引擎，根本不知道山是什么。

这种「不知道你是谁」，我自己今年也撞上过一次，只是代价小得多。5 月底到 6 月初我去阿拉斯加玩了一周：出发前一周才定下来，行程直接让 ChatGPT 排了开车、不开车两个版本，我看着合适，两小时内敲定不开车那版，跟同伴接着订机票、酒店、火车。订完才发现，它推荐的住宿多是 Lodge 一类，对我这种习惯订快捷酒店的年轻人来说价格偏高；懒得再改行程，照单订了。到了当地，一路遇到的八成是退休的老爷爷老奶奶，几乎看不到年轻人，顶多是大人带着很小的孩子的家庭。写这篇文章时我查了查公开数据，这大体是季节和目的地本身的属性：阿拉斯加的游客整体偏年长，[州访客统计项目 2011 年夏季报告里的平均年龄是 50.7 岁](https://www.frontiersman.com/state-releases-2011-summer-visitor-numbers/)，[Anchorage 的这个数字到 2016 年涨到 54 岁](https://www.anchorage.net/articles/post/anchorage-visitor-snapshot/)；而 5 月底 6 月初学校还没放假，[带孩子的家庭很少在这个时段出行](https://www.alaska.org/advice/best-time-to-cruise-alaska)，留下的自然多是退休游客。所以满眼银发不能算 ChatGPT 的错，但住宿那个错配仍然成立：模型给出的默认方案对应的是某一档典型用户，在阿拉斯加这条线上就是有 Lodge 预算的年长游客，未必是提问的你。我的错配停在酒店账单上，Shasta 这三个人的错配，走进了两天一夜的救援里。

**第三，也是最关键的：安全规划要的不是准确估计，是带边际的估计。** 多背两升水的代价是包重一点；少带两升的代价可能是命。损失两头不对称的时候，正确的做法是按坏情况备——护林站的建议听起来总是啰嗦保守，因为搜救队见过每一次失败，这次警长办公室发声明提醒公众，本身就是那个反馈回路在运转。模型没有这个回路。它输出一个居中的、自信的答案，不会自动加安全边际，除非你明确要求。在订餐厅、排行程这类低风险场景，居中的答案叫好用；在雪山上，同一种行为叫危险。

## 怎么用：把反问的活儿接过来

警长 Jeremiah LaRue [对本地电视台说](https://krcrtv.com/news/local/sheriff-discusses-mount-shasta-rescue-after-hikers-relied-on-ai-to-plan-trip)的版本比声明温和：AI 可以当研究工具，但把自己放进可能生死攸关的场景之前，要从专业的人那里拿到全部信息。我同意这个分界，再补四条具体的：

1. **变量自己喂全。** 日期、路线、团队人数、每个人的经验和体能、有没有高海拔经历、日出日落时间。模型可能问、可能不问，你不能赌它替你问全——这和理财那篇的结论是同一条。
2. **强制要坏情况。** 问「假设我们比攻略慢一倍，补给怎么变」「列出你这个估计做了哪些假设」。模型答得出假设清单，只是默认不给。
3. **硬规则不从对话里来。** 正午折返这类规则是历次事故换来的，它的存在就是为了在你状态最差、最想赌一把的时刻替你做决定。任何聊天输出都不该覆盖它。
4. **数字找权威源头对一遍。** 用时、水源、路况，打给护林站或查管理方页面。AI 的输出当草稿用，草稿的作用是让你带着问题去打那个电话，而不是替你省掉它。

最后一个判断。这次事故和 AI 理财建议的失败是同一个签名：关键信息不全，模型不坚持问全就作答，损失不对称，输出却照样自信。理财场景里这个组合造成的是慢性损失，雪山上是急性的。认出这个签名，比记住「别用 AI 规划徒步」有用——下一次它出现的地方，多半不在山上。

## 参考来源

- [Siskiyou County Sheriff's Office Facebook 声明](https://www.facebook.com/SiskiyouCountySheriff/posts/pfbid02D23TtBRnd8FKorvr4DXKQt57zFRJu6GQGEf5uKS9RXt9pvnEp5QJD4jBdNYwGXLKl) — 事件一手披露：折返时间、「critical misstep」、Gemini 补给建议、给公众的建议
- [CBS Sacramento 报道](https://www.cbsnews.com/sacramento/news/mount-shasta-hikers-rescued-california-ai-incorrect-instructions/) — 完整时间线：周六扎营 8,400 英尺、凌晨 3 点出发、膝伤、露营过夜、周一获救
- [ABC News 报道](https://abcnews.com/US/3-hikers-ai-plan-trip-rescued-after-becoming/story?id=136176177) — 三人为 Roseville 新手；Google 未回应置评
- [KRCR 对警长 LaRue 的采访](https://krcrtv.com/news/local/sheriff-discusses-mount-shasta-rescue-after-hikers-relied-on-ai-to-plan-trip) — 「AI 可以当研究工具」引语；8 月 31 日周一救援
- [TechCrunch 报道](https://techcrunch.com/2026/09/05/hikers-rescued-after-using-google-gemini-for-planning/) — 选题来源，事件概述
- [Mount Shasta Avalanche Center：Clear Creek 路线描述](https://www.shastaavalanche.org/general-route-description/clear-creek) — 「强者一天、多数人两到三天」、晚季碎石路况、8,600 英尺泉水；USFS 与 NWS 合作运营
- [USGS：Mount Shasta 地质页](https://www.usgs.gov/volcanoes/mount-shasta/science/geology-and-history-mount-shasta) — 海拔 14,162 英尺
- [The Narwhal：BC 省徒步别用 Google Maps](https://thenarwhal.ca/bc-hiking-avoid-google-maps/) — Lions Bay SAR 案例（5 小时 13 分 vs 实际 8–14 小时）、Masiar 引语、Google 回应
- [Frontiersman：州政府发布 2011 年夏季访客数据](https://www.frontiersman.com/state-releases-2011-summer-visitor-numbers/) — 阿拉斯加访客统计项目（AVSP）2011 年夏季平均年龄 50.7 岁
- [Visit Anchorage：访客画像快照](https://www.anchorage.net/articles/post/anchorage-visitor-snapshot/) — Anchorage 访客平均年龄 2016 年达 54 岁
- [ALASKA.ORG：什么时候去阿拉斯加坐邮轮](https://www.alaska.org/advice/best-time-to-cruise-alaska) — 5 月、9 月家庭游客少，原因是学校日历
- [我此前的文章：AI 理财建议赢了谁](/zh/ai-financial-advice-right-questions) — 「模型不追问、按给定 context 作答」机制的前一个案例
