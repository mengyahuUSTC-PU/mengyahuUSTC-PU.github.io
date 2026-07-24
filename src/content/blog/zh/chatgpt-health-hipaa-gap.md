---
title: "病历交给 ChatGPT 的那一刻，HIPAA 的保护就结束了"
description: "ChatGPT Health 面向全美开放，可接入病历和 Apple Health。它不需要违反 HIPAA 的任何条款——这正是问题所在：HIPAA 盯的是机构，不是数据。"
pubDate: 2026-07-23
tags: [health-ai, privacy, ai-governance]
lang: zh
slug: chatgpt-health-hipaa-gap
translationOf: chatgpt-health-hipaa-gap
---

7 月 23 日，OpenAI 把 ChatGPT Health [推向了全美所有 18 岁以上用户](https://openai.com/index/health-in-chatgpt/)，免费版也能用（[MacRumors](https://www.macrumors.com/2026/07/23/chatgpt-apple-health-integration/)）。用户可以把自己的电子病历直接连进来——通过与聚合平台 b.well 的合作，覆盖 Epic、Oracle Health 等主流病历系统，b.well 的网络号称接入约 220 万医疗服务提供者（[Fierce Healthcare](https://www.fiercehealthcare.com/ai-and-machine-learning/openai-launches-chatgpt-health-connect-data-health-apps-medical-records)、[TechCrunch](https://techcrunch.com/2026/07/23/openai-makes-chatgpt-health-available-to-all-u-s-users/)）。再加上 Apple Health、MyFitnessPal 这些应用，ChatGPT 从此可以对着你真实的化验单、用药记录和睡眠数据回答问题。

先把一件事说清楚：只要 OpenAI 不落入 HIPAA 约束的实体范围——就公开信息看它不落入，下一节展开——这整个流程就不违反 HIPAA 的任何一个条款。

这不是 OpenAI 找到了什么漏洞。我入行 Responsible AI 的第一个项目，就是和医疗 AI 公司 Nuance 合作，给医患对话的自动摘要做幻觉检测。「合规」和「受保护」经常被当成同义词用——ChatGPT Health 是把这两个词拆开的最好教材：产品可以全程合规，而你的病历自始至终不在这部专门法律的保护之内。

## 空白不是钻出来的，是法律本来就长这样

HIPAA 是美国 1996 年的医疗隐私法。很多人以为它保护的是「医疗数据」这个类别，其实不是——它约束的是[一份实体名单](https://www.hhs.gov/hipaa/for-professionals/covered-entities/index.html)：医疗服务提供者、保险计划、清算机构（合称 covered entities，受覆盖实体），外加替这些机构处理数据的承包商（business associates，业务伙伴）。不在名单上、也不替名单上的机构处理数据的公司，拿到同样的病历，就不受 HIPAA 约束。华盛顿的智库 Center for Democracy and Technology 在点评这次发布时说得直白：AI 公司通常根本不在 HIPAA 覆盖范围内（[Fierce Healthcare](https://www.fiercehealthcare.com/ai-and-machine-learning/openai-launches-chatgpt-health-connect-data-health-apps-medical-records)）。

更关键的是数据出口这一环。HIPAA 赋予患者「访问权」（right of access）：你有权要求医院把病历发给你指定的任何第三方应用，医院一般不得拒绝。美国卫生与公众服务部（HHS）2019 年的[官方指南](https://www.hhs.gov/hipaa/for-professionals/privacy/guidance/access-right-health-apps-apis/index.html)把责任边界划得清清楚楚：只要接收方应用是患者自己选的、不是医院提供的，病历送达之后应用怎么用、怎么共享，医院一概不担责；HIPAA 对接收方的使用「不施加任何限制」。

也就是说，保护不是被谁绕开的——它在设计上就终止于交接那一刻。医院不但拦不住这次传输，故意设障反而可能违反[信息封锁（information blocking）](https://www.healthit.gov/topic/information-blocking)的规定。病历跨过 API 的那条线，监管就从「有专门法律、有联邦执法机构、有法定患者权利」切换成「看用户协议」——外侧不是完全无法可依，FTC 的规则和一些州法还在（后文细说），但专门的医疗隐私架构到这里就停了。

## 承诺替代法律之后，差的是什么

OpenAI 给出的隐私承诺本身不算含糊：连接的病历和 Apple Health 数据、以及用到这些数据的对话，不用于训练基础模型，不用于广告定向；健康数据有额外的加密和隔离；默认每次调用病历前请求许可（用户可改为「始终允许」）；断开连接后 30 天内删除数据（[MacRumors](https://www.macrumors.com/2026/07/23/chatgpt-apple-health-integration/)、[Glitchwire](https://glitchwire.com/news/openai-relaunches-health-in-chatgpt-with-expanded-us-access-after-a-six-month-re/)）。我不怀疑这些承诺是认真的。要比的不是诚意，是「承诺」和「法律」这两种约束在机制上差在哪。拆三个具体的看。

**第一，隔离承诺和产品方向在对着走。** OpenAI 自己披露，1 月试点期间超过 70% 的健康对话发生在专门的 Health 空间之外——用户安排饭菜时顺口问过敏，查食谱时提到忌口（[Glitchwire](https://glitchwire.com/news/openai-relaunches-health-in-chatgpt-with-expanded-us-access-after-a-six-month-re/)）。所以 7 月这版重新设计的卖点，恰恰是让健康上下文经用户授权后可以进入日常对话，而不是关在单独空间里。这在产品上完全合理，但它意味着「健康数据与其他对话隔离」这堵墙，正是产品要拆的那堵。一旦化验结果作为上下文进过日常对话、相关内容又经健康对话沉淀进跨对话记忆（OpenAI 说明记忆不会直接从连接的病历创建，但可以从健康对话生成），「断开连接、30 天删除」删的是数据源，散落在别处的衍生信息怎么清理，公开材料没有讲细。

**第二，删除承诺让位于法律程序。** 这不是假设。2025 年《纽约时报》诉 OpenAI 版权案中，法院曾下令 OpenAI 保留全部用户对话日志——包括用户已经删除的——OpenAI [公开抗辩](https://openai.com/index/response-to-nyt-data-demands/)，但在保留令收窄前只能照办。这件事和健康无关，机制教训却直接适用：聊天记录在法律上是普通的商业记录，可以被诉讼保全、被取证。病历在医院手里时，HIPAA 对司法程序中的披露有[专门规则](https://www.hhs.gov/hipaa/for-individuals/court-orders-subpoenas/index.html)和最小化要求；同一份内容进了聊天记录，就只是又一份电子证据。「我们会删除你的数据」这句话，永远默认附带一行小字：除非法院不让。

**第三，广告承诺有过先例，先例的结局不好。** OpenAI 正在探索广告收入，专家因此提醒健康数据与广告系统之间的隔离必须严丝合缝（[Fierce Healthcare](https://www.fiercehealthcare.com/ai-and-machine-learning/openai-launches-chatgpt-health-connect-data-health-apps-medical-records)）。OpenAI 现行的[广告说明](https://help.openai.com/en-us/articles/20001047-ads-in-chatgpt)也把个人健康列为不投放广告的敏感场景——但这同样是一条可以修订的产品政策。而「承诺不拿健康数据做广告、后来做了」在这个行业有现成判例：处方折扣平台 GoodRx 曾向用户保证健康信息不外流，实际把用药数据传给了 Facebook 等广告平台，2023 年被 FTC 依据健康数据泄露通知规则（Health Breach Notification Rule）[罚款 150 万美元](https://www.ftc.gov/news-events/news/press-releases/2023/02/ftc-enforcement-action-bar-goodrx-sharing-consumers-sensitive-health-info-advertising)——这是该规则生效十四年来第一次动用。这就是 HIPAA 之外的执法现状：FTC 靠《联邦贸易委员会法》禁止欺骗和不公平行为、靠泄露通知规则要求事后告知，主要在事后追责，而不是像 HIPAA 那样事前规定你能对数据做什么；用户协议还可以单方面修订，今天的承诺约束不了明天的版本。

顺带一个值得记下的对照：这次发布面向美国用户，病历接入也仅限美国的医疗系统，欧洲经济区、瑞士和英国明确不在开放名单上（[Fierce Healthcare](https://www.fiercehealthcare.com/ai-and-machine-learning/openai-launches-chatgpt-health-connect-data-health-apps-medical-records)）。欧洲的 GDPR 和 HIPAA 走的是相反的路线：它按数据类别保护——健康数据属于[特殊类别个人数据](https://gdpr-info.eu/art-9-gdpr/)，无论落到谁手里，接手处理的一方都要承担相应的法定义务。数据走到哪，保护跟到哪。HIPAA 盯机构、GDPR 盯数据，ChatGPT Health 暴露的这种监管空白，正是前一种架构的产物。

## 同样的数据放在 HIPAA 内侧：Nuance 的先例

开头提到的 Nuance，恰好站在这条边界的另一侧，它的履历值得单独一节。这家公司做了几十年医疗语音：Dragon Medical 系列做医生的语音录入，eScription 做医疗转写，主打产品 DAX Copilot 在诊室里录下医患对话、自动生成临床病历，直接嵌进 Epic 电子病历系统（[官方发布稿](https://www.prnewswire.com/news-releases/nuance-announces-general-availability-of-dax-copilot-embedded-in-epic-transforming-healthcare-experiences-with-automated-clinical-documentation-302037590.html)）——我当年参与的幻觉检测，对应的就是这条产品线。2022 年起它是 Microsoft（我的雇主）的[子公司](https://news.microsoft.com/source/2022/03/04/microsoft-completes-acquisition-of-nuance-ushering-in-new-era-of-outcomes-based-ai/)，本节内容全部来自公开报道与公开文件。

论经手的数据，Nuance 和 ChatGPT Health 高度重叠：病历、化验结果、医患之间说的每一句话。论法律位置，两者正好隔着 HIPAA 那条线。Nuance 面向医院卖服务，在法律上是医院（受覆盖实体）的业务伙伴，必须签业务伙伴协议（BAA），处理数据的每一环都背着 HIPAA 的[法定义务](https://www.hhs.gov/hipaa/for-professionals/privacy/guidance/business-associates/index.html)；ChatGPT Health 面向患者本人，靠访问权拿到同样的数据——上游的医院和病历系统仍在 HIPAA 之内，但数据一送达 OpenAI，HIPAA 就不再跟着走。所以它是一份现成的参照：同样的数据托管在监管最重的一侧，会出什么事，出事之后又是什么局面。

答案是照样出事，十年里出了三次大的。2017 年，NotPetya 恶意软件（那年殃及全球企业的一场网络攻击）击穿 Nuance 内网，旗舰转写平台 eScription 停摆数周，多家医院退回纸笔记录；据 [Healthcare IT News](https://www.healthcareitnews.com/news/hackers-hit-nuance-again-2017-while-notpetya-cost-98-million-lost-revenue) 报道累计财务影响约 9,800 万美元，Nuance 的 [SEC 10-Q 文件](https://www.sec.gov/Archives/edgar/data/1002517/000100251718000017/nuan1231201710-q.htm)中拆分为约 6,800 万美元收入损失加约 2,400 万美元修复相关成本。2023 年，第三方文件传输工具 MOVEit 的漏洞波及 Nuance，约 122 万人的数据暴露，集体诉讼以 850 万美元和解（[HIPAA Journal](https://www.hipaajournal.com/nuance-communications-moveit-data-breach-settlement/)）。同年，一名被解雇两天的前员工回头访问并窃取了客户 Geisinger 医疗系统约 120 万患者的信息，两家公司最终共同支付 500 万美元和解（[TechTarget](https://www.techtarget.com/healthtechsecurity/news/366634778/Geisinger-Health-Nuance-reach-5M-settlement-over-data-breach)）。三件事对应三类失效——外部攻击、供应链漏洞、内部人员——而公开记录里，没有一起被监管机构认定源于 HIPAA 违规：就已知信息看，Nuance 是在合规运营中被打穿的。本文反复说「合规不等于受保护」，这个命题在 HIPAA 内侧同样成立。

内外两侧真正的区别在出事之后。MOVEit 和 Geisinger 两起泄露都触发了 HIPAA 的法定泄露通知义务（NotPetya 主要造成系统停摆，公开报道未见其被认定为须通知的患者数据泄露）：多少人受影响、何时通知、通知谁，都有[联邦规则](https://www.hhs.gov/hipaa/for-professionals/breach-notification/index.html)兜底。HIPAA 本身并不给患者对泄露提起诉讼的私人诉权，集体诉讼走的是州法等民事主张，但正是这套通知机制让患者知道了出事——两笔和解都发生在通知之后。换到 HIPAA 外侧，这套机制主要只剩 FTC 的健康数据泄露通知规则（2024 年更新后对健康应用的覆盖才更明确）、少数州的健康数据法，加上事后的消费者集体诉讼——不是没有救济，而是更薄、更晚、先例更少。

能直接搬到 ChatGPT Health 场景的教训有三条。第一，别问会不会出事，问出事之后你有什么。Nuance 背着全套 HIPAA 义务运营，十年仍有三次大事故；指望 OpenAI 凭工程能力做到零事故不现实，真正的变量是事后患者手里的牌。第二，数清链条上有多少双手。MOVEit 之所以成为缺口，就因为它是数据链条里用户从没听说过的一环；ChatGPT Health 的链条里同样有 b.well 这样的聚合中间层，你看到的是 ChatGPT 的界面，数据实际经过的主体更多。第三，知情同意经得起法庭逐字检验才算数。诊室环境录音这一产品类别正在引来窃听类集体诉讼——2025 年 11 月，使用 AI 转写工具 Abridge 的 Sharp HealthCare 因涉嫌未经患者明确同意录音被集体起诉（[KPBS](https://www.kpbs.org/news/health/2025/12/11/lawsuit-claims-sharp-healthcare-secretly-recorded-exam-room-conversations-without-patient-consent)）；2026 年 4 月，同样部署 Abridge 的 Sutter Health 与 MemorialCare 也被诉（[TechTarget](https://www.techtarget.com/healthtechsecurity/news/366641717/Sutter-Health-MemorialCare-face-class-action-lawsuit-over-AI-scribe-use)），两案被告都是医疗系统本身。ChatGPT Health 默认每次调用病历前请求许可，这个设计方向是对的，但这批诉讼提醒所有人：同意的粒度、告知的充分性，最终是在法庭上被逐条验的。

## 能带走什么

我不打算劝人别用。用自己的真实化验单提问，比让模型对着一句模糊描述瞎猜要好，健康提问本来就是 ChatGPT 的高频场景——据报道每周有约 3 亿人次向它提出健康相关问题（[TechCrunch](https://techcrunch.com/2026/07/23/openai-makes-chatgpt-health-available-to-all-u-s-users/) 转述 OpenAI 自报数据），OpenAI 认真做这个产品比放任用户在普通对话框里贴病历要负责任。何况 OpenAI 条款里也写明了：该服务不用于任何健康状况的诊断或治疗（[TechCrunch](https://techcrunch.com/2026/07/23/openai-makes-chatgpt-health-available-to-all-u-s-users/)）。

但连接之前，值得用正确的心智模型做决定：把它当成一次实质上不可逆的披露，而不是一次可以随时撤销的授权——断开连接、删除数据的开关都在，但已经发生的披露收不回来。30 天删除是产品政策而非法定权利（HIPAA 给患者的是访问权和更正权，[不含一般意义的删除权](https://www.hhs.gov/hipaa/for-professionals/faq/2042/what-personal-health-information-do-individuals/index.html)），诉讼保全可以压过它，衍生上下文未必删得干净。粒度也在你手里——想解读一张化验单，贴那一张就够了，不必把整个病历库直连进来。

更大的判断是：这个空白填不上，除非立法。HHS 的指南写明了保护止于何处，FTC 2024 年[更新了](https://www.ftc.gov/business-guidance/blog/2024/04/updated-ftc-health-breach-notification-rule-puts-new-provisions-place-protect-users-health-apps)泄露通知规则、进一步明确纳入健康应用，[华盛顿州](https://www.atg.wa.gov/protecting-washingtonians-personal-health-data-and-privacy)等地也开始为脱离 HIPAA 的健康数据单独立法（My Health My Data Act），但这些都是补丁：通知规则管泄露后的告知，不管日常怎么用；州法的适用范围以本州居民和经营联系为界。HIPAA 的实体名单定格在 1996 年的医疗体系里，2026 年的产品让病历流进了对话式 AI 的上下文窗口。在两者之间的落差被立法填上之前，「你的病历受保护」这句话，在你点下「连接」按钮之后，语法上就该改成过去时。

## 参考来源

- [Launching Health in ChatGPT — OpenAI](https://openai.com/index/health-in-chatgpt/) — 官方公告（站点反爬未能直接抓取，关键内容经多家报道交叉核对）
- [OpenAI launches ChatGPT Health to connect data from health apps, medical records — Fierce Healthcare](https://www.fiercehealthcare.com/ai-and-machine-learning/openai-launches-chatgpt-health-connect-data-health-apps-medical-records) — b.well 合作与网络规模、CDT 评论、广告风险提醒、欧洲不在首发范围
- [ChatGPT's Apple Health Integration Now Rolling Out to U.S. Users — MacRumors](https://www.macrumors.com/2026/07/23/chatgpt-apple-health-integration/) — 发布时间、覆盖用户与平台、隐私承诺、1 月试点背景
- [OpenAI makes ChatGPT Health available to all U.S. users — TechCrunch](https://techcrunch.com/2026/07/23/openai-makes-chatgpt-health-available-to-all-u-s-users/) — Epic/Oracle Health 病历接入、条款免责声明、试点数据、健康提问规模
- [OpenAI Relaunches Health in ChatGPT — Glitchwire](https://glitchwire.com/news/openai-relaunches-health-in-chatgpt-with-expanded-us-access-after-a-six-month-re/) — 70% 对话发生在 Health 空间外、30 天删除、一月试点到七月重发的过程
- [Covered Entities and Business Associates — HHS](https://www.hhs.gov/hipaa/for-professionals/covered-entities/index.html) — HIPAA 约束的实体范围
- [The access right, health apps, & APIs — HHS](https://www.hhs.gov/hipaa/for-professionals/privacy/guidance/access-right-health-apps-apis/index.html) — 患者访问权下第三方应用不受 HIPAA 约束的官方指南
- [Breach Notification Rule — HHS](https://www.hhs.gov/hipaa/for-professionals/breach-notification/index.html) — HIPAA 泄露通知义务的联邦规则
- [FTC Enforcement Action to Bar GoodRx from Sharing Consumers' Sensitive Health Info for Advertising — FTC](https://www.ftc.gov/news-events/news/press-releases/2023/02/ftc-enforcement-action-bar-goodrx-sharing-consumers-sensitive-health-info-advertising) — GoodRx 150 万美元罚款、HBNR 首次执法
- [Updated FTC Health Breach Notification Rule — FTC](https://www.ftc.gov/business-guidance/blog/2024/04/updated-ftc-health-breach-notification-rule-puts-new-provisions-place-protect-users-health-apps) — 2024 年规则更新进一步明确纳入健康应用
- [How we're responding to The New York Times' data demands — OpenAI](https://openai.com/index/response-to-nyt-data-demands/) — NYT 诉讼中的用户日志保留令
- [Art. 9 GDPR — Processing of special categories of personal data](https://gdpr-info.eu/art-9-gdpr/) — 健康数据在 GDPR 下属特殊类别
- [Protecting Washingtonians' Personal Health Data and Privacy — Washington State Attorney General](https://www.atg.wa.gov/protecting-washingtonians-personal-health-data-and-privacy) — My Health My Data Act 覆盖 HIPAA 之外的健康数据
- [Microsoft completes acquisition of Nuance — Microsoft](https://news.microsoft.com/source/2022/03/04/microsoft-completes-acquisition-of-nuance-ushering-in-new-era-of-outcomes-based-ai/) — 2022 年 3 月收购完成（官方公告）
- [Nuance Announces General Availability of DAX Copilot Embedded in Epic — PR Newswire](https://www.prnewswire.com/news-releases/nuance-announces-general-availability-of-dax-copilot-embedded-in-epic-transforming-healthcare-experiences-with-automated-clinical-documentation-302037590.html) — DAX Copilot 产品定位与 Epic 集成（官方发布稿）
- [Hackers hit Nuance again in 2017, while NotPetya cost $98 million in lost revenue — Healthcare IT News](https://www.healthcareitnews.com/news/hackers-hit-nuance-again-2017-while-notpetya-cost-98-million-lost-revenue) — NotPetya 停摆与累计财务影响（媒体口径）
- [Nuance 10-Q（2017 财季）— SEC](https://www.sec.gov/Archives/edgar/data/1002517/000100251718000017/nuan1231201710-q.htm) — NotPetya 约 6,800 万美元收入损失与约 2,400 万美元修复成本的官方口径
- [Nuance Communications Settles MOVEit Lawsuit for $8.5 Million — HIPAA Journal](https://www.hipaajournal.com/nuance-communications-moveit-data-breach-settlement/) — MOVEit 泄露波及约 122 万人、850 万美元和解
- [Geisinger Health, Nuance reach $5M settlement over data breach — TechTarget](https://www.techtarget.com/healthtechsecurity/news/366634778/Geisinger-Health-Nuance-reach-5M-settlement-over-data-breach) — 前员工窃取 120 万患者数据、500 万美元和解
- [Lawsuit claims Sharp HealthCare secretly recorded exam room conversations — KPBS](https://www.kpbs.org/news/health/2025/12/11/lawsuit-claims-sharp-healthcare-secretly-recorded-exam-room-conversations-without-patient-consent) — Sharp HealthCare 使用 Abridge 录音的集体诉讼
- [Sutter Health, MemorialCare face class-action lawsuit over AI scribe use — TechTarget](https://www.techtarget.com/healthtechsecurity/news/366641717/Sutter-Health-MemorialCare-face-class-action-lawsuit-over-AI-scribe-use) — 2026 年 4 月 Sutter Health/MemorialCare 被诉

<!-- 待用户确认：开头及 Nuance 一节提到的本人与 Nuance 的合作经历（医患对话自动摘要的幻觉检测）为作者个人经历描述，请确认该合作可公开提及、不涉及雇主内部信息。Nuance 一节的全部事实（产品线、NotPetya 损失、MOVEit 与 Geisinger 和解、录音同意诉讼）均来自公开报道与公开文件，未使用任何内部信息。NotPetya 财务数字已按核查员比对的 SEC 10-Q 口径改写（约 6,800 万美元收入损失 + 约 2,400 万美元修复成本，媒体累计口径约 9,800 万美元）；SEC 与 HHS 页面反爬无法直接抓取，内容以核查员经二手渠道比对的结果为准。 -->
