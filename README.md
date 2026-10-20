# PM Essential Skills

Reusable AI skills that reduce avoidable context, repeated investigation, and unnecessary coordination across projects. Preserve useful work and the user's control while improving total task efficiency.

The suite works across project types. It does not prescribe how to code, design, research, or produce the project's deliverables. Git, GitHub, and other services can be optional adapters; none is required to use the suite. See [suite principles and skill boundaries](docs/suite-principles.md).

## Skills

| Skill | Responsibility | Avoidable work addressed |
| --- | --- | --- |
| [Context Management](skills/context-management/SKILL.md) | Conversation boundaries, project association, and reliable handoffs | Carrying obsolete conversation context and repeating work after a bad transfer. |
| [Source Selection](skills/source-selection/SKILL.md) | Locate and read sufficient task-relevant evidence | Repeatedly loading entire collections, unchanged files, and unrelated search results. |

Each skill works independently. Neither requires another manager skill or a mandatory project structure.

## First skill: Context Management

[`skills/context-management`](skills/context-management/SKILL.md) keeps conversations focused on a coherent outcome and moves work into a fresh thread when there is a useful boundary or excessive context. It creates a concise handoff, preserves the project association, and resumes the authorized work when the host supports thread creation.

The first version is a reviewable implementation, not a measured token-savings claim. Long conversations can increase usage, but caching, automatic compaction, model choice, reasoning, and reconstruction costs affect whether a fresh thread is cheaper. More threads are not automatically better.

## Use it

1. Install the `skills/context-management` directory in a skill location supported by your host. For Codex, a repository-local location is `.agents/skills/context-management`; a personal location is `~/.codex/skills/context-management`. Do not copy this suite into every project unless you want project-local installations.
2. In the target project, send the [activation prompt](skills/context-management/assets/activation-prompt.txt). This gives standing authorization to create and coordinate threads within the requested work. It does not authorize new project scope.
3. Continue asking for work normally. The skill checks boundaries during active turns and at safe checkpoints. It avoids interrupting useful work just to satisfy a message-count rule.

Install `skills/source-selection` in the same way when useful. Invoke it with `$source-selection` for a retrieval-heavy task, or let the host select it implicitly when appropriate. It needs no standing write authorization or tracking database: it uses available read tools, keeps existing source requirements, and does not create project files by default.

Implicit skill selection is enabled, but selection is not a guaranteed per-turn hook. For persistent project discovery, the activation workflow offers a small, project-local instruction referencing the skill. It preserves existing instructions. A skill cannot run while the assistant is idle or change an app's context policy by itself.

This repository does not enable management for itself, install globally, or modify any project just by being checked out.

## What is automatic

| Capability | Behavior |
| --- | --- |
| Detect a task boundary | Separate independently describable outcomes; keep related edits and follow-up fixes together. |
| Join an existing long chat | Assess already-visible history immediately; issue one evidence-based pressure notice and prepare a same-project handoff when justified. No waiting for future growth. |
| Recognize standalone work | Offer project setup once when warranted; obtain the user's name and consent, create/move only through supported host capabilities, and verify membership. |
| Evaluate context pressure | Use fresh current-context telemetry when exposed. Otherwise use labeled structural signals. |
| Prepare continuation | Record current state, binding decisions, references, pending work, and a specific next action. |
| Create a fresh chat | Use the host's supported thread tools under standing user authorization. Preserve the project and execution location. |
| Complete the transfer | Verify creation, record the destination, and finish the source turn without duplicate implementation. |
| Missing capabilities | Keep working when possible and provide a ready-to-use handoff. Do not fabricate a thread or measurement. |

Thread tools are currently documented for the Codex desktop adapter. The core workflow is domain independent; other hosts need an equivalent supported adapter or use the manual handoff fallback. The skill is not a background monitor and cannot guarantee every turn will invoke it.

The current authoring host can move chats to existing projects but exposes no app-project creation tool. The skill includes the complete capability-gated setup flow and an honest fallback. Moving an existing chat organizes it; a separate fresh-thread handoff is what can reduce carried context.

## Development

Requires Python 3.10+ for the optional deterministic policy helper; the skill itself is instruction based. Runtime Python dependencies: none.

```powershell
py -3 -m unittest discover -s tests -v
py -3 scripts/validate_repository.py
```

Example policy assessment:

```powershell
py -3 skills/context-management/scripts/assess_context.py --input tests/fixtures/high-context.json
```

The helper only assesses supplied observations. It neither reads chat histories nor creates threads. See the [design and implementation plan](docs/context-management-design.md) and [behavioral evaluation cases](tests/behavioral-cases.md).

The [research and edge-case review](docs/research-and-edge-cases.md) explains source-based decisions, project setup, capability gaps, and failure handling.

The agent execution path is deliberately small: a core skill under 700 words, conditional policy/adapter references, no extra management calls during unchanged same-task work, and compact JSON from the optional helper. Measured token savings still require a real project pilot.

## Contributing

Keep each skill responsible for one distinct source of avoidable project work. Prefer a small entrypoint with conditional references over a large instruction bundle. Add scripts only for repeatable decisions or mechanics that benefit from deterministic behavior. Preserve the user's workflow, authorization, tools, and chosen project structure.

Changes to routing or handoffs need examples where continuation should happen, where it should not, and where a transfer fails. Evaluate output quality and coordination overhead alongside usage. Do not claim savings from chat age, cumulative token counts, or a dashboard category alone.
