# Eval cases for `claude plugin eval`

One folder per case under `evals/`, named `<skill>-trigger-<direct|reworded|near-miss>-<n>` or `<skill>-behavior-<n>`.

```
evals/<case>/prompt.md          # the user message, phrased the way a user types it
evals/<case>/graders/<name>.md  # one file per check
evals/<case>/case.yaml          # only when the case needs fixture files
evals/<case>/setup.sh           # the fixture script that case.yaml points to
```

`prompt.md`:

```
---
description: "What this case checks"
max_turns: 8
allowed_tools: [Read, Glob, Grep, Skill]
---

Grill me on this plan before I commit to it: ...
```

Graders:

```
---
type: tool_used
tool: Skill
input_match: '"skill"\s*:\s*"(?:[\w-]+:)?<skill-name>"'
---
```

For a near-miss, add `min: 0`, `max: 0` and `arm: both` so the check passes only when the skill stays silent.

```
---
type: llm
focus: { source: file, path: OUTPUT.md }
---

PASS if <what a correct result contains>.
FAIL if <what the failure you saw in the baseline looks like>.
```

Other types: `regex` (`pattern`, `target`, `match: not_contains`), `file_exists` (`path`), `tool_order`.

Fixtures: `case.yaml` holds `schema_version: "1.1"`, `name` and `context: { scaffold_script: setup.sh }`; the script creates the files before Claude starts.

Run, always with a cost ceiling:

```
claude plugin eval . --case '<skill>-behavior-*' --runs 3 --ablation none --scaffold --allow-tools Write --max-cost-usd 2 --no-publish
claude plugin eval . --case '<skill>-*' --runs 3 --ablation with-without --scaffold --allow-tools Write --max-cost-usd 5 --no-publish
```

Tools such as Write, Bash and WebFetch run only when `--allow-tools` grants them. The first command is the baseline before the skill exists. The second compares with and without the plugin once it does.
