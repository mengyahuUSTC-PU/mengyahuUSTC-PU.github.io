---
title: "隐私政策是一份文件，你的车发出的流量是另一份"
description: "东北大学与 Consumer Reports 把 21 辆车开进法拉第帐篷抓包：19 辆在向第三方发数据，车载 AI 助手正要接入同一条数据链。"
pubDate: 2026-10-01
tags: [privacy, connected-cars, data-brokers]
lang: zh
slug: connected-cars-surveillance-study
translationOf: connected-cars-surveillance-study
---

研究者在 Consumer Reports 位于康涅狄格州的汽车测试场里搭了一顶法拉第帐篷——一种能屏蔽所有无线电信号的金属网帐篷，把特斯拉、凯迪拉克、Rivian、Lucid 等品牌的电动车一辆辆开进去，再记录车辆试图与外界建立的每一次网络连接。从 2024 年 10 月到 2025 年 8 月，他们一共测了 21 辆车（覆盖 19 个品牌，2022–2025 年款）和 30 个车企官方 App。

结果：21 辆车里 19 辆在向至少一家第三方公司发送数据；30 个 App 里 28 个把数据发给了广告或分析公司（[Consumer Reports 调查](https://www.consumerreports.org/electronics/personal-information/your-car-is-sharing-data-with-big-tech-companies-study-finds-a4474820962/)）。这是东北大学隐私研究团队与 Consumer Reports 合作的研究，论文《[Automatic Transmission](https://automatictransmission.khoury.northeastern.edu/)》发表在今年 10 月的 ACM 互联网测量会议（IMC '26）上。Bruce Schneier [转评](https://www.schneier.com/blog/archives/2026/10/connected-cars-are-a-surveillance-platform.html)的就是这项工作。

## 这次不是推测，是抓包

「车联网很可怕」的论调已经很多，这项研究的价值在于它测的是线上的真实流量，而非隐私政策里的书面承诺。车辆流量大多加密，但加密保护的是内容，不保护「发给谁」：研究者靠 DNS 查询和 TLS 握手中明文携带的目标域名，照样识别出了数据去向。

几个具体发现：

- **收数据的名单是熟面孔**：Amazon、Google、Meta、Microsoft、Pinterest、Snap、Yahoo、Reddit。特斯拉 Model 3 一辆车就连接了 34 个广告/追踪域名。
- **30 个 App 里 7 个外发了可识别个人身份的信息**：车主姓名、邮箱、精确位置，以及 VIN——车辆识别码。VIN 相当于车的身份证号，与注册、保险、维修记录绑定；拿到 VIN 加精确位置，等于拿到一个可以跨数据库串联的持久身份标识。
- **手机 App 让暴露面翻倍**：给车配对官方 App 后，车辆接触的广告/追踪实体数量大约翻了一倍。
- **车企自己也未必清楚数据流向**：Honda 在看到研究结果后，才通知其分析供应商 Amplitude 删除所收的位置数据。事后补救本身说明，隐私政策与实际数据流之间的缺口，车企内部也没有人逐条核对过。

## 数据流向哪里才是重点

广告公司拿到车辆数据只是链条的前半段。后半段有现成判例：FTC 在 2025 年 1 月[对通用汽车采取执法行动](https://www.ftc.gov/news-events/news/press-releases/2025/01/ftc-takes-action-against-general-motors-sharing-drivers-precise-location-driving-behavior-data)，指控 GM 通过 OnStar 的 Smart Driver 功能收集精确位置和驾驶行为数据，卖给消费者信用报告机构（类似征信机构的角色），保险公司再用这些报告定价、拒保。很多车主直到保费上涨才知道自己「被参加」了这个项目。和解令禁止 GM 在五年内向信用报告机构出售此类数据。

这解释了为什么急刹车、急加速这类看起来不值钱的数据会被车企收集：它在保险定价市场上有明确买家。

那拒绝呢？研究记录了一个细节：特斯拉在用户关闭数据共享时警告，这可能导致车辆「功能受限、严重损坏或无法运行」。其他车企温和一些，但结构相同——数据收集默认开启，关闭的代价由车主承担。

## AI 助手正在接入同一条数据链

今年 4 月，GM 宣布把 Google Gemini 推送到约 400 万辆带 Google 车机的车上（[GM 官方公告](https://news.gm.com/home.detail.html/Pages/news/us/en/2026/apr/0428-Google-Gemini.html)），并预告今年晚些时候推出自研助手，用 OnStar 车辆数据微调（据 [TechCrunch 报道](https://techcrunch.com/2025/10/22/gm-is-bringing-google-gemini-powered-ai-assistant-to-cars-in-2026)）。注意这个组合：OnStar 数据就是 FTC 案子里被卖给信用报告机构的那批数据，现在它成了训练车载助手的原料。

对话式助手会新增一类此前不存在的数据：你在车里问了什么、说了什么。这项研究测的是网络流量和 App，没有覆盖语音助手的数据流向——这是测量上的空白，不是安全上的背书。我的判断是：一个连「隐私政策与实际流量对不上」都要靠外部研究者搭帐篷才能发现的行业,没有理由相信它会在 AI 层突然变得克制。

## 车主能做什么

能做的事有限但不是零：部分车企允许在车机或 App 里关闭数据共享（Ford 在 FordPass、Toyota 在其 App 中可拒绝主数据授权）；在有隐私法的州，可以向车企提交数据删除/停止共享请求；[Privacy4Cars](https://privacy4cars.com/) 提供免费服务，代为定位各车企的请求入口。买二手车时值得记住：前车主的数据和配对关系可能还留在车机里。

但逐个设置解决不了结构问题。这项研究最有用的地方是给出了一个可复用的检验标准：车企说什么不重要，车发出的流量才是事实。接下来值得盯的测量对象，就是车载 AI 助手上线后，这顶帐篷里会多出哪些新域名。

## 参考来源

- [Automatic Transmission 项目页（东北大学）](https://automatictransmission.khoury.northeastern.edu/) — 论文标题、方法论（法拉第帐篷、tcpdump、mitmproxy）、19/21 与 7/30 等核心数字、App 配对翻倍发现
- [Consumer Reports 调查报道](https://www.consumerreports.org/electronics/personal-information/your-car-is-sharing-data-with-big-tech-companies-study-finds-a4474820962/) — 测试规模与时间、第三方公司名单、特斯拉 34 个追踪域名、Honda/Amplitude 事例、特斯拉关闭共享的警告文案
- [Schneier on Security 转评](https://www.schneier.com/blog/archives/2026/10/connected-cars-are-a-surveillance-platform.html) — 选题来源
- [FTC 对 GM 的执法公告](https://www.ftc.gov/news-events/news/press-releases/2025/01/ftc-takes-action-against-general-motors-sharing-drivers-precise-location-driving-behavior-data) — OnStar Smart Driver 数据卖给信用报告机构、五年禁令
- [GM 官方新闻稿：Gemini 推送至数百万车辆](https://news.gm.com/home.detail.html/Pages/news/us/en/2026/apr/0428-Google-Gemini.html) — 400 万辆规模、适用品牌
- [TechCrunch：GM 自研车载助手计划](https://techcrunch.com/2025/10/22/gm-is-bringing-google-gemini-powered-ai-assistant-to-cars-in-2026) — 用 OnStar 数据微调自研助手的预告
