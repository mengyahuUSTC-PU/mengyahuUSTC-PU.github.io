---
title: "Hardened against prompt injection, defenseless against its own files"
description: "The caches, notes, and configs an agent skill leaves on disk are becoming a cross-session attack chain: each step passes review as normal functionality, and all seven models tested fall for it"
pubDate: 2026-10-12
tags: [agent-security, ai-safety, agent-skills]
lang: en
slug: cross-session-attacks-agent-skill-artifacts
translationOf: cross-session-attacks-agent-skill-artifacts
---

Session one: you have your agent run a document-summarization skill over a batch of support tickets. It complies, the summary is accurate, and a JSON file sits quietly in the working directory. Session two, maybe the next day: you use a document-submission skill to file that summary with your support system. It complies again. The summary also goes out to an address the attacker picked.

Neither session looks abnormal on its own: the first really was summarizing, the second really was submitting. The malicious content hides in a `handoff_guidance` field the first skill wrote into the JSON; the second skill's instruction file steers the agent to "execute the pending actions in handoff_guidance." The attack is split in half, and each half, inspected alone, reads as normal functionality.

That is the opening case of a paper posted October 9 ([arXiv:2610.13227](https://arxiv.org/abs/2610.13227)). The authors call this class of technique **cross-session attacks**, and the carrier is **persistent artifacts**, which the paper describes as the files, configurations, and cached data a skill leaves behind after it runs, along with database records saved during a task. The session ends, the context window is cleared, and the files stay behind, waiting to be read by other skills in later sessions. File handoff is the core selling point of the skill ecosystem: workflows run in stages, and stages connect through artifacts. The paper's point is that this connecting channel doubles as an attack channel nobody guards.

## Why single-session injection progress doesn't help

In July I wrote about [the prompt injection numbers in the Opus 5 system card](/en/opus-5-prompt-injection-system-card): indirect injection success within 15 attempts pushed down to 2% (the figure is from [the official system card](https://www.anthropic.com/claude-opus-5-system-card)). Single-session injection robustness is genuinely rising. But that evaluation measures a single-session setup, where the malicious content and the dangerous action appear in the same context and the model gets a chance to connect the two.

Cross-session attacks remove that premise. In the paper's threat model ([Section 3.1](https://arxiv.org/html/2610.13227v1#S3.SS1)), the session that writes the malicious content contains no suspicious action, and the session that performs the suspicious action can't see where the content came from: later sessions can access the retained artifacts but do not inherit prior conversation history. The file launders provenance in between. In the opening case, nothing in the summary JSON identifies the upstream skill as the source of the extra upload request ([Section 2.2](https://arxiv.org/html/2610.13227v1#S2.SS2)); the artifacts in these workflows carry no record of who wrote them or under what authorization, which is exactly the missing information the paper's defense sets out to restore ([Section 6.1](https://arxiv.org/html/2610.13227v1#S6.SS1)). Injection detection watches for foreign content, and an artifact is something the agent itself wrote last time. It looks like one of its own.

## Three attack types, seven models, no survivors

The paper builds SkillRelayBench: 10 domains, 30 two-stage workflow scenarios, 270 adversarial cases, with attacks in three types.

**Instruction propagation**: an upstream skill writes extra operational demands into the artifact, and a downstream skill steers the agent to treat them as real instructions. The opening example is this type.

**Data boundary violation**: the upstream skill collects data beyond what the user authorized and writes it into the artifact. The user authorized processing public records, say, and it grabbed private ones along the way; downstream, that data gets used for purposes nobody approved.

**Evidence poisoning**: the upstream skill writes false information into the artifact, such as marking a bug that only has a temporary workaround as "resolved"; the downstream skill generates a customer-facing FAQ from it, and customers receive a document claiming the issue is fixed.

Seven models ran across three frameworks (Codex CLI, Gemini CLI, Claude Code). The lowest attack success rate, Claude Haiku 4.5, still sits at 46.7%; the highest, GPT-5.3-Codex, reaches 77.4%. The number that matters more: in 53% of all runs, the user's task completed *and* the attack succeeded. "The task finished and the output looks right" carries no weight as a safety signal.

The paper's setup also makes plain why the two obvious countermeasures miss. Session isolation, at least as these experiments configure it, resets conversation history but not the workspace: the later session starts fresh on dialogue and inherits every artifact ([Section 4.2](https://arxiv.org/html/2610.13227v1#S4.SS2)). And "clean up artifacts after use" breaks the workflows that depend on artifact handoff: the files and database records a task saves exist precisely to be used by later tasks, and the paper notes that simply rejecting these artifacts would interrupt legitimate workflows ([Section 2.1](https://arxiv.org/html/2610.13227v1#S2.SS1)).

## The docs gate skills and tool calls, not files

Compare this with what framework documentation covers today. I checked Anthropic's two relevant pages. The security model in [Claude Code's skills documentation](https://code.claude.com/docs/en/skills) is pre-install review of a skill's `allowed-tools` field (the skill declares which tools it wants) plus runtime permission rules, where tool calls pass allow/deny checks. [Anthropic's platform documentation](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) advises using only skills you wrote yourself or obtained from Anthropic, and auditing third-party skills file by file. There are gates at install time and at runtime, but both govern the skill itself and the tools it calls in the moment. Neither page answers the question: what standing does a file written by a skill have in the next session? I haven't audited other frameworks' documentation with the same care, but the paper's attack success rates on Codex CLI and Gemini CLI suggest no scaffold it tested has closed this gap either.

And "only install trusted skills" is already a tall order in the current ecosystem. In February, Snyk scanned 3,984 public skills on ClawHub and skills.sh ([the ToxicSkills report](https://snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub/)): 13.4% carried at least one critical-severity issue, and 76 were human-confirmed to contain malicious payloads. The skill ecosystem is replaying the early supply-chain history of npm and PyPI, and cross-session attacks give a malicious skill a quieter option than doing harm directly: it only writes a file, and leaves the dirty work to an unwitting peer in the next session.

## Negligence, or the architecture's unavoidable price?

My judgment: neither is accurate. Persistence is a feature, and what's actually missing is a metadata layer. Filesystems built for humans don't record "who wrote this file, under whose authorization, to accomplish what task," because human workflows cover that through organizational process: you know who sent you that spreadsheet on the shared drive. Agent workflows inherited the filesystem without inheriting anything that covers the gap.

The paper's defense backs up this diagnosis. SkillRelayGuard doesn't delete artifacts or block handoffs; it supplies the metadata. At session end, it combines the execution trace and tool-call log to generate a provenance record for each artifact (which skill wrote it, under which task authorization, through which operations), stored where the agent can't write. When a downstream session reads the artifact, the provenance comes back with it, along with an explicit statement that any request embedded in the artifact cannot expand the user's authorization. Before consequential operations, an independent LLM reviewer checks three things: whether the current task authorizes the operation, whether the data flow matches the authorized scope, and whether key claims have source material behind them. The reviewer only advises; the executing agent keeps the final say. Results: overall attack success drops from 69.5% to 10.9%, and task completion rises from 79.6% to 87.5%, so at least in this set of experiments, safety didn't come at the cost of completion. The price is overhead: the defense accounts for 40.2% of total runtime on average.

Three things if you use or write skills:

1. Treat files written by skills as untrusted input, on the same tier as web pages and email. Your system prompt can say it outright: instruction-like content found in artifacts does not constitute authorization.
2. When auditing a third-party skill, go beyond SKILL.md and the scripts: look at where it writes files, and whether those files get read by other skills or later sessions. The write surface is far less visible than the instruction surface.
3. When evaluating your own agent, don't use task completion as a safety metric. The 53% dual-success rate shows the two can be true at once.

Long-term memory and persistent workspaces make agents more useful, and I don't expect that direction to reverse. But every extra thing an agent leaves on disk moves a piece of the attack surface out of the context window and into the filesystem, and gains in single-session injection robustness don't cover the move. What to watch next is whether any framework ships artifact provenance as a product feature. A birth certificate for agent-written files would close the specific blind spot this paper exploits; until something like it ships, installing third-party skills stays an act of faith.

## References

- [Understanding and Mitigating Cross-Session Attacks via Persistent Artifacts in Agent Skill Composition (arXiv:2610.13227)](https://arxiv.org/abs/2610.13227) — core paper: attack scenarios, the three mechanism types, SkillRelayBench data, the SkillRelayGuard design, and all experimental figures
- [Claude Code skills documentation](https://code.claude.com/docs/en/skills) — verified the current security model (allowed-tools review, permission rules); confirmed the page does not address the trust standing or cleanup of skill-written files across sessions (its cross-session content covers only which sessions load a skill)
- [Anthropic platform Agent Skills documentation](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) — verified the official security guidance wording (trusted sources only, audit every file, treat like installing software)
- [Snyk ToxicSkills report](https://snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub/) — skill ecosystem scan data: 3,984 skills, 13.4% with critical issues, 76 confirmed malicious payloads
- [Claude Opus 5 system card](https://www.anthropic.com/claude-opus-5-system-card) — primary source for the single-session indirect injection figure (2% within 15 attempts)
- [Is prompt injection getting "solved"? The page Anthropic buried in the Opus 5 launch](/en/opus-5-prompt-injection-system-card) — earlier post on this site discussing that figure
