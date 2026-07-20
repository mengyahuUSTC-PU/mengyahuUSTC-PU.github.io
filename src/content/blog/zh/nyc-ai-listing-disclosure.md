---
title: "管住 AI 修图，靠的不是 AI 检测器"
description: "纽约拟强制房产广告披露 AI 修图。对比加州 AB 723 和欧盟 AI Act 后我的判断是：可执行的机制不是检测 AI，而是让广告方留住原图。"
pubDate: 2026-07-20
tags: [AI治理, 内容披露, 政策]
lang: zh
slug: nyc-ai-listing-disclosure
translationOf: nyc-ai-listing-disclosure
---

7 月 16 日，纽约市长 Zohran Mamdani 发布了一份《租房宰客报告》（Rental Ripoff Report），里面有一条被媒体单独拎出来讲的主张：要求房东、中介和房源网站在租房广告里用 AI 生成或数字修饰的图片、视频时，做出「清晰醒目」的披露（[官方公告](https://www.nyc.gov/mayors-office/news/2026/07/mayor-mamdani-releases--rental-ripoff-report---outlining-new-act)，[IBTimes 报道](https://www.ibtimes.co.uk/nyc-targets-housefishing-ai-disclosure-rules-1809133)）——注意这还是政策方案，尚未成法。这份报告一共提了 23 项政策，来自五个区 2400 多名纽约人在听证会和线上提交的证词（[The Next Web](https://thenextweb.com/news/mamdani-ai-apartment-listings-streeteasy)）。租房市场已经给这类操作起了名字：housefishing——从 catfishing（交友照骗）衍生来的词，照片里的公寓明亮宽敞，人到了现场发现窗户对着砖墙。

我看到这条新闻的第一反应不是「又一个 AI 监管」，而是一个更具体的问题：这套方案打算怎么执行？误导性照片最坑的是没法提前实地看房的人，等人到了现场，才发现照片和实物对不上。纽约的方案听上去顺理成章，但「要求披露」四个字背后，藏着两个不解决就会让规则空转的难题。

## 难题一：什么算「AI 修过」

严格说来，今天几乎没有一张房源照片是「没修过」的。手机拍照本身就在做计算摄影——HDR 多帧合成、白平衡、畸变矫正，全是算法在动像素（Google 的 [HDR+ 论文](https://research.google/pubs/burst-photography-for-high-dynamic-range-and-low-light-imaging-on-mobile-cameras/)描述的就是这条管线）。如果「数字修饰就要披露」按字面执行，那每张照片都得挂标签——而当所有照片都有标签时，标签就等于不存在。这是披露类监管的老病：触发条件定得太宽，披露会退化成壁纸。

加州管售房广告的 [AB 723](https://leginfo.legislature.ca.gov/faces/billNavClient.xhtml?bill_id=202520260AB723) 今年 1 月 1 日已生效（[CRMLS 行业指引](https://kb.crmls.org/knowledgebase/californias-altered-image-law-ca-ab-723-faqs/)），它在这一点上做了细致的切割：法条明确排除了亮度、锐化、白平衡、裁剪、曝光这类不改变房产真实状况的常规调整，只管「增加、移除或改变图中元素」的编辑——家具、地板、墙面、绿化，包括从房子里能看到的邻居物业。欧盟 [AI Act 第 50 条](https://artificialintelligenceact.eu/article/50/)（8 月 2 日起适用，就在两周后）也留了类似的口子：辅助性的标准编辑、不实质改变内容语义的，免于标注。纽约目前公布的只有「清晰醒目地披露」这个要求本身，边界切在哪里，要等消费者与工人保护局（DCWP）的规则制定——这恰恰是整件事成败所系的部分。

## 难题二：谁能证明照片被 AI 动过

假设边界定清楚了，下一个问题是取证。这里有个容易犯的直觉错误：用 AI 检测器去查图。做过内容安全的人都知道这条路走不通——检测模型对没见过的生成器泛化很差（[GenDet, arXiv:2312.08880](https://arxiv.org/abs/2312.08880)），这样的误报漏报水平，很难单独撑起执法证据；C2PA 这类溯源元数据也指望不上——Tim Bray 的[实测](https://www.tbray.org/ongoing/When/202x/2025/09/18/C2PA-Investigations)发现，社交平台和发布软件在处理图片时几乎都会把元数据剥掉。如果 DCWP 的执行方案建立在「检测出 AI」上，那它建立在沙子上。

AB 723 的聪明之处正在于绕开了检测：它要求披露声明旁边必须附上链接或二维码，指向**未经修饰的原图**。实际效果是把核查的方向调了个头——执法者不用去证明图是 AI 改的，把广告图和公示的原图一对照，改没改、改在哪，一目了然；发现货不对板的人要投诉，证据也是现成的。整个链条不依赖任何 AI 取证技术。我的判断是：纽约这版规则最终好不好用，就看 DCWP 抄不抄「留原图」这一条。

执法的另一个抓手是平台。DCWP 已经在和 StreetEasy、Zillow 协调（[The Next Web](https://thenextweb.com/news/mamdani-ai-apartment-listings-streeteasy)），这比挨家挨户查房东现实得多：平台可以在上传管线里加一个强制声明字段，把标签固化在图片展示层，而不是只写在说明文字里——图片一旦被转发、被聚合到别的页面，光靠文字说明未必跟得住。有意思的是，Zillow 自己去年 9 月就[上线了 AI 虚拟布置功能](https://www.prnewswire.com/news-releases/zillow-brings-ai-powered-virtual-staging-to-showcase-listings-302550554.html)：买家在 Showcase 房源上可以让 AI 给空房间换七种装修风格。乍看是「裁判下场踢球」，但看它的产品设计——图上有专门图标，滑块可以随时切回原图——这其实就是「披露 + 原图可查」的交互样板。区别只在一个是买家自己开的滤镜，一个是卖家偷偷开的滤镜；监管要管的是后者。

## 还缺什么

对比下来，纽约方案有一处比加州更进一步、也更难落地：适用范围。AB 723 管的是持牌经纪人、销售人员和代表他们行事的人，而且只覆盖售房广告（[法案原文](https://leginfo.legislature.ca.gov/faces/billNavClient.xhtml?bill_id=202520260AB723)）——牌照是现成的执法抓手，法案摘要也写明，故意违反《房地产法》构成刑事犯罪。纽约的方案对准的是租房市场，其中不乏房东直租的房源，没有牌照可吊；把房东纳入义务主体是对的（不然规则会漏掉最容易「照骗」的那部分市场），但对小房东的执法成本和罚则设计，报告目前没有给出答案。已公布的信息里也没有罚款金额——而纽约本来就有禁止欺骗性商业行为的消费者保护法（[纽约州《一般商业法》第 349 条](https://www.nysenate.gov/legislation/laws/GBS/349)），误导性照片本来就可能构成违法。新规则真正的增量在于把「证明欺骗」（要证明误导是实质性的、逐案来）变成「核对披露」（改了没改、标了没标，按条款打勾），逐案证明的成本有望省下一大块。如果罚则最后定得不痛不痒，这个增量也就兑现不了。

把这三个例子摆在一起——欧盟管到模型提供方（机器可读标记）和部署方（披露义务），加州让售房广告留原图，纽约想借平台把义务压到房东头上——三地各管一段，但拼起来正好是一套可执行的方案：触发条件切干净（欧盟和加州都写了常规编辑豁免）、留证义务压给广告方（目前只有加州明确要求原图可查）、执法卡点放在平台（纽约正在和平台协调，细则未出）。这套拼图里最不重要的一块，恰恰是公众直觉里最重要的那件事：识别 AI。对做生成式图像产品的人，这是个实际的信号：与其等检测军备竞赛出结果，不如现在就把「原图保留 + 展示层标注」做进产品管线——加州已经把前者写进法条，纽约的细则会不会跟上，值得盯着。

## 参考来源

- [Mayor Mamdani Releases "Rental Ripoff Report"（纽约市长办公室官方公告）](https://www.nyc.gov/mayors-office/news/2026/07/mayor-mamdani-releases--rental-ripoff-report---outlining-new-act) — 报告发布与披露要求的一手来源（页面对自动抓取返回 403，内容经下列多家媒体交叉核实）
- [Mamdani wants NYC landlords to label the AI in their apartment photos（The Next Web）](https://thenextweb.com/news/mamdani-ai-apartment-listings-streeteasy) — 23 项政策、2400 多名纽约人证词、DCWP 规则制定、尚未成法、平台协调
- [What Is 'Housefishing'?（IBTimes UK）](https://www.ibtimes.co.uk/nyc-targets-housefishing-ai-disclosure-rules-1809133) — housefishing 一词、「清晰醒目」披露措辞、三年分阶段推进
- [Mayor Mamdani Says Landlords Can't Secretly Use AI Images（PetaPixel）](https://petapixel.com/2026/07/16/mayor-mamdani-says-landlords-cant-secretly-use-ai-images-to-advertise-properties/) — 选题来源，公告日期与背景
- [AB-723 Real estate: digitally altered images: disclosure（加州立法机构法案原文）](https://leginfo.legislature.ca.gov/faces/billNavClient.xhtml?bill_id=202520260AB723) — 修图定义、常规编辑豁免、原图链接/二维码要求、适用于持牌经纪人及其代理、仅覆盖售房广告、2025 年 10 月 10 日签署
- [California's Altered Image Law (CA AB 723) FAQs（CRMLS）](https://kb.crmls.org/knowledgebase/californias-altered-image-law-ca-ab-723-faqs/) — 2026 年 1 月 1 日生效
- [EU AI Act Article 50 全文](https://artificialintelligenceact.eu/article/50/) — 提供方机器可读标记与部署方披露义务、辅助编辑豁免、2026 年 8 月 2 日起适用
- [New York General Business Law § 349（纽约州参议院法条原文）](https://www.nysenate.gov/legislation/laws/GBS/349) — 禁止商业活动中的欺骗性行为
- [GenDet: Towards Good Generalizations for AI-Generated Image Detection（arXiv:2312.08880）](https://arxiv.org/abs/2312.08880) — 检测器对未见过的生成器泛化差
- [C2PA Investigations（Tim Bray 实测）](https://www.tbray.org/ongoing/When/202x/2025/09/18/C2PA-Investigations) — 社交平台与发布软件普遍剥离图片元数据
- [Burst photography for high dynamic range and low-light imaging on mobile cameras（Google Research）](https://research.google/pubs/burst-photography-for-high-dynamic-range-and-low-light-imaging-on-mobile-cameras/) — 手机计算摄影（HDR+）管线
- [Zillow brings AI-powered Virtual Staging to Showcase listings（Zillow 官方新闻稿）](https://www.prnewswire.com/news-releases/zillow-brings-ai-powered-virtual-staging-to-showcase-listings-302550554.html) — 2025 年 9 月 10 日发布，七种风格、虚拟布置图标、原图滑块对比
