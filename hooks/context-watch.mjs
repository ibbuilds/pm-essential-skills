#!/usr/bin/env node
// UserPromptSubmit hook: once the conversation fills a set share of the context window,
// tell Claude to suggest a handoff so the next session starts with only what matters.
// Never blocks the prompt.
//
// PM_CONTEXT_WARN_PERCENT  first warning, percent of the window (default 50)
// PM_CONTEXT_WARN_STEP     warn again every this many more percent (default 10)
// PM_CONTEXT_WINDOW        window size in tokens; otherwise 1,000,000 once usage has
//                          passed 200,000 tokens in this session, else 200,000
import { readFileSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

const SMALL_WINDOW = 200_000;
const LARGE_WINDOW = 1_000_000;

function readStdin() {
  try {
    return JSON.parse(readFileSync(0, "utf8"));
  } catch {
    return {};
  }
}

function usageTokens(usage) {
  return (usage.input_tokens || 0) + (usage.cache_creation_input_tokens || 0) + (usage.cache_read_input_tokens || 0);
}

// Returns the context size of the last model call and the largest seen in the transcript.
export function contextTokens(transcriptText) {
  let last = 0;
  let peak = 0;
  for (const line of transcriptText.split("\n")) {
    if (!line.includes('"usage"')) continue;
    let entry;
    try {
      entry = JSON.parse(line);
    } catch {
      continue;
    }
    const usage = entry?.message?.usage;
    if (!usage) continue;
    last = usageTokens(usage);
    peak = Math.max(peak, last);
  }
  return { last, peak };
}

function main() {
  const input = readStdin();
  if (!input.transcript_path) return;
  let tokens;
  try {
    tokens = contextTokens(readFileSync(input.transcript_path, "utf8"));
  } catch {
    return;
  }
  const window = Number(process.env.PM_CONTEXT_WINDOW) || (tokens.peak > SMALL_WINDOW ? LARGE_WINDOW : SMALL_WINDOW);
  const warnAt = Number(process.env.PM_CONTEXT_WARN_PERCENT) || 50;
  const step = Number(process.env.PM_CONTEXT_WARN_STEP) || 10;
  const percent = Math.round((tokens.last / window) * 100);
  if (percent < warnAt) return;

  // Warn at the threshold, then once per further step, not on every prompt.
  const level = Math.floor((percent - warnAt) / step);
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
    // the warning still goes out; it may repeat on the next prompt
  }

  process.stdout.write(
    JSON.stringify({
      hookSpecificOutput: {
        hookEventName: "UserPromptSubmit",
        additionalContext: `The conversation has used about ${percent}% of the context window (${Math.round(tokens.last / 1000)}k tokens). Answers get less reliable as old detail piles up. Finish the current step, then tell the user in one line and offer /handoff so a fresh session continues with only the essential context.`,
      },
    }),
  );
}

if (process.argv[1] && process.argv[1].endsWith("context-watch.mjs")) main();
