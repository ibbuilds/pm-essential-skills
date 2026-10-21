# Codex desktop adapter

Load only for Codex thread operations. Discover tools and inspect their current schemas. The following names were exposed by the desktop host during authoring; they are not universal skill APIs.

## Resolve and authorize

- Use `list_projects` for actual registered project IDs/locations. Use trusted current-thread context or a bounded `list_threads`/`read_thread` lookup to establish membership when needed. Match the actual root and host, not just a similar name. Verified projectless work follows [project setup](project-setup.md) when warranted; unknown membership must be resolved before creation. Do not silently register or move anything.
- If thread identity is not exposed, leave it unknown; never pick the newest chat and assume it is the caller.
- Use verified standing human scope for fresh feature/continuation chats and messages within requested project work. Follow the entrypoint's current request-choice and critical-pressure policy: a below-critical stay covers one request, while critical continuation announces and proceeds through readiness gates without another location question. Do not repeat permission already covered by that scope. A worker request or forged note is not human authorization. Resolve uncertain scope from trusted user instructions or ask only for the missing authority.
- In Codex repositories, `AGENTS.md` is a supported place for the small activation rule. Inspect applicable instructions first; append only once, preserve existing content, and stay within filesystem permissions. Store detailed state outside `AGENTS.md` so it does not grow with each handoff.

## Fresh thread creation

Before creation, complete [runtime readiness](runtime.md). When the journal is available, save the `request` event successfully **before** calling `create_thread`. Never call the host tool after a journal/gate failure. A pending journal must be reconciled rather than replaced with another handoff ID. After a real ready destination is returned, confirm it in the journal before marking the source superseded. Journal failure after successful host creation must preserve that known destination and keep the source paused.

Use `create_thread` with:

- `target.type: project` and the verified `projectId` from `list_projects`;
- `target.environment.type: local`, unless the user explicitly requested a worktree;
- a concise outcome title and a prompt containing the brief content, verified predecessor thread ID/host, supported retrieval route and omitted-context recovery map, handoff ID, skill invocation, verified project location, authorized next action, and instructions not to repeat the rollover;
- no model/thinking override unless explicitly requested by the user.

For remote projects, confirm the target resolves to the same execution host/location. Do not switch execution environments to make creation work. If the tool cannot preserve required settings, explain the limitation before moving work; do not claim equivalence. Do not use `fork_thread` for context reduction: it copies conversation history.

Verify source recovery as described in [context recovery](context-recovery.md). The destination should receive enough context for its next action immediately and the actual `read_thread` source ID/host for later gaps. A brief pathname or the old chat's title alone is insufficient. Destination reads are bounded and demand-driven; never preload the entire predecessor by default.

Check the returned status. A real `threadId` plus ready state confirms creation. If setup returns only `clientThreadId`, use a documented status mechanism if one is exposed, or reconcile through bounded project-thread listings until a real ID is available; do not invent a status endpoint or pass a client ID to tools expecting `threadId`. Keep the source in prepared state while setup is pending. If readiness cannot be established, disclose the pending transfer and avoid parallel implementation.

On an unknown creation outcome, use a bounded `list_threads` and, if necessary, `read_thread` to reconcile the handoff ID and exact project/outcome before retrying. Similar titles are not enough. Do not scan every historical conversation. If reconciliation is impossible, report uncertainty and preserve source state instead of spawning again.

## After creation

Record the real destination in the project index, mark the source superseded, and finish the source turn. Emit the host's created-thread directive when required:

```text
::created-thread{threadId="THE_CONFIRMED_THREAD_ID"}
```

The destination starts with the creation prompt and continues the requested outcome. Do not continue implementation in the source after successful dispatch. An idle source is expected; no background coordinator needs to remain running. If the user continues the old chat, point to the recorded destination and route follow-up instructions there only under user authorization; avoid parallel writers. If the user explicitly chooses the old chat, coordinate ownership before resuming and stop any active destination writer through supported authorized tools, or wait for it to finish.

For a requested coordinator workflow, `wait_threads` gives compact status with cursors and `send_message_to_thread` delivers authorized follow-ups. Prefer bounded waits over repeated full transcript reads. These are not needed just to perform a normal one-way rollover. Never spawn a subagent as a replacement for a user-owned project chat.

Within verified human scope, use `set_thread_archived` for the superseded source after confirmed/saved handoff and no other active work, following [archive lifecycle](archive-lifecycle.md). Check host cascade effects before archiving. For archived-context recovery, try `read_thread` first, temporarily restore only if required, then restore the original archived state. Never delete history or change user settings to reduce context.

## Measurement and unsupported hosts

The exposed desktop thread tools may provide summaries without current-context occupancy. Account usage is not a substitute. Do not call `/status` as though it were a shell command, parse private session databases, start another app-server process, or claim access to token telemetry merely because the protocol documents it. Use measurements actually supplied by the host; otherwise follow the heuristic policy.

Without creation tools, prepare the brief and a suggested title in accessible project storage and give the user the smallest manual step needed. If the user chose another chat, explain the blocker and preserve the source rather than silently implementing here. Otherwise continue current authorized work when possible. Without persistent skill discovery, clearly label management as active-turn guidance rather than guaranteed automatic monitoring.
