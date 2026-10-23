# Standalone chat to project

Load only when verified standalone work needs durable organization, or the user explicitly requests project setup. A generated working directory is not proof of project membership. Unknown membership requires resolution, not a sales prompt.

## When and how to offer

At a safe checkpoint, offer once when fresh measured context reaches the review threshold or observed proxy pressure indicates ongoing work. Do not interrupt a short question, a completed task with no successor, or relevant work solely because time passed. An explicit user request can enter setup without waiting for a threshold.

Discover native project-create, project-list, chat-move, and membership-read capabilities once before promising automation. Cache capability facts within the session. If full support exists, ask one question:

> This conversation is becoming substantial enough to organize as a project. Would you like me to create one and move this chat into it? If so, what name should I use? You can also choose an existing project or keep this as a standalone chat.

If creation is unsupported, explain that fact in the offer: say you can move this chat after the user creates/selects a project, if movement is supported. Never offer to execute a capability the host does not expose. A folder, GitHub repository, sidebar section, Page, or LaTeX project is not a substitute for an app project.

Persist a declined or deferred offer only for this chat/work scope, using existing supported state or current conversation context. Do not keep asking at each threshold. Revisit only on an explicit user request or a meaningful scope change. Declining a project is not permission to ignore context or deny help: continue here, use concise checkpoints, and consider supported compaction when appropriate. Do not silently activate persistent project management after a move; carry forward only authorization the user actually gave.

## Create, move, verify

1. Preserve the actual current chat identity, execution location, pending operations, essential attachments, and original membership. Do not guess which chat is current from recency. Resolve safe stopping points before moving.
2. Obtain consent and the exact user-selected display name. Never derive it from a generated directory or invent one. If a supported local project requires a folder, prefer the current actual workspace when appropriate; request any missing required location in the same setup exchange. Do not create a Git repository or move files implicitly.
3. List existing projects once. If a matching name already exists, distinguish by actual ID/location and ask whether to use it or create another; names are not identities. If a prior setup attempt exists, reconcile it before creating again.
4. Create through the supported host API/UI with the given name and required location. Confirm the returned real project ID. On a lost response, reconcile before retrying. Do not fabricate an ID, blindly repeat creation, or change the name to bypass a collision.
5. Move the **existing current chat**, retaining its identity/history, to the confirmed project using the supported host operation. This consent covers this chat, not every open conversation. Preserve the execution host and source access; complete any host-managed consent flow without bypassing it.
6. Verify actual membership via a supported read. A creation result is not a move result. Only after membership is confirmed initialize or reuse project notes and project-scoped routing. If reads cannot confirm it, report the move as pending/unverified rather than complete.

Creation success + move failure: retain the created project, explain the partial result, and retry only the move if safe. Do not delete the project or recreate it. Unknown move outcome: read membership before retrying. Do not resume duplicate execution while a transfer is unresolved. If source-folder access requires a user action, preserve state and identify that one action rather than widening permissions.

Moving a chat does **not** shorten its context. Once membership is verified, reassess current pressure. If justified and authorized, use the normal handoff into one fresh project thread; otherwise keep this chat. A project is an organizational container, not a token-saving mechanism by itself.

## Current Codex desktop capability boundary

The authoring session exposed `list_projects`, `move_thread_to_project`, and thread reads, but no native app-project creation tool. `create_latex_project` creates document files and must not be used for this. Recheck available host capabilities when executing; this may change.

`move_thread_to_project` requires the correct backend/source and actual thread ID. ChatGPT chats need a ChatGPT project; Codex chats preserve their execution host. Some source-folder access requires the user to move the chat in the sidebar. Follow the actual returned result and consent requirements. Do not start a new conversation and claim the original was moved.
