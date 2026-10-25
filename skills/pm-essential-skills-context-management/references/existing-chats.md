# Request prompts and critical continuations

Load on first activation in an existing conversation, or when deciding whether to notify the user about context pressure. The skill applies to old project chats immediately; it does not wait for a new project or a new conversation.

## Check every new request before domain work

Check each substantive new user request against already-visible history. A long project chat qualifies when substantial prior research/planning/resolved work can be replaced by a focused brief, fresh occupancy reaches the review threshold, or supported proxy/catch-up evidence warrants review. Assess old history immediately; do not wait for post-install growth. Accepted planning followed by implementation is a boundary even with low/unknown occupancy. Do not wait for a numeric threshold at these structural boundaries. Before a new below-critical pressure-only question, reuse known transfer costs/reconstruction evidence: if no next phase/outcome was explicitly requested and essential destination context is unavailable or a move is already known to cost at least as much as continuing or repeat completed investigation, continue quietly or preserve a concise checkpoint instead. This exception never dismisses an unanswered question, overrides a human location choice, or changes critical policy. Unknown costs are not a reason to invent estimates or run extra calls. Otherwise, below critical pressure, ask through the host's supported selectable-input tool when available and permitted in the current mode. The following is question content, not a substitute for that tool:

> [Name the observed replaceable material, or label the supplied complete cost comparison and its basis.] A focused handoff may help. Start this request in a new chat in this project, or continue here for this request?

Present two concrete choices: “New chat in this project” and “Continue here for this request”; recommend the justified option and briefly state its consequence. Honor the tool schema, language and free-text support. If no permitted interactive tool exists, ask the same choice plainly in text; do not invent buttons, change mode or install tooling just to ask. A clear written answer settles the choice too; never require a second click. A preselected option, tool acknowledgement or timeout is not a human answer.

Use an actual observed reason, not the bracketed placeholder or a generic claim about length. For a backstop-only review without identified replaceable material or a complete cost comparison, state the observed occupancy/proxy and that the benefit is unestablished. Context occupancy alone is not proof of savings.

Wait before implementation or domain investigation. An asynchronous question remains pending until answered. Do not stack questions or interpret elapsed time as consent. Standing routing authority permits execution after the choice; it does not answer a below-critical location question.

“Continue here” applies to the current request, not the entire phase or chat. Complete that request without further prompts. On the next distinct request, if the chat still qualifies, ask again—even for a small follow-up edit. A location answer alone, clarification of unfinished work, status check, or tool result does not create another request. Never ask repeatedly within the same process.

Evaluate what a user reply requests, not its transport wrapper. After a delivered build, result, or verification checkpoint, “it works, now fix/change these things” requests new work even when submitted through an asynchronous testing question. The testing reply is not a location-choice answer. Allocate a new request label and perform the continuation assessment before investigating or changing the newly requested work. A feature or project remaining unfinished does not keep all future user requests inside one perpetual request. Pure “yes, it works” feedback without more work needs no new location prompt. Steering received while implementation is still in progress stays with that current request; do not interrupt each mid-process correction.

Track a stable current request label, the request answered/prompted, and the count of actual stay choices in this chat. Host IDs may be reused when exposed; otherwise use a labeled local request identifier, not a fabricated host ID. Prefer visible context or existing notes; keep only a bounded current record when persistence is useful. Increment stay count once per actual answer, never per helper/tool call. New request IDs expire older answers. Preserve unknown counts as unknown; do not invent an escalation history.

After an answer, clear the pending-choice flag and associate the answer with this request ID. Do not increment the count again when reusing that answer. If a new request arrives while a question is still unanswered, incorporate the request into the pending decision rather than stacking another question.

Escalate concise recommendations after stays: first, offer a fresh chat; next, say “I recommend moving this request to a fresh chat”; after repeated stays, say “I strongly recommend moving this request now.” Keep the two choices available below critical pressure. Firm wording must reflect actual structural or measured evidence; never claim that tokens are wasted, quality has failed, or a percentage is known without evidence. Saturate at strong rather than inventing increasingly dire claims.

An explicit “stop asking,” persistent “always stay here,” disabled management, or suggest-only preference is different from a one-request stay and remains binding until changed. An explicit new-chat request needs no repeated question. With unknown membership, resolve it through supported tools first. Short chats without a qualifying signal remain quiet; standalone work requires no project-setup interview.

If the user chooses a new chat, carry decisions, constraints, artifacts, findings, and next action into the handoff. Preserve project, settings, predecessor recovery, and one owner. If readiness blocks execution, explain that blocker once; do not silently implement here against the chosen location.

## Assess useful retained context, not a goal label

At new requests and natural safe checkpoints, use already-known content to identify material that a focused brief can replace: superseded requirements, resolved investigations or redundant logs. Preserve active constraints, decisions, evidence references and the next authorized action. A nominal "goal finished" label, elapsed time or message count does not prove a move helps; a useful brief must avoid lost context and repeated investigation. Substantial replaceable history already permits early review without waiting for percentages. A fresh supplied comparable cost advantage can also justify an early recommendation at low occupancy; label its basis and apply [policy](policy.md). No extra model calls, full-history scans, token guesses or routine logging are required. Reuse a current request's location answer and never stack another question.

## Catch-up assessment

1. Verify current project membership and whether management is enabled. Reuse known host facts. Installing the skill does not automatically activate it in every historical chat.
2. Assess the current material already available to the agent. Use a fresh current-context meter when exposed. Exact counts visible in the current supplied history may include pre-activation turns. If history is incomplete, leave total counts unknown rather than treating unknown as zero.
3. Set `admission_check: true` for this initial assessment. Without telemetry or sufficient counters, at least two distinct, concrete obsolete-context observations can trigger a heuristic `review`. Examples: superseded requirements plus lengthy output from a resolved investigation. The vague assertion that the chat is long is not evidence. This catch-up branch does not itself order rollover.
4. Do not fetch a complete transcript, parse private app data, or inspect every project conversation to make this check. If available evidence is insufficient, continue; state the measurement limitation only when relevant. Do not invent proof of high spending.
5. Evaluate the candidate handoff's relevance and reconstruction cost. Prepare a fresh thread in the **same existing project** when justified, without offering to create another project. Preserve current work before transferring.

Existing successful compaction is respected: fresh low occupancy overrides old counters and qualitative catch-up signals. Old chat age and historical cumulative usage alone never justify restarting.

## Critical pressure: announce, then transfer

At critical pressure, do not ask another location question. Announce the observed reason and perform the authorized continuation at a safe checkpoint. Critical pressure means fresh occupancy at/above the configured rollover ratio (default 85%), or supported critical heuristics in [policy](policy.md). A previous one-request stay or unanswered below-critical prompt does not permanently veto this threshold. Explicit persistent opt-outs still apply.

Measured example:

> This chat is using 87% of its current context window. I'll preserve the current decisions and pending work, then continue in a fresh thread in this project.

Use the actual supplied value, not the example's number. This percentage does not measure wasted tokens or remaining plan allowance.

Heuristic example:

> This chat carries superseded requirements and substantial logs from resolved work. That may add unnecessary context. I'll check what needs to carry forward before continuing.

Missing metrics remain unknown; chat age alone is not a critical measurement. For heuristics, name concrete observed problems rather than assert an invented occupancy percentage. Essential-context loss, unsafe work, inaccessible references, or missing host capabilities defer/block actual creation. Preserve a ready brief and source recovery rather than force a broken transfer.

The helper's `prompt_level` is 1–3 and derives from known prior stay choices. Record `last_prompt_request_id` only after actually asking. Reassessing that request returns `await_thread_choice` until answered; the next request is eligible again. Legacy `last_notice_level` deduplicates informational pressure notices, never the next request's location prompt. A deferred unsafe transfer produces no pressure notice until a safe checkpoint.

After confirmed handoff, start the destination's request/escalation history fresh; do not repeat rollover on arrival. Effective compaction resets pressure notices when warranted, but does not erase known one-request choices or fabricate a new task. A failed transfer requires recovery, not another successor or repeated permission loop. After success, apply the existing archive lifecycle to the superseded source.
