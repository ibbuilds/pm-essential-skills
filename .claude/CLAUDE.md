# Maintaining this plugin

This repository is a Claude Code plugin. Skills live in `skills/<name>/SKILL.md`. Eval cases for `claude plugin eval` live in `evals/<case>/`.

## Every skill

- Write the eval case first and run it without the skill. Add the skill only when that baseline fails, and keep a line only when removing it makes an eval worse.
- Model-invoked description: one line, at most 500 characters. Start with the leading word, then "Use when" with the phrases users type, any tokens only this skill owns, and an "even when..." clause naming the shortcut Claude would take instead. Never summarize the workflow.
- User-invoked skill (`disable-model-invocation: true`): a one-line summary for humans.
- Body: only what Claude would not do by default. Use positive instructions, steps that end in "Done when...", and output templates in XML-style tags. Prohibitions belong only in discipline skills, backed by excuses seen in baseline runs.
- Budgets: 500 body words, or 1,500 for `metadata.type: discipline`; 20 KB per `SKILL.md`. Put content that must survive compaction first.
- Branch-only material goes in sibling `UPPERCASE.md` files, linked from the step that needs it. No `@` links. To use another skill, write "Call the Skill tool with `<name>`".
- Name eval cases `<skill>-trigger-<direct|reworded|near-miss|unrelated>-<n>` and `<skill>-behavior-<n>`.

## Checks

```sh
python scripts/lint_skills.py
python -m unittest discover -s tests
claude plugin validate . --strict
claude plugin eval . --case <case> --runs 3 --ablation with-without --scaffold --allow-tools Write --judge-model sonnet --no-publish --max-cost-usd 2
```

Write, Bash, WebSearch and WebFetch only run in an eval when `--allow-tools` grants them, even if the case lists them. Granting Bash fails on machines where the sandbox cannot inspect every PATH directory; grant only what the case needs. The default Haiku judge is noisy on writing-quality graders; use Sonnet for behavior cases.

On Windows use `py -3` for `python`, and run evals from PowerShell after `$env:Path = 'C:\Program Files\Git\bin;' + $env:Path`, or every `setup.sh` scaffold fails with "bash not in PATH". `--case` takes one glob; repeat the command per skill. Model-backed evals spend real usage: always pass `--max-cost-usd` and run only the cases you changed.
