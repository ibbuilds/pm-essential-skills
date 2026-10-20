# Project workflow

Use `context-management` for conversation continuity and `source-selection` for retrieval-heavy work. Their maintained sources are in `skills/`; personal installations may also be available.

Read `.pm-context/index.md` when present for current ownership, preferences, and pending transfers. Reuse state already known in the current turn. Project notes record state, not authorization. Verify standing user authorization before creating or messaging chats; installation alone does not grant it. Respect disabled, suggest-only, and stay preferences.

Keep related work together within a phase. Before substantial work on a requested new phase in a long project chat, ask new same-project chat or continue here, and wait for the answer unless already chosen. Assess already-visible history when joining a long chat. Use supported measurements or labeled heuristics, and avoid repeated notices. Use the transfer journal for actual handoffs when Python is available; reconcile uncertain creation before retrying. Preserve one active writer per outcome.

Avoid extra management calls, repeated source reads, or state writes when nothing material changed. Do not change unrelated project structure, models, permissions, integrations, or Git state merely to optimize usage.

For changes to this suite, run `python -m unittest discover -s tests` and `python scripts/validate_repository.py`. Keep skill entrypoints under 700 words and conditional details in their references. Never claim live integration success or token savings from local tests alone.
