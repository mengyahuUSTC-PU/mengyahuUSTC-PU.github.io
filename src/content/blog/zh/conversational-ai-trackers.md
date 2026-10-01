---
title: "AI 替你总结的对话标题，转头就发给了 Meta 和 TikTok"
description: "IMDEA Networks 实测九款对话式 AI：自动生成的对话标题、默认公开的永久链接、服务器端转发，拒绝 cookie 后 80.8% 的追踪器照常工作。"
pubDate: 2026-09-29
tags: [privacy, trust-and-safety]
lang: zh
slug: conversational-ai-trackers
translationOf: conversational-ai-trackers
---

你问 AI：年薪 8.5 万美元，在纽约买房能贷多少？助手一边回答，一边替你把这轮对话总结成一个标题挂在侧边栏，比如「Salary 85k NYC: Mortgage of 280-350k」。这个标题不只是给你看的。论文合著者 Jorge García Herrero [举的正是这个例子](https://www.zeropartydata.es/p/i-do-not-know-if-ai-will-kill-us)：在多款产品里，这类 AI 自动生成的标题会随着页面数据一起发给 Meta、TikTok、DoubleClick 的追踪脚本。

这来自 IMDEA Networks 与马德里卡洛斯三世大学团队的论文 [Prompt like a Butterfly, Sting like a Tracker](https://jorgegarciaherrero.com/wp-content/interactivos/20260916-Prompt-like-a-butterfly-sting-like-a-tracker-(clean).pdf)（标题戏仿拳王阿里的「轻盈如蝶、蜇人如蜂」），据合著者说明已被隐私技术会议 PoPETs 2027 接收。9 月 29 日它冲上 [Hacker News 首页](https://news.ycombinator.com/item?id=49890226)，截至写稿时四百多个赞。团队实测了九款助手：ChatGPT、Claude、Gemini、Copilot、Grok、Perplexity、Le Chat（Mistral）、DeepSeek、Meta AI，覆盖网页端和 Android 端、免费和付费档、接受和拒绝 cookie 的各种组合。

结果：九款全部至少集成一个第三方广告或追踪服务；九个网页客户端里有六个、八个可测的 Android 应用里有三个，把对话 URL、标题、prompt 或截图泄漏给第三方，而且通常连着邮箱哈希这类持久标识符一起发。也就是说，追踪器拿到的不是匿名的「有人在问房贷」，而是能和广告体系里既有用户画像对上号的「你在问房贷」。

## 老基建，新语义

论文里没有一项发现依赖新技术。Meta Pixel、TikTok Pixel、Google Analytics，都是网站装了多年的东西：网页里嵌一段第三方脚本，把当前页面的地址、标题和你浏览器里的广告 cookie 一起发回广告商服务器，用来把「你看了什么」和「你是谁」对上号。

变化在于喂给这套基建的数据。普通电商网站上，页面标题是「某某牌跑鞋」，追踪器知道你在逛鞋。而在聊天产品里，页面标题是模型刚替你生成的对话摘要：你的健康疑问、财务状况、法律麻烦，被压缩成一句话，恰好塞进了追踪脚本例行上报的那个字段。论文把这称为一个新的隐私攻击面：泄漏源不是用户自己发的内容，是服务商加工出的「对话工件」。九个网页客户端里有三个把这种 AI 生成的标题发给了包括 Meta、TikTok、DoubleClick 在内的九个第三方。

Grok 走得最远。它的对话永久链接默认公开、需要手动关闭；分享时，[研究团队的项目网站](https://leakylm.github.io/)记载，消息原文会被写进网页的 Open Graph 元数据（本来是给社交平台生成预览卡片用的字段，包括标题和图片说明），于是读取这些字段的 TikTok 脚本连标题、prompt 带截图一起收走。

永久链接这个坑我不陌生：8 月我写过 [Claude 分享链接是怎么进 Google 搜索的](/zh/claude-share-links-google-indexed)，问题出在「拿到链接就能看」的 capability URL 一旦流出就等于公开。这篇论文把同一条链路又推进一步：链接根本不用流出去，页面里内嵌的追踪脚本当场就把它读走了。Perplexity 的访客对话同样始终公开。

## 拒绝 cookie 之后

最扎心的数字在同意机制这一节：拒绝全部非必要 cookie 后，80.8% 的第三方追踪器照常工作，九款服务里四款继续向第三方发数据。

一部分原因是追踪转移到了用户看不见的地方。以 Claude 为例，论文测到 Anthropic 经由 Segment 的转化接口，把用户事件从自家服务器直接转发给 Facebook、LinkedIn、TikTok、Reddit、Google 等 11 个广告平台。这叫服务器端追踪：数据不经过你的浏览器，adblocker 和隐私浏览器拦的都是浏览器里的脚本，对这条路径无从下手。

Android 端更直接：多数应用压根不弹 cookie 选择框，装上就得接受服务条款，「拒绝」这个选项不存在。而移动客户端联系的各类端点里，71% 来自应用内嵌浏览器（WebView），网页端那套追踪原样搬了进来。网页端也有不给选的：Le Chat 必须整体接受服务条款和隐私政策才能用。

## 能做什么，不能指望什么

用户侧还有几件事值得做。拒绝非必要 cookie 依然有意义，它砍不掉八成追踪器，但能砍掉两成：论文测到 Claude 在用户拒绝后，Meta Pixel 和那 11 个服务器端转发目标都没有激活。别用对话分享和永久链接功能，Grok 用户应手动关掉默认公开；分享过的链接去设置里撤销。真正敏感的话题，用不登录的访客模式反而危险（Perplexity 访客对话公开）；要绕开这整套第三方传输，得用完全离线、不带遥测的本地部署。

但读完论文的判断是：这不是用户侧能解决的问题。服务器端转发用户根本看不见，同意机制形同虚设，论文作者自己给的建议也全部指向平台，别默认公开永久链接、别让自动生成的标题进入第三方可见的字段。值得记下的一个先例是：据项目网站记载，Perplexity 在一起集体诉讼立案后，于 2026 年 4 月 3 日移除了 Meta Pixel。项目网站的措辞很谨慎，只说这「可能是对诉讼的回应」；如果推测成立，先让平台改掉做法的，是法庭。

这一年围绕 AI 隐私的讨论，注意力几乎都在模型层：训练数据、模型记忆、对话会不会被拿去训练。这篇论文测的则是包在模型外面那层普通 web 产品，用的全是最老一代的广告技术，只是没人在把聊天框接上这套基建时重新问一句：现在流过这里的数据，和当年的商品浏览记录还是一回事吗？接下来值得盯的是欧盟的动作。论文的法律分析认为，向第三方披露对话工件这类处理需要事先知情同意，也很难拿「履行合同」当合法依据，按 GDPR 和 ePrivacy 指令的标准站不住；而这套实测本身就是 2026 年 5 月在西班牙完成的，九款产品运行在欧盟监管够得到的地方。

## 参考来源

- [Prompt like a Butterfly, Sting like a Tracker（论文 PDF）](https://jorgegarciaherrero.com/wp-content/interactivos/20260916-Prompt-like-a-butterfly-sting-like-a-tracker-(clean).pdf) — 核心数据：九款产品测试范围、6/9 与 3/8 泄漏比例、80.8%、Claude 的 11 个服务器端转发目标、Grok 永久链接默认公开、Android 无同意机制、71% 的端点来自 WebView
- [LeakyLM 项目网站（研究团队官方）](https://leakylm.github.io/) — Grok 经 Open Graph 元数据向 TikTok 泄漏消息原文的机制细节、Perplexity 移除 Meta Pixel 的时间线
- [合著者 Jorge García Herrero 的说明长文](https://www.zeropartydata.es/p/i-do-not-know-if-ai-will-kill-us) — PoPETs 2027 录用信息、「Salary 85k NYC」标题示例
- [Hacker News 讨论](https://news.ycombinator.com/item?id=49890226) — 热度数据（截至写稿时 412 赞、130 评论）
- [本站旧文：点一下「分享」，你就发布了](/zh/claude-share-links-google-indexed) — capability URL 与分享链接被搜索引擎收录的前情
