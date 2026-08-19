---
title: "OpenAI 终于不再相信你自己填的生日了"
description: "拆解 ChatGPT for Teens：哪些是真机制升级，哪些是旧功能打包，以及为什么迟到了三年半。"
pubDate: 2026-08-18
tags: [ai-safety, trust-and-safety, openai]
lang: zh
slug: chatgpt-for-teens-age-gate
translationOf: chatgpt-for-teens-age-gate
---

8 月 18 日，OpenAI 上线了 [ChatGPT for Teens](https://openai.com/index/chatgpt-for-teens/)，一个面向 13 到 17 岁用户的版本。TechCrunch 当天的标题不客气：[「青少年开始用它好几年之后，OpenAI 终于发布了更安全的青少年版」](https://techcrunch.com/2026/08/18/openai-launches-a-safer-chatgpt-for-teens-years-after-teens-started-using-it/)。

这个批评有事实基础。ChatGPT 2022 年底上线，到今年 2 月周活跃用户已经 9 亿；青少年从第一天起就在用户里，只是产品一直假装看不见。注册时填个生日，填 18 岁就是 18 岁。做了三年半通用产品之后才补年龄分级，这在消费互联网行业里确实算慢的。

但「迟到」和「没用」是两回事。我的本职工作是内容审核，这篇想拆开看看：这次发布里哪些是真的机制变化，哪些是旧功能重新打包，以及那个更尖锐的问题，为什么是现在。

## 先分清：哪些是新的，哪些是打包

把公告和过去一年的时间线对着看，会发现大部分组件早就存在：

- **家长控制**：[2025 年 9 月底就上线了](https://www.forbes.com/sites/kirkogunrinde/2025/09/29/openai-launches-parental-controls-for-chatgpt-following-lawsuit-from-teens-death/)。家长通过邮件邀请绑定孩子账号，可以关掉记忆和聊天历史、设置禁用时段，系统检测到孩子处于急性心理危机时会通知家长。这次的增量是把通知范围扩展到饮食失调相关的情形。
- **未成年人模型行为规范**：OpenAI 的 Model Spec（一份规定模型在各种场景下该怎么回应的公开文档）[2025 年 12 月就加入了 Under-18 条款](https://techcrunch.com/2025/12/19/openai-adds-new-teen-safety-rules-to-models-as-lawmakers-weigh-ai-standards-for-minors/)：禁止沉浸式恋爱角色扮演和第一人称亲密对话，不得对青少年使用亲昵称呼，不得暗示自己有感情或意识；自杀自残、身体意象、危险物品等高危话题要特别处理。
- **Teen Safety Blueprint**：[2025 年 11 月发布](https://www.axios.com/2025/11/06/openai-blueprint-teen-ai-safety-standards)的政策文件，给监管者和同行提建议。

这次真正的新东西是两块：一是教育功能，Study Mode 引导做题而非直接给答案，检测到疑似抄作业时弹提醒，外加更频繁的休息提示和上传隐私图片前的警告；二是[年龄推断（age prediction）从「在做了」变成默认开启](https://openai.com/index/our-approach-to-age-prediction/)：自称 13 到 17 岁的用户、以及被系统推断为未成年的用户，会被自动放进青少年版，拿不准的一律按未成年处理。

第二块才是这次发布的核心。

## 年龄闸门挪了一级

内容审核行业把「确认用户年龄」这件事叫 age assurance，大致分三级。第一级是自我申报：注册时填生日，谎报零成本，行业里没人真指望它挡住谁。第二级是年龄推断：不问你，系统根据行为信号猜，据报道 OpenAI 用的信号包括填报年龄、账号注册时长、使用时段等模式。第三级是强验证：身份证件或人脸，准确但有实打实的隐私代价。

OpenAI 这次做的事，本质上是把默认闸门从第一级挪到第二级，并且在推断不确定时按未成年处理，被误判的成年人[据报道](https://gulfnews.com/technology/media/chatgpt-will-now-guess-your-age-to-protect-teens-from-sensitive-content-1.500415454)需要向第三方身份验证服务 Persona 提交自拍才能恢复完整功能。

「拿不准就按未成年算」是整个设计里最重要的一个决定。任何年龄分类器都会出错，错有两个方向：把成年人误判成青少年，代价是用户摩擦和隐私成本，你得交自拍自证成年；把青少年漏判成成年人，代价是伤害暴露和法律风险。OpenAI 选择把成本压到前一种，这符合监管者的期待，也和社交平台已经走过的路线一致：Instagram 在 [2024 年 9 月推出青少年账户](https://about.fb.com/news/2024/09/instagram-teen-accounts/)时，就是把 18 岁以下账户默认转成受限模式。所以准确地说，OpenAI 不是先行者，是补课者，补的还是社交行业两年前的课。

但方向是对的。这一层我认为是真机制，不是公关。

## 规范不等于执行

真正的弱点在另一处：Model Spec 是行为规范，不是能力保证。写进文档「不得如何如何」，和模型在第 200 轮对话里仍然做到「不得如何如何」，是两件事。

这正是 Raine 案戳破的地方。2025 年 8 月 26 日，16 岁的 Adam Raine 的父母[起诉 OpenAI 和 Sam Altman](https://techcrunch.com/2025/12/19/openai-adds-new-teen-safety-rules-to-models-as-lawmakers-weigh-ai-standards-for-minors/)：孩子与 ChatGPT 数月长聊后自杀，诉状称对话中上千次出现自杀相关内容，OpenAI 自己的审核系统标记了 377 条自残消息，但服务从未中断。同一天 OpenAI 发博客[承认](https://openai.com/index/helping-people-when-they-need-it-most/)：防护在常见的短对话里更可靠，「随着对话来回增多，模型安全训练的部分效果可能退化」，模型可能在第一次提及自杀意念时正确给出求助热线，长聊之后却给出违背防护规则的回答。

对照这个已知缺陷去读这次的公告，会发现它没有回答关键问题：长对话场景下的防护退化改善了多少，没有评测数据；年龄推断的误判率是多少、按年龄段怎么分布，没有公布；危机通知的准确率和漏报率，也没有。TechCrunch 还点了一个所有做过家长控制的平台都熟悉的老问题：青少年绕过管控的能力向来很强，注册个新账号自称成年，年龄推断需要多久把他抓回来？同样没有数字。

没有这些数字，外部只能验证「架构对了」，验证不了「效果有了」。这一点我拿不准，而且在 OpenAI 公布评测之前，所有人都拿不准。

## 为什么是现在

把监管事件和产品动作排在一条时间线上：2025 年 8 月 Raine 案起诉；9 月 FTC 对 OpenAI、Meta、Character.AI 等七家公司发出 6(b) 调查令（FTC 的一种权限，不以执法为前提就能强制企业提交内部资料）；9 月底家长控制上线；10 月加州签署规范陪伴型聊天机器人的 SB 243，42 个州的总检察长联名致函要求平台加装保护，参议员 Hawley 的法案更主张直接禁止未成年人使用 AI 聊天机器人；11 月 Blueprint；12 月 Model Spec 加条款；2026 年 6 月佛罗里达又一起针对 OpenAI 和 Altman 的诉讼；8 月，ChatGPT for Teens。

每一步产品动作前面，都站着一个法律或监管事件。这不能证明发布是纯姿态，机制本身是实的；但它说明青少年安全的优先级是被外部压力排上去的，而且「展示已采取合理措施」本身就是诉讼防御材料。对平台来说，这两个动机从来不冲突。

## 我的判断

架构上，这次是真升级：年龄推断加默认从严加分级模型行为，是内容审核行业验证过的正确结构。效果上，它目前不可核验：误判率、长对话安全评测、通知系统准确率，三组关键数字一个都没公布。判断它成色如何，要么等 OpenAI 把评测放出来，要么等下一起诉讼的证据开示把数据翻出来。

还有一笔账公告里不会替你算：默认从严意味着全体用户的年龄都要被推断一遍，被误判的成年人要向第三方交出人脸照片。青少年保护的成本从来不只落在青少年身上，这次也一样。

## 参考来源

- [Introducing ChatGPT for Teens — OpenAI](https://openai.com/index/chatgpt-for-teens/) — 官方公告：功能清单、13–17 岁范围、默认从严策略
- [Updating our Model Spec with teen protections — OpenAI](https://openai.com/index/updating-model-spec-with-teen-protections/) — Under-18 行为规范条款
- [Our approach to age prediction — OpenAI](https://openai.com/index/our-approach-to-age-prediction/) — 年龄推断机制
- [Helping people when they need it most — OpenAI](https://openai.com/index/helping-people-when-they-need-it-most/) — 长对话防护退化的官方承认
- [OpenAI launches a safer ChatGPT for teens — TechCrunch](https://techcrunch.com/2026/08/18/openai-launches-a-safer-chatgpt-for-teens-years-after-teens-started-using-it/) — 9 亿周活、批评角度、诉讼背景
- [OpenAI adds new teen safety rules to models — TechCrunch](https://techcrunch.com/2025/12/19/openai-adds-new-teen-safety-rules-to-models-as-lawmakers-weigh-ai-standards-for-minors/) — 2025 年 12 月 Model Spec 条款、Raine 案数字、立法背景
- [OpenAI launches parental controls — Forbes](https://www.forbes.com/sites/kirkogunrinde/2025/09/29/openai-launches-parental-controls-for-chatgpt-following-lawsuit-from-teens-death/) — 家长控制 2025 年 9 月底上线
- [OpenAI unveils blueprint for teen AI safety standards — Axios](https://www.axios.com/2025/11/06/openai-blueprint-teen-ai-safety-standards) — Teen Safety Blueprint 发布时间与内容
- [ChatGPT will now guess your age — Gulf News（转述 TechCrunch/Reuters）](https://gulfnews.com/technology/media/chatgpt-will-now-guess-your-age-to-protect-teens-from-sensitive-content-1.500415454) — 年龄推断信号、Persona 自拍验证
- [Introducing Instagram Teen Accounts — Meta](https://about.fb.com/news/2024/09/instagram-teen-accounts/) — 社交平台默认受限模式的先例
