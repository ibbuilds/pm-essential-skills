# Functional validation of the seven PM workflows

The seven workflows were exercised on actual synthetic tasks with fresh
executors, produced artifacts and independent outcome checks on 25 October 2026.
This extends the earlier installation audit: it is evidence of applying the
procedures, not only parsing their metadata. The source was PM `853a4cd` with SWE
`0f8d5e4` where a domain procedure was needed.

## Observed outcomes

| PM skill | Procedure actually applied | Result |
| --- | --- | --- |
| Task Coordination | Finish a report and repair, then two bounded decision artifacts; preserve prior accepted work | Complete artifacts delivered; a future large-batch benchmark was correctly left outside the authorized preparation task |
| Context Management | Assess a declared handoff with a current stay choice, missing source identity and account quota data | Completed the request in place; did not interpret 91% account usage as context occupancy or create/message a chat |
| Resource Selection | Compare available deterministic parsing, model extraction, an unconnected hosted classifier and an unverified CLI | Chose the tested local owner; no upload, installation, model switch or invented capacity claim |
| Source Selection | Read the supplied policy collection fully and distinguish superseded rules from current exceptions | Report retained all three current exceptions, revoked the old retry shortcut and identified an unresolved overlap rather than inventing precedence |
| Execution Efficiency | Diagnose the repeated deterministic rejection and select checks; then make a wording-only change | Changed the causal condition before rerunning; the later copy edit changed only the requested summary, without repeating code tests |
| Workflow Improvement | Correct the existing invoice validator rather than add another workflow system | Fixed per-invoice line scope, batch invoice uniqueness, valid zero amounts and finite/nonboolean amounts; no global rule or tracker added |
| Concise Communication | Deliver a complete report and a separate owner summary | Summary was 187 words under the 220-word request, retained the owner decision and actual checks, and did not replace the full report |

Source Selection, Workflow Improvement, Context Management and Execution
Efficiency were selected for the ordinary compound request. A follow-up explicitly
named Coordination, Resource Selection and Concise Communication to verify their
direct invocation. This is not a claim that all seven implicitly activated.

The invoice executor's ten tests passed after a failing baseline. A separate
reviewer then ran twenty contract probes against the delivered validator, including
scope, duplicate identity, empty input, zero, invalid amounts, opaque Unicode and
input preservation; all passed. The summary-only control changed exactly one
preexisting artifact. Source inputs stayed unchanged.

## Reproducible helper decisions

An independent procedure audit read all seven entrypoints and applicable
continuity/source/recovery references. It found no demonstrated material procedure
defect requiring a rewrite. It also executed 29 declared synthetic observations:

- 12 context decisions: current/expired choices, pending questions, critical
  pressure, persistent opt-outs, incomplete readiness and transfer-cost guards.
- 6 source decisions: reuse, changed revision, required complete read, denied
  access, unknown freshness and unnecessary retrieval.
- 5 preflight decisions: readiness, authority, recovery access, missing source
  identity and a correctly identified standalone source.
- 6 archive/recovery decisions: eligible source, other active work, readable
  archived history, generic read failure and confirmed/unconfirmed restoration.

The exact inputs and expected fields are retained in
[procedure-cases.json](../evaluations/procedure-cases.json). Re-run them with:

```sh
python -B evaluations/replay_procedure_cases.py
```

The replay imports the maintained pure helper functions and performs no host
mutation or model request. The count preserves this frozen set's completeness;
it is not a quota for future tests. These checks supplement the existing required
repository tests; normal skill use does not run them.

## Method and scope

[OpenAI's evaluation method](https://developers.openai.com/blog/eval-skills) calls
for checking captured execution and outputs, including explicit and negative
controls. [Anthropic's evaluation guidance](https://www.anthropic.com/research/demystifying-evals-for-ai-agents)
also distinguishes actual outcomes from an agent's declaration of success. The
cases use those methods with the suites' existing expert-source research; no
third-party procedure was copied into the runtime.

Executors received the actual task and raw fixtures, not the reviewer's intended
answer or independent checks. Follow-ups preserved context within each worker;
the invoice repair, planning and engineering workflows began in separate fresh
workers. Manual review assessed report meaning and decision ownership; behavioral
probes assessed executable artifacts. Cooperative records do not establish an
exhaustive security trace. No model/effort isolation, matched baseline for overall
guidance benefit, token telemetry, live chat transfer or archival was performed.
The cases establish these completed procedures, not universal adherence or a
numerical savings claim.
