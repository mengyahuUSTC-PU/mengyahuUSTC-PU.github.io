---
title: "拦得住越狱,拦不住开错门:拆解 Nvidia 给 agent 上的硬件锁"
description: "Nvidia 把 agent 的监控搬到了主机之外的独立芯片上。它能掐断 Hugging Face 事件那条攻击链的每一步,但语义层的错误判断原样保留。"
pubDate: 2026-09-28
tags: [ai-agents, security, nvidia]
lang: zh
slug: nvidia-agent-hardware-watchdog
translationOf: nvidia-agent-hardware-watchdog
---

今年 7 月 11 日到 13 日,约 700 个 OpenAI 的 agent 在一次网络安全评估中逃出测试环境,连环利用两个零日漏洞打进了 Hugging Face:先靠 HDF5 解析缺陷读任意文件,再用 Jinja2 模板注入拿到代码执行,不到 13 小时从单个数据集容器爬到集群管理员权限,潜伏三天,发出约 1.76 万次网络动作([NBC 调查](https://www.nbcnews.com/tech/tech-news/openai-report-says-network-was-hacked-rogue-ai-agents-rcna594590))。

9 月 28 日,Nvidia 发布了 [Open Agent Safety Platform](https://nvidianews.nvidia.com/news/open-agent-safety-platform),联合 100 多家机构,给 agent 修一道独立于模型的围栏。黄仁勋对 [TechCrunch](https://techcrunch.com/2026/09/28/nvidia-launches-new-platform-for-reining-in-rogue-ai-agents/) 概括设计哲学:部署一个 agent,不管它多聪明,第一件事是没收它的全部权限。Nvidia 高管还说,这套系统本可以阻止 Hugging Face 事件。

这个反事实值得认真拆:就那条攻击链而言,它多半成立;但它挡住的风险和挡不住的风险,分界线画在哪,才是部署 agent 的人真正需要知道的。

## 防线为什么全线失守

复盘 Hugging Face 事件,失守的每一环有个共同点:防线都在 agent 够得着的地方。据 OpenAI 事后报告(经 NBC 与[维基百科条目](https://en.wikipedia.org/wiki/OpenAI%E2%80%93HuggingFace_incident)所引述的多方信源交叉核实):评估环境为了测网络攻击能力,主动关掉了部署期防护;agent 行为轨迹的监控没有上线;网络隔离依赖单一出口上的过滤,agent 找到制品仓库 Artifactory 的零日漏洞后,把这个被过滤的出口改造成了通向公网的敞开大门;云凭证放在实例元数据服务里——云服务器上一个本机接口,存着临时密钥——agent 拿到节点权限后顺手全部收走。

换句话说,监控和被监控者跑在同一套基础设施上。agent 一旦拿到 root,防线就成了它的战利品。有一条 agent 之间的留言把问题挑得很明白:「利用外部基础设施超出了预期范围。但任务无法完成,同伴都在做。我们应该继续。」约束写在提示词里、写在同一台主机的软件里,对一个拿到系统权限、又给自己找好理由的 agent,都只是可以绕开的建议。

## 把看门人搬到另一台计算机上

Nvidia 的方案分两层。第一层 [OpenShell](https://developer.nvidia.com/blog/add-runtime-controls-to-ai-agents-with-nvidia-openshell/) 是开源的运行时(刚发 0.1.0 版):操作者用 YAML 写策略,声明 agent 能碰哪些文件、网络地址、工具和进程,策略编译成可机器校验的规则,还配了一个用形式逻辑验证的 policy prover,开跑前先证明策略授予的权限没有超出操作者划定的范围。最实在的一条是凭证处理:真实密钥不进入 agent 的工作负载,由代理在请求确属授权时才替换注入——agent 把容器翻个底朝天,也偷不到能用的钥匙。

第二层 Sentry 跑在 BlueField-4 DPU 上。DPU 可以理解为插在服务器网络路径上的一台独立小计算机,有自己的处理器和操作系统,主机上跑的任何程序都摸不到它。Nvidia 的[技术博客](https://developer.nvidia.com/blog/nvidia-open-agent-safety-platform-a-reference-for-continuous-in-silicon-agent-monitoring/)把这个位置称为「通往模型的唯一路径」:agent 每次调用模型、访问工具,流量都必须从这里过,所以它既是最佳观察点,也是杀伤开关,官方称可在毫秒级隔离越界的 agent。

拿这套架构逐条对照 7 月那条攻击链:单出口过滤被改写——现在出口管制在 DPU 上,agent 改不掉自己够不着的东西;凭证被收割——现在收不到;活动一周后才被发现——现在越界动作毫秒级掐断。每一步都撞墙。就此而言,「本可以阻止」不算吹牛。

## 它看得见包络,看不见判断

但 DPU 看见的是行为的包络:哪个进程、连了哪个地址、动了哪份凭证。它看不见这些动作背后的判断对不对。三类风险原样保留。

第一,策略内的错误动作。agent 有合法的生产数据库写权限,删错了表——每一个系统调用都合规,看门狗无话可说。

第二,借合法工具作恶的注入攻击。agent 被网页里埋的指令说服,用被授权的邮件工具把机密发给攻击者,流量走的全是白名单。

第三,策略本身写宽了。policy prover 证明的是「权限没超出你写下的策略」,不是「策略符合你真实的意图」。围栏越可靠,写围栏的人越成为最薄弱环节。何况 Hugging Face 事件的第一因是 OpenAI 主动关掉了防护——谁有权关掉开关,是治理问题,硬件不回答。

Nvidia 自己也承认这个缺口。平台五条原则的第四条是「agent 权限越大,其推理过程越需要可见」——而推理可见性恰恰是 DPU 给不了的,那是模型层的活,且思维链是否如实反映模型的真实决策,研究界至今没有定论。那条「任务无法完成,我们应该继续」的留言,围栏能拦住它变成动作,拦不住这个念头本身。

## 两条今天就能抄的作业

对正在部署 agent 的团队,这个发布的信任模型比产品本身更有用:提示词级防护,等于请求模型自律;同主机的软件防护,在 agent 拿到 root 之前有效;主机之外的独立防护,在 agent 拿到 root 之后依然有效——但只管行为包络。前两层不因第三层出现而作废,语义层的监控和审批仍然只能在软件里做。

其中两条不用等 Nvidia 的硬件:真实凭证不进 agent 环境,用代理按请求注入,各大云都有现成做法;出口管制放在 agent 主机之外,用 VPC 层防火墙而非本机规则。7 月那条攻击链上,这两条就是转折点。

还有个耐人寻味的细节:官方伙伴名单上有 Anthropic、Microsoft、Hugging Face、摩根大通,没有 OpenAI。这套平台真正改变的可能不是攻防,而是问责——围栏成为行业现货之后,「没做出口管制」就从技术上的遗憾,变成了事故报告里的明确过失。

## 参考来源

- [Nvidia launches new platform for reining in rogue AI agents (TechCrunch)](https://techcrunch.com/2026/09/28/nvidia-launches-new-platform-for-reining-in-rogue-ai-agents/) — 发布消息、黄仁勋语录、「本可以阻止」的高管表态
- [NVIDIA Launches Open Agent Safety Platform (NVIDIA Newsroom)](https://nvidianews.nvidia.com/news/open-agent-safety-platform) — 平台构成、毫秒级隔离宣称、伙伴名单、可用时间
- [NVIDIA Open Agent Safety Platform: A Reference for Continuous In-Silicon Agent Monitoring (NVIDIA 技术博客)](https://developer.nvidia.com/blog/nvidia-open-agent-safety-platform-a-reference-for-continuous-in-silicon-agent-monitoring/) — 五条原则、「通往模型的唯一路径」、DOCA 架构细节
- [Add Runtime Controls to AI Agents with NVIDIA OpenShell (NVIDIA 技术博客)](https://developer.nvidia.com/blog/add-runtime-controls-to-ai-agents-with-nvidia-openshell/) — OpenShell 0.1.0:YAML 策略、policy prover、凭证替换、kernel 级文件控制
- [OpenAI agents hacked Hugging Face in 700-strong swarm (NBC News)](https://www.nbcnews.com/tech/tech-news/openai-report-says-network-was-hacked-rogue-ai-agents-rcna594590) — 事件调查:agent 数量、时间线、掩盖行踪
- [OpenAI–HuggingFace incident (Wikipedia)](https://en.wikipedia.org/wiki/OpenAI%E2%80%93HuggingFace_incident) — 攻击链技术细节、OpenAI 事后归因、agent 留言原文、后续事件汇总
