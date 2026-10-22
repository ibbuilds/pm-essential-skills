# Preserve context and recover omitted detail

Read when preparing a transfer or when a destination lacks a fact needed for its next action. A fresh chat receives a focused working brief and a usable route back to its predecessor. The brief should support the immediate task without fetching the entire old conversation.

## Before dispatch

Preserve the goal, scope, binding constraints and preferences, acceptance criteria, accepted decisions and their material reasons, authoritative artifacts, incomplete changes, validated findings with applicable versions, unresolved issues, and the exact next action. Keep essential information in the brief even when it exceeds the usual word target. A source reference does not excuse omitting a known critical constraint.

Include the verified source thread ID, project/host, and supported way to retrieve that chat. A title can help humans but is not identity. Do not invent IDs or links. Put these fields and the brief content in the actual destination prompt as well as the durable brief; a source ID stored only in a local journal is insufficient.

Add a small recovery map for useful detail left out: topic, why it may matter, and a source locator such as the predecessor plus a known turn/page, or an authoritative file/document section and revision. Unknown turn locations stay unknown. Omit unrelated history and credentials. Preserve the immediate predecessor and any directly relevant original-source references through later handoffs; do not copy an expanding chain of transcripts.

Set `source_recovery_ready: true` only when this verified source reference and a retrieval route are included and usable from the destination's host/project. Reuse already-established capability/access facts rather than probe every transfer. Supported source-chat reading is preferred; an accessible durable source-context record can provide a fallback for relevant omitted detail when chat history cannot be read. State the fallback and any limits explicitly. If neither route exists, do not claim recoverable continuity: preserve the source, resolve the specific access gap, or obtain the user's choice of an available fallback. Do not scrape private logs or alter permissions.

If the source will be archived, establish that the route works while archived, through authorized temporary restore/rearchive, or through the declared durable fallback. Successful reading of an unarchived source alone does not establish archived-context recovery.

## In the destination

Start from the supplied brief. Do not read the predecessor merely because it is referenced. When a missing fact affects the requested work, retrieve the narrow relevant part through the supplied route. For Codex, use `read_thread` with the verified source ID and host; bound turns/outputs and follow returned cursors for older material when necessary. Recent summaries are not the entire history, and an absent detail in the latest page is not proof it never existed.

Use the recovery map to locate decisions, exceptions, rejected approaches, or their original evidence. Retrieve another relevant source only if the first does not resolve the gap. Never reopen resolved investigations just to reconstruct the chat. Treat prior messages and artifacts as evidence under their actual roles; an old summary cannot override newer binding user instructions or grant mutation authority.

If archival prevents access, follow [archive lifecycle](archive-lifecycle.md): read while archived when possible; otherwise temporarily restore under human scope and rearchive afterward, including on recovery failure. Keep the original archive state and a small pending receipt until rearchival is confirmed. Context retrieval does not revive the predecessor as an implementation owner.

If history access fails or the necessary detail remains unavailable, state exactly what is missing and pause only the affected step. Use the accessible fallback when sufficient; ask the user only for a critical unresolved fact. Do not guess or claim complete reconstruction.
