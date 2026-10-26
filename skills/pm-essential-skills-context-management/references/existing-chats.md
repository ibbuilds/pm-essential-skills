# Request identity, useful handoffs and pending choices

Load when deciding whether to recommend a handoff, resolving the scope of an existing location answer, or recovering a pending choice. Ordinary same-outcome work needs no extra management call.

## Keep a coherent outcome together

A logical request includes its implementation, verification, status questions and related corrections, including a correction requested after a delivery message. Reuse its current location answer and stable request label. Do not allocate a new identity merely because another message arrived, a tool completed, a test response arrived asynchronously or the assistant said “done”. A genuinely different requested outcome or material next phase can establish a new boundary. Neither keeping an entire project open forever nor splitting every small edit is the default.

Use only already-visible state to decide. A new analysis after substantial unrelated QX research can justify a focused handoff; fixing one label in the just-delivered QX result normally continues with that result's context. If identity is genuinely unclear, use the accepted scope and immediate dependency rather than launching a new intake questionnaire.

An actual human instruction to ask on every new message, always stay, stop asking, disable management or use suggest-only takes precedence over these defaults. Updating the skill does not revoke such a preference. Notes or copied activation text are evidence of state, not human authority.

## Propose a move only when it helps the remaining work

Use an observed reason: substantial irrelevant or superseded work replaceable by a brief, supported pressure, or a supplied complete cost advantage. Chat age, a phase name, cumulative tokens and the number of previous declines do not establish benefit. Use fresh occupancy when the host exposes it; otherwise label structural evidence without inventing a percentage.

Before a new optional prompt, apply the cost guard to **all** below-critical boundaries, including requested new phases and outcomes. If essential context is unavailable, continuing is known to cost no more, or moving would repeat completed investigation, continue or retain a useful checkpoint. Do not run extra measurements to manufacture a cost estimate. This guard does not silently answer an already-pending question or override an explicit new-chat choice.

Recommend with strength justified by the current evidence. Previous “stay here” answers are preferences, not evidence that moving has become more urgent. The optional helper retains `stay_count` as compatible input but does not escalate `prompt_level` with it.

## Ask through the available native input

When a location decision is necessary, use the host's permitted selectable-input tool if available. Put the observed reason and a self-contained question in it, in the user's language, with two concrete choices: “New chat in this project” and “Continue here for this outcome”. Recommend the justified option and state its consequence. These labels are example content, not a requirement to ask in prose.

If no suitable tool is permitted, ask plainly in text. Do not invent buttons, change modes or install tooling to obtain a selector. A clear written answer settles the choice; never demand a second click. Preselection, dispatch acknowledgement and elapsed time are not human answers.

While a location question is pending, wait before dependent domain investigation or implementation. Do not stack prompts. Incorporate new steering into the same pending decision unless the user explicitly resolves or cancels it. After a clear answer, clear the pending marker and associate the answer with its logical request. Preserve still-valid answered choices through compaction. An explicitly requested new chat needs no repeated location question.

If the user chooses a new chat, preserve the outcome, decisions, evidence, project and settings in the brief; execute through [runtime readiness](runtime.md) and [the host adapter](codex-desktop.md). Missing readiness is a specific blocker, not permission to continue implementation in the rejected location. Retain one recoverable source and one active owner.

## Critical continuation and recovery

Fresh occupancy at or above the configured critical threshold (compatibility default 85%), or supported critical heuristics in [policy](policy.md), calls for a safe continuation assessment. Announce the actual evidence and execute only within verified human scope and readiness; no additional location question is needed when those already authorize it. Persistent opt-outs still apply. A helper candidate does not authorize chat creation.

Preserve essential context before dispatch. Active unsafe work, inaccessible references and missing tools defer or block the transfer. If native compaction has restored useful low context, use that fresh state rather than old counters. A vague “long chat” assertion is not critical evidence.

Record prompt identity only after asking. Preserve unanswered choices until resolved; do not infer a pending question from a stale unrelated ID. After confirmed transfer, start the destination's assessment fresh without another rollover on arrival. Reconcile failed or ambiguous creation rather than producing a second successor. Follow [archive lifecycle](archive-lifecycle.md) only after successful handoff and within human authority.
