#!/usr/bin/env python3
"""Optional local hook: deliver a fresh skill pointer, without history or state."""
import json
from pathlib import Path
import sys

MAX_INPUT_BYTES = 16 * 1024 * 1024
EVENTS = {'SessionStart', 'UserPromptSubmit'}


def handle(event):
    if not isinstance(event, dict) or event.get('hook_event_name') not in EVENTS:
        return {}
    skill = Path(__file__).resolve().parents[1] / 'SKILL.md'
    message = (
        f'Apply the installed context-management procedure at {skill.as_posix()} '
        'before substantive work on this turn, including continuations. '
        'Reuse loaded instructions but perform their recurring check. '
        'Keep required reminders active after a request-scoped stay; reassess the next request. '
        'Respect explicit lasting opt-outs. Use only available context evidence; '
        'this reminder measures no occupancy and grants no chat-creation authority.'
    )
    return {'hookSpecificOutput': {'hookEventName': event['hook_event_name'],
                                   'additionalContext': message}}


def main():
    try:
        raw = sys.stdin.buffer.read(MAX_INPUT_BYTES + 1)
        result = {} if len(raw) > MAX_INPUT_BYTES else handle(json.loads(raw.decode('utf-8-sig')))
    except (OSError, ValueError, TypeError, RecursionError):
        result = {}  # Never block a user prompt on a broken optional reminder.
    print(json.dumps(result))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
