---
title: "政府嫌太松，白帽嫌太紧：AI 护栏到底在防谁？"
description: "从 Fable 5 被下架 18 天，到漏洞研究员集体转向本地开源权重：两用能力的信任判定，为什么不该压在内容分类器上"
pubDate: 2026-07-24
tags: [ai-safety, cybersecurity]
lang: zh
slug: ai-guardrails-offensive-security-researchers
translationOf: ai-guardrails-offensive-security-researchers
---

2026 年 6 月 12 日美东时间下午 5 点 21 分，Anthropic 收到美国商务部的指令：立即暂停所有外国公民对 Fable 5 和 Mythos 5 的访问，无论对方身在境内还是境外。理由是政府认为发现了一种绕过 Fable 5 安全防护的方法。Anthropic 公开表示不认同——他们复核后认为那只是一个「狭窄的潜在越狱」，复现出的是少量已知的小漏洞，「不应成为召回一款商用模型的理由」（[Anthropic 官方声明](https://www.anthropic.com/news/fable-mythos-access)）——但还是照办了。管制持续约 18 天，6 月 30 日解除（[CNBC](https://www.cnbc.com/2026/06/30/anthropic-says-trump-admin-has-lifted-export-controls-on-claude-fable-5-and-mythos-5.html)）。

六周后，TechCrunch 采访了一批进攻性安全研究员——也就是受雇模拟攻击、替客户找漏洞的白帽——得到的抱怨方向正好相反：护栏不是太松，是太紧，紧到正当的安全工作没法做（[TechCrunch](https://techcrunch.com/2026/07/23/how-ai-guardrails-are-impeding-the-work-of-offensive-cybersecurity-researchers/)）。

同一套护栏，监管者嫌它拦得太少，一线使用者嫌它拦得太多。这不是谁在无理取闹，而是护栏这个机制本身被放在了一个它解不了的题上。

## 白帽的账单

TechCrunch 采访里的抱怨很具体。漏洞研究员 Mark Dowd 的不满在于裁量权：「这些大公司来任意决定安全研究里什么算安全、什么不算——这让我很不舒服。」NCC Group 首席科学家 Chris Anley 解释了为什么白帽绕不开「写攻击代码」这一步：要确认一个漏洞真实可利用，就得实际把利用代码做出来，模型一拒答，受损的是防御方。

Offensive AI Con 创始人 Chris Thompson 的抱怨更工程化：护栏的表现每天都不一样，同样的请求今天过、明天不过，研究员「大量时间花在跟模型讨价还价上」。一位供职于手机零部件厂商的匿名研究员说，因为雇主没进 Anthropic 的认证计划，模型「一旦察觉我们在做跟安全沾边的事，就直接停了」，基本没法用。

结果是用脚投票。Crowdfense 的 CTO Paolo Stagno 说他的团队做漏洞工作根本不用云端模型——怕未披露的漏洞信息经由厂商泄漏——转而在本地跑 GLM 这类没有护栏限制的中国开放权重模型。这是整篇报道里最值得停下来看的一句：护栏的直接后果之一，是把最专业的用户推向了完全没有护栏、厂商也完全看不见的替代品。

## 为什么分类器解不了这道题

护栏的主体是内容层的分类器：看请求和回复的文本，判断该不该拦。但两用（dual-use）能力的麻烦恰恰在于，合法与否的信号不在文本里。

「写出这个缓冲区溢出的利用代码」——受雇渗透测试客户系统的白帽这么问，和真想入侵的人这么问，字面上一模一样。区别在意图和授权：有没有合同、打的是不是自己有权测试的目标。而这些恰恰是分类器从单条 prompt 里读不到的东西。于是它只能退到一个次优策略：按话题的危险度一刀切。凡是沾「漏洞利用」「攻击代码」的就倾向拒答。

这直接决定了误判的分布。对分类器来说，漏报（放过真攻击者）代价极高、极显眼——出一次事就是头条和监管信；误报（拦下合法白帽）代价被摊薄、看不见——研究员被拒答不会上新闻，顶多自己转头去用别的工具。理性的厂商会把阈值调向「宁可错杀」。Thompson 说的「每天表现不一样」也是同一枚硬币：分类器阈值在持续调整，而调整的压力几乎全部来自漏报那一侧。

更麻烦的是，这套逻辑跟模型自身的进步方向是拧着的。厂商宣传新模型「更难被 prompt injection」「更难越狱」，指的是模型更稳地拒绝它判定为恶意的请求。但当「恶意」的判定本身建立在话题而非授权之上时，越稳固的拒绝，对拿不到豁免的合法白帽就越是一堵越来越硬的墙。安全性的提升和对合法用户的可用性，在这个设计下不是正相关。

## 例外通道：已经建了，但补丁不是墙

厂商其实清楚分类器的天花板，两家都搭了「可信研究者例外通道」，思路一致：既然文本里读不出授权，那就在文本之外先把人验明正身。

Anthropic 的叫 Cyber Verification Program（CVP）。它把封禁明确切成两层：一层是「禁止用途」（prohibited use）——勒索软件、恶意软件投递、C2 基础设施这类几乎没有正当防御场景的，对所有人一律封死，认证也不放行；另一层是「高风险两用」（high-risk dual use）——漏洞利用分析、进攻性安全工具开发这类有正当防御用途的，默认拦截，但通过认证的组织可以解锁。申请以组织为单位（绑定 organization ID，不是个人账号），Anthropic 审核，目标是两个工作日内给答复；误拦可以走申诉表（以上均见 [Anthropic 帮助中心](https://support.claude.com/en/articles/14604842-real-time-cyber-safeguards-on-claude-opus-and-sonnet)）。OpenAI 的对应物叫 Trusted Access for Cyber（TAC），同样靠 KYC 和身份验证放行，通过审核的防御者拿到的是「更低的分类器拒答率」，覆盖漏洞识别、恶意软件分析、二进制逆向等工作流（[OpenAI](https://openai.com/index/trusted-access-for-cyber/)；扩容情况见 [CyberScoop](https://cyberscoop.com/openai-expands-trusted-access-for-cyber-to-thousands-for-cybersecurity/)）。

方向是对的：把判定的锚点从「这句话危不危险」挪到「这个组织可不可信」，正是两用问题该有的解法。但 TechCrunch 里的抱怨说明，这个补丁现在还是筛子。

第一，粒度是组织，不是个人。认证绑定 organization ID——那位手机零部件厂商的匿名研究员被卡住，不是因为他不合格，而是因为他雇主整个没进计划。独立研究员、小团队、给多家客户做外包的顾问，恰恰最难满足「以合格组织身份申请」这个前提。而这批人正是漏洞挖掘的主力。

第二，认证只调低拒答率，没根除不一致。TAC 官方措辞是「更低的分类器拒答率」——底层还是那个概率分类器，只是把阈值调松。Thompson 抱怨的「每天表现不一样」在通道内依然存在，只是频率低些。

第三，也是最根本的：例外通道是选择性加入的，而它要防的对象根本不会来申请。CVP、TAC 拦住的是愿意走正门、留下真实身份的白帽；真正的攻击者从不填 KYC 表——他们直接去本地跑开放权重模型，正是 Stagno 团队已经在做的事。于是通道形成一种错配：给守规矩的人设了道门槛，对不守规矩的人一点约束力都没有。

## 给从业者的三个判断

把 6 月的下架和 7 月的抱怨叠在一起看，浮出来的是同一个结构性事实：内容分类器是个天生会误判两用能力的工具，而两个方向的误判正在把它从两头挤压。

**第一，别再指望调分类器阈值能同时满足监管和白帽——这两个诉求在分类器这一层是零和的。**松一格，漏报风险上升，监管侧的压力（乃至 Fable 5 那样的下架）就逼近；紧一格，误报增加，合法白帽被推向不受控的替代品。真正的出路不在阈值刻度上，而在把授权判定移出内容层：身份验证、组织问责、可审计的使用日志——让「谁在用、有没有授权」变成可以核验的信号，而不是让分类器去猜。

**第二，例外通道的设计要专门补上「个人研究者」这一档。**当前 CVP、TAC 都是组织粒度，把独立研究者和外包顾问挡在门外，而他们是漏洞挖掘的主力。可行的方向是引入个人可携带的资质认证（类比其他高风险行业的执业许可），让资质随人走，而不是绑死在雇主的组织账号上。

**第三，认清例外通道的能力边界，别把它当安全护栏。**它是「可用性补丁」——修的是合法用户被误伤的问题；它不是「防扩散护栏」——真正的攻击者绕过它的成本几乎为零（本地开放权重模型触手可及）。把 CVP、TAC 宣传成「防止能力落入坏人之手」是对它的误读。它们真正的价值，是让守规矩的防御者不至于被自家工具反锁在门外——这本身就够重要，但别指望它干超出这个范围的活。

护栏的本意是挡住坏人。可当好人被挡在门外、坏人从没打算走这道门时，该修的或许不是护栏拦得够不够严，而是我们一开始有没有把「拦住坏人」这道题，交给了一个从文本里根本读不出授权的裁判。

## 参考来源

- [How AI guardrails are impeding the work of offensive cybersecurity researchers](https://techcrunch.com/2026/07/23/how-ai-guardrails-are-impeding-the-work-of-offensive-cybersecurity-researchers/)（TechCrunch）—— 研究员受访内容、具体抱怨场景、转向本地 GLM 等开放权重模型
- [Statement on the US government directive to suspend access to Fable 5 and Mythos 5](https://www.anthropic.com/news/fable-mythos-access)（Anthropic 官方）—— 6 月 12 日下架指令的时间、理由、Anthropic 的异议表述
- [Anthropic says Trump admin has lifted export controls on Claude Fable 5 and Mythos 5](https://www.cnbc.com/2026/06/30/anthropic-says-trump-admin-has-lifted-export-controls-on-claude-fable-5-and-mythos-5.html)（CNBC）—— 出口管制约 18 天后于 6 月 30 日解除
- [Real-time cyber safeguards on Claude Opus and Sonnet](https://support.claude.com/en/articles/14604842-real-time-cyber-safeguards-on-claude-opus-and-sonnet)（Anthropic 帮助中心）—— CVP 的两层封禁划分、组织粒度、两个工作日 SLA、申诉机制
- [Introducing Trusted Access for Cyber](https://openai.com/index/trusted-access-for-cyber/)（OpenAI 官方）—— TAC 的 KYC 门槛、「更低分类器拒答率」的表述、覆盖的工作流
- [OpenAI expands Trusted Access for Cyber program](https://cyberscoop.com/openai-expands-trusted-access-for-cyber-to-thousands-for-cybersecurity/)（CyberScoop）—— TAC 扩容至数千组织/个人
