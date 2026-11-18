#!/usr/bin/env node
// UserPromptSubmit hook: when the conversation's context grows past a threshold,
// add a note telling Claude to suggest a handoff. Never blocks the prompt.
//
// PM_CONTEXT_WARN_TOKENS  first warning, in tokens (default 100000)
// PM_CONTEXT_WARN_STEP    warn again after this many more tokens (default 50000)
import { readFileSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

const threshold = Number(process.env.PM_CONTEXT_WARN_TOKENS) || 100_000;
const step = Number(process.env.PM_CONTEXT_WARN_STEP) || 50_000;

function readStdin() {
  try {
    return JSON.parse(readFileSync(0, "utf8"));
  } catch {
    return {};
  }
}

// Context size = what the last model call read: fresh input plus cache reads and writes.
export function lastContextTokens(transcriptText) {
  const lines = transcriptText.split("\n");
  for (let index = lines.length - 1; index >= 0; index -= 1) {
    const line = lines[index].trim();
    if (!line.includes('"usage"')) continue;
    let entry;
    try {
      entry = JSON.parse(line);
    } catch {
      continue;
    }
    const usage = entry?.message?.usage;
    if (!usage) continue;
    return (usage.input_tokens || 0) + (usage.cache_creation_input_tokens || 0) + (usage.cache_read_input_tokens || 0);
  }
  return 0;
}

function main() {
  const input = readStdin();
  if (!input.transcript_path) return;
  let tokens;
  try {
    tokens = lastContextTokens(readFileSync(input.transcript_path, "utf8"));
  } catch {
    return;
  }
  if (tokens < threshold) return;

  // Warn at the threshold, then once per further `step` tokens, not on every prompt.
  const level = Math.floor((tokens - threshold) / step);
  const stateFile = join(tmpdir(), `pm-context-watch-${String(input.session_id || "session").replace(/[^\w-]/g, "")}.json`);
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
    // warning still goes out; it may repeat next prompt
  }

  const thousands = Math.round(tokens / 1000);
  process.stdout.write(
    JSON.stringify({
      hookSpecificOutput: {
        hookEventName: "UserPromptSubmit",
        additionalContext: `The conversation context is about ${thousands}k tokens, past the ${Math.round(threshold / 1000)}k warning point where answers start to lose earlier details. Finish the current step, then tell the user in one line and suggest /handoff to continue in a fresh session.`,
      },
    }),
  );
}

if (process.argv[1] && process.argv[1].endsWith("context-watch.mjs")) main();
