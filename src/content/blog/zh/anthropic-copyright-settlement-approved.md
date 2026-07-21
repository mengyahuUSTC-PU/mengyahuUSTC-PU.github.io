---
title: "15 亿美元，买不来一个判例"
description: "Anthropic 版权和解案终获法院批准：钱赔的是盗版下载，不是 AI 训练——而行业最需要答案的那个问题，恰恰被这笔钱从法庭上买走了。"
pubDate: 2026-07-20
tags: [ai-copyright, ai-governance, training-data]
lang: zh
slug: anthropic-copyright-settlement-approved
translationOf: anthropic-copyright-settlement-approved
---

7 月 20 日，旧金山联邦地区法院，法官 Araceli Martinez-Olguin 签字批准了 Anthropic 与作家集体诉讼的 15 亿美元和解协议（[TechCrunch](https://techcrunch.com/2026/07/20/anthropics-landmark-1-5b-copyright-settlement-is-approved/)）。这是美国版权史上已知最大的一笔和解金（[Reuters](https://www.investing.com/news/stock-market-news/us-judge-approves-anthropics-15-billion-settlement-of-copyright-lawsuit-4801706)）。初步批准是去年 9 月由现已退休的 William Alsup 法官签发的，如今尘埃落定：约 50 万部作品，每部约 3000 美元，超过 91% 的类别成员提交了索赔（[Reuters 通稿](https://wsau.com/2026/07/20/us-judge-approves-anthropics-1-5-billion-settlement-of-copyright-lawsuit/)）。

按理说这是原告的大胜。但批准当天，仍有一些作者向法院提出反对（[Reuters](https://wsau.com/2026/07/20/us-judge-approves-anthropics-1-5-billion-settlement-of-copyright-lawsuit/)）。不满集中在钱：有人嫌每部约 3000 美元太低，有人抗议 1.01 亿美元的律师费从赔偿池里分走太多；也有人连价格带条款一并不接受，干脆退出和解、另行起诉。但钱只是表层——往下看条款，会发现这份协议给作家的，比金额显示的还要少。

## 这笔钱买断的范围，比看上去窄得多

和解条款里写着三条限制（[Copyright Alliance 条款说明](https://copyrightalliance.org/participating-bartz-v-anthropic-settlement/)）：

- 豁免只覆盖 **2025 年 8 月 26 日之前**的行为；
- 和解**不构成对未来使用的授权**——Anthropic 拿不到任何继续用这些书的许可；
- **模型输出侵权的索赔被明确排除在外**，作者日后仍可就此起诉。

换句话说，这份豁免结清的是旧账：Anthropic 当年从 Library Genesis 和 Pirate Library Mirror 下载盗版书，以及 2025 年 8 月 26 日之前用这些合格作品做训练、研究和产品开发可能引发的索赔（[Copyright Alliance](https://copyrightalliance.org/participating-bartz-v-anthropic-settlement/)）。此外 Anthropic 还须销毁从这两个盗版库下载的全部文件及副本。

而真正决定行业走向的问题——**用受版权保护的书训练大模型，是不是合理使用**——Alsup 在 2025 年 6 月的简易判决里已经回答过了，答案对 AI 公司有利。要看懂这个判决，得把 Anthropic 做的事拆成两步：先拿到书，再用书训练。

**第一步是拿书，合法与否取决于书的来路。** Anthropic 拿书走了两条路：一条是从那两个盗版库直接下载 700 多万本电子书，存成一个内部的「中央图书馆」；另一条是后来花钱买实体书，拆开扫描成电子版、销毁原书。Alsup 判定：买书再扫描属于合理使用——自己花钱买的书，换个格式存起来备用，没问题；从盗版库下载则不构成合理使用，这部分的侵权责任和赔偿本要留给陪审团审理，和解让庭审没有开场。更糟的是，库里还有大量 Anthropic 自己都决定不用于训练的盗版书，一直原样存着，连「为训练服务」这层辩护都套不上（[Reuters](https://wsau.com/2026/07/20/us-judge-approves-anthropics-1-5-billion-settlement-of-copyright-lawsuit/)）。可见法院划的线不在「建了个库」，而在库里的书是买来的还是偷来的：为训练而存合法买来的书，本身就被法院认可。

**第二步是训练，Alsup 给了 AI 公司最想要的答案：** 就本案涉案作品和训练方式而言，用书训练大模型是高度转化性的使用，构成合理使用。也就是说，在这个案子里，法院认为问题出在书的来路上，而不在训练本身。

把两步拼起来，这份和解的边界就清楚了：15 亿美元结清的是 2025 年 8 月 26 日之前的旧账，Anthropic 日后若再去盗版库下书，就是新的侵权，不在豁免之内；它若继续买书、扫描、训练，倚仗的也不是这份和解，而是 Alsup 的裁定——不过裁定裁的是本案的具体事实，换了做法或换了争议点（比如模型输出），仍可能引来新的诉讼。

作家们最想推翻的，恰恰是「训练属合理使用」这半句。可和解一签，没人上诉，这个裁定原封不动地留了下来。Anthropic 副总法律顾问 Aparna Sridhar 在声明里特意强调的正是这一点：和解建立在法院确认训练属合理使用的基础之上（[Reuters](https://wsau.com/2026/07/20/us-judge-approves-anthropics-1-5-billion-settlement-of-copyright-lawsuit/)）。

所以这场官司的真实结局是：**驱动这 15 亿赔偿的是盗版下载，不是 AI 训练。**

## 3000 美元一本，这个数是怎么算出来的

每部 3000 美元不是拍脑袋。锚点是美国版权法的法定赔偿区间（[17 U.S.C. § 504](https://www.law.cornell.edu/uscode/text/17/504)）：一般侵权每部 750 到 3 万美元，故意侵权最高 15 万美元，具体数额由法院在区间内酌定，「故意」还须原告另行证明。

把这个区间套在 50 万部已登记作品上，就明白 Anthropic 为什么愿意掏 15 亿：如果陪审团认定故意侵权并顶格判罚，理论敞口是 750 亿美元——对一家公司来说是生存问题。哪怕只按法定下限判，也有 3.75 亿。3000 美元约等于法定下限的四倍：对 Anthropic，这是消除灭顶风险的保险费，分四期付到 2027 年 9 月（[Authors Guild](https://authorsguild.org/advocacy/artificial-intelligence/what-authors-need-to-know-about-the-anthropic-settlement/)）；对单个作者，这笔钱默认还要和出版社五五分（[Authors Guild](https://authorsguild.org/advocacy/artificial-intelligence/what-authors-need-to-know-about-the-anthropic-settlement/)），名义上剩 1500 美元，再扣掉管理费用等实际到手还会更少——这大概就是「历史性和解」与作家们的失望之间的落差。

还有一个容易被忽略的门槛：进入这 50 万部的前提是作品有 ISBN/ASIN **且在规定时限内完成了版权局登记**（[Authors Guild](https://authorsguild.org/advocacy/artificial-intelligence/what-authors-need-to-know-about-the-anthropic-settlement/)）。没登记的书，连被赔的资格都没有。

## 为什么这个「标志性判例」其实不是判例

和解不产生判例效力，这是程序法常识；但这个案子的特殊之处在于，它把一个本来可能成为判例的裁定也一并「封存」了。

Alsup 的合理使用裁定只是地区法院层面的判决，对其他法官只有说服力、没有约束力。正常路径下，这类关键裁定会被上诉到第九巡回法院——巡回法院的已发布判决对辖区内所有法院有约束力（[Ninth Circuit](https://www.ca9.uscourts.gov/decisions)）。但和解意味着没人上诉——**这个行业最需要权威答案的问题，在本案里停在了一审**；要等别的案子把它送上巡回法院，才可能有约束性的答案。

后果立竿见影：Google、Meta、Midjourney、OpenAI 都还在被诉，上周大型出版商又对 Google 提了新的训练数据诉讼（[TechCrunch](https://techcrunch.com/2026/07/14/google-faces-another-ai-training-lawsuit-from-major-publishers/)）。每一位主审法官都可以对合理使用问题自由心证，完全不必跟随 Alsup。NYT v. OpenAI 至今还陷在证据开示的缠斗里（[TechCrunch](https://techcrunch.com/2026/07/09/new-york-times-says-openai-hid-evidence-in-chatgpt-copyright-trial/)），一旦走到判决，完全可能给出相反答案。

从机制上看，走到和解并不意外。关键在于，「和解」与「败诉判例」是两种完全不同的结局——区别不在赔不赔钱，而在赔多少、按谁的规矩赔、以后还能不能接着干。

和解金是谈出来的打折价，且只结这一个案子的账。15 亿听着惊人，放在 750 亿的理论顶格敞口旁边只有 2%。原告肯打这个折，是因为在没有判例的现状下，他们自己也可能输——合理使用悬而未决，换一个法官可能判 Anthropic 全赢，作家一分钱拿不到。这份不确定性，就是 AI 公司谈判桌上最大的筹码。

败诉判例则会把这个筹码没收。假设本案不和解、一路打完上诉，第九巡回法院推翻「训练=合理使用」，那么从判决之日起，辖区内的法院在同一法律问题上都须遵循这个结论。下一批作者起诉任何一家 AI 公司时，被告最硬的一道抗辩就没了——原告仍要逐案证明权属、复制事实、登记和损害，「故意」也要另行举证，和解也仍会发生，但天平已经倒向原告：不确定性折扣大幅缩水，要价可以贴着法定区间（故意侵权每部最高 15 万美元）去谈。同样是赔钱，两种赔法差得远：没判例时，赔的是带不确定性折扣的价，一案一结；有判例后，每个后来的原告手里都多了同一件武器。

而败诉的代价还不止钱。若上诉法院认定训练侵权，Anthropic 可能面临包括禁令在内的救济——禁令的范围要看具体作品、模型和衡平因素，未必是「停用全部模型」，但矛头指向的是「用书训练模型」这条路本身，此后每一次训练都可能要先逐一拿到授权。把这笔账摆出来，就是一个不对称的赌局：上诉赢了，省下的主要是和解金；上诉输了，赌上的可能是商业模式。这是我从公开信息做的机制推演——真实决策还牵涉胜诉概率、禁令标准、诉讼成本等外界看不到的变量——但它至少能解释，为什么双方都愿意在这里停手：花钱买确定性。

如果这个逻辑成立，类似案件就都有在形成上诉判例之前和解掉的动力：反复被诉、反复和解，每次付的都是打过折的价；而一场败诉，付的是全价，外加禁令风险，外加给所有后来的原告递上同一件武器。本案是不是个例，要看后面这批诉讼怎么收场。

## 它没定规则，但定了价

这份和解真正的行业影响，是给训练数据的「合规差价」标出了一个看得见的数。

用盗版数据的事后成本，现在有了一个可参照的量级——本案折算下来每部约 3000 美元。要说明的是，这是和解谈出来的毛额，不是法院定的最低赔偿，更不是未来案件的法定起价；但加上销毁数据集、诉讼费用和多年的不确定性，这笔账已经够清楚了。而 Alsup 的裁定确认了另一条路在本案中合法：Anthropic 买入实体书、拆开扫描、销毁原书，法院认定这是格式转换——自己花钱买断的纸书换成电子版自用，市面上流通的副本一本没多，属于合理使用（[裁定原文](https://copyrightalliance.org/wp-content/uploads/2025/06/Bartz-v.-Anthropic-Order.pdf)）。

不过这条「合法路径」的边界，比很多报道暗示的窄。它不是「任何公司买一份任何作品就能拿来训练」的通用许可，有三层限定不能略过：

- **它不是全行业通行证。** 这是地区法院一审裁定，对其他法官只有说服力、没有约束力。别家 AI 公司照做，被诉时仍要重新说服自己的主审法官接受同样的分析。
- **它只裁了「买纸书、扫描、销毁原书」这一种做法。** 合理使用在这里成立的关键，是花钱买断的实体副本被数字副本一比一替换，没有多出任何副本。买电子书是另一回事：电子书一般按许可协议售卖，能不能复制、能不能用于文本挖掘取决于具体条款，这条路 Alsup 没有裁过，本案裁定帮不上忙。
- **电影、音乐更不能照搬。** 合理使用是逐案权衡的抗辩，不是一条通用规则；换了作品类型，分析可能完全不同——「对原作潜在市场的影响」本就是合理使用四要素之一（[17 U.S.C. § 107](https://www.law.cornell.edu/uscode/text/17/107)），影视、音乐素材存在成熟的授权交易市场，这一要素未必还向使用方倾斜。而且买来的 DVD、蓝光普遍带数字加密（DVD 的 CSS、蓝光的 AACS 都在版权局反规避规则的覆盖范围内，[37 CFR § 201.40](https://www.copyright.gov/title37/201/37cfr201-40.html)），绕过加密提取视频和音频，可能违反 DMCA 的反规避条款（[17 U.S.C. § 1201](https://www.law.cornell.edu/uscode/text/17/1201)）——这是独立于版权侵权之外的另一项违法，普通的合理使用抗辩在这里帮不上忙，只有版权局每三年一轮公布的少数豁免（比如非营利机构研究者的文本与数据挖掘豁免）是例外。

所以准确的说法是：买书扫描这条路，在这个案子里被一位法官认可了一次——它是一个可参照的样板，不是一张通用许可证。但即便打上这些折扣，差价的逻辑仍然成立：正常买一本书的价钱，和每部约 3000 美元的事后账单之间，隔着的就是训练数据授权市场的定价空间。只要这个差价存在，批量购买、扫描、与出版商签打包授权，就很可能从「良心选择」变成财务上更划算的选择——这是推断，不是已经发生的行业事实，但账面的方向不难看出来。

据此给三类读者各留一个判断：

**AI 公司**：本案把「数据怎么来的」变成了最先被清算的问题，但「拿来干什么」的仗还在后面——输出侵权的索赔被和解明确保留。数据溯源记录从工程习惯变成了法务资产：将来被诉时，能证明每本书来路的公司，抗辩的起点完全不同。

**作者**：这个案子里，版权登记是拿到赔偿的入场券。对美国市场的作者，及时登记从「律师建议」变成了有真金白银差别的动作。

**行业观察者**：别盯和解金额，盯上诉法院。只要合理使用问题没在巡回法院层面定音，每个新案子都是重新掷骰子。

15 亿美元买来的是安静，不是规则。对 Anthropic，这是一笔划算的买卖；对行业，训练数据的法律地基还是那块没浇筑的空地——只不过现在，空地上立了一块标价牌。

## 参考来源

- [Anthropic's landmark $1.5B copyright settlement is approved — TechCrunch](https://techcrunch.com/2026/07/20/anthropics-landmark-1-5b-copyright-settlement-is-approved/) — 批准消息、案件背景、买书扫描合法性、其他在诉公司名单
- [US judge approves Anthropic's $1.5 billion settlement of copyright lawsuit — Reuters（WSAU 联合发布版）](https://wsau.com/2026/07/20/us-judge-approves-anthropics-1-5-billion-settlement-of-copyright-lawsuit/) — 批准法官、91% 索赔率、1.01 亿律师费、700 万本盗版书与 Alsup 裁定表述、双方声明、反对者情况
- [US judge approves Anthropic's $1.5 billion settlement — Reuters（Investing.com 联合发布版）](https://www.investing.com/news/stock-market-news/us-judge-approves-anthropics-15-billion-settlement-of-copyright-lawsuit-4801706) — 「美国版权案件已知最大和解」表述、Sridhar 声明原文
- [Bartz v. Anthropic 合理使用裁定原文（2025-06-23，Alsup 法官）— Copyright Alliance 存档](https://copyrightalliance.org/wp-content/uploads/2025/06/Bartz-v.-Anthropic-Order.pdf) — 买纸书扫描并销毁原书的格式转换分析、训练构成合理使用、盗版下载不构成合理使用
- [What Authors Need to Know About the Anthropic Settlement — Authors Guild](https://authorsguild.org/advocacy/artificial-intelligence/what-authors-need-to-know-about-the-anthropic-settlement/) — 约 50 万部作品、每部约 3000 美元、分期付款时间表（末期 2027-09-25）、作品资格（ISBN/ASIN 与登记时限）、作者-出版社五五分
- [Bartz v. Anthropic Settlement FAQ — Authors Alliance](https://www.authorsalliance.org/resources/generative-ai/bartz-v-anthropic-settlement-faq/) — 未登记作品不具赔偿资格
- [What to Know About the Bartz v. Anthropic Settlement — Copyright Alliance](https://copyrightalliance.org/participating-bartz-v-anthropic-settlement/) — 豁免截止 2025-08-26 及所涵盖的过往训练/研究/产品开发索赔、不含未来授权、排除输出侵权、销毁盗版文件条款
- [Google faces another AI training lawsuit from major publishers — TechCrunch](https://techcrunch.com/2026/07/14/google-faces-another-ai-training-lawsuit-from-major-publishers/) — Google 新诉讼
- [New York Times says OpenAI hid evidence in ChatGPT copyright trial — TechCrunch](https://techcrunch.com/2026/07/09/new-york-times-says-openai-hid-evidence-in-chatgpt-copyright-trial/) — NYT v. OpenAI 仍在证据开示阶段
- [Opinions — Ninth Circuit](https://www.ca9.uscourts.gov/decisions) — 巡回法院已发布判决的约束力
- [17 U.S.C. § 107 — Cornell LII](https://www.law.cornell.edu/uscode/text/17/107) — 合理使用四要素
- [17 U.S.C. § 504 — Cornell LII](https://www.law.cornell.edu/uscode/text/17/504) — 法定赔偿区间
- [17 U.S.C. § 1201 — Cornell LII](https://www.law.cornell.edu/uscode/text/17/1201) — DMCA 反规避条款
- [37 CFR § 201.40 — 美国版权局](https://www.copyright.gov/title37/201/37cfr201-40.html) — DVD（CSS）/蓝光（AACS）反规避豁免规则
