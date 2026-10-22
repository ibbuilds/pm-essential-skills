# Execution Efficiency: evidence and boundaries

Research reviewed 2026-10-22. This is a focused third skill, not a mandatory execution pipeline. Context Management owns continuity; Source Selection owns retrieval. Execution Efficiency owns calibration of repeated verification and recovery during implementation or repair. Simple answers and retrieval-only tasks are negative controls.

## Recent evidence and what we adopted

- **Official guidance, 2026-09-11:** Eric Provencher's [Rethinking skills and prompts for GPT-6 Astra](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra) recommends narrower skill descriptions, contextual instructions, and reconsidering excessive testing recipes. It also emphasizes defining completion rather than stopping at a first implementation. We adopt a narrow trigger, conditional examples, and outcome-based completion. This is model-specific guidance, not evidence that every host should skip tests.
- **Maintainer release, 2026-10-21:** [Superpowers v7.0.1](https://github.com/obra/superpowers/releases/tag/v7.0.1) responds to formulaic questions by using existing context before clarification, and moves conditional material into references. We adopt context-first questions and progressive disclosure. We do not import its mandatory brainstorming approval sequence or fixed fix-round limit into this general suite. Its reported scenario results concern its own workflow, not ours.
- **Community failure signal, 2026-10-21:** [This Codex discussion](https://www.reddit.com/r/codex/comments/1xbbi8b/codex_is_now_just_full_wasting_usage_for/) reports repeated “fixed and tested” claims without a working fix and excessive test activity. These are anecdotes, not a controlled diagnosis of model changes, usage attribution, or proof of savings. They motivate negative cases where passing checks do not satisfy the user's actual acceptance conditions.

- **Cross-vendor primary documentation, accessed 2026-10-22:** [Claude Code cost guidance](https://code.claude.com/docs/en/costs#offload-processing-to-hooks-and-skills) describes preprocessing verbose output before model ingestion and loading task-specific instructions on demand. Source Selection now applies that portable principle using existing tools. We add explicit producer-status, coverage, count, and raw-recovery safeguards; we do not transplant Claude hooks or its sample test-output pipeline. The page has no asserted publication date here, and its product-specific usage figures are not evidence of this suite's savings.

All skill wording is original synthesis; no third-party skill implementation is vendored. This increment adds no dependency, model API call, background collector, mandatory log, or global installation.

## Design judgments to validate

The following are our design choices, not measured research findings:

- Before an optional repeat check, identify the material uncertainty it could resolve. Preserve required gates even if they repeat earlier coverage.
- Reuse verification only while its relevant inputs and freshness remain applicable; invalidate it after relevant code, dependency, configuration, environment, or acceptance changes.
- Retain failed hypotheses in working context, or existing notes when continuation needs them. Keep concise findings and existing raw-log pointers rather than a new ledger.
- Distinguish deterministic failure, transient failure, and uncertain external mutation. Retry based on new evidence and operation semantics, not a hard attempt count.
- Match verification to impact, not diff size. A one-line permission change can require stronger checks than a large copy edit.
- Prefer completion events or sensible waits over busy polling; delegate independent scoped work only when coordination is worthwhile.

A compact extra skill still adds discovery overhead. Benefit must be tested on complete tasks, including the cost of loading it. Do not install or invoke it for irrelevant work merely because it exists.

## Verification and limits

The existing installer/package tests exercise all three skills independently and together in disposable profiles, including extracted downloads and restoration. They verify delivery, not model judgment. [Behavioral fixtures](../tests/execution-efficiency-cases.json) define observable acceptance and failure conditions; automated unit tests do not run them against a model.

No paid model evaluation or live user-host installation was performed for this increment. Follow the [complete-task evaluation protocol](efficiency-evaluation.md) before claiming behavior improvements or savings. Preserve quality failures, missing telemetry, and overhead. Existing context thresholds and repeated-chat preference behavior are intentionally unchanged.

## Expanded survey decisions (checked 2026-10-22)

Current maintained documentation below has no publication date asserted here. These are portable mechanisms, not a transfer of vendor-specific settings or measured savings. Older sandboxing articles were not used as the primary rationale for this increment; failure classification is a correctness safeguard, not a claim about recent model performance.

| Mechanism and evidence | Decision | Scope |
| --- | --- | --- |
| Exact symbol navigation: [Claude Code costs](https://code.claude.com/docs/en/costs#install-code-intelligence-plugins-for-typed-languages) | Adopted | Prefer already-available semantic navigation when suitable; bounded search fallback, no installation, diagnostics are not tests. |
| Review-induced over-engineering: [Claude Code best practices](https://code.claude.com/docs/en/best-practices#add-an-adversarial-review-step) | Adopted | Concrete correctness/requirements findings; no manufactured defects or mandatory reviewer pipeline. |
| Nested work and separate usage: [Claude Code subagents](https://code.claude.com/docs/en/sub-agents#let-subagents-spawn-their-own-subagents) | Adopted | Explicit outcome ownership, avoid duplicate recursive reviews; no imported depth limit or configuration mutation. |
| Tool schemas: [OpenAI function calling](https://developers.openai.com/api/docs/guides/function-calling), [Anthropic tool definitions](https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools) | Adopted | Inspect applicable schema after unfamiliarity/validation failure, preserve returned IDs, avoid guessed arguments. |
| Repeated reads, bulky results, and weak handoffs | Already covered | Source Selection bounds/reuses evidence and preserves output status; Context Management retains recoverable continuity. No second memory system. |
| Failed retries and claims detached from the user's actual path | Strengthened | Classify code vs environment/dependency/auth/access failures; distinguish implemented, integrated, and verified. No automatic baseline suite. |
| Global model changes, automatic plugin installs, hard attempt/depth caps, mandatory multi-agent pipelines | Deferred/not adopted | These alter user choices or impose overhead without complete-task evidence. |

The schema-validated behavioral fixtures include negative cases for unavailable semantic tools, infrastructure failures, unsupported review findings, and duplicate delegation. They are evaluation inputs, not proof that a model follows the guidance. Community reports can identify scenarios worth testing but do not establish causes or savings; no recommendation here depends on an anecdote being representative.


A further [community workflow report](https://www.reddit.com/r/codex/comments/1xc22qs/tokensresets_to_burn_before_20x_is_nerfed_perhaps/), read 2026-10-22, explicitly describes self-reported heavy usage rather than an efficiency optimum. We adopt only the narrow hypothesis that batching routine worker progress may avoid unnecessary coordination, while preserving prompt blocker/decision escalation. Its usage and output totals do not generalize. Model pinning, file-size ratchets, third-party authentication gateways, and large orchestrators remain host/domain-specific rather than PM defaults. The existing evaluator already requires per-request usage identities instead of summing inherited session totals. Non-code artifact and material-choice fixtures preserve install-and-work behavior without setup interviews or assumed approvals.
