# Contextual activation and workspace hygiene — 6 November 2026

The maintained suite now has eight independently installable skills. The new
workspace-hygiene owner addresses generated-file and backup accumulation during
active work. Existing entrypoints use observable task/risk triggers; coordination
and resource selection require loading matching procedures and revisiting the
selection when the work changes. No new router skill, service, model API,
background job, per-turn scan or required tracking file is introduced.

## Source mechanisms and adaptation

These sources were read directly; their prose and implementation are not copied.

| Source | Mechanism retained | Adaptation |
| --- | --- | --- |
| [Matt Pocock: writing for agents](https://github.com/mattpocock/skills/blob/4ae2317ddb22b046e26455e4f9c9b3aaaf62212d/skills/productivity/writing-for-agents/SKILL.md) | Discovery wording controls reaching a procedure; branch-specific detail belongs behind conditional pointers | Keep model-facing triggers and checkable completion; automatic contextual selection is the requested mode |
| [Addy Osmani: skill selection](https://github.com/addyosmani/agent-skills/blob/301b02b12bff98e4688e6984af6556802322bbde/skills/using-agent-skills/SKILL.md) | Route actual work to relevant engineering disciplines and compose where needed | Integrate selection into existing owners; preserve accepted scope and avoid a compulsory whole lifecycle |
| [Jesse Vincent / Superpowers: writing skills](https://github.com/obra/superpowers/blob/22f0b463e7a5e579904dd6211a520321035526f7/skills/writing-skills/SKILL.md) | Use observable symptoms, pressure/variation cases and executed outcomes | Exercise realistic isolated tasks and a simple negative control; no mandatory test-first ritual or paid evaluation service |
| [OpenAI: evaluating skills](https://developers.openai.com/blog/eval-skills) | Distinguish discovery, loading, application, outcome and efficiency | Keep helper tests separate from candidate loading and native host behavior |
| [Anthropic: authoring practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) | Concise guidance, progressive disclosure and real usage feedback | Preserve technical obligations while removing duplicated generic input-tool prose |

## Storage contract

Keep scratch, deliverables and recovery material distinct. Before producing bulk
artifacts, bound the copy/output scope and retirement condition. Prevent backups
inside their own source and repeated inclusion of previous backups. Reuse
version control when it supplies the needed recovery boundary.

The new optional standard-library inventory reads metadata and never deletes or
writes files. It limits traversal by entry count and elapsed time, skips observed
links/reparse points and reports access errors and incomplete coverage. Logical
file bytes are not physical allocation or guaranteed reclaimable capacity; hard
links count per path. It is a non-atomic observation of a mutable filesystem.
The skill permits scoped retirement of known task-owned regenerable scratch
within existing authority while retaining unknown/shared/user recovery material.

## Executed candidate exercises

Fresh independent executors received a catalog of candidate names, descriptions
and paths plus raw offline task artifacts. The user requests named no skill.
Expected answers and independent acceptance checkers were withheld. This tests
selection and application through a supplied candidate catalog, not native host
discovery. The executors had the usual host instructions and capabilities; these
are bounded forward exercises, not blinded trials or a causal improvement study.

| Natural request | Observed loading and outcome |
| --- | --- |
| Repair an export that accumulates backups | Loaded workspace hygiene, SWE debugging and construction. Removed the recursive backup mechanism, produced the correct 4,650-cent report, retained input/user note/old recovery, and retired only the authorized 12,288-byte task scratch. Two export runs produced no new backups. |
| Prevent a duplicate reservation after a lost response | Loaded SWE debugging, client engineering and verification. A regression failed before correction; eight focused tests passed afterward. The independent contract checker confirmed one effect while outcome is unknown and a legitimate new save after reconciliation. |
| Change one label and preserve its newline | Loaded no candidate skill; changed only the label and checked exact bytes. No housekeeping or verification pipeline was introduced. |

Workspace helper tests exercise nested backup visibility, preserved file bytes,
entry/time limits, access errors, link/cycle avoidance where supported, Windows
reparse detection, invalid bounds and CLI exit status. Behavioral case data in
`tests/workspace-hygiene-cases.json` adds Spanish/contextual and negative cases;
fixture integrity is not evidence that a model executed those cases.

Required repository gates and archive builds are recorded for the final candidate.
Neither shorter entrypoints nor these exercises establish measured token savings,
universal selection reliability or equivalence to another author's skill suite.
