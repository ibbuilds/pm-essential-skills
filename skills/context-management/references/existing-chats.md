# Existing chats and pressure notices

Load on first activation in an existing conversation, or when deciding whether to notify the user about context pressure. The skill applies to old project chats immediately; it does not wait for a new project or a new conversation.

## Phase choice before domain work

At turn entry, distinguish continuing the current phase from a requested next phase or distinct outcome. When a substantial project chat has established the research or accepted plan and the user says to start implementation, ask once:

> Start implementation in a new chat in this project, or continue here?

Wait for the answer before substantial implementation or further domain investigation. Acknowledge the requested work and reuse the accepted plan to make the choice concrete; do not begin the work while the question is pending. An asynchronous question is still pending until answered. Standing routing authorization permits execution after the choice; it does not choose the location for this phase.

`new_phase` means a human-requested next stage, not an invented assistant task. `substantial_history` means already-visible research, planning, iterations, or resolved material that can be replaced by a concise authoritative brief. This is a structural judgment, not a token measurement. Low or unavailable occupancy does not suppress the choice. Small plans followed by small edits, unfinished reasoning within one phase, and related follow-up fixes do not automatically trigger it.

Reuse a location choice already made for this phase. An explicit request for a new chat, an explicit choice to stay, or a relevant standing stay/disabled preference needs no repeated question. “Implement it” requests the work; by itself it does not choose the chat. A later substantial phase may warrant a fresh choice; do not ask on every turn. With unknown project membership, verify it using supported tools first. Standalone work does not require project creation or a setup interview.

If the user chooses a new chat, carry the accepted decisions, constraints, artifact references, changed work, and next action into the handoff. Preserve the same project, settings, and one owner. If essential context or capabilities block execution, explain that specific blocker once; do not silently start implementation here. If the user chooses this chat, continue immediately without pressure prompts for that choice.

## Catch-up assessment

1. Verify current project membership and whether management is enabled. Reuse known host facts. Installing the skill does not automatically activate it in every historical chat.
2. Assess the current material already available to the agent. Use a fresh current-context meter when exposed. Exact counts visible in the current supplied history may include pre-activation turns. If history is incomplete, leave total counts unknown rather than treating unknown as zero.
3. Set `admission_check: true` for this initial assessment. Without telemetry or sufficient counters, at least two distinct, concrete obsolete-context observations can trigger a heuristic `review`. Examples: superseded requirements plus lengthy output from a resolved investigation. The vague assertion that the chat is long is not evidence. This catch-up branch does not itself order rollover.
4. Do not fetch a complete transcript, parse private app data, or inspect every project conversation to make this check. If available evidence is insufficient, continue; state the measurement limitation only when relevant. Do not invent proof of high spending.
5. Evaluate the candidate handoff's relevance and reconstruction cost. Prepare a fresh thread in the **same existing project** when justified, without offering to create another project. Preserve current work before transferring.

Existing successful compaction is respected: fresh low occupancy overrides old counters and qualitative catch-up signals. Old chat age and historical cumulative usage alone never justify restarting.

## Notice once, then act

For same-phase context pressure, at a safe checkpoint give a short pressure notice before a justified transfer or material review. Name observed evidence and the next action. With standing authorization, proceed with the handoff; this pressure notice is informational. The phase-location choice above requires an answer and takes precedence when both signals apply.

Measured example:

> This chat is using 87% of its current context window. I'll preserve the current decisions and pending work, then continue in a fresh thread in this project.

Use the actual supplied value, not the example's number. This percentage does not measure wasted tokens or remaining plan allowance.

Heuristic example:

> This chat carries superseded requirements and substantial logs from resolved work. That may add unnecessary context. I'll check what needs to carry forward before continuing.

If the review supports rollover, explain the decision briefly and execute the authorized transfer. If current history remains useful, continue instead. Avoid blame and unsupported claims about how quickly the user is spending tokens.

The helper's `notice` is `none`, `review`, or `rollover`. Record the level only **after** the notice was actually shown. Supply it as `last_notice_level` on later assessments: the same or a lower level is suppressed, while escalation from review to rollover can notify once. A deferred unsafe transfer produces no pressure notice until the safe checkpoint. A standalone project offer supplies its own message; do not add a second pressure warning.

Reset notice history after a confirmed handoff, verified effective compaction, or a materially changed work scope. Do not reset it merely because one occupancy reading fluctuated. Respect a user request to stay or disable management without repeated warnings. A failed transfer does not justify repeating the pressure notice; report the actual failure/recovery action instead.
