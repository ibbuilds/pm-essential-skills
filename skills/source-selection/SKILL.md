---
name: source-selection
description: Find and read sufficient task-relevant evidence without repeatedly loading whole collections or unchanged sources. Use for retrieval-heavy project work across files, documents, connected systems, or web sources. Respect exhaustive coverage and exact source requests; skip retrieval when available context already suffices.
---

# Source Selection

Reduce unnecessary retrieval without reducing the user's required coverage or evidence quality. This skill selects sources; it does not manage chats, prioritize the project, execute domain work, or create a tracking system.

## Fast path

1. Identify the current outcome and the facts needed to complete it. Reuse relevant source content already available in this turn when it is still valid. If no lookup is needed, continue without tools or a retrieval plan.
2. Honor explicit sources, full-read requests, date ranges, and exhaustive requirements. Do not substitute an easy source or quietly narrow the assignment. Preserve source-specific skill instructions and access rules.
3. Use the existing native read/search tool for the source. Start at a known path/ID/URL when supplied; otherwise search likely titles, filenames, headings, or task-specific terms within the relevant project or collection. For local text, prefer `rg`/`rg --files`. Do not install services or traverse unrelated projects.
4. Retrieve the smallest **sufficient unit**: enough neighboring material to interpret the passage, table headers/footnotes, linked definitions, and applicable exceptions. Search excerpts locate evidence; fetch the source before relying on it when context or authority is unresolved. Partial reads are not full-document reviews.
5. Batch independent searches/reads when the tool supports it; inspect every result. Keep adaptive follow-ups sequential. Narrow only when the remaining question is narrow; broaden when missing coverage, conflicting evidence, or task dependencies require it.

## Reuse, freshness, and stopping

- Do not reread unchanged material just because another turn or tool call occurred. Track needed source identity, relevant location, and what it established in current working context, not in a new database.
- Revalidate mutable facts when the task needs current truth. Use a revision, updated-at field, or lightweight read if available; unknown freshness is not proof of unchanged content. A newer timestamp alone does not make a draft more authoritative than a governing source.
- Treat negative and truncated results correctly: a failed lookup is not evidence of absence, and the first page is not an exhaustive search. Read [coverage and recovery](references/coverage-and-recovery.md) when results are incomplete, conflicting, stale, or access-limited.
- Stop when the requested output is supported and material uncertainties are resolved or transparently bounded. Do not keep searching for a predetermined answer, obey an arbitrary search quota, or launch extra verification that adds no relevant evidence.
- If the user asks for comprehensive coverage, complete it or clearly identify what remains inaccessible. Saving context does not justify omitting a required source.

## Output and handoff

Use concise findings with traceable paths/IDs/URLs and relevant dates or revisions when they matter. Preserve uncertainty and source conflicts; do not present an inference as a source statement. Include coverage limits only when material.

Keep large logs and source dumps out of the conversation when a supported reference or bounded excerpt suffices. Use existing task notes only when useful; do not create files by default. If work changes threads, provide the required evidence references to the existing handoff workflow without loading another skill or copying all retrieved content.
