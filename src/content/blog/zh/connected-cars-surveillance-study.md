---
title: "21 辆车逐一抓包：19 辆在向第三方发流量"
description: "东北大学与 Consumer Reports 抓包实测 21 辆车和 30 个车企 App：19 辆车在向第三方发流量，28 个 App 把数据发给广告商，车载 AI 助手正要接入同一条数据链。"
pubDate: 2026-10-01
tags: [privacy, connected-cars, data-brokers]
lang: zh
slug: connected-cars-surveillance-study
translationOf: connected-cars-surveillance-study
---

研究者在 Consumer Reports 位于康涅狄格州的汽车测试场里，通过静态和行驶测试，记录了 21 辆联网汽车经受控 Wi-Fi 网络发出的流量。其中 11 辆电动车还被开进一顶一辆车大小的法拉第帐篷——金属网帐篷，能把无线电信号衰减约 93 dB；车辆连不上蜂窝网络，流量只能走研究者架设的网络。从 2024 年 10 月到 2025 年 8 月，他们一共测了 21 辆车（覆盖特斯拉、凯迪拉克、Rivian、Lucid 等 19 个品牌，2022–2025 年款）和 30 个车企官方 App。

结果：21 辆车里 19 辆在向至少一家第三方发送流量；30 个 App 里 28 个把数据发给了广告或分析公司（[Consumer Reports 调查](https://www.consumerreports.org/electronics/personal-information/your-car-is-sharing-data-with-big-tech-companies-study-finds-a4474820962/)）。这是东北大学隐私研究团队与 Consumer Reports 合作的研究，论文《[Automatic Transmission](https://automatictransmission.khoury.northeastern.edu/)》已被 ACM 互联网测量会议（IMC '26）接收，将于今年 10 月正式发表。Bruce Schneier [转评](https://www.schneier.com/blog/archives/2026/10/connected-cars-are-a-surveillance-platform.html)的就是这项工作。

## 这次不是推测，是抓包

「车联网很可怕」的论调已经很多，这项研究的价值在于它测的是线上的真实流量，而非隐私政策里的书面承诺。车辆流量大多加密，但加密保护的是内容，不保护「发给谁」：研究者靠 DNS 查询和 TLS 握手中明文携带的目标域名，照样识别出了数据去向。

几个具体发现：

- **收数据的名单是熟面孔**：Amazon、Google、Meta、Microsoft、Pinterest、Snap、Yahoo、Reddit。特斯拉 Model 3 一辆车就连接了 34 个广告/追踪域名。
- **30 个 App 里 7 个外发了可识别个人身份的信息**：这几个 App 合计发出了车主邮箱、电话号码、精确位置，以及 VIN——车辆识别码。VIN 唯一标识一辆车，车辆登记、保险记录都以它索引（[NHTSA](https://www.nhtsa.gov/document/vehicle-identification-number-vin)）。研究者指出，这类稳定标识符能让广告公司把车主与来自其他网站和 App 的行为数据、购买记录串联起来（[Northeastern News](https://news.northeastern.edu/2026/09/29/connected-car-privacy-violation-research/)）。
- **手机 App 让暴露面翻倍**：给车配对官方 App 后，车辆接触的广告/追踪实体数量大约翻了一倍。
- **车企自己也未必清楚数据流向**：Honda 在看到研究结果后，才通知其分析供应商 Amplitude 删除所收的位置数据。研究记录到的只是补救这一步；在外部研究者找上门之前，Honda 内部做过怎样的核查，我不知道。

## 数据流向哪里才是重点

广告公司拿到车辆数据只是链条的前半段。后半段有现成判例：FTC 在 2025 年 1 月[对通用汽车采取执法行动](https://www.ftc.gov/news-events/news/press-releases/2025/01/ftc-takes-action-against-general-motors-sharing-drivers-precise-location-driving-behavior-data)，指控 GM 通过 OnStar 的 Smart Driver 功能收集精确位置和驾驶行为数据，卖给消费者信用报告机构（类似征信机构的角色），保险公司再用这些报告定价、拒保。一些车主直到发现数据被用在保险定价上，才知道自己「被参加」了这个项目。这份和解令已于 2026 年 1 月[正式生效](https://www.ftc.gov/news-events/news/press-releases/2026/01/ftc-finalizes-order-settling-allegations-gm-onstar-collected-sold-geolocation-data-without-consumers)，禁止 GM 五年内向信用报告机构披露此类数据。

急刹车、深夜驾驶、超速——这类看起来不值钱的数据，在保险定价市场上有现成的买家。

那拒绝呢？研究记录了一个细节：特斯拉在用户关闭数据共享时警告，这可能导致车辆「功能受限、严重损坏或无法运行」。特斯拉只是措辞最直白的一家；在各家车企那里，选择退出通常都意味着放弃部分功能，这笔代价要由车主自己承担。

## AI 助手落在同一套基础设施上

今年 4 月，GM 宣布将向约 400 万辆符合条件、带 Google 车机的车推送 Google Gemini（[GM 官方公告](https://news.gm.com/home.detail.html/Pages/news/us/en/2026/apr/0428-Google-Gemini.html)），并预告 2026 年晚些时候推出自研助手。关于自研助手用什么数据，公开说法有两处：GM 产品管理总监 Anna Santos 称它结合对话式 AI、「GM 车辆知识和 OnStar 智能」（[GM Authority](https://gmauthority.com/blog/2026/08/gm-proprietary-ai-assistant-launching-this-year/)）；更早的 [TechCrunch 报道](https://techcrunch.com/2025/10/22/gm-is-bringing-google-gemini-powered-ai-assistant-to-cars-in-2026)称其基础模型以车辆规格类数据训练。FTC 案里被卖掉的数据同样经由 OnStar，但这层重合并不能证明自研助手和 Smart Driver 项目共用一条数据管道；至于那类位置和驾驶行为数据会不会进入助手的训练数据，GM 的公开公告没有说，我也没有证据说有，只能存疑观察。

对话式助手还会带来一类此前不存在的数据：你在车里问了什么、说了什么。这些内容会被怎样收集和保留，公告没有说明。这项研究测的是网络流量和 App，没有覆盖语音助手的数据流向——这是测量上的空白，不是安全上的背书。我的判断是：一个连「隐私政策与实际流量对不上」都要靠外部研究者抓包才能发现的行业，没有理由相信它会在 AI 层突然变得克制。

## 车主能做什么

能做的事有限但不是零。部分车企提供关闭或限制数据共享的入口：Toyota 车主可在官方 App 的 Data Privacy Portal 里调整数据授权，Ford 的[隐私说明](https://www.ford.com/help/privacy/)列出了车机设置和恢复出厂（Master Reset）等途径；各家具体怎么操作，Consumer Reports 有一份[逐厂商指南](https://www.consumerreports.org/electronics/personal-information/how-to-stop-your-car-from-collecting-sharing-driving-data-a1233378612/)。在有隐私法的州，居民可以向车企提交限制使用、停止共享或删除数据的请求；[Privacy4Cars](https://privacy4cars.com/) 提供[免费工具](https://www.prweb.com/releases/privacy4cars-releases-new-and-improved-free-methods-for-consumers-to-learn-about-privacy-practices-in-automotive-and-express-privacy-preferences-302408955.html)，能定位各车企的请求入口，还可以作为代理人替你提交这些请求。买二手车时值得记住：前车主的数据和配对关系可能还留在车机里，FTC [专门提醒过](https://consumer.ftc.gov/consumer-alerts/2018/08/selling-your-car-clear-your-personal-data-first)车辆换手前要恢复出厂、解除 App 配对。

但逐个设置解决不了结构问题。这项研究最有用的地方是给出了一个可复用的检验标准：车企说什么不重要，车发出的流量才是事实。接下来值得盯的测量对象，就是车载 AI 助手上线后，下一轮抓包清单里会多出哪些新域名。

## 参考来源

- [Automatic Transmission 项目页（东北大学）](https://automatictransmission.khoury.northeastern.edu/) — 方法论（11 辆电动车进一辆车大小的法拉第帐篷、tcpdump、mitmproxy）、19/21 与 7/30 等核心数字（VIN、邮箱、电话号码、精确位置）、App 配对翻倍发现、IMC '26 发表信息
- [Northeastern News 报道](https://news.northeastern.edu/2026/09/29/connected-car-privacy-violation-research/) — 稳定标识符带来的跨场景追踪、Honda/Amplitude 补救事例
- [Consumer Reports 调查报道](https://www.consumerreports.org/electronics/personal-information/your-car-is-sharing-data-with-big-tech-companies-study-finds-a4474820962/) — 测试规模与时间、第三方公司名单、特斯拉 34 个追踪域名、Honda/Amplitude 事例、特斯拉关闭共享的警告文案
- [Consumer Reports 逐厂商关闭指南](https://www.consumerreports.org/electronics/personal-information/how-to-stop-your-car-from-collecting-sharing-driving-data-a1233378612/) — Toyota Data Privacy Portal 操作路径、各州隐私法下的三类请求
- [Schneier on Security 转评](https://www.schneier.com/blog/archives/2026/10/connected-cars-are-a-surveillance-platform.html) — 选题来源
- [FTC 对 GM 的执法公告（2025 年 1 月）](https://www.ftc.gov/news-events/news/press-releases/2025/01/ftc-takes-action-against-general-motors-sharing-drivers-precise-location-driving-behavior-data) — OnStar Smart Driver 数据卖给信用报告机构的指控细节
- [FTC 最终命令公告（2026 年 1 月）](https://www.ftc.gov/news-events/news/press-releases/2026/01/ftc-finalizes-order-settling-allegations-gm-onstar-collected-sold-geolocation-data-without-consumers) — 和解令生效、五年禁令
- [GM 官方新闻稿：Gemini 推送计划](https://news.gm.com/home.detail.html/Pages/news/us/en/2026/apr/0428-Google-Gemini.html) — 约 400 万辆符合条件车辆、适用品牌
- [GM Authority：GM 自研助手年内推出](https://gmauthority.com/blog/2026/08/gm-proprietary-ai-assistant-launching-this-year/) — Anna Santos 关于结合 GM 车辆知识与 OnStar 智能的说法
- [TechCrunch：GM 自研车载助手计划](https://techcrunch.com/2025/10/22/gm-is-bringing-google-gemini-powered-ai-assistant-to-cars-in-2026) — 基础模型以车辆规格数据训练的预告
