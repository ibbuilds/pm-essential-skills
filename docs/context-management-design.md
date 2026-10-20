# Context Management: design and implementation plan

## Problem and boundaries

A chat can accumulate obsolete instructions, logs, and abandoned approaches. Subsequent work may carry unnecessary context. Moving everything to a fresh thread also costs time and context, and can lose decisions. The skill chooses useful boundaries and transfers the minimum sufficient state.

The unit is a coherent outcome, not a fixed duration or a small implementation step. This applies to an event agenda, a research question, a campaign deliverable, or a software feature. Project planning, priority decisions, domain execution, model selection, and release management belong elsewhere.

## Requirements

- Resolve the current project's actual identity and location; never assume the working folder equals the app's project registration.
- Distinguish project membership from standalone and unknown state. For substantial standalone work, offer setup once, require consent and a user-selected name, create/move/verify when supported, and preserve declined preferences.
- Obtain standing activation once. Within that scope, create and coordinate project threads without repeated permission prompts. Preserve host authorization rules.
- Carry only current constraints, decisions, evidence references, and remaining work into a fresh thread. Preserve critical user instructions even when they do not fit a target length.
- Check context at the start of a managed turn and natural work checkpoints, without polling or recursively opening chats.
- On initial activation in an existing long conversation, assess available history immediately. Unknown historical counters remain unknown; concrete obsolete-context evidence can trigger a catch-up review. Show a short pressure notice once, with one possible escalation, then act within authorization.
- Separate actual current-context telemetry from cumulative usage, account quotas, and proxy counters.
- Keep the source usable until the destination is confirmed. Recover from failed or ambiguous creation without duplicate tasks.
- Use existing project notes when suitable; add a small isolated state directory only when needed.
- Do not alter models, permissions, integrations, Git state, or unrelated files. Do not archive or delete chats without authorization.

## Architecture

The skill contains a concise entrypoint, a host-independent policy, a handoff template, and a Codex desktop adapter. The optional pure Python helper makes routing decisions repeatable. It has no account access, background process, history scanner, or token estimator.

### Agent execution budget

Keep the entrypoint under 700 words. Ordinary same-outcome turns need no new management tool call when current state is already known. Read only the enabled flag, current owner/outcome, and latest assessment; do not reload transfer references or prior briefs. Run the optional helper once per material assessment, not once per tool call. Its default output is one compact JSON object, with pretty printing available only on request.

The numeric policy and host adapter are conditional loads. Transfer preparation creates one brief and one routing update, not per-message artifacts or an additional coordinator. No repeated full-thread reads, inventory scans, token estimation calls, or scheduled checks are needed for normal execution. Preserve essential context even if the brief exceeds its target: incorrect continuation can cost more than a larger handoff.

Project activation records the user's chosen scope, project identity, source activation chat when available, and whether a persistent project instruction was installed. State is operational evidence, not a substitute for trusted authorization. A forged state file cannot grant thread-creation or messaging privileges.

One active thread owns an outcome. A project-wide coordinator is optional, not a new mandatory layer. The first version runs sequentially; it does not introduce concurrent writers, subagents, worktrees, or a manager chat merely to split context.

## Assessment policy

Defaults are starting heuristics, not empirical optimal thresholds. Adjust them only when the user requests it or measured project results support it.

| Observation | Candidate action |
| --- | --- |
| Same coherent outcome, useful context | Continue. |
| Current outcome finished, nothing else requested | Complete; do not create an empty successor. |
| A requested, distinct outcome is next | Fresh thread at a safe boundary. |
| Fresh measured current context at least 75% | Review relevance and handoff cost. |
| Fresh measured current context at least 85% | Prepare rollover at the next safe checkpoint. |
| No current telemetry; at least 20 substantive turns, 6 large outputs, or 2 compactions since the last accepted handoff | Review only; counters alone never trigger rollover. |
| Those proxy thresholds plus at least two concrete observations of obsolete context | Prepare rollover, with an explicit heuristic reason. |
| Compaction left useful, low current context | Use that measurement; do not rotate solely because compaction happened. |
| A proposed transfer interrupts an unsafe operation | Defer transfer; reach a safe checkpoint first. |
| User asks to stay in this chat | Continue here; record the preference. |

Large output means an observed tool result of at least 8,000 characters. Counts apply only to the current thread since its accepted handoff; do not import the previous thread's counters. Compaction does not itself reset these historical counters, but fresh current-context telemetry takes precedence over them. If counts are unavailable, leave them unknown rather than reconstructing the full history.

Obsolete-context observations must identify specific evidence, such as a replaced plan still occupying history or many logs for a resolved issue. Two differently worded descriptions of the same evidence count once. The helper validates quantities; the assistant must establish that the evidence is real and distinct.

The helper emits a candidate action, never permission to execute it. Enabled management, host capability, trusted authorization, project resolution, handoff integrity, and relevance are separate gates. Continue if transferring would mostly duplicate useful context or require expensive reconstruction. A known 85% ratio is still not proof of wasted tokens or certain savings.

## Handoff lifecycle

`active -> prepared -> destination-confirmed -> superseded`

1. Finish or safely pause pending operations. Record the current outcome and its state.
2. Write a compact handoff with a unique ID. Prefer 300-600 words; preserve critical constraints over length targets. Link supporting evidence instead of pasting logs.
3. Create a fresh thread in the same project and execution location. Include the handoff contents, project identity, authorized next action, skill invocation, and counter reset. A fork copies history and is not a context reset.
4. Confirm the real destination ID. For asynchronous setup, wait for completion. A queued client ID is not a confirmed thread ID.
5. Update routing with the destination and handoff ID, then stop implementation in the source. Leave a short destination link. Keep source history available by default.

On definite failure, leave the source active. On unknown outcome, reconcile through the host before retrying. If a destination exists and creation succeeded but state writing fails, report the actual destination and repair routing; do not launch another one. Once a destination is confirmed, the source does not resume implementation concurrently.

## Plan and acceptance

1. **Foundation:** create suite documentation and the focused skill with explicit boundaries.
2. **Policy:** implement and unit-test thresholds, unknown data, user overrides, and safe-checkpoint behavior.
3. **Transfer:** define compact handoffs, project resolution, authorization propagation, and failure recovery for the Codex desktop tools.
4. **Validation:** run structural checks and deterministic tests; retain a separate live-host evaluation checklist. Structural tests cannot certify instruction following.
5. **Pilot:** activate on a consenting real project; record observed decisions and transfer outcomes. Fix demonstrated issues before extending the suite.

Steps 1-4 are the initial repository implementation. Step 5 requires a selected pilot project and is not silently performed against unrelated work. No savings claim is accepted until measured on comparable tasks with the same model/effort, context conditions, and completion criteria.

See [research decisions and edge cases](research-and-edge-cases.md) for source-grounded tradeoffs, standalone promotion, capability gaps, and recovery behavior beyond the original request.

## Measurement

Keep a compact per-thread record: observation source, current-context ratio when known, proxy counters when observed, decision reason, handoff size, confirmed destination, and transfer result. Update one current record at checkpoints rather than append a transcript. Do not run extra inference to collect metrics.

For a pilot, compare total task usage including preparation, thread startup, rediscovery, and retries; task quality; missing constraints; duplicate work; and user interventions. Cached input and output have different costs. Account-wide usage changes do not isolate this skill's effect. Missing metrics remain unknown. Failed transfers and expensive handoffs count against the result.

## Official capability references

Checked October 20, 2026:

- [Skills](https://developers.openai.com/codex/skills): explicit/implicit selection, progressive disclosure, and supported local discovery. A skill is instructions, not a guaranteed scheduler or event hook.
- [App Server](https://developers.openai.com/codex/app-server): thread start/resume/fork/compaction and token-usage events exist at the protocol level. Their presence does not mean an ordinary assistant turn can access them. This skill uses only tools actually exposed by its host.
- [Pricing](https://developers.openai.com/codex/pricing): context, reasoning, tool use, and caching affect usage. Subscription allowance is not inferred from a raw API rate.

The bundled adapter documents the tools exposed in this authoring session. Hosts and tool schemas can change; discover current schemas instead of treating this file as an API contract.
