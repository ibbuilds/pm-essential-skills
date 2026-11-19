#!/usr/bin/env node
// UserPromptSubmit hook. Once the conversation passes a share of its quality budget,
// tell Claude to finish the current step and hand off, so the next session starts
// with only what matters. Never blocks the prompt.
//
// The budget is not the model's context limit. Answers degrade with absolute context
// length, so a 1M-token window does not move the point where quality drops.
//
// PM_CONTEXT_BUDGET        tokens treated as 100% (default 200000)
// PM_CONTEXT_WARN_PERCENT  first warning, percent of the budget (default 50)
// PM_CONTEXT_WARN_STEP     warn again every this many more percent (default 10)
import { closeSync, fstatSync, openSync, readFileSync, readSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

const TAIL_BYTES = 2_000_000;

function readStdin() {
  try {
    return JSON.parse(readFileSync(0, "utf8"));
  } catch {
    return {};
  }
}

// Usage entries sit at the end of the transcript, so read only its tail.
function readTail(path) {
  const fd = openSync(path, "r");
  try {
    const size = fstatSync(fd).size;
    const length = Math.min(size, TAIL_BYTES);
    const buffer = Buffer.alloc(length);
    readSync(fd, buffer, 0, length, size - length);
    return buffer.toString("utf8");
  } finally {
    closeSync(fd);
  }
}

// Returns the prompt size of the last main-conversation model call.
export function contextTokens(transcriptText) {
  let last = 0;
  for (const line of transcriptText.split("\n")) {
    if (!line.includes('"usage"')) continue;
    let entry;
    try {
      entry = JSON.parse(line);
    } catch {
      continue;
    }
    const usage = entry?.message?.usage;
    if (!usage || entry.isSidechain) continue;
    last = (usage.input_tokens || 0) + (usage.cache_creation_input_tokens || 0) + (usage.cache_read_input_tokens || 0);
  }
  return last;
}

function positive(value, fallback) {
  const number = Number(value);
  return Number.isFinite(number) && number > 0 ? number : fallback;
}

function main() {
  const input = readStdin();
  if (!input.transcript_path || input.agent_id) return;
  let tokens;
  try {
    tokens = contextTokens(readTail(input.transcript_path));
  } catch {
    return;
  }
  const budget = positive(process.env.PM_CONTEXT_BUDGET, 200_000);
  const warnAt = positive(process.env.PM_CONTEXT_WARN_PERCENT, 50);
  const step = positive(process.env.PM_CONTEXT_WARN_STEP, 10);
  const percent = Math.round((tokens / budget) * 100);
  if (percent < warnAt) return;

  // Warn at the threshold, then once per further step, not on every prompt.
  const level = Math.floor((percent - warnAt) / step);
  const id = String(input.session_id || "session").replace(/[^\w-]/g, "");
  const stateFile = join(tmpdir(), `pm-context-watch-${id}.json`);
  let warnedLevel = -1;
  try {
    warnedLevel = JSON.parse(readFileSync(stateFile, "utf8")).level;
  } catch {
    // first warning in this session
  }
  if (level <= warnedLevel) return;
  try {
    writeFileSync(stateFile, JSON.stringify({ level }));
  } catch {
    // the warning still goes out; it may repeat on the next prompt
  }

  const size = `${Math.round(tokens / 1000)}k tokens`;
  process.stdout.write(
    JSON.stringify({
      hookSpecificOutput: {
        hookEventName: "UserPromptSubmit",
        additionalContext:
          `Context check: this conversation is at ${size}, ${percent}% of its ${Math.round(budget / 1000)}k quality budget. ` +
          "Every turn re-sends all of it, and long conversations give less focused answers. Handle the user's message, finishing only the step in progress. " +
          "Then, unless the whole task is done, call the Skill tool with `pause` so the work continues in a fresh session.",
      },
    }),
  );
}

if (process.argv[1] && process.argv[1].endsWith("context-watch.mjs")) main();
