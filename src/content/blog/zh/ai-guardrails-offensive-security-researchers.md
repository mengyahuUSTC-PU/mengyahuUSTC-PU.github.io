---
title: "政府嫌太松，安全研究员嫌太紧：AI 护栏到底在防谁？"
description: "从 Fable 5 被下架 18 天，到漏洞研究员集体转向本地开源权重：两用能力的信任判定，为什么不该压在内容分类器上"
pubDate: 2026-07-24
tags: [ai-safety, cybersecurity]
lang: zh
slug: ai-guardrails-offensive-security-researchers
translationOf: ai-guardrails-offensive-security-researchers
---

2026 年 6 月 12 日美东时间下午 5 点 21 分，Anthropic 收到美国商务部的指令：立即暂停所有外国公民对 Fable 5 和 Mythos 5 的访问，无论对方身在境内还是境外。理由是政府认为发现了一种绕过 Fable 5 安全防护的方法。Anthropic 公开表示不认同——他们复核后认为那只是一个「狭窄的潜在越狱」，复现出的是少量已知的小漏洞，「不应成为召回一款商用模型的理由」（[Anthropic 官方声明](https://www.anthropic.com/news/fable-mythos-access)）——但还是照办了。管制持续约 18 天，6 月 30 日解除（[CNBC](https://www.cnbc.com/2026/06/30/anthropic-says-trump-admin-has-lifted-export-controls-on-claude-fable-5-and-mythos-5.html)）。

六周后，TechCrunch 采访了一批进攻性安全研究员——也就是受雇模拟攻击、替客户找漏洞的人——得到的抱怨方向正好相反：护栏不是太松，是太紧，紧到正当的安全工作没法做（[TechCrunch](https://techcrunch.com/2026/07/23/how-ai-guardrails-are-impeding-the-work-of-offensive-cybersecurity-researchers/)）。

同一套护栏，监管者嫌它拦得太少，一线使用者嫌它拦得太多。这个两头挨骂的处境，我再熟悉不过——我的本职工作就是内容审核（content moderation），同一个模型，有人抱怨误报（false positive，正常内容被误拦），有人抱怨漏报（false negative，该拦的没拦住），这就是日常。所以我不觉得是哪一方在无理取闹，而是护栏这个机制本身被放在了一道它解不了的题上。这道题也从来不只属于安全圈，安全场景只是把它推到了赌注最高、矛盾最公开的地方。

## 安全研究员的账单

TechCrunch 采访里的抱怨很具体。漏洞研究员 Mark Dowd 的不满在于裁量权：「这些大公司来任意决定安全研究里什么算安全、什么不算——这让我很不舒服。」NCC Group 首席科学家 Chris Anley 解释了为什么安全研究员绕不开这一步：让模型实际尝试利用一个漏洞，是确认它真实存在、可被利用的关键环节，模型一拒答，受损的是防御方。

Offensive AI Con 创始人 Chris Thompson 的抱怨则落在稳定性上：护栏的表现每天都不一样，同样的请求今天过、明天不过，研究员「大量时间花在跟模型讨价还价上」。一位供职于手机零部件厂商的匿名研究员说，因为雇主没进 Anthropic 的认证计划，模型「一旦察觉我们在做跟安全沾边的事，就直接停了」，基本没法用。

结果是用脚投票。Crowdfense 的 CTO Paolo Stagno 说，他的团队在漏洞挖掘和利用开发环节不用云端模型——怕未披露的漏洞信息经由厂商泄漏——改在本地跑开源模型；逆向工程这类环节，他们仍在用云端的前沿模型。Thompson 则点名了研究员被推向的方向：GLM 这类可以免费下载、本地运行、不受云端认证和使用限制约束的中国开放权重模型。这是整篇报道里最值得停下来看的一处：护栏的直接后果之一，是把最专业的用户推向了厂商完全看不见的替代品。

## 为什么分类器解不了这道题

厂商的防护从来不止一层：安全训练、实时监控、账号执行、访问控制都在清单上（[Anthropic](https://www.anthropic.com/news/building-safeguards-for-claude)）。但研究员日常撞上的那道墙，主要是内容层的分类器——看请求和回复的文本，判断该不该拦。而两用（dual-use）能力的麻烦恰恰在于，合法与否的信号不在文本里。

「写出这个缓冲区溢出的利用代码」——受雇给客户做渗透测试的安全研究员这么问，和真想入侵的人这么问，字面上一模一样。区别在意图和授权：有没有合同、打的是不是自己有权测试的目标。这一点连 OpenAI 自己都承认：网络安全工具天生两用，访问权限该取决于使用者是谁、怎么用、有什么信任信号（[OpenAI](https://openai.com/index/trusted-access-for-cyber/)）。而这些都是分类器从单条 prompt 里读不到的东西。厂商也在分类器之外叠加意图推断、对话上下文这类辅助信号，但落到高风险话题上，实际的取向仍是从严：凡是沾「漏洞利用」「攻击代码」的就倾向拒答。

把镜头拉远，这个困境并不是网络安全独有，而是内容审核这类分类任务的通病——也是我每天工作里反复面对的题。判断图片里有没有一只猫，答案客观存在；判断一句话算不算「性暗示」、露骨到什么程度该拦，类别边界是人划出来的——两个极端人人意见一致，中间隔着大片模糊地带。对仇恨言论、冒犯性内容这类主观任务的研究早就发现，标注员之间的分歧是系统性的，反映的是各自的价值观和视角，而把标注聚合成单一的标准答案（ground truth，即模型学习所依据的正确标签）反而会把这些分歧掩盖掉（[TACL 2022](https://aclanthology.org/2022.tacl-1.6/)）。模型训练得再好，学的也只是一条本来就画不清的线。

语境和提问者身份同样在改变答案：专职红队——受雇故意发送最出格的内容、检验防线牢不牢的人——发再露骨的东西也是正当用途，而这个信息在文字里一个字都读不到。再往深一层，就算分类器把厂商自己写下的定义执行到满分，也满足不了所有人：用户基数一大，每个人对同一条内容的接受度都不一样，一套全局统一的审核标准注定同时收到「太松」和「太紧」两个方向的抱怨。两用能力只是把这套通病推到了极端：合法与恶意的文本可以一字不差，而两个方向误判的代价都被放大到了头条级别。

这直接决定了误判的分布。就我在审核一线的体会，日常里绝大多数抱怨来自误报——大部分用户只关心自己要的答案有没有拿到，被拦一次就是一次投诉；漏报的声音要少得多。但两边的分量完全不对称：误报再多，研究员被拒答很难成为新闻，顶多转头去用别的工具；漏报只要出一次事，就可能是头条和监管压力——6 月那道下架令就是现成的例子。声音大的没分量，有分量的不出声，在这个激励结构下，厂商把阈值往「宁可错杀」的方向调，是顺理成章的选择。Thompson 说的「每天表现不一样」，多半也是这枚硬币的另一面——他只描述了现象，没有说成因，但按上面的不对称推演，一个合理的解释是分类器在持续调整，而调整的压力主要来自漏报那一侧。

更麻烦的是，这套逻辑跟模型自身的进步方向是拧着的。厂商宣传新模型「更难被 prompt injection」「更难越狱」，指的是模型更稳地拒绝它判定为恶意的请求。但当「恶意」的判定本身建立在话题而非授权之上时，越稳固的拒绝，对拿不到豁免的合法研究员就越是一堵越来越硬的墙。安全性的提升和对合法用户的可用性，在这个设计下不是正相关。

## 例外通道：已经建了，但补丁不是墙

厂商其实清楚分类器的天花板，两家都搭了「可信研究者例外通道」，思路一致：既然文本里读不出授权，那就在文本之外先把人验明正身。

Anthropic 的叫 Cyber Verification Program（CVP）。它把封禁明确切成两层：一层是「禁止用途」（prohibited use）——勒索软件、恶意软件投递、C2 基础设施这类几乎没有正当防御场景的，对所有人一律封死，认证也不放行；另一层是「高风险两用」（high-risk dual use）——漏洞利用分析、进攻性安全工具开发这类有正当防御用途的，默认拦截，但通过认证的组织可以解锁。申请以组织为单位（绑定 organization ID，不是个人账号），Anthropic 审核，目标是两个工作日内给答复；误拦可以走申诉表（以上均见 [Anthropic 帮助中心](https://support.claude.com/en/articles/14604842-real-time-cyber-safeguards-on-claude-opus-and-sonnet)）。OpenAI 的对应物叫 Trusted Access for Cyber（TAC），同样靠 KYC 和身份验证放行，通过审核的防御者拿到的是「更低的分类器拒答率」，覆盖漏洞识别、恶意软件分析、二进制逆向等工作流（[OpenAI](https://openai.com/index/trusted-access-for-cyber/)；扩容情况见 [CyberScoop](https://cyberscoop.com/openai-expands-trusted-access-for-cyber-to-thousands-for-cybersecurity/)）。

方向是对的：把判定的锚点从「这句话危不危险」挪到「这个组织可不可信」，正是两用问题该有的解法。但 TechCrunch 里的抱怨说明，这个补丁现在还是筛子。

第一，CVP 的粒度是组织，不是个人。认证绑定 organization ID——那位手机零部件厂商的匿名研究员被卡住，不是因为他不合格，而是因为他雇主整个没进计划。独立研究员、小团队、给多家客户做外包的顾问，恰恰最难满足「以合格组织身份申请」这个前提，而他们是漏洞研究生态里不可忽视的一部分。OpenAI 在这一点上走得远些：TAC 已向个人开放申请，其覆盖对象就包括数千名个人研究者（[CyberScoop](https://cyberscoop.com/openai-expands-trusted-access-for-cyber-to-thousands-for-cybersecurity/)）。

第二，认证只调低拒答率，没根除不一致。TAC 官方措辞是「更低的分类器拒答率」——底层还是那个概率分类器，只是把阈值调松；OpenAI 也明确说明，通过认证并不移除全部防护和拒答（[OpenAI 帮助中心](https://help.openai.com/en/articles/20001259-trusted-access-for-cyber-common-issues-and-troubleshooting)）。Thompson 抱怨的「每天表现不一样」在通道内依然存在，只是频率低些。

第三，也是最根本的：例外通道靠的是自愿申请，而它要防的对象没有理由来申请。CVP、TAC 验的是愿意走正门、留下真实身份的人；不打算守规矩的人大可绕开这道门，直接下载开放权重模型在本地跑——连 Stagno 这样目的完全正当的团队，出于保密考虑都已经走上这条技术路径，这条路的门槛可想而知。于是通道形成一种错配：对守规矩的人是道门槛，对不守规矩的人约束有限。

## 这道题有解吗？

先把最不舒服的答案摆出来——这也是我做内容审核最深的体会：在内容分类这一层，没有解，只有管理。堵死「做对」这条路的不是工程投入不够，而是三件叠在一起的事。定义本身没有唯一答案——模糊地带里连人类标注员都达不成一致，模型没有标准答案可学。关键信号不在文本里——意图、授权、语境决定同一段文字是攻击还是测试，而分类器只看得到文字。标准因人而异——就算把厂商自己的定义执行到满分，不同用户的接受度也不同，全局统一的标准注定两头挨骂。何况模型本身还有误差。这三条任何一条单独成立，这道题就没有精确解；现实是三条同时成立。

承认无解不等于无事可做，它只是把目标换掉了：不再问「怎么让分类器判对」，改问「每一类误判由谁承担、怎么兜底」。把 6 月的下架和 7 月的抱怨叠在一起看，这个新问题在当下有三个具体的落点。

**第一，别再指望调分类器阈值能同时满足监管和安全研究员——这两个诉求在分类器这一层是零和的。**松一格，漏报风险上升，监管侧的压力（乃至 Fable 5 那样的下架）就逼近；紧一格，误报增加，合法研究员被推向不受控的替代品。真正的出路不在阈值刻度上，而在把授权判定移出内容层：身份验证、组织问责、可审计的使用日志——让「谁在用、有没有授权」变成可以核验的信号，而不是让分类器去猜。同一个原则也适用于两用之外的普通审核场景：不同客户对内容的接受度，厂商在全局层面根本无从知道，那就守住法律和灾难性滥用的底线，把底线之上的松紧开放给部署方按自己的用户群配置——把每个判定交给离信息最近的那一层，而不是让一个全局分类器替所有人拿主意。这不会让模糊地带消失，但至少让画线的人换成了最了解自己用户的人。

**第二，「个人研究者」这一档，两家给的答案不一样，但都还没到位。**CVP 只认组织，把独立研究者和外包顾问挡在门外；TAC 已向个人开放，靠 KYC 验明身份。但身份验证解决的只是「你是谁」，回答不了审核真正要回答的「这个人会不会起坏心」——意图没有任何可核验的凭据，过往清白也不担保将来。所以我更看好的补充路径，不是让厂商自己去猜人心，而是借用行业已有的信誉机制——执业认证、公开的漏洞披露记录（CVE 署名、bug bounty 履历）这类由第三方长期积累的信号，厂商只验证书、不判意图。这是一条政策建议，不是已被验证的方案；而且得接受个人通道天生比组织通道难兜底——组织出了事有明确的担责主体，个人没有——只能靠可审计的使用日志和随时可撤销的访问在事后补救。

**第三，认清例外通道的能力边界。**身份验证、使用日志、组织问责本身是实打实的安全机制，两家官方也都把它们列为降低误用风险的层级之一。但这些机制约束的只是走进这道门的人：对根本不打算走正门的人，开放权重模型是一条现成的绕行路线——自行部署要花硬件和工程功夫，但对有能力发起攻击的人算不上高墙。所以这条通道最确定的价值，是让守规矩的防御者不至于被自家工具反锁在门外；这本身就够重要，只是「防止能力落入坏人之手」的担子，不能压在它身上。

护栏的本意是挡住坏人。可当好人被挡在门外、坏人从没打算走这道门时，该修的就不只是拦截的松紧。这个裁判天生读不到它最需要的证据——授权、意图、每个用户各自的尺度。能做的不是把它调成完美，而是把它管不了的判定挪到有信息的那一层，再给它必然犯下的错留好申诉和撤销的后路。分类器守不住这道门，从来不是因为它不够努力，而是我们把一道需要看见人的题，交给了一个只能看见字的裁判。

## 参考来源

- [How AI guardrails are impeding the work of offensive cybersecurity researchers](https://techcrunch.com/2026/07/23/how-ai-guardrails-are-impeding-the-work-of-offensive-cybersecurity-researchers/)（TechCrunch）—— 研究员受访内容、具体抱怨场景、转向本地开源模型与 GLM 等开放权重模型
- [Statement on the US government directive to suspend access to Fable 5 and Mythos 5](https://www.anthropic.com/news/fable-mythos-access)（Anthropic 官方）—— 6 月 12 日下架指令的时间、理由、Anthropic 的异议表述
- [Anthropic says Trump admin has lifted export controls on Claude Fable 5 and Mythos 5](https://www.cnbc.com/2026/06/30/anthropic-says-trump-admin-has-lifted-export-controls-on-claude-fable-5-and-mythos-5.html)（CNBC）—— 出口管制约 18 天后于 6 月 30 日解除
- [Building safeguards for Claude](https://www.anthropic.com/news/building-safeguards-for-claude)（Anthropic 官方）—— 多层防护体系：政策、训练、测试、实时分类器与账号执行、持续监控
- [Real-time cyber safeguards on Claude Opus and Sonnet](https://support.claude.com/en/articles/14604842-real-time-cyber-safeguards-on-claude-opus-and-sonnet)（Anthropic 帮助中心）—— CVP 的两层封禁划分、组织粒度、两个工作日 SLA、申诉机制
- [Introducing Trusted Access for Cyber](https://openai.com/index/trusted-access-for-cyber/)（OpenAI 官方）—— TAC 的 KYC 门槛、「更低分类器拒答率」的表述、覆盖的工作流、对工具「天生两用」的表述
- [Trusted Access for Cyber - Common Issues and Troubleshooting](https://help.openai.com/en/articles/20001259-trusted-access-for-cyber-common-issues-and-troubleshooting)（OpenAI 帮助中心）—— 认证不移除全部防护和拒答
- [OpenAI expands Trusted Access for Cyber program](https://cyberscoop.com/openai-expands-trusted-access-for-cyber-to-thousands-for-cybersecurity/)（CyberScoop）—— TAC 扩容至数千组织/个人
- [Dealing with Disagreements: Looking Beyond the Majority Vote in Subjective Annotations](https://aclanthology.org/2022.tacl-1.6/)（TACL 2022）—— 主观标注任务中标注者的系统性分歧、单一 ground truth 掩盖视角差异
