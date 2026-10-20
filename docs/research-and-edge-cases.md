# Research decisions and edge cases

This records why the workflow takes its current shape. It is maintainer documentation, not part of the normal agent instruction path.

## Findings translated into behavior

| Evidence | Design consequence |
| --- | --- |
| [Codex best practices](https://developers.openai.com/codex/learn/best-practices) recommends one chat per coherent unit and often keeping the same problem in the same chat. Automatic compaction already exists. | No age-based restarts, no one-chat-per-edit rule, and no mandatory splitting when relevant reasoning is still useful. |
| [Prompt caching](https://developers.openai.com/api/docs/guides/prompt-caching) reuses unchanged prefixes; compaction or rewriting can reduce reuse. | Do not equate fewer historical tokens with lower total cost. Keep stable instructions small, do not rewrite them each turn, and count startup/cache effects in pilots. |
| [Prompt Caching 201](https://developers.openai.com/cookbook/examples/prompt_caching_201) discusses the tradeoff between context engineering and cache stability. | Treat thresholds as hypotheses to evaluate. Do not apply a universal cache-length threshold across models or change cache settings in a skill. |
| [Skills documentation](https://developers.openai.com/codex/skills) describes selection and progressive disclosure, not a guaranteed always-on listener. | Small core, conditional references, one project activation rule, and honest idle/invocation limits. |
| [App-server documentation](https://developers.openai.com/codex/app-server) separates thread start, history-preserving forks, compaction, and token events. | Use a fresh thread for context reset, and use only telemetry actually exposed by the host. Do not infer accessible metrics from protocol features. |
| This session exposes listing, membership moves, and thread creation, but no native app-project creation tool. | Capability-gated standalone setup; never repurpose a document/folder tool or promise an unsupported automatic project creation. |

These sources were fetched on October 20, 2026. API-level caching mechanisms explain the tradeoff; they do not establish this user's exact subscription billing or a guaranteed savings percentage.

## Cases beyond the initial idea

| Case | Required response |
| --- | --- |
| Chat is standalone | Offer a project only when useful, obtain name/consent, then create/move/verify through real capabilities. |
| Membership is unknown | Resolve identity; do not assume standalone or choose the newest chat. |
| User declines or defers | Record the scoped preference and continue helping; no repeated prompts. |
| Existing project has the same display name | Use IDs/paths; ask reuse vs new before creating a duplicate. |
| Project creation succeeds; chat move fails | Keep the new project; recover the move only. Never delete or recreate blindly. |
| Move succeeds | Verify membership; remember that context has not shrunk. Evaluate a fresh-thread handoff separately. |
| Remote/local or ChatGPT/Codex backend mismatch | Preserve execution host and valid project type; honor actual host restrictions. |
| Required folder access needs consent | Complete the supported consent flow or provide the one manual action; do not widen access. |
| Current thread ID unavailable | Preserve an unknown field; request reliable identity before moving anything. |
| Binding attachment or unsaved artifact is unavailable in the destination | Resolve access/save a suitable artifact before transfer, or stay here. |
| User instructions changed repeatedly | Preserve the latest binding decision and any reason needed to avoid reversing it. Distinguish assumptions. |
| A handoff is too lossy | Keep critical constraints even if the brief grows; reject a transfer that mostly reconstructs the old context. |
| Multiple outcomes share one workspace | Track ownership, run sequentially, and avoid introducing simultaneous writers. |
| Superseded chat gets another message | Locate its successor and route authorized follow-up; no duplicate implementation. |
| Duplicate or ambiguous create response | Reconcile by handoff ID and project before another create. Similar titles do not prove identity. |
| Unsupported tool disappears mid-work | Preserve state and disclose the limitation once; do not loop or pretend success. |
| Sensitive information is in history | Keep only needed operational facts; reference accessible sources instead of spreading credentials or private transcripts. |
| Already effective compaction | Fresh low occupancy wins over historical counters; continue useful work. |
| User disables management | Respect the disabled state even if a persistent project rule still references the skill. |

## Validation boundary

Deterministic tests cover observation validation, routing, configurable intervention modes/thresholds, standalone offers, capability preflight, transfer persistence, source identity/revision/coverage, and recovery. A local host simulation exercises creation-response loss followed by reconciliation without duplicate creation. Storage tests exercise process restart, stale revisions, locks, and atomic-write failure. These tests do not call real project/chat tools. Structural checks cover skill YAML/UI metadata, entrypoint budget, local links, and Python syntax. Live-host cases remain separate and have not been run against real user projects.

The initial release must not be described as flawless or proven to reduce usage. The next validation step is a disposable or user-selected pilot with actual thread tools and observable task outcomes. Compare total work, including handoff cost, rediscovery, retries, and missing constraints, with a comparable task completed without forced rollover. Revise only on evidence rather than adding arbitrary universal rules.
