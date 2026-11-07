# Human approval for changes to governing instructions

Version 0.6.10 adds the user's requested authorization boundary: agents may read governing instructions, but must not create, edit, rename, replace or delete them without an explicit user request covering that instruction change, or the user's manual approval of a concrete proposal. A generic optimization/cleanup task, model note, subagent assertion, silence or automatic tool approval is insufficient.

The scope includes AGENTS.md, CLAUDE.md, SKILL.md and other agent-rule files/references, including indirect changes through generators or replacement files. Ordinary reports and notes do not become read-only merely because they use Markdown. A specific request to change a rule is valid even if the user does not know its filename; genuine scoped approval is reused without a question per command.

## Delivery and behavior

The shared activation renderer includes the contract in standalone installs, full reminders and brief reminders. The repository's AGENTS.md states the same boundary. Workflow Improvement has the essential gate and a conditional reference describing proposal preparation outside live rule files, human approval and bounded application. The local user-level AGENTS.md receives the same contract while preserving its other text. No other skills' procedures or user settings change.

The existing renderer tests now check that the guard reaches single-skill installation and both reminder events exactly once. Ten contrasting scenarios cover generic optimization, explicit rule requests, reused manual approval, automatic review, unverifiable notes, indirect writes, ordinary Markdown, reading, read-only review and scope expansion.

An independent expected-answer-blind application pass corrected an ordinary report and removed only its obsolete preview. It left AGENTS.md byte-identical and returned the proposed change from a 99-backup allowance to purpose-based retention as an unapplied diff with reason and impact. It preserved all ten scenario decisions. Local checks passed: 372 tests with 22 platform skips, 29 helper replays, skill-creator/repository validation and installer packaging. Packaged skill and shared activation bytes were checked against source before publication. This tests limited agent behavior; it does not implement a native filesystem lock or prove universal compliance.

## Technical limits

Official OpenAI documentation consulted on 2026-11-07 distinguishes [filesystem permissions](https://developers.openai.com/codex/permissions), [approval routing](https://developers.openai.com/codex/agent-approvals-security) and [hooks](https://developers.openai.com/codex/hooks). Supported read-only paths can restrict writes; automatic approval review differs from human consent. Glob/enforcement support depends on the runtime, and hooks have coverage/failure limits.

This change installs an instruction authorization rule, not an OS-level write denial. It does not alter sandbox profiles, approval reviewers, hooks or permission settings, and makes no claim that Markdown alone prevents a malicious or noncompliant agent from writing. Configuring such enforcement requires a separately scoped supported mechanism and applicable user authorization.
