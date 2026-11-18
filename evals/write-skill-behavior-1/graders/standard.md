---
type: llm
focus: { source: file, path: skills/commit-message/SKILL.md }
---

PASS only if all hold: the frontmatter description is a single line that says when to use the skill with phrases a user would actually type (for example "commit message"), and does not list the skill's steps; the body is short (roughly under 300 words) and includes a concrete template or example of a Conventional Commits message; the body does not explain things Claude already knows, such as what git is.
FAIL if the description summarizes the workflow or has no user phrases, or the body is long, generic or has no template or example.
