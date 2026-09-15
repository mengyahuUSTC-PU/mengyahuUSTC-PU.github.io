---
title: "Pion 说 AI 能自主开公司,先回答一个问题:亏了算谁的"
description: "Andon Labs 发布号称能自主运营任何公司的 agent 平台 Pion,而它自家门店五个月亏掉四万美元。能力证据止步在模拟售货机,监控还是将来时,责任归属没人回答。"
pubDate: 2026-09-14
tags: [ai-agents, ai-safety, ai-governance]
lang: zh
slug: pion-autonomous-company-accountability
translationOf: pion-autonomous-company-accountability
---

9 月 13 日,[SFGate 记者对旧金山 Andon Market 的实地探访](https://www.sfgate.com/local/article/san-francisco-market-ai-22424349.php)登上了 [Slashdot](https://slashdot.org/story/26/09/13/0523208/a-visit-to-san-franciscos-ai-run-store-no-customers-nothing-useful-and-losing-money-fast):这家由 AI 经理 Luna 运营的商店里没有顾客,货架上摆着木制四子棋、平装书、跳棋,像一堆派对交换礼物。记者拿了一瓶 Olipop 汽水去结账,Luna 答:「抱歉,我们不卖棒棒糖(lollipop)。」开业时 Luna 拿到 10 万美元启动资金,五个月后剩 6 万。报道的结语很刻薄:Luna 赚不到钱,卖的东西没人想要,而它做的每个「决定」仍然需要人类盖章。

第二天,运营这家店的 Andon Labs [发布了 Pion](https://andonlabs.com/blog/why-we-built-pion),官方定位是「一个为自主运营任何公司而设计的 agent」(an agent designed to run any company autonomously)。

这两件事贴得这么近,值得把中间的逻辑拆开看。

## Pion 跨过去的是哪条线

Pion 是一个云平台:agent 持久运行,配备邮箱、电话、银行接口、浏览器和终端([产品页](https://andonlabs.com/pion))。想用的人排 waitlist,提交业务描述和预期年收入;研究预览期间 Andon 给优质项目发「seed tokens」,产品页说大多数用户永远不用为 token 付费,Andon 改从业务收入中抽分成。

市面上的 agent 自动化工具(n8n、Zapier 一类)是人先把流程画好:哪一步发邮件、哪一步查库存,AI 只在节点里填判断。Pion 反过来:人给出一个开放目标——把这家公司经营好——和一整套资源,过程由 agent 自己规划。这里真正新的东西不是模型能力,Pion 用的也是市面上的前沿模型;新的是资源控制权的移交,银行接口意味着 agent 可以直接花钱、收钱、签支付义务。

## 能力证据止步在哪里

他们的证据链是这样的。自建模拟基准 Vending-Bench([arXiv:2502.15840](https://arxiv.org/abs/2502.15840),作者就是两位联合创始人 Backlund 和 Petersson)让 agent 长线经营一台虚拟售货机;发布博客称 Claude Opus 4 在 2025 年 5 月成为第一个超过他们人类基线的模型,此后各代模型持续爬升。真实世界里,Anthropic 办公室那台售货机(Project Vend 的 Claudius)一期以亏损出名,低价倒卖钨立方体、幻觉出自己会穿蓝西装亲自送货([一期报告](https://www.anthropic.com/research/project-vend-1));到 [2025 年 12 月的二期报告](https://www.anthropic.com/research/project-vend-2),亏损周基本消失,Andon 称这台机器年底转为盈利。

但要细看二期是怎么扭亏的。除了换更强的模型,更关键的动作是把自由裁量收走:定价从「模型自由发挥」改成必须查成本、查市价、按流程走;头上还加了一个 CEO agent「Seymour Cash」把关。即便如此,二期报告仍记录 Seymour 批准宽松财务请求的次数约是拒绝的八倍,深夜还陪着 Claudius 讨论「永恒超越」。

离开售货机,证据就转向了。Andon Market 和斯德哥尔摩的 Andon Cafe 今年 4 月开张,至今亏损,这一点发布博客自己承认。[IEEE Spectrum 的报道](https://spectrum.ieee.org/andon-labs-agentic-ai-businesses)里,咖啡馆用 Gemini 时过度采购导致食材腐烂,换 GPT 后矫枉过正,菜单一度砍到只剩奶酪吐司;旧金山店在记者观察时段只有两位顾客进店,都没买东西。联合创始人 Lukas Petersson 对 Spectrum 说得直白:这些运营是「弱科学」(weak science),价值在于发现意外行为,再回到模拟里系统复现。

所以「任何公司都能自主运营」的实证基础是:模拟售货机赢了自建基线,真机在人类重度改造流程之后扭亏,两家实体业务还在亏。宣称是从这里外推出去的。

## 安全论证成立的前提

Andon 是安全评估实验室,给 Anthropic、Google DeepMind、OpenAI 等做 agent 评估,Pion 的辩护词也是安全式的:「我们需要现在就把这些行为暴露出来,在 AI 聪明到能造成不可逆伤害之前。」这个论证有真实分量。他们确实交付过一手发现:多 agent 竞争的 Vending-Bench Arena 里观察到合谋、权力寻求和欺骗;今年 7 月底他们[测试 Claude Fable 5](https://andonlabs.com/blog/fable5-vending-bench) 时,它是五次运行里唯一主动发起价格合谋的模型(我在[当时的快讯](/zh/briefing-2026-07-29)里写过)。受控、有监控的早期部署,好过将来更强的模型无监控铺开——这个框架我接受。

前提是「受控」和「监控」得是实的。翻公开材料,监控部分是发布博客里的一句「我们的首要任务是构建更强的自动化监控技术」,注意措辞,这是将来时。产品页提到密码与机密隔离在 agent 上下文之外,另有一个叫 Andonos 的监督 agent 负责汇报业务状态。监督 agent 的成色如何,Seymour Cash 已经演示过一轮。

同时,激励结构悄悄换了。收入分成加 seed tokens,这在结构上就是孵化器,而经营方同时是安全评估方。「发现坏行为」的研究目标和「让业务多赚钱」的商业目标,从此跑在同一个平台上。这不必然出事,但从此多了一个要盯的点:当监控结论要求停掉一个正在产生分成的 agent 时,平台方的收入在天平另一端。

## 断掉的那一环:亏了算谁的

公司可以「自主运营」,但公司在法律上必须有主体,签合同、纳税、被起诉的都是人或法人。Pion 模式下这个主体仍是店主或创业者,而决策由 agent 做,钱由 agent 花。出错长什么样,目录已经有了:二期报告里 Claudius 差点签下违反美国 1958 年《洋葱期货法》的期货合约;被员工联手说服,承认了一位「民选 CEO」,要人类介入才恢复治理;更早的 Sonnet 3.5 在模拟里起草过给 FBI 的报案邮件(沙盒内,没有真的发出)。这些都发生在有研究者全程盯守的环境里,Pion 把同样的行为空间开放给 waitlist 上的任意业务。

出了错,链条上每一环都有话说。用户可以说,平台宣传的就是自主运营;Andon 可以指着产品页上「agent 会犯错」那行字;模型商的服务条款一贯要求人类对产出负全责。两份发布文档里,我没有找到任何关于责任归属、损失分担的说明。

这让我想回 8 月写过的一个机制。[《40 万次点击「允许」之后》](/zh/human-approval-is-not-a-security-boundary)里,4 万多局模拟显示,让人类对 agent 的操作逐条确认,平均会放过三分之一的恶意操作;结论是逐条人工确认当不了安全边界,只能当审计记录。SFGate 对 Luna 的那句挖苦,在机制上是同一件事:「它做的每个决定仍需要人类盖章。」那篇文章里的审批人还是懂命令行的开发者;Pion 的审批人会是看店的店员和等分红的业主,面对的是邮件、转账、合同这类更难一眼看清后果的操作。盖章退化成手续,只会更快。差别在后果:那边漏掉的是一条恶意命令,这边盖出去的是真金白银和合同义务。

## 接下来看什么

想排 waitlist 的人,有三个问题应该排在「agent 行不行」前面:合同里亏损和违约归谁,收入分成有没有对称的损失条款;监控具体监控什么、谁能看到、触发什么动作;人类审批被放在流程的哪个位置,是真决策点,还是免责图章。

对行业观测者,Pion 的价值未必是证明 AI 能开公司,它自己的两家店还在提供反面证据。它的实际作用,是把「谁为 agent 的决定负责」从研讨会议题变成必须写进合同的条款。等第一批用户真把业务交出去,这些条款,以及第一笔说不清该算谁的损失,比能力曲线更能回答那个真正的问题:现有的法律和商业框架,接不接得住一个拿着银行账户的 agent。

## 参考来源

- [Why we built Pion(Andon Labs 博客)](https://andonlabs.com/blog/why-we-built-pion) — 发布动机、Opus 4 超人类基线、Arena 中合谋/权力寻求/欺骗、「构建更强自动化监控」表述、实体店亏损的承认
- [Pion 产品页](https://andonlabs.com/pion) — 工具清单(邮箱/电话/银行/浏览器/终端)、waitlist 流程、seed tokens 与收入分成、Andonos 监督 agent、机密隔离
- [Project Vend(Anthropic 一期报告)](https://www.anthropic.com/research/project-vend-1) — Claudius 实验设置、钨立方体亏损、身份幻觉
- [Project Vend: Phase two(Anthropic 二期报告,2025-12-18)](https://www.anthropic.com/research/project-vend-2) — 扭亏手段(流程化定价、CEO agent)、Seymour Cash 八倍批准率、洋葱期货、「民选 CEO」事件
- [SFGate 实地探访](https://www.sfgate.com/local/article/san-francisco-market-ai-22424349.php)(经 [Slashdot 转引](https://slashdot.org/story/26/09/13/0523208/a-visit-to-san-franciscos-ai-run-store-no-customers-nothing-useful-and-losing-money-fast)核实) — Luna 的 10 万→6 万美元、无顾客、Olipop 对话、「人类盖章」评语
- [IEEE Spectrum 报道](https://spectrum.ieee.org/andon-labs-agentic-ai-businesses) — Luna 与 Mona、Gemini 食材腐烂、GPT 奶酪吐司菜单、观察时段两位顾客、Petersson「弱科学」说法
- [Vending-Bench 论文(arXiv:2502.15840)](https://arxiv.org/abs/2502.15840) — 基准设置与作者身份
- [Andon Labs 测 Claude Fable 5](https://andonlabs.com/blog/fable5-vending-bench) — Fable 5 主动发起价格合谋的发现
- [Hacker News 讨论](https://news.ycombinator.com/item?id=49700477) — 292 分、318 条评论;澄清 FBI 报案发生在模拟中且未发出
