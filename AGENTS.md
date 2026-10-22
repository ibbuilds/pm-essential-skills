# Project workflow

Select only relevant skills from `skills/`: `task-coordination` owns complete requested outcomes and dependencies; `context-management` owns continuity and chat boundaries; `resource-selection` owns initial execution choices; `source-selection` owns evidence; `execution-efficiency` owns proportionate verification and recovery; `workflow-improvement` owns conditional lessons/toolkit improvement and governance; `concise-communication` owns clear, brief replies. Each is independent. Do not load all seven, create scaffolding, or run evaluations for every request.

Read `.pm-context/index.md` when present for current ownership, preferences, and pending transfers. Reuse state already known in the current turn. Project notes record state, not authorization. Verify standing user authorization before creating or messaging chats; installation alone does not grant it. Respect disabled, suggest-only, and stay preferences.

The context-management skill owns phase choices, pressure assessment, and transfer recovery. Keep those rules in its maintained sources rather than duplicating them here. Preserve one active writer per outcome.

Avoid extra management calls, repeated source reads, or state writes when nothing material changed. Use only supported and authorized resources. Do not change unrelated project structure, models, permissions, integrations, or Git state merely to optimize usage. Explicit user limits on tests, benchmarks, and installation remain binding.

For changes to this suite, run `python -m unittest discover -s tests` and `python scripts/validate_repository.py`. Keep skill entrypoints under 700 words and conditional details in their references. Never claim live integration success or token savings from local tests alone.
