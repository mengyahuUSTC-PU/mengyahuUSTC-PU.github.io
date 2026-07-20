---
title: "管住 AI 修图，靠的不是 AI 检测器"
description: "纽约拟强制房产广告披露 AI 修图。对比加州 AB 723 和欧盟 AI Act 后我的判断是：可执行的机制不是检测 AI，而是让广告方留住原图。"
pubDate: 2026-07-20
tags: [AI治理, 内容披露, 政策]
lang: zh
slug: nyc-ai-listing-disclosure
translationOf: nyc-ai-listing-disclosure
---

7 月 16 日，纽约市长 Zohran Mamdani 发布了一份《租房宰客报告》（Rental Ripoff Report），里面有一条被媒体单独拎出来讲的主张：要求房东和中介在租房广告里用 AI 生成或数字修饰的图片、视频时，做出「清晰醒目」的披露，执行上再与房源平台协调（[官方公告](https://www.nyc.gov/mayors-office/news/2026/07/mayor-mamdani-releases--rental-ripoff-report---outlining-new-act)，[IBTimes 报道](https://www.ibtimes.co.uk/nyc-targets-housefishing-ai-disclosure-rules-1809133)）——注意这还是政策方案，尚未成法。这份报告一共提了 23 项政策，来自五个区 2400 多名纽约人在听证会和线上提交的证词（[The Next Web](https://thenextweb.com/news/mamdani-ai-apartment-listings-streeteasy)）。租房市场已经给这类操作起了名字：housefishing——从 catfishing（交友照骗）衍生来的词，照片里的公寓明亮宽敞，人到了现场发现窗户对着砖墙。

我看到这条新闻的第一反应不是「又一个 AI 监管」，而是一个更具体的问题：这套方案打算怎么执行？租客往往到实地看房、甚至签了约，才发现照片和实物对不上；下决定前看不到实物的人，手里只有照片。纽约的方案听上去顺理成章，但「要求披露」四个字背后，藏着两个不解决就会让规则空转的难题。

## 难题一：什么算「AI 修过」

严格说来，今天几乎没有一张房源照片是「没修过」的。手机拍照本身就在做计算摄影——按一次快门，算法把多张连拍对齐合成，再做一整串后处理才出图（Google 的 [HDR+ 论文](https://research.google/pubs/burst-photography-for-high-dynamic-range-and-low-light-imaging-on-mobile-cameras/)描述的就是这条从连拍 raw 起算的管线）。如果「数字修饰就要披露」按字面执行，那每张照片都得挂标签——而当所有照片都有标签时，标签就等于不存在。在我看来，这是披露类监管最容易踩的坑：触发条件定得太宽，披露就退化成壁纸。

加州管售房广告的 [AB 723](https://leginfo.legislature.ca.gov/faces/billNavClient.xhtml?bill_id=202520260AB723) 今年 1 月 1 日已生效（[CRMLS 行业指引](https://kb.crmls.org/knowledgebase/californias-altered-image-law-ca-ab-723-faqs/)），它在这一点上做了细致的切割：法条明确排除了亮度、锐化、白平衡、裁剪、曝光这类不改变房产真实状况的常规调整，只管「增加、移除或改变图中元素」的编辑——家具、地板、墙面、绿化，包括从房子里能看到的邻居物业。欧盟 [AI Act 第 50 条](https://artificialintelligenceact.eu/article/50/)（8 月 2 日起适用，就在两周后）也留了类似的口子：辅助性的标准编辑、不实质改变内容语义的，免于标注。纽约目前公布的只有「清晰醒目地披露」这个要求本身，边界切在哪里，要等消费者与工人保护局（DCWP）的规则制定——这恰恰是整件事成败所系的部分。

## 难题二：谁能证明照片被 AI 动过

假设边界定清楚了，下一个问题是取证。这里有个容易犯的直觉错误：用 AI 检测器去查图。做过内容安全的人都知道这条路走不通——检测模型对没见过的生成器泛化很差，连专攻泛化的检测研究也把「难以识别未见过生成器的产物」当作公认前提写进问题设定（[GenDet, arXiv:2312.08880](https://arxiv.org/abs/2312.08880)）。在我看来，这样的误报漏报水平当线索尚可，没有其他证据时不宜单独拿来执法；C2PA 这类溯源元数据也指望不上——Tim Bray 的[实测](https://www.tbray.org/ongoing/When/202x/2025/09/18/C2PA-Investigations)发现，社交平台和发布软件在处理图片时几乎都会把元数据剥掉。如果 DCWP 的执行方案建立在「检测出 AI」上，那它建立在沙子上。

AB 723 的聪明之处正在于绕开了检测：它要求披露声明旁边必须附上链接或二维码，指向**未经修饰的原图**。实际效果是把核查的方向调了个头——执法者不用去证明图是 AI 改的，把广告图和公示的原图一对照，改没改、改在哪，一目了然；发现货不对板的人要投诉，证据也是现成的。整个链条里没有 AI 取证技术的位置——法条压根没提检测，核查靠披露声明和原图对照就能闭环。我的判断是：纽约这版规则最终好不好用，就看 DCWP 抄不抄「留原图」这一条。

执法的另一个抓手是平台。DCWP 已经在和 StreetEasy、Zillow 协调（[The Next Web](https://thenextweb.com/news/mamdani-ai-apartment-listings-streeteasy)），这比挨家挨户查房东现实得多：平台可以在上传管线里加一个强制声明字段，把标签固化在图片展示层，而不是只写在说明文字里——图片一旦被转发、被聚合到别的页面，光靠文字说明未必跟得住。有意思的是，Zillow 自己去年 9 月就[上线了 AI 虚拟布置功能](https://www.prnewswire.com/news-releases/zillow-brings-ai-powered-virtual-staging-to-showcase-listings-302550554.html)：买家在 Showcase 房源上可以让 AI 给空房间换七种装修风格。乍看是「裁判下场踢球」，但看它的产品设计——图上有专门图标，滑块可以随时切回原图——这其实就是「披露 + 原图可查」的交互样板。区别只在一个是买家自己开的滤镜，一个是卖家偷偷开的滤镜；监管要管的是后者。

## 水印呢？生成的图有标，AI 改的图才刚开始有

做 responsible AI 的人看到这里，多半会想到另一条路：水印和溯源（provenance）。纯 AI 生成的图，这套基础设施已经初具规模——Google 的 SynthID 把不可见水印直接嵌进像素，解码就能确认图是不是自家模型生成的；中国 2025 年 9 月起施行的[《人工智能生成合成内容标识办法》](https://www.cac.gov.cn/2025-03/14/c_1743654684782215.htm)走得更细，第五条要求隐式标识里写进服务提供者名称或编码、内容编号，解出来不光知道「是 AI」，还知道「谁家的 AI、哪一单生成的」。但房源照骗的主场不是「生成」，是「编辑」：照片是真拍的，只是窗外的砖墙被 AI 抹掉了。编辑也有水印吗？

法规层面，义务其实已经写进去了。欧盟 AI Act 第 50 条的机器可读标记义务，原文写的是「detectable as artificially generated **or manipulated**」——「修改」和「生成」并列，AI 改图落在义务范围内。中国的标识办法把对象定义为「利用人工智能技术生成、合成的」内容，条文没有单独点名「编辑」这个动作，但 AI 改图的产出归入「合成」是自然读法。

厂商实践刚起步。Google 从 2025 年 2 月起给 Magic Editor 里 Reimagine 功能改过的照片嵌 SynthID 水印（[官方公告](https://blog.google/feed/synthid-reimagine-magic-editor/)）——水印从「生成」延伸到了「编辑」。但公告自己就写明了限制：编辑太小——比如改掉背景里一朵小花的颜色——可能小到 SynthID 既标不上也检不出。这几乎是难题一的像素版重演：「多小的改动算改动」，这条线从法条一路划到了水印层。

研究界有个思路干脆把方向调了个头。CVPR 2024 的 EditGuard（[arXiv:2312.08883](https://arxiv.org/abs/2312.08883)）不指望 AI 编辑器主动配合打标，而是事先给原图嵌一层水印，图被改过之后，靠解码出的水印残缺就能定位篡改区域，论文报告的定位精度超过 95%。这和 AB 723 的「留原图」在机制上是同一件事：都是让「改动前的状态」留下可核对的凭据——一个把原图挂在链接里，一个把原图的指纹藏进像素里。

但要把水印当成明天就能用的执法抓手，还差两步。第一步是覆盖：水印义务压在工具方头上，SynthID 只覆盖 Google 自家管线；房东用哪家工具改图，监管方说了不算，不配合打标的工具（比如本地跑的开源模型）出来的图就是干净的。第二步是验证：元数据类的标记（C2PA、标识办法要求写进文件元数据的隐式标识）在分发链条里会被剥掉——Tim Bray 的实测前面说过；像素级水印转存转发倒剥不掉，可解码要靠厂商自己的检测入口，执法闭环绕不开厂商配合。所以我的判断不变：水印是值得铺的长期基础设施，欧盟的标记义务八月起会推着厂商往这个方向走，但 DCWP 的规则等不起这个周期——今天就能闭环的，仍然是「留原图 + 对照」。

## 不只是房源：电商已经先跑了一轮

同样的剧情，中国的电商市场已经演过一遍，而且演得更完整。《法治日报》今年 1 月的[调查](https://www.thepaper.cn/newsDetail_forward_32380169)记录了一串典型投诉：宣传图里绒毛蓬松、眼睛透亮的「软萌兔子挂件」，实物毛发粗糙、眼睛歪斜；预售四个月的暹罗猫毛绒挂件到货后毛发起球、颜色不均，商家干脆承认「宣传图是 AI 生成的」。[央视网记者](https://m.thepaper.cn/newsDetail_forward_32382618)自己下单了一只「敦煌飞天猫」玩具，收到的实物脸和身体像被压扁过，商家的解释是「图片好看是我们摄影师拍照技术好」。上游还有一条现成的供给链：有博主专门向商家兜售 AI 制图工具，299 元包月就能批量生成上百张「实拍级」商品图。[上观新闻今年 5 月的实测](https://www.xhby.net/content/s6a1a3892e4b07fc6ee8bb2d3.html)从各电商平台随机取了 20 张商品图，被鉴定工具判定存在 AI 生成痕迹的超过半数。

值得注意的是，电商这边给出的两条治理路线，恰好对应前面两个难题。淘宝去年 3 月出的 [AI 假图治理规则](https://www3.xinhuanet.com/tech/20250327/cc956c250a264379a7d13552a63c6543/c.html)（据报道是电商平台里第一个），把违规的边界切在**结果**而不是**手段**上：管的是材质款式与实物不符、效果显著失真、违反物理规律的人体这类「货不对板」，不纠结你用没用 AI——这和加州「常规调整豁免、只管改动元素」是同一个思路，而且平台把拦截直接做进了上传管线，据报道上线识别模型后已拦下近 10 万张假图。另一条线是前面提到的《标识办法》：显式标识加隐式标识，义务压在生成方和传播平台头上——主线是在生成那一刻就把标记打进去，方向上和欧盟第 50 条的机器可读标记一致（办法也要求传播平台对缺少标识的内容核验生成痕迹，但那是补位，不是承重墙）。《法治日报》采访的学者还点出了执法的另一半：AI 图未标识又货不对板，若构成欺诈，消费者可依消费者权益保护法主张退一赔三。

这套剧情也不只在中国上演。TikTok Shop 新的 [AI 内容规则](https://seller-us.tiktok.com/university/essay?knowledge_id=491489038501663&lang=en)7 月 13 日刚生效——比纽约的报告还早三天。切法和淘宝几乎一个模子：禁止用 AI 改变商品的尺寸、颜色、功能等外观特征，禁止伪造夸大的使用效果；完全由 AI 生成或经显著编辑的内容必须打标，调色、裁剪、降噪这类常规编辑豁免；处罚阶梯式，从警告、限流到严重造假永久封禁。触发条件切在结果上、常规编辑留口子、执法压给平台——前面拆出来的几块拼图，它一块不少。美国联邦层面的动作落在另一个位置：FTC 的[虚假评论与证言规则](https://www.ftc.gov/news-events/news/press-releases/2024/08/federal-trade-commission-announces-final-rule-banning-fake-reviews-testimonials)（规则文本见 [Federal Register](https://www.federalregister.gov/documents/2024/08/22/2024-18519/trade-regulation-rule-on-the-use-of-consumer-reviews-and-testimonials)）2024 年 10 月生效，AI 生成的假评论明确在禁止之列，违者可处民事罚款——管的是评论区不是商品图，但逻辑同款：盯着「冒充真实消费者」这个欺骗结果，不问你用什么工具造的假。欧盟那边，商品图误导本身早有 2005 年的[《不公平商业行为指令》](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32005L0029)兜底，和纽约手里的《一般商业法》第 349 条是一个道理；针对数字环境的新一轮消费者立法 [Digital Fairness Act](https://www.europarl.europa.eu/legislative-train/theme-protecting-our-democracy-upholding-our-values/file-digital-fairness-act) 还在提案筹备阶段，矛头指向暗模式和误导性网红营销。

不过中国消费者端的实践正在滑回检测那条路：国家反诈中心 App 上线了「AI 内容鉴定」功能，上观那次 20 张图的实测用的就是它和第三方的鉴别工具。检测当线索没问题——提示消费者多留个心眼、给媒体实测找选题——可一旦要当证据，前面说的泛化问题一个都躲不掉。电商纠纷最后能落地，靠的其实是一个房产市场没有的条件：商品会寄到消费者手里，**实物本身就是「原图」**，收货就能对照，退货和索赔都有现成抓手。租房不一样——人要么白跑一趟，要么签了约才发现照片骗人，纠错成本高得多。这正是房产广告更需要「事前留原图」的原因：既然实物不会自己寄上门，就得强制广告方把「实物的替身」公示出来。

## 还缺什么

对比下来，纽约方案有一处比加州更进一步、也更难落地：适用范围。AB 723 管的是持牌经纪人、销售人员和代表他们行事的人，而且只覆盖售房广告（[法案原文](https://leginfo.legislature.ca.gov/faces/billNavClient.xhtml?bill_id=202520260AB723)）——牌照是现成的执法抓手，法案摘要也写明，故意违反《房地产法》构成刑事犯罪。纽约的方案对准的是租房市场，其中不乏房东直租、全程没有经纪人参与的房源（纽约市 DCWP 对 [FARE Act 的说明](https://www.nyc.gov/site/dca/about/FAQ-Broker-Fees.page)就把这类租赁单列一类），没有牌照可吊；把房东纳入义务主体是对的（不然规则会漏掉最容易「照骗」的那部分市场），但对小房东的执法成本和罚则设计，报告目前没有给出答案。已公布的信息里也没有罚款金额——而纽约本来就有禁止欺骗性商业行为的消费者保护法（[纽约州《一般商业法》第 349 条](https://www.nysenate.gov/legislation/laws/GBS/349)），误导性照片本来就可能构成违法。新规则真正的增量在于把「证明欺骗」（按判例确认的三要件，要逐案证明行为面向消费者、存在实质性误导、造成了损害——[Himmelstein v. Matthew Bender](https://www.nycourts.gov/reporter/3dseries/2021/2021_03485.htm)）变成「核对披露」（改了没改、标了没标，按条款打勾），逐案证明的成本有望省下一大块。如果罚则最后定得不痛不痒，这个增量也就兑现不了。

把这三个例子摆在一起——欧盟管到模型提供方（机器可读标记）和部署方（披露义务），加州让售房广告留原图，纽约想借平台把义务压到房东头上——三地各管一段，但拼起来正好是一套可执行的方案：触发条件切干净（欧盟和加州都写了常规编辑豁免）、留证义务压给广告方（加州已明确要求原图可查）、执法卡点放在平台（纽约正在和平台协调，细则未出）。电商的经验从另一头印证了同一套拼法：淘宝和 TikTok Shop 不约而同把违规定义压在「货不对板」的结果上、把拦截做进平台管线，标识办法把标记义务压给生成方。检测在这几套方案里也有位置——淘宝的识别模型、标识办法里平台的痕迹核验——但都摆在辅助拦截的位置上，认定违规靠的始终是标识义务和货不对板，没有哪一套把成败押在「认出 AI」上。这套拼图里最不重要的一块，恰恰是公众直觉里最重要的那件事：识别 AI。对做生成式图像产品的人，这是个实际的信号：与其等检测军备竞赛出结果，不如现在就把「原图保留 + 展示层标注」做进产品管线——加州已经把前者写进法条，纽约的细则会不会跟上，值得盯着。

## 参考来源

- [Mayor Mamdani Releases "Rental Ripoff Report"（纽约市长办公室官方公告）](https://www.nyc.gov/mayors-office/news/2026/07/mayor-mamdani-releases--rental-ripoff-report---outlining-new-act) — 报告发布与披露要求的一手来源
- [Mamdani wants NYC landlords to label the AI in their apartment photos（The Next Web）](https://thenextweb.com/news/mamdani-ai-apartment-listings-streeteasy) — 23 项政策、2400 多名纽约人证词、DCWP 规则制定、尚未成法、平台协调
- [What Is 'Housefishing'?（IBTimes UK）](https://www.ibtimes.co.uk/nyc-targets-housefishing-ai-disclosure-rules-1809133) — housefishing 一词、「清晰醒目」披露措辞、三年分阶段推进
- [Mayor Mamdani Says Landlords Can't Secretly Use AI Images（PetaPixel）](https://petapixel.com/2026/07/16/mayor-mamdani-says-landlords-cant-secretly-use-ai-images-to-advertise-properties/) — 选题来源，公告日期与背景
- [AB-723 Real estate: digitally altered images: disclosure（加州立法机构法案原文）](https://leginfo.legislature.ca.gov/faces/billNavClient.xhtml?bill_id=202520260AB723) — 修图定义、常规编辑豁免、原图链接/二维码要求、适用于持牌经纪人及其代理、仅覆盖售房广告、2025 年 10 月 10 日签署
- [California's Altered Image Law (CA AB 723) FAQs（CRMLS）](https://kb.crmls.org/knowledgebase/californias-altered-image-law-ca-ab-723-faqs/) — 2026 年 1 月 1 日生效
- [EU AI Act Article 50 全文](https://artificialintelligenceact.eu/article/50/) — 提供方机器可读标记与部署方披露义务（标记义务原文覆盖 generated or manipulated，生成与修改都在内）、辅助编辑豁免、2026 年 8 月 2 日起适用
- [New York General Business Law § 349（纽约州参议院法条原文）](https://www.nysenate.gov/legislation/laws/GBS/349) — 禁止商业活动中的欺骗性行为
- [Himmelstein, McConnell, Gribben, Donoghue & Joseph, LLP v. Matthew Bender & Co.（纽约州终审法院判决，2021）](https://www.nycourts.gov/reporter/3dseries/2021/2021_03485.htm) — § 349 诉求三要件：面向消费者的行为、实质性误导、造成损害
- [Fairness in Apartment Rental Expenses (FARE) Act FAQ（纽约市 DCWP）](https://www.nyc.gov/site/dca/about/FAQ-Broker-Fees.page) — 纽约租赁市场中房东直租（无经纪人参与）情形的官方说明
- [有商家用AI图引流卖货，还有人向商家兜售AI工具（法治日报，澎湃转载）](https://www.thepaper.cn/newsDetail_forward_32380169) — 兔子挂件、暹罗猫挂件等投诉案例，AI 制图工具兜售链条与价格，学者关于标识义务与退一赔三的分析，2026 年 1 月 14 日
- [网购"AI照骗"，实物与商品图不符，商家竟称是"摄影技术好"？（央视网）](https://m.thepaper.cn/newsDetail_forward_32382618) — 记者下单实测「敦煌飞天猫」，商家「摄影师拍照技术好」回应，2026 年 1 月 14 日
- [实测：20张商品图，约半数"AI生成"！（上观新闻，新华报业转载）](https://www.xhby.net/content/s6a1a3892e4b07fc6ee8bb2d3.html) — 20 张商品图实测、国家反诈中心 App「AI 内容鉴定」功能、北京市消协与 8 家电商平台签订《促进AI技术规范应用承诺书》，2026 年 5 月 30 日
- [淘宝新规拒绝AI"照骗"，已拦截10万AI假图（新华网报道）](https://www3.xinhuanet.com/tech/20250327/cc956c250a264379a7d13552a63c6543/c.html) — 2025 年 3 月 27 日发布的平台治理规则：以「显著失真、货不对板」界定违规，上线识别模型源头拦截；淘宝官方公告原文未检索到公开页面，事实以新华网报道为据
- [《人工智能生成合成内容标识办法》（国家网信办官方发布页）](https://www.cac.gov.cn/2025-03/14/c_1743654684782215.htm) — 显式/隐式双标识（隐式标识写入文件元数据，含服务提供者名称或编码、内容编号）、生成方与传播平台义务（含平台对缺标识内容的痕迹核验）、2025 年 9 月 1 日施行
- [AI-Generated Content Restrictions and Requirements（TikTok Shop 官方卖家政策）](https://seller-us.tiktok.com/university/essay?knowledge_id=491489038501663&lang=en) — 2026 年 7 月 13 日生效：禁止 AI 改变商品外观、伪造使用效果，完全生成/显著编辑内容须打标，常规编辑豁免，阶梯式处罚
- [Federal Trade Commission Announces Final Rule Banning Fake Reviews and Testimonials（FTC 官方公告）](https://www.ftc.gov/news-events/news/press-releases/2024/08/federal-trade-commission-announces-final-rule-banning-fake-reviews-testimonials) — AI 生成假评论纳入禁止范围、可处民事罚款，2024 年 10 月 21 日生效；规则全文见 [Federal Register](https://www.federalregister.gov/documents/2024/08/22/2024-18519/trade-regulation-rule-on-the-use-of-consumer-reviews-and-testimonials)
- [Directive 2005/29/EC on unfair commercial practices（EUR-Lex 官方文本）](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32005L0029) — 欧盟禁止误导性商业行为的现行框架
- [Digital Fairness Act（欧洲议会立法追踪页）](https://www.europarl.europa.eu/legislative-train/theme-protecting-our-democracy-upholding-our-values/file-digital-fairness-act) — 提案筹备阶段，针对暗模式、误导性网红营销等数字环境消费者保护议题
- [GenDet: Towards Good Generalizations for AI-Generated Image Detection（arXiv:2312.08880）](https://arxiv.org/abs/2312.08880) — 「难以检测未见过生成器的产物」为该领域公认前提（该文以此为问题设定）
- [EditGuard: Versatile Image Watermarking for Tamper Localization and Copyright Protection（arXiv:2312.08883，CVPR 2024）](https://arxiv.org/abs/2312.08883) — 预先给原图嵌水印、事后解码定位篡改区域，论文报告定位精度超过 95%
- [C2PA Investigations（Tim Bray 实测）](https://www.tbray.org/ongoing/When/202x/2025/09/18/C2PA-Investigations) — 社交平台与发布软件普遍剥离图片元数据
- [Google Photos brings SynthID to Reimagine in Magic Editor（Google 官方博客）](https://blog.google/feed/synthid-reimagine-magic-editor/) — 2025 年 2 月起对 Reimagine 编辑的图片嵌入 SynthID 水印；官方注明过小的编辑可能无法标记和检测
- [Burst photography for high dynamic range and low-light imaging on mobile cameras（Google Research）](https://research.google/pubs/burst-photography-for-high-dynamic-range-and-low-light-imaging-on-mobile-cameras/) — 手机计算摄影（HDR+）管线
- [Zillow brings AI-powered Virtual Staging to Showcase listings（Zillow 官方新闻稿）](https://www.prnewswire.com/news-releases/zillow-brings-ai-powered-virtual-staging-to-showcase-listings-302550554.html) — 2025 年 9 月 10 日发布，七种风格、虚拟布置图标、原图滑块对比
