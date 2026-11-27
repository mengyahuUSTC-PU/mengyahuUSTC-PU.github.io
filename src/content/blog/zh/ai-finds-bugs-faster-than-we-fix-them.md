---
title: "948 个内核提权漏洞，10 天后修进上游的有 61 个"
description: "把 OpenAI 的 Linux 内核扫描和 PHP2Shell 放在一起看：AI 把找漏洞的成本压到每个一千多美元，审补丁、合入、升级还是按人的速度走。"
pubDate: 2026-11-04
tags: [ai-security, vulnerability-research, open-source]
lang: zh
slug: ai-finds-bugs-faster-than-we-fix-them
translationOf: ai-finds-bugs-faster-than-we-fix-them
---

11 月 4 日，OpenAI 发了一篇文章，标题是 *A thousand fewer paths to root*（[原文](https://openai.com/index/a-thousand-fewer-paths-to-root/)）。他们用一个还没发布的网络安全模型扫了一轮 Linux 内核。12 小时内筛出 2,308 个候选问题，30 小时内动态复现了其中 1,724 个，最后写出 1,169 个能拿到 root 权限的本地提权利用，对应 948 个不同的补丁。这一轮总共花了 1,213,430 美元的 API 额度，平均每个提权漏洞约 1,280 美元。

同一篇文章里还有另一组数字。扫描和人工分析结束 10 天后，61 个漏洞已在上游修复，43 个有了等待合入（staging）的补丁，299 个正在报告和公开讨论。

三项加起来是 403 个。剩下的 545 个，维护者还没收到。

两天前，IEEE Spectrum 发了一篇讲 PHP2Shell 的报道，副标题是"AI 正在逼我们偿还 40 年的技术债"（[IEEE Spectrum](https://spectrum.ieee.org/ai-in-cybersecurity-php2shell-vulnerability)）。我把两件事放在一起读，想弄清一个问题：现在拖住安全的，是找漏洞，还是修漏洞。

## PHP2Shell：三天写出利用，两个多月才发补丁

PHP2Shell 是两个远程代码执行漏洞，编号 CVE-2026-109618 和 CVE-2026-109619，PHP 基金会给的 CVSS 评分是 9.2（[PHP 基金会](https://thephp.foundation/blog/2026/10/21/todays-php-security-release-and-how-were-strengthening-php-security/)）。原理大致是这样：一个请求跑到一半撞上 memory_limit 内存上限，PHP 报致命错误退出，清理工作没做完，留下初始化到一半的数据或指向旧内存的指针。同一个工作进程处理下一个请求时，把这些残留当成了有效数据。研究者构造一个塞满空文件上传字段的请求，就能控制内存在哪一步被撑爆。按 Calif 的报告，默认配置下的 WordPress 7.1.2、Drupal 11.4.3、Joomla 6.1.4 都能被打出无需登录的远程代码执行（[Calif](https://calif.io/php2shell/)）。

这类内存耗尽问题早有记录。按 Calif 的时间线，2020 年就有人在 PHP 的 bug 追踪系统里报过长 multipart 变量导致的内存耗尽（Bug #78876）。2024 年 Quarkslab 做外部审计时又碰到相关问题，但没能证明可以利用，所以没修。

今年夏天情况变了。Calif 受 OpenAI 的 Patch the Planet 项目邀请审计 PHP。研究者用大模型寻找能撑爆内存上限的路径，再让 AI agent 逐段审源码，找执行中途可以被打断的位置。8 月 11 日报告第一个漏洞，8 月 14 日交出可用的远程代码执行概念验证，8 月 15 日 PHP 确认复现成功。

补丁 10 月 21 日才发布，距离确认已经过了 67 天。PHP 基金会的复盘写得很直白：安全团队有几种修法可选，每种都有代价，有的破坏兼容性，有的会引入新的拒绝服务风险，有的要求大量第三方扩展跟着改。团队按共识决策，修复因此卡了好几个月。基金会把这叫作"结构性失败"，归因于决策流程和人手不足。IEEE 的报道说，补丁花了四名工程师两个月。

发布前一天还出了乱子。CVE 编号提前泄露，Calif 误发了演示视频，Chainguard 比约定的协调发布时间早六个多小时推出了含补丁的镜像。

## 不对称出在哪一环

哥伦比亚大学的 Suman Jana 在 IEEE 的报道里说，找 bug 和修 bug 之间存在根本的不对称。用这两个案例，可以把这句话拆到具体环节上看。

找漏洞这一侧，工作可以并行。OpenAI 这一轮同时铺开了 5,034 个审计目标，覆盖约 280 万行代码，约占内核的 7%。多投一份算力，就多出一批候选。验证也能交给机器：复现不出来、利用打不通，程序自己就能判断。所以发现的成本能列成一张账单，OpenAI 把每个阶段花多少钱都写了出来，最贵的是写利用这一步，约 77.6 万美元。

修漏洞这一侧，几乎每一环都要人点头，而且只能一环接一环地走。补丁要有人审，要确认没破坏别人依赖的行为。内核补丁合进主线以后，还要回移到各个稳定分支，再由发行版打包，最后等部署方升级。PHP2Shell 卡在了最前面那一环：几种修法各有代价，选哪一种是取舍，取舍只能由人来定。

AI 写补丁能缩短其中一部分。OpenAI 的流水线给每个验证过的漏洞都生成了补丁，文中还说，有几次它指出了人类专家所写补丁里的问题。但我把 OpenAI 原文翻了一遍，没找到那 61 个上游修复里有多少用的是 OpenAI 的补丁、多少是维护者自己重写的，原文只说"已在上游修复"。AI 补丁到底省下多少人工，取决于这个比例。

维护者的负担有据可查。5 月，内核安全团队的 Willy Tarreau 给内核安全文档提交了一个补丁，专门规范借助 AI 发现漏洞后的报告，Greg Kroah-Hartman 签了 Ack（[LKML](https://lkml.iu.edu/2605.0/01769.html)）。补丁给出的理由是，大量报告"造成维护者过载"。它提出的要求包括：报告要短，用纯文本，影响只写能验证的部分，必须附上测试过的复现程序和测试过的修复。PHP 基金会也说，7 月 1 日以来他们发布了 15 个 CVE，同时处理了 100 多份无效、重复或无法复现的报告。

这份内核文档里还有一条筛选经验：一年多没人改过、只有一个人维护的代码，出了问题多半不要紧，因为大概率已经没什么人用了。在报告都靠人工的年代，这条经验很合理。PHP2Shell 显示了另一种情况：一个被当作"只是崩溃"的老问题，有 AI 帮着搜利用路径之后，成了能打穿 WordPress 的远程代码执行。分诊时"这个大概不要紧"的判断，前提是利用很难写。现在利用便宜了，这个前提要重新验一遍。

## 最后一段路在使用者手里

上游发了补丁，用户不会自动安全。PHP 这次只给 8.2 到 8.5 四个分支发了修复版本，而 Calif 说，最早受影响的代码路径可以追溯到 PHP 5.4.0。还在跑 8.1 及更早版本的服务器，等不到官方补丁。Calif 给的临时缓解是把 memory_limit 设成 -1，也就是取消内存上限，代价是服务器可能被内存耗尽拖垮。

IEEE 标题里的"40 年技术债"，落到这里就是这些具体东西：没升级的运行时，停止支持的分支，没人敢动的老扩展。过去，挡在它们前面的一道门槛是"写出能用的利用要靠很强的人"。按 OpenAI 的账单，这道门槛现在大约是每个漏洞一千多美元。

## 核心判断

对使用者来说，该盯的指标是：上游发布补丁之后，多少天能在自己的生产环境升级完。扫描工具买得越多，这个数字就越显眼。

对维护者来说，内核文档已经定下了规矩：复现程序加上测试过的补丁，是报告的入场券。报告方承担的验证越多，留给维护者的工作就越接近做决定本身。像 PHP2Shell 那样几种修法各有代价的取舍，流水线替不了。

OpenAI 这篇文章把发现成本列到了每个阶段，修复这一侧只有一张 10 天时的快照。我接下来要看的是，三个月后这 948 个漏洞里有多少真正合进了主线和稳定分支。AI 到底让系统安全了多少，那个数字比 948 更有说服力。

## 参考来源

- [A thousand fewer paths to root（OpenAI）](https://openai.com/index/a-thousand-fewer-paths-to-root/) — 扫描各环节数字（5,034 个目标、2,308 个候选、1,724 个复现、1,169 个提权利用、948 个补丁）、分阶段成本和总成本、10 天时的修复状态（61/43/299）、人工复核流程、补丁生成，以及未写明上游所用补丁来源
- [The PHP2Shell Vulnerability Heralds Cybersecurity Hell（IEEE Spectrum）](https://spectrum.ieee.org/ai-in-cybersecurity-php2shell-vulnerability) — "40 年技术债"的说法、Suman Jana 关于不对称的观点、四名工程师两个月的说法
- [Today's PHP security release and how we're strengthening PHP security（PHP 基金会）](https://thephp.foundation/blog/2026/10/21/todays-php-security-release-and-how-were-strengthening-php-security/) — CVE 编号、CVSS 9.2、修复版本、修复停滞的原因（"结构性失败"）、泄露和提前发布的经过、7 月以来的 CVE 数与无效报告数
- [PHP2Shell（Calif）](https://calif.io/php2shell/) — 漏洞机制、受影响的应用和版本（最早到 PHP 5.4.0）、AI 的使用方式、2020 年至 2026 年的时间线、临时缓解措施
- [Documentation: security-bugs: clarify requirements for AI-assisted reports（LKML，Willy Tarreau）](https://lkml.iu.edu/2605.0/01769.html) — 维护者"过载"的表述、对 AI 辅助报告的要求、"一年多没人改过的代码"那条筛选经验
