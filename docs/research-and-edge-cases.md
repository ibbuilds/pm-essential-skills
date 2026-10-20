# Research decisions and edge cases

This records why the workflow takes its current shape. It is maintainer documentation, not part of the normal agent instruction path.

## Findings translated into behavior

| Evidence | Design consequence |
| --- | --- |
| [Codex best practices](https://developers.openai.com/codex/learn/best-practices) recommends one chat per coherent unit and often keeping the same problem in the same chat. Automatic compaction already exists. | No age-based restarts, no one-chat-per-edit rule, and no mandatory splitting when relevant reasoning is still useful. |
| [Prompt caching](https://developers.openai.com/api/docs/guides/prompt-caching) reuses unchanged prefixes; compaction or rewriting can reduce reuse. | Do not equate fewer historical tokens with lower total cost. Keep stable instructions small, do not rewrite them each turn, and count startup/cache effects in pilots. |
| [Prompt Caching 201](https://developers.openai.com/cookbook/examples/prompt_caching_201) discusses the tradeoff between context engineering and cache stability. | Treat thresholds as hypotheses to evaluate. Do not apply a universal cache-length threshold across models or change cache settings in a skill. |
| [Skills documentation](https://developers.openai.com/codex/skills) describes selection and progressive disclosure, not a guaranteed always-on listener. | Small core, conditional references, optional discovery pointers without duplicated workflow policy, and honest idle/invocation limits. |
| [App-server documentation](https://developers.openai.com/codex/app-server) separates thread start, history-preserving forks, compaction, and token events. | Use a fresh thread for context reset, and use only telemetry actually exposed by the host. Do not infer accessible metrics from protocol features. |
| This session exposes listing, membership moves, and thread creation, but no native app-project creation tool. | Capability-gated standalone setup; never repurpose a document/folder tool or promise an unsupported automatic project creation. |

These sources were fetched on October 20, 2026. API-level caching mechanisms explain the tradeoff; they do not establish this user's exact subscription billing or a guaranteed savings percentage.

## Skill-authoring audit, October 20, 2026

Read the current primary sources, not only search excerpts:

| Source finding | Applied change |
| --- | --- |
| [Build skills](https://learn.chatgpt.com/docs/build-skills) describes metadata-first selection, description shortening, native discovery locations, and duplicate-name behavior. | Shorten descriptions and front-load both triggers and exclusions; keep implicit invocation enabled. Document current native paths without silently duplicating or migrating the working legacy installation. |
| [Rethinking skills and prompts](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra) favors focused descriptions, conditional detail, and contextual guidance over repeated mandatory reads. | Keep workflow policy inside the independent skill folders, reduce the global rule to pointers/scope, remove stale setup requirements from maintainer docs, and keep runtime guidance conditional. |
| [Testing skills with evals](https://developers.openai.com/blog/eval-skills) separates outcome/process/efficiency goals and includes implicit and negative-control requests. | Add input/expectation fixtures for each skill alone and together, including pending answers, ordinary small edits, full coverage, truncation, and predecessor recovery. Test extracted individual resources and helpers without activation files. |
| [Harness-aware evaluation](https://developers.openai.com/cookbook/examples/partners/harness_aware_plugin_evals/harness_aware_plugin_evals) shows that tool tests and controlled model tests can differ from product behavior. | Report mechanical checks, independent interpretation tests, and desktop integration separately. Do not infer live dispatch or savings from local success. |

The source audit found no personal chat names, project IDs, or machine paths in packaged skill logic. Optional observation helpers use generic inputs; thresholds remain tunable. Build validation now rejects linked resources outside an individual skill, preventing a sibling skill or maintainer document from becoming an unnoticed runtime dependency. The global installation rule still records human-selected scope because a skill cannot grant itself coordination authority.

Independent read-only forward passes, with expected answers withheld, selected the intended workflow and next action across 19 representative cases: 11 initial cases, three predecessor-recovery cases, and five archive cases. They found a minor runtime-loading ambiguity, now clarified, and reduced confidence in negative controls after description shortening, addressed by moving exclusions earlier. A later receipt-wording ambiguity was clarified to require confirmed rearchival. This is controlled instruction interpretation, not an unmodified-host implicit invocation test or a token comparison. The user separately reported that the corrected phase-choice behavior worked; no new live desktop transfer or archive operation was performed by this audit.

The requested continuity contract is now explicit in [context recovery](../skills/context-management/references/context-recovery.md): immediate task context travels in the brief; a verified predecessor reference and recovery map travel in the actual creation prompt; later retrieval is bounded and demand-driven. Source identity alone does not prove access or completeness. Mechanical recovery checks require a source ID in the brief and declared destination access/fallback readiness, without pretending to verify semantic completeness.

The archive lifecycle follows the user's requested managed-source scope. [Projects and chats](https://learn.chatgpt.com/docs/projects) documents reversible chat archival; the [app-server reference](https://learn.chatgpt.com/docs/app-server) also documents descendant-cascading archive behavior. The skill therefore requires isolated archival after confirmed/saved handoff with no other active source work. It reads archived context directly when possible; otherwise it preserves original state before temporary restoration and confirms rearchival afterward, including on recovery failure. Originally visible chats and later human preferences remain unchanged. Missing controls or unknown cascade behavior are capability limits, not permission to improvise through private storage or another backend.

## Cases beyond the initial idea

| Case | Required response |
| --- | --- |
| Chat is standalone | Continue quietly; offer a project only when useful and permitted, obtain name/consent, then create/move/verify through real capabilities. |
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
| Already effective compaction | Fresh low occupancy wins over historical pressure counters; a separately justified requested phase still receives its location choice. |
| User disables management | Respect the disabled state even if a persistent project rule still references the skill. |

## Validation boundary

Deterministic tests cover observation validation, routing, configurable intervention modes/thresholds, standalone offers, capability preflight, transfer persistence, source identity/revision/coverage, and recovery. A local host simulation exercises creation-response loss followed by reconciliation without duplicate creation. Storage tests exercise process restart, stale revisions, locks, and atomic-write failure. These tests do not call real project/chat tools. Structural checks cover skill YAML/UI metadata, entrypoint budget, local links, and Python syntax. Live-host cases remain separate and have not been run against real user projects.

The initial release must not be described as flawless or proven to reduce usage. The next validation step is a disposable or user-selected pilot with actual thread tools and observable task outcomes. Compare total work, including handoff cost, rediscovery, retries, and missing constraints, with a comparable task completed without forced rollover. Revise only on evidence rather than adding arbitrary universal rules.
