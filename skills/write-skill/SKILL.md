---
name: write-skill
description: 'Skill authoring. Use when the user asks to create, write, edit, fix or test a skill or SKILL.md, or to turn a procedure they keep repeating into a skill, even when the change looks like one quick paragraph.'
metadata:
  type: technique
---

# Write a skill

A **skill** earns its tokens only with what Claude would not do on its own: a procedure with checkpoints, an output template, a script, or a rule backed by a failure someone actually saw.

## Process

1. Pick the primitive. Something that must happen every time is a hook. A standing fact or rule is a line in CLAUDE.md. The style of every reply is an output style. A recognizable situation, or a ritual the user starts, is a skill. Done when you can say why the chosen one fits.
2. Write the eval cases before the skill, in the format in [EVALS.md](EVALS.md): two direct, two reworded and two near-miss trigger prompts in the user's own words, plus one or two behavior cases graded on the result. Done when the case files exist.
3. Run the behavior cases without the skill, or give the user the command when you can't run it. If the baseline already passes, the skill is not needed; say so and stop. Done when you have seen the baseline fail.
4. Write the smallest SKILL.md that fixes what failed:

   <skill-template>
   ---
   name: {task verb or noun, at most three words}
   description: '{Leading word}. Use when the user says "{phrase}" or "{phrase}", or {observable symptom}, even when {the shortcut Claude would take instead}.'
   ---

   # {Title}

   **{Key term}** is {one-sentence definition}.

   ## Process

   1. {Step}. Done when {checkable condition}.

   <{output}-template>
   {the exact shape of what the skill produces}
   </{output}-template>
   </skill-template>

   The description holds triggers only, on one line, never the steps: it is loaded on every turn, and Claude follows a summarized workflow instead of reading the body. The body gives positive instructions and stays under 500 words, with the steps that must survive compaction first, since only the start of a long skill is kept. Name a convention Claude already knows instead of explaining it: write "semantic versioning", not a description of major, minor and patch. Keep only this project's choices and the steps Claude gets wrong; material only one branch needs goes in a sibling UPPERCASE.md linked from that step. A skill the user starts on purpose gets `disable-model-invocation: true` and a one-line description for humans. Done when every line answers a failure from step 3.
5. Run all cases with the skill, then delete each line whose removal leaves the results unchanged. Done when the cases pass and nothing more can go.
