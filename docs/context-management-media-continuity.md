# Media continuity in fresh-chat handoffs

The intended outcome is a destination that can continue using the same relevant visual/temporal evidence, without asking the user to rebuild context. A text-only brief, source chat ID or filename cannot establish that outcome when the task depends on the original image or recording.

## Behavior

- Select images, videos and other attachments needed for remaining work; omit obsolete or unrelated media.
- Recover originals through exposed source-conversation/attachment tools, known original files or durable artifacts. Reuse access facts. Do not scan unrelated chats, private logs or caches, and do not ask for reattachment before exhausting supported recovery.
- Put original provenance, purpose, authoritative version, destination-usable locator, read/transport method and access evidence or blocker in the existing brief and destination prompt. Reuse originals; retain at most one scoped copy when access/lifetime requires it. Never clone the whole history or put base64 payloads into the prompt.
- The destination opens required images before visual work. For video, retain original and relevant timestamps; preserve timing, motion or audio when the task depends on them. Derived frames/OCR/transcripts must be sufficient for the actual task and explicitly labeled with omissions. They are not blanket substitutes.
- Missing essential media blocks complete readiness. A source-local path does not prove remote access; an expired link or textual chat summary does not recover original content. Do not claim receipt, inspection or successful visual continuity without corresponding evidence. Keep the source recoverable and required assets retained.

The existing preflight accepts two additional declared boolean observations: `media_required` and `media_context_ready`. When media is required, unknown/missing/false readiness blocks `transfer_ready`, even if text/source-reference gates are true. Unknown relevance and explicit media-access failure also block it. Legacy text-only clients remain accepted without these fields; that is not evidence of a media review. The skill requires a relevance assessment before declaring readiness. Missing media must propagate to the existing references/recovery journal gates, rather than bypass a failed preflight with invented all-true flags. No downloader, new journal format, background process or extra per-turn file is introduced.

## Host capability boundary

Reviewed the exposed desktop tool schemas on 6 November 2026: `create_thread` and `send_message_to_thread` accept a text prompt, not an attachments array; `read_thread` provides turn/status summaries, not guaranteed attachment bytes. When exposed native forwarding is unavailable, a verified original file accessible to the destination plus an instruction to load it is a usable alternative. It must not be described as native attachment forwarding.

The [official app-server protocol](https://learn.chatgpt.com/docs/app-server) supports text, image and localImage turn inputs. That lower-level capability does not make those fields available in every desktop connector. This skill does not start another server, invent parameters, change settings, or claim universal video support. A future host exposing native attachment retrieval/forwarding can use it without changing the purpose or fidelity checks.

The earlier comparison with [Pocock's handoff](https://github.com/mattpocock/skills/blob/main/skills/productivity/handoff/SKILL.md) and [Osmani's context-engineering](https://github.com/addyosmani/agent-skills/blob/main/skills/context-engineering/SKILL.md) supports concise artifacts, selective context and restartable work. Those general patterns do not establish media transport in this host; the actual tool contract and destination access determine it.

## Verification scope

Focused preflight tests cover all-text gates passing with required media missing/false/unknown, available required media, irrelevant media, unknown relevance, explicit access failure, legacy text-only clients, and invalid truthy values. Existing transfer gates and the current40% warning/60% ceiling policy remain required. These tests validate declared readiness decisions, not actual retrieval or forwarding.

An isolated destination-agent check uses an original synthetic image on shared storage and the available image viewer, plus scenario checks for a missing recording needed for timing/audio, a history summary without original image access, unrelated media and an unreachable remote path. This is separate from native desktop chat creation/forwarding; no user chats or private media are used for the check.

The independent check opened the actual PNG with `view_image` and correctly described its orange upper-right triangle and blue lower-left circle on white, without receiving that description in its task. The fixture SHA-256 was `76cb657c0aed87a482035c35851cfd760b65ecda1591a89e6d8c693bed0bfd9a`. It rejected two stills as insufficient for timing/audio diagnosis, rejected a text summary as sufficient for exact styling, omitted irrelevant media, and rejected a source-local path as proof of remote access. It identified an ambiguous use of “ready”; the procedure now names transport readiness and actual inspection separately. These checks establish the observed isolated behavior, not a universal native forwarding capability.
