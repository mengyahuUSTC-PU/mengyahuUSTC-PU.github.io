---
title: "Hassabis 退居二线,Jeff Dean 出走:谷歌把 AI 的方向盘交给了谁?"
description: "谷歌 AI 权力重组:Hassabis 卸任 CEO,Jeff Dean 携三位老将创办 Discovery Loop。拆解重组后安全治理话语权的去向,以及新公司与 DeepMind 安全框架的一个耐人寻味的对照。"
pubDate: 2026-08-05
tags: [ai-governance, google-deepmind, ai-safety]
lang: zh
slug: google-ai-leadership-reshuffle
translationOf: google-ai-leadership-reshuffle
---

2026 年 8 月 5 日,Sundar Pichai 在谷歌官方博客发了一篇[公告](https://blog.google/company-news/inside-google/message-ceo/next-chapter-ai-momentum/),一天官宣两件大事:Demis Hassabis 卸任 Google DeepMind CEO,转任 DeepMind 董事长兼 Alphabet 首席科学家;1999 年加入、在谷歌待了 27 年的 Jeff Dean 离职,与 Sanjay Ghemawat、Oriol Vinyals、Quoc Le 一起创办新公司 Discovery Loop(创始公告[发在 X 上](https://x.com/JeffDean/status/2085034604172603724),官方仅在 X 公告)。Pichai 给整篇公告定的调子是加速:"We have to accelerate all this work and stay focused on the AI frontier."

我把公告原文通读了一遍,专门搜了 safety 和 responsibility 两个词:全文一次都没出现。人事公告本来就不是安全文件,这件事单独看说明不了太多。但交出日常管理权的这个人,恰好是所有大厂 AI 掌门里公开谈 AGI 安全最多的一位。安全议题在谷歌 AI 决策桌上的座次会不会变,是这次重组最值得盯的问题。

## 这次到底动了什么

接手的人是 Koray Kavukcuoglu。他 2012 年加入 DeepMind,是 DQN、WaveNet 这批标志性工作的作者之一,后来做到 CTO。2025 年 6 月,他已经被任命为谷歌历史上第一位 Chief AI Architect,搬到山景城、直接向 Pichai 汇报([Semafor](https://www.semafor.com/article/06/11/2025/google-names-new-chief-ai-architect-to-advance-developments)),那个职位的使命写得很直白:让模型更快变成产品。这次重组后,他以 Google DeepMind SVP 的身份统管 Gemini 模型开发、前沿 AI 研究、Gemini 应用和开发者团队,继续向 Pichai 汇报。

一句话概括:研究、模型、产品三条线并进了一个人手里,而这个人过去一年的职务使命就是加速产品化。公告里挑出来展示的数字也在强调同一个方向:Gemini 应用月活超 9.5 亿,Gemma 系列模型下载超 9 亿。

Hassabis 的新位置在运营链条之外。董事长不管日常,首席科学家是影响力职位,两者都不握「模型发不发、评估过不过」这类决策。他自己的说法是「交出日常运营职责,腾出时间和空间聚焦大局」,同时把更多精力投入他一直兼任 CEO 的药物发现公司 Isomorphic Labs。他在公告里重复了他讲过多次的话:AI 的第一应用应该是改善人类健康。

## 头衔变化为什么和安全有关

先看 Hassabis 的安全记录具体到什么程度。他多次公开主张,AGI 研发的最后阶段最好放进一个类似 CERN 的机构里进行(CERN 是欧洲多国合资共建的粒子物理实验室,特点是国际协作、成果公开),再配一个类似国际原子能机构 IAEA 的监督方盯住高风险项目(如 [2026 年 1 月达沃斯与 Dario Amodei 的对谈](https://www.weforum.org/podcasts/radio-davos/episodes/ai-agi-dario-amodei-demis-hassabis/));2023 年他签署了 CAIS 那份将 AI 风险与核战争并列的[声明](https://safe.ai/work/statement-on-ai-risk)。在他任内,DeepMind 于 2024 年推出 [Frontier Safety Framework](https://deepmind.google/blog/introducing-the-frontier-safety-framework/):一套公司对自己的承诺协议,约定当内部评估发现模型接近某些高危能力,比如大幅助力生物武器研发,或把 AI 研发本身加速到失稳水平,就必须先完成安全论证,再决定是否发布。[2025 年 9 月的第三版](https://deepmind.google/blog/strengthening-our-frontier-safety-framework/)由安全团队负责人 Anca Dragan 等人署名,新增了「有害操纵」(模型系统性改变人类信念)风险类别,并扩展了针对模型规避人类控制、抵制关机一类失对齐行为的应对方案。

框架、安全团队、AGI Safety Council 这些机构都还在,人事变动不会让它们消失。问题在另一层:这套框架是自愿承诺,没有外部执法者,「安全评估结果要不要卡住一个发布」最终是运营层的决定。过去,这套安全机器的最终裁决人本人就是它最积极的倡导者;现在,裁决权移交给了一位公开履历集中在研究突破和产品整合上的继任者。这不是暗示 Koray 会轻视安全,我没有任何证据支持那种说法。可查的事实只有两条:他过去对外的角色里没有多少安全治理的公开记录,而他接手的岗位使命写满了加速。安全议程从「CEO 本人的日程」变成「有待新负责人表态的日程」,这是目前能下的最准确的判断。

## Discovery Loop:把安全框架里的风险项当主营业务

另一半故事是 Jeff Dean 的新公司。四位创始人彼此合作了 14 到 30 年:Dean 和 Ghemawat 搭档写出了谷歌基础设施的大半地基,Quoc Le 是 Google Brain 创始成员,Oriol Vinyals 是 DeepMind 副总裁、Gemini 核心研发负责人之一。Discovery Loop 要做的事,是把科学发现的循环本身自动化:提出假设、设计并运行实验、评估结果、再迭代,全部交给机器,并且成千上万个实验并行跑。Dean 的说法是,这样「实验的数量和质量都会上去,进而带来科学突破」([TechCrunch](https://techcrunch.com/2026/08/05/jeff-dean-and-other-top-ai-researchers-are-leaving-google-to-launch-their-own-startup/))。第一个目标领域是自动化机器学习研究自己,之后再扩展到硬件设计、药物发现、清洁能源。种子轮由 Radical Ventures 和 Khosla Ventures 共同领投,Kleiner Perkins、Lightspeed、Doerr Capital 和 Alphabet 参投;谷歌是创始投资人兼云服务合作方。

对照一下会看到一个耐人寻味的细节:DeepMind 自家的安全框架里,「把 AI 研发加速到可能失稳的水平」正是被点名要做安全论证的高危能力之一。Dean 的新公司把这个能力当成了主营业务。公司注册为 public benefit corporation(公益公司:董事会在股东利益之外,可以合法地把章程写明的公共使命纳入决策依据,Anthropic 和 OpenAI 的营利实体也用类似结构),但这个结构本身不附带强制透明度或外部监督,约束力取决于章程细节。我没能找到 Discovery Loop 公开的安全政策或治理条款,这一点只能等它后续披露。

对谷歌来说,这次同时送走了两位最有号召力的 AI for Science 旗手:Hassabis 把精力转去 Isomorphic 做药物发现,Dean 把科研自动化带出门创业。不过谷歌以创始投资人加云合作方的身份留在 Discovery Loop 的股权表和账单上,与其说是方向流失,不如说是把一个高风险、长周期的方向外置,保留了敞口。真正没法对冲的损失在 Gemini 本身:Vinyals 和 Le 是模型研发的核心人物,这种级别的离开,股权敞口补不回来。

## 接下来看什么

有三个具体信号可以校验这篇文章的担忧是否成立。一是 Frontier Safety Framework 的下一次更新:还更不更新、由谁署名、风险阈值是收紧还是放松。二是下一代 Gemini 主力模型发布时,安全评估和 model card 的详略程度比前代是升是降。三是 Koray 会不会接过对外谈安全的角色,还是把这件事留给安全团队的博客。

制度可以沉淀一位创始人的意志,但制度的解释权始终握在运营者手里。Hassabis 用十几年把安全承诺写进了 DeepMind 的流程;从这周开始,这些条文是约束还是陈设,取决于执行它们的新人。

## 参考来源

- [Google 官方公告:The next chapter of our AI momentum](https://blog.google/company-news/inside-google/message-ceo/next-chapter-ai-momentum/) — 人事变动、新头衔、汇报关系、Gemini/Gemma 数字、Pichai 与 Hassabis 原话;全文无 safety/responsibility 字样的核对依据
- [Jeff Dean 在 X 上的创始公告](https://x.com/JeffDean/status/2085034604172603724) — Discovery Loop 使命、四位创始人及合作年限、PBC 结构(官方仅在 X 公告)
- [TechCrunch:Jeff Dean and other top AI researchers are leaving Google](https://techcrunch.com/2026/08/05/jeff-dean-and-other-top-ai-researchers-are-leaving-google-to-launch-their-own-startup/) — 融资阵容、创始人背景、Dean 引语
- [CNBC:Google chief scientist Jeff Dean leaving company after 27 years](https://www.cnbc.com/2026/08/05/google-chief-scientist-jeff-dean-leaving-company-after-27-years.html) — 27 年任期、Hassabis 转任细节交叉印证
- [Semafor:Google names new chief AI architect](https://www.semafor.com/article/06/11/2025/google-names-new-chief-ai-architect-to-advance-developments) — Koray 2025 年 6 月任 Chief AI Architect 及该职位使命
- [DeepMind:Introducing the Frontier Safety Framework](https://deepmind.google/blog/introducing-the-frontier-safety-framework/) — 框架定位与机制
- [DeepMind:Strengthening our Frontier Safety Framework](https://deepmind.google/blog/strengthening-our-frontier-safety-framework/) — 第三版新增风险类别、署名作者、ML 研发加速风险域原文
- [CAIS:Statement on AI Risk](https://safe.ai/work/statement-on-ai-risk) — Hassabis 为签署人
- [WEF Radio Davos:The day after AGI(Hassabis 与 Amodei 对谈)](https://www.weforum.org/podcasts/radio-davos/episodes/ai-agi-dario-amodei-demis-hassabis/) — Hassabis 的 CERN/IAEA 治理主张
