# Evidence-led workflow comparison: 23 October 2026

Compared with `102d3ede7abfc40b21859998e809e43d6d20942f`, after the
repository-name correction. This is maintainer evidence, not another runtime
instruction bundle or a measured token-saving result.

## Changes worth making

| Gap | Smallest useful change | Cost boundary |
| --- | --- | --- |
| A coordinator receives changed constraints while a delegate still has the old task | Notify affected active owners; distinguish cancellation requests from cessation; reconcile late effects before conflicting replacement or integration | No broadcast for harmless changes, global shutdown, routine polling or new tracker |
| An old source still matches its fingerprint but no longer governs the current decision | Clarify content identity versus applicability, with a supersession example | No universal refresh or semantic authority claim from a helper |
| A tool returns an error without throwing, or a parallel mutation batch fails partially | Interpret operation status before payloads; reconcile uncertain dispatched effects rather than replaying the whole batch | Reuse settled receipts and documented atomic guarantees; no extra checks for valid text-only responses |

The procedures live in [task coordination](../skills/pm-essential-skills-task-coordination/SKILL.md)
and [source reuse](../skills/pm-essential-skills-source-selection/references/source-reuse.md).
Authored cases include [delegate changes](../tests/task-coordination-cases.json)
and [source applicability](../tests/source-reuse-cases.json). They specify expected
behavior; checking their structure does not demonstrate model adherence.

## Evidence and counterexamples

The [OpenAI SDK lifecycle reference](https://github.com/openai/openai-agents-python/blob/0dc4cf152bff1f50bdc0e41f28808563406545b2/.agents/references/runner-lifecycle.md)
distinguishes requesting cancellation from completion of cleanup.
[Anthropic's multiagent reference](https://github.com/anthropics/skills/blob/dbd4588f9e1033efb41dad4bef2f7947c8993d44/skills/claude-api/shared/managed-agents-multiagent.md)
describes explicit context communication between threads. These are host-specific
mechanics, not universal cancellation guarantees. Unaffected work and safe
read-only work can continue; a conflicting replacement writer needs reconciled
ownership. A late side effect is neither impossible nor newly authorized.

[Stale constraints, v3](https://arxiv.org/html/2608.25553v3) (28 August 2026)
and [STALE, v1](https://arxiv.org/html/2605.06527v1) (7 May 2026) support checking
whether inherited conclusions still apply, but their constrained/synthetic
settings do not establish a universal verification order or savings percentage.
Existing source-selection freshness rules already cover most of the mechanism;
the addition is an edge-case clarification. Historical questions can correctly
use an older source, and new facts cannot revoke explicit user restrictions.

The [MCP tool-error contract](https://modelcontextprotocol.io/specification/2026-07-28/server/tools#error-handling)
and [Promise.all semantics](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise/all)
support two [recovery examples](../skills/pm-essential-skills-execution-efficiency/references/verification-and-recovery.md):
a normal return is not necessarily operation success, and a failed aggregate is
not evidence that every peer stopped or rolled back. Errors may follow partial
effects. Valid text-only success, settled per-operation receipts and documented
atomic rollback must not provoke redundant checks or a mandatory result wrapper.
[Authored recovery cases](../tests/execution-efficiency-cases.json) cover these boundaries.

## Investigated but not adopted

- A universal routing gateway or model switcher: [this cost study](https://arxiv.org/html/2609.28919v1)
  (24 September 2026) uses emulated scenarios and dated API prices, not this
  suite's subscription usage or independently verified task quality. PM already
  considers reconstruction, caching and whole-outcome cost. No savings figure or
  extra classifier was imported.
- Mandatory schema-first execution: [this harness study](https://arxiv.org/html/2608.26197v1)
  (25 August 2026) uses two fixed, four-state synthetic pipelines and two models.
  Some determinism differences concern plan wording; latency effects differ by
  model. It does not justify forcing arbitrary project work into that controller.
- Another clarification engine or failure-memory layer: current skills already
  resolve material missing choices, preserve accepted decisions and turn verified
  recurring failures into scoped improvements. More machinery was not warranted.
- Removing UI short descriptions: a dataflow audit disproved the suspected
  routing problem. In [Codex 0.163.0's parser](https://github.com/openai/codex/blob/83086188ae0614bd882818ff1aa23f3194962012/codex-rs/skills/src/parser.rs)
  and [host provider](https://github.com/openai/codex/blob/83086188ae0614bd882818ff1aa23f3194962012/codex-rs/ext/skills/src/provider/host.rs),
  the catalog override comes from frontmatter `metadata.short-description`, not
  `agents/openai.yaml`'s UI field. Neither suite sets that override. Keep the UI
  metadata; actual host/version and model selection remain separate questions.

## Verification limits

This pass used primary documentation, pinned implementation inspection,
counterexamples and local integrity checks. It did not run paid model evaluations,
execute upstream projects, install on the user's host or prove net savings.
No new controller, mandatory service, benchmark runner or installation step was
added. Existing handoff policy, opt-outs and user-owned decisions remain intact.
