---
title: "15 亿美元，买不来一个判例"
description: "Anthropic 版权和解案终获法院批准：钱赔的是盗版下载，不是 AI 训练——而行业最需要答案的那个问题，恰恰被这笔钱从法庭上买走了。"
pubDate: 2026-07-20
tags: [ai-copyright, ai-governance, training-data]
lang: zh
slug: anthropic-copyright-settlement-approved
translationOf: anthropic-copyright-settlement-approved
---

7 月 20 日，旧金山联邦地区法院，法官 Araceli Martinez-Olguin 签字批准了 Anthropic 与作家集体诉讼的 15 亿美元和解协议（[TechCrunch](https://techcrunch.com/2026/07/20/anthropics-landmark-1-5b-copyright-settlement-is-approved/)）。这是美国版权史上已知最大的一笔和解金。初步批准是去年 9 月由现已退休的 William Alsup 法官签发的，如今尘埃落定：约 50 万部作品，每部约 3000 美元，超过 91% 的类别成员提交了索赔（[Reuters 通稿](https://wsau.com/2026/07/20/us-judge-approves-anthropics-1-5-billion-settlement-of-copyright-lawsuit/)）。

按理说这是原告的大胜。但当天最耐人寻味的，是不少作家的反应：失望。明面上的不满集中在钱：有人嫌每部约 3000 美元太低，有人抗议 1.01 亿美元的律师费从赔偿池里分走太多；也有人连价格带条款一并不接受，干脆退出和解、另行起诉（[Reuters](https://wsau.com/2026/07/20/us-judge-approves-anthropics-1-5-billion-settlement-of-copyright-lawsuit/)）。但钱只是表层——往下看条款，会发现这份协议给作家的，比金额显示的还要少。

## 这笔钱买断的范围，比看上去窄得多

答案藏在和解条款的三条限制里（[Copyright Alliance 条款说明](https://copyrightalliance.org/participating-bartz-v-anthropic-settlement/)）：

- 豁免只覆盖 **2025 年 8 月 26 日之前**的行为；
- 和解**不构成对未来使用的授权**——Anthropic 拿不到任何继续用这些书的许可；
- **模型输出侵权的索赔被明确排除在外**，作者日后仍可就此起诉。

换句话说，15 亿美元买断的只有一件事：Anthropic 当年从 Library Genesis 和 Pirate Library Mirror 下载盗版书这个历史行为。此外 Anthropic 还须销毁从这两个盗版库下载的全部文件及副本。

而真正决定行业走向的问题——**用受版权保护的书训练大模型，是不是合理使用**——Alsup 在 2025 年 6 月的简易判决里已经回答过了，答案对 AI 公司有利。要看懂这个判决，得把 Anthropic 做的事拆成两步：先拿到书，再用书训练。

**第一步是拿书，合法与否取决于书的来路。** Anthropic 拿书走了两条路：一条是从那两个盗版库直接下载 700 多万本电子书，存成一个内部的「中央图书馆」；另一条是后来花钱买实体书，拆开扫描成电子版。Alsup 判定：买书再扫描属于合理使用——自己花钱买的书，换个格式存起来备用，没问题；违法的是盗版下载——问题不在「建了个库」，而在这个库里的书是偷来的。更糟的是，库里还有大量 Anthropic 自己都决定不用于训练的盗版书，一直原样存着，连「为训练服务」这层辩护都套不上（[Reuters](https://wsau.com/2026/07/20/us-judge-approves-anthropics-1-5-billion-settlement-of-copyright-lawsuit/)）。所以并不存在「存书不行、训练就行」的悖论：为训练而存合法买来的书，本身就是被法院认可的。

**第二步是训练，Alsup 给了 AI 公司最想要的答案：** 用书训练大模型是高度转化性的使用，构成合理使用。只要书的来路干净，拿它训练模型这件事本身不侵权。

把两步拼起来，也就回答了「赔完之后还能不能接着干」：15 亿美元结清的只是 2025 年 8 月 26 日之前的盗版下载旧账，Anthropic 日后若再去盗版库下书，就是新的侵权，不在豁免之内；但它若继续买书、扫描、训练，根本用不着这份和解的保护——Alsup 的判决已经确认这条路合法。

作家们最想推翻的，恰恰是「训练属合理使用」这半句。可和解一签，没人上诉，这个裁定原封不动地留了下来。Anthropic 副总法律顾问 Aparna Sridhar 在声明里特意强调的正是这一点：和解建立在法院确认训练属合理使用的基础之上。

所以这场官司的真实结局是：**Anthropic 赔的是盗版下载，不是 AI 训练。**

## 3000 美元一本，这个数是怎么算出来的

每部 3000 美元不是拍脑袋。锚点是美国版权法的法定赔偿区间（[17 U.S.C. § 504](https://www.law.cornell.edu/uscode/text/17/504)）：一般侵权每部 750 到 3 万美元，故意侵权最高 15 万美元。

把这个区间套在 50 万部已登记作品上，就明白 Anthropic 为什么愿意掏 15 亿：如果陪审团认定故意侵权并顶格判罚，理论敞口是 750 亿美元——对一家公司来说是生存问题。哪怕只按法定下限判，也有 3.75 亿。3000 美元约等于法定下限的四倍：对 Anthropic，这是消除灭顶风险的保险费，分四期付到 2027 年 9 月（[Authors Alliance FAQ](https://www.authorsalliance.org/resources/generative-ai/bartz-v-anthropic-settlement-faq/)）；对单个作者，这笔钱默认还要和出版社五五分（[Authors Guild](https://authorsguild.org/advocacy/artificial-intelligence/what-authors-need-to-know-about-the-anthropic-settlement/)），到手可能只有 1500 美元——这大概就是「历史性和解」与作家们的失望之间的落差。

还有一个容易被忽略的门槛：进入这 50 万部的前提是作品有 ISBN/ASIN **且在规定时限内完成了版权局登记**（[Authors Alliance FAQ](https://www.authorsalliance.org/resources/generative-ai/bartz-v-anthropic-settlement-faq/)）。没登记的书，连被赔的资格都没有。

## 为什么这个「标志性判例」其实不是判例

和解不产生判例效力，这是程序法常识；但这个案子的特殊之处在于，它把一个本来可能成为判例的裁定也一并「封存」了。

Alsup 的合理使用裁定只是地区法院层面的判决，对其他法官只有说服力、没有约束力。正常路径下，这类关键裁定会被上诉到第九巡回法院，形成对整个辖区有约束力的先例。但和解意味着没人上诉——**这个行业最需要权威答案的问题，永远停在了一审**。

后果立竿见影：Google、Meta、Midjourney、OpenAI 都还在被诉，上周大型出版商又对 Google 提了新的训练数据诉讼（[TechCrunch](https://techcrunch.com/2026/07/14/google-faces-another-ai-training-lawsuit-from-major-publishers/)）。每一位主审法官都可以对合理使用问题自由心证，完全不必跟随 Alsup。NYT v. OpenAI 如果走到判决，完全可能给出相反答案。

从机制上看，这几乎是必然的均衡：对 AI 公司，上诉输了是灭顶之灾，赢了也只是省下和解金，风险收益严重不对称，理性选择就是花钱买确定性。于是每个案子都倾向于在形成上诉判例之前和解掉——行业一次次付钱，把规则一次次买出法庭。

## 它没定规则，但定了价

这份和解真正的行业影响，是第一次给训练数据的「合规差价」标了数：

用盗版数据的事后成本，现在有了参考价——每部 3000 美元起，外加销毁数据集、诉讼费用和多年的不确定性。而 Alsup 同一份裁定确认了另一条路合法：Anthropic 后来买入实体书、拆掉扫描用于训练，法院认可这属于合理使用（[TechCrunch](https://techcrunch.com/2026/07/20/anthropics-landmark-1-5b-copyright-settlement-is-approved/)）。一本二手书几美元到几十美元，和 3000 美元的事后账单之间，就是训练数据授权市场的定价空间。只要这个差价存在，批量购买、扫描、与出版商签打包授权，就会从「良心选择」变成财务上的最优解。

据此给三类读者各留一个判断：

**做模型的**：诉讼风险的重心在「数据怎么来的」，不在「数据拿来干什么」。数据溯源记录从工程习惯变成了法务资产——将来被诉时，能证明每本书来路的公司和不能证明的公司，赔付敞口差几个数量级。

**写书的**：这个案子里，版权登记是拿到赔偿的入场券。对美国市场的作者，及时登记从「律师建议」变成了有真金白银差别的动作。

**看行业的**：别盯和解金额，盯上诉法院。只要合理使用问题没在巡回法院层面定音，每个新案子都是重新掷骰子。

15 亿美元买来的是安静，不是规则。对 Anthropic，这是一笔划算的买卖；对行业，训练数据的法律地基还是那块没浇筑的空地——只不过现在，空地上立了一块标价牌。

## 参考来源

- [Anthropic's landmark $1.5B copyright settlement is approved — TechCrunch](https://techcrunch.com/2026/07/20/anthropics-landmark-1-5b-copyright-settlement-is-approved/) — 批准消息、案件背景、买书扫描合法性、其他在诉公司名单
- [US judge approves Anthropic's $1.5 billion settlement of copyright lawsuit — Reuters（WSAU 联合发布版）](https://wsau.com/2026/07/20/us-judge-approves-anthropics-1-5-billion-settlement-of-copyright-lawsuit/) — 批准法官、91% 索赔率、1.01 亿律师费、700 万本盗版书与 Alsup 裁定表述、双方声明、反对者情况
- [Bartz v. Anthropic Settlement FAQ — Authors Alliance](https://www.authorsalliance.org/resources/generative-ai/bartz-v-anthropic-settlement-faq/) — 分期付款时间表、作品资格（ISBN/登记时限）、作者-出版社五五分
- [What Authors Need to Know About the Anthropic Settlement — Authors Guild](https://authorsguild.org/advocacy/artificial-intelligence/what-authors-need-to-know-about-the-anthropic-settlement/) — 约 50 万部作品、每部约 3000 美元
- [What to Know About the Bartz v. Anthropic Settlement — Copyright Alliance](https://copyrightalliance.org/participating-bartz-v-anthropic-settlement/) — 豁免截止 2025-08-26、不含未来授权、排除输出侵权、销毁盗版文件条款
- [Google faces another AI training lawsuit from major publishers — TechCrunch](https://techcrunch.com/2026/07/14/google-faces-another-ai-training-lawsuit-from-major-publishers/) — Google 新诉讼
- [17 U.S.C. § 504 — Cornell LII](https://www.law.cornell.edu/uscode/text/17/504) — 法定赔偿区间
