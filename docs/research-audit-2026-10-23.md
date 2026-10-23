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

The pinned SDK [parent-cancellation regression case](https://github.com/openai/openai-agents-python/blob/0dc4cf152bff1f50bdc0e41f28808563406545b2/tests/test_run_step_execution.py#L2733-L2788)
explicitly leaves child cleanup unfinished after the parent exits. Conversely,
[cooperative nested cancellation](https://github.com/openai/openai-agents-python/blob/0dc4cf152bff1f50bdc0e41f28808563406545b2/tests/test_agent_as_tool.py#L3806-L3872)
checks the relevant child and handler have stopped. Reuse such scoped evidence;
neither a completion flag nor parent exit universally settles external effects.
These upstream tests were inspected, not executed.

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


## Extended comparison: error handling and evaluation health

The inspected [Anthropic skill-evaluation helper](https://github.com/anthropics/skills/blob/dbd4588f9e1033efb41dad4bef2f7947c8993d44/skills/skill-creator/scripts/run_eval.py#L210-L239)
coerces worker exceptions to `False`, then uses low activation rates to pass
expected-negative cases. Static inspection therefore identifies a path where
execution failure can look like favorable negative-control behavior; it does not
establish that a whole mixed evaluation passes or that a particular reported run
was affected. The helper was not executed or imported. Our evaluator has no live
runner and does not synthesize those observations. A maintainer-only note in
[efficiency evaluation](efficiency-evaluation.md) now separates execution health
and trace coverage from activation, retaining failed attempts and their costs.
A valid completed answer without a tool call remains a valid negative.

Current [Superpowers debugging](https://github.com/obra/superpowers/blob/2ce8aa15d05bd57213e6f746f953aafb7ded7a8b/skills/systematic-debugging/SKILL.md)
and [verification](https://github.com/obra/superpowers/blob/2ce8aa15d05bd57213e6f746f953aafb7ded7a8b/skills/verification-before-completion/SKILL.md)
were compared against existing diagnostic evidence, ownership and freshness
rules. No fixed retry-count architecture gate, universal test-first repair or
same-message rerun requirement was adopted. An unchanged verified artifact can
reuse applicable evidence; a clear new supported hypothesis can justify another
attempt without a mandatory escalation. Popularity is not evidence that every
procedure is efficient for every task.


## Locally reproduced helper failures

- A version-1 installation receipt with `files: []` raised an uncaught attribute
  error. Field/record validation now rejects malformed receipts before use,
  preserves their bytes and returns the existing structured error format.
- Replacing an interrupted transaction target with a FIFO blocked recovery while
  opening it. Transaction reads now reject nonregular files and verify the opened
  descriptor; the regression preserves the journal and other targets, then
  recovers only after explicit fixture reconciliation. This is not permission
  for the helper to delete unexpected user objects.
- Lowering a transfer journal's attempt counter while leaving its event history
  intact bypassed the resolved-failure retry gate. Version-1 history is complete
  and unpruned, so validation now checks lifecycle consistency and request count.
  Inconsistent state is rejected unchanged; history still does not prove host
  outcomes or grant authorization. Durable journal/brief reads also reject
  nonregular files before blocking; failed preparation releases its owned lock.
  Regular symlinked briefs and explicit event-input streams remain supported.

- Conflicting duplicate JSON fields in recovery evidence were accepted with
  last-value semantics: a duplicated `before` could turn restoration into
  deletion and remove the journal. Persistent receipt/journal parsing now rejects
  duplicates before mutation, while a valid `before: null` still restores the
  intentional absence of a newly created file.
- The optional hook independently read its receipt and could block on a FIFO or
  emit guidance from malformed selection metadata. Its standalone reader now
  rejects nonregular inputs, checks the opened descriptor and validates selection
  shape. Broken metadata produces the established neutral result; valid selected
  skills still work, without reflecting prompt text or adding installer imports.

These are isolated local reproductions and regression checks, unlike the
upstream tests inspected above. They do not establish live host integration or
change the existing handoff permission policy.


## Malformed-input diagnostics remain usable

Isolated malformed YAML exceeded the parser's recursion capacity and escaped
both repository validators as a traceback. Decoder-local handling now collects
a concise file-labelled error and continues other checks; it does not impose a
new depth limit or catch arbitrary business-logic exceptions. PM additionally
collects unreadable Markdown/Python and invalid manifest-shape errors, while
resource failures still prevent package creation. Containment checks continue
to precede existence checks for already-outside links.

The stateless JSON helpers preserve their existing exit-2/JSON-error contract
when the decoder reaches its own nesting limit. The local source reader likewise
normalizes path-resolution failures without rejecting valid regular-file aliases.
Tests preserve normal stdin/file input and avoid tying acceptance to a particular
Python version's diagnostic wording. These are error-path corrections, not a
change to skill-selection or handoff policy.


## Duplicate metadata and host compatibility

A temporary skill with repeated `name` or `description` keys passed the prior
PyYAML-based validators because the later value replaced the earlier one.
Codex [0.163.0's typed frontmatter parser](https://github.com/openai/codex/blob/83086188ae0614bd882818ff1aa23f3194962012/codex-rs/skills/src/parser.rs)
uses a derived deserializer whose [pinned duplicate-field handling](https://github.com/serde-rs/serde/blob/v1.0.228/serde_derive/src/de/struct_.rs#L265-L272)
rejects repeated recognized fields. Its loader records that parse failure rather
than adding the skill. This is a source-backed discovery mismatch, not a live
host-selection test.

The validator now rejects duplicate explicit string keys before merge expansion,
with file/key location diagnostics. Tests retain optional metadata, shared aliases
and legal merge overrides instead of confusing inherited values with explicit
duplicates. Invalid optional UI metadata is a separate case: the Codex metadata
loader can discard it without discarding the skill itself. No claim is made that
these checks emulate every host parser or prove model adherence.


## Generalize the useful correction, not every successful step

[XRepoSkill v1](https://arxiv.org/html/2609.36807v1) contrasts trajectories and
separates source and evaluation cases. Its reported per-issue cost exceeds the
no-skill baseline on both benchmark averages, with offline discovery outside
those totals; it is not evidence of token savings for these suites. Inspected
[scoring](https://github.com/XREPOSKILL/XRepoSkill/blob/26fd70345698108c0fdce2d8904293a38b9cd42f/src/xreposkill/score.py)
and [generalization](https://github.com/XREPOSKILL/XRepoSkill/blob/26fd70345698108c0fdce2d8904293a38b9cd42f/src/xreposkill/generalize.py)
also limit causal interpretation: issue stratification is not randomized rule
assignment, and cluster membership need not mean every member was independently
scored. No claim of actual benchmark contamination follows from this inspection.

The existing workflow-improvement owner gains one conditional distinction:
separate useful corrections from incidental work before widening a lesson.
Available contrasting cases can support that judgment; absent broader evidence,
keep its conditions rather than demanding a paid campaign. Two authored cases
contrast cargo-cult full scans/tests with a separately supported narrow invariant.
No retrieval engine, learning pipeline, fixed rule count or model evaluation was
added.

[Authoring Agent Skills v1](https://arxiv.org/html/2607.25032v1) is a design note,
not a controlled efficiency study; its useful progressive-disclosure and
availability guidance is already covered. [GitSkills v3](https://arxiv.org/html/2608.10906v3)
is descriptive, not effectiveness evidence. Identical entrypoint bytes do not
establish identical referenced scripts or package provenance. No dataset-mining
or popularity-based automation was imported.


## Portable field validation versus native permissiveness

The validators now consistently apply the published [Agent Skills field contract](https://agentskills.io/specification):
nonblank descriptions up to 1,024 characters, and a string-to-string mapping when
optional `metadata` is present. Missing metadata and an empty map remain valid;
diagnostics explain quoting scalar values or omitting an unused field. Unknown
root extensions are not rejected by an invented allowlist.

These are bounded portable-format checks, not claims about every Codex rejection.
The inspected Codex release preserves overlong descriptions and accepts some
scalar coercions or blank metadata that the portable contract does not. PM's
whitespace-only description case is a demonstrated local false-green against the
host's normalized nonempty requirement. All checked-in skills already meet these
field constraints; this work does not establish a current live-loading failure
or guarantee future host selection.


### Preserve hook ownership on malformed optional-installer receipts

A temporary fixture reproduced a malformed `hooks.groups` traceback. Review then
found a consequential falsey-record case: changing an installed receipt’s `hooks`
to `[]` let uninstall remove the managed helper while leaving registered hooks.
The receipt reader now rejects present malformed or empty ownership before any
mutation; absence still means no hooks, and valid `original: null` remains valid.
A local regression checks structured failure and unchanged receipt, helper,
guidance and hook bytes, alongside valid ownership restoration. This changes
only the optional legacy installer, not normal skill installation or host policy.

## Direct Codex review of real repository code

A user-authorized Codex chat reviewed fixed SWE `a36c47d` and PM `8facb21`
source using the supplied Software Review and Execution Efficiency instructions.
Relevant source was provided directly after isolated-run setup failed; this was
not automatic skill discovery, a baseline comparison, or an evaluation of every
skill. The SWE validator review reported no actionable finding within its scope.

The PM usage-evaluator review produced two static findings, both independently
reproduced against the actual source before correction:

- An unpaired run with a known quality failure was reported as unknown. The
  aggregate improvement guard already remained false; the correction preserves
  the failure without calling an incomplete successful pair passed.
- Accepted integer totals could overflow the derived floating-point ratio and
  escape the CLI's structured-error boundary. That boundary now handles overflow;
  large exact totals with representable ratios remain accepted.

Focused regressions cover these failures and neighboring valid cases. This is
concrete useful review output, not evidence that the skills caused better review
quality or reduced tokens. Review usage and net savings were unavailable, and
setup failures do not count as successful negative controls.
