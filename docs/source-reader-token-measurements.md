# Source-reader serialization measurements

Measured 23 October 2026 using tiktoken 0.14.0 with explicit `cl100k_base` and `o200k_base` encodings. These are exact saved-artifact counts, not active-model, billing, weekly-quota, or whole-task measurements.

The reader previously escaped all non-ASCII characters. It now emits native Unicode only on UTF-8 stdout; other encodings retain ASCII escaping. Inputs, parsed JSON, source text, revision hashes, coverage, pagination, status and errors are preserved. No new instructions, dependencies, setup, or tool calls are required at runtime.

| Actual project source | cl100k before → after | o200k before → after |
|---|---:|---:|
| `existing-chats.md` | 2,075 → 2,034 | 2,065 → 2,024 |
| `verification-and-recovery.md` | 1,491 → 1,474 | 1,490 → 1,473 |

These two observed responses save 58 tokens combined under either encoding; identical request text does not change the difference. The small absolute gain reflects mostly ASCII documents. ASCII input and restricted-output controls remain unchanged. Twelve deterministic cases checked JSON equivalence, errors, restart, reuse, pagination, controls and Unicode separators. This does not establish a universal reduction for every string/tokenizer. A host that parses and reserializes tool output can change or erase the serialization advantage; model-delivered content must be checked in that host.

Separately, the existing substantial four-step source-reuse fixture saved 1,331 request+response tokens versus fresh-helper reads under both encodings. Tiny controls instead added 160–174 tokens. Loading the entire Source Selection skill and bounded-reading reference exclusively for reuse costs 2,405–2,411 tokens, more than one such workload saves. Reuse is therefore conditional, not a mandatory step on every read; native targeted reads remain appropriate for simple work.

Offline reproducible scripts, exact inputs/outputs and hashes are supplied in the accompanying cloud-workflow evidence bundle. No Codex task, CLI, external model API or live account usage was involved. The tokenizer is an evaluation-only dependency, not a suite dependency.

## Conditional reference loading

A subsequent documentation split retains the reader protocol verbatim in
`bounded-reading.md` and moves unrelated reduction/capture guidance verbatim into
`output-reduction.md`. Both old section anchors redirect to the new location.
The skill links directly to the relevant reference. No helper behavior changes.

With complete-file loading, Source Selection plus reader guidance decreases
from 2,411 to 1,573 cl100k tokens and from 2,405 to 1,566 o200k tokens: 838/839
fewer tokens. Loading both references instead adds 40/41 tokens because of the
compatibility redirects. Already-loaded guidance incurs no new setup cost, and
callers already selecting only the needed section do not gain this full-file
saving. The earlier four-read reuse workload still does not amortize exclusive
setup: it remains 242/235 tokens above the fresh-helper comparison. These limits
are part of the measurement, not exceptions to omit.

Independent comparison verified exact retained prose, relative links and legacy
anchors; nine deterministic reader-contract cases passed. This is reduced
conditional instruction payload, not proof of automatic selection or net task
savings.
