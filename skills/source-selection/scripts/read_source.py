#!/usr/bin/env python3
"""Read a bounded local UTF-8 source page, reusing known unchanged coverage.

No cache database, persistent writes, account access, or token estimates.
Spans use zero-based character offsets [start, end); line bounds are one-based.
"""

import argparse
import hashlib
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from assess_source import assess, unique

FIELDS = {"path", "start_line", "end_line", "max_chars", "cursor", "expected_revision",
          "loaded_source_id", "loaded_revision", "loaded_spans", "reread_spans", "content_available",
          "required_full_read", "force_read"}
MAX_BYTES = 16 * 1024 * 1024


def integer(value, label, minimum=0):
    if type(value) is not int or value < minimum:
        raise ValueError(f"{label} must be an integer >= {minimum}")
    return value


def merge(spans):
    result = []
    for start, end in sorted(spans):
        if start == end:
            continue
        if result and start <= result[-1][1]:
            result[-1][1] = max(result[-1][1], end)
        else:
            result.append([start, end])
    return result


def missing(start, end, spans):
    result, position = [], start
    for left, right in spans:
        if right <= position or left >= end:
            continue
        if left > position:
            result.append([position, left])
        position = max(position, right)
    if position < end:
        result.append([position, end])
    return result


def read_source(value):
    if not isinstance(value, dict) or set(value) - FIELDS:
        raise ValueError("Unknown source-read fields or non-object input")
    if not isinstance(value.get("path"), str) or not value["path"].strip():
        raise ValueError("path is required")
    for key in ("content_available", "required_full_read", "force_read"):
        if key in value and type(value[key]) is not bool:
            raise ValueError(f"{key} must be a boolean")
    for key in ("loaded_source_id", "loaded_revision", "expected_revision"):
        if key in value and (not isinstance(value[key], str) or not value[key].strip()):
            raise ValueError(f"{key} must be nonempty text")
    budget = integer(value.get("max_chars", 12000), "max_chars", 1)
    if budget > 100000:
        raise ValueError("max_chars exceeds 100000; paginate or use a specialized reader")
    path = Path(value["path"]).expanduser().resolve(strict=True)
    # Bound the actual read, including a concurrent growth of the file.
    with path.open("rb") as stream:
        raw = stream.read(MAX_BYTES + 1)
    if len(raw) > MAX_BYTES:
        raise ValueError("Local reader supports files up to 16 MiB; use a streaming/specialized reader")
    revision = "sha256:" + hashlib.sha256(raw).hexdigest()
    text = raw.decode("utf-8-sig")
    if "\x00" in text:
        raise ValueError("Binary source; use a specialized reader")
    # Match physical LF-delimited source lines used by rg and native code tools.
    # Keep CR (including CRLF) and Unicode separators in the original offsets.
    parts = text.split("\n")
    lines = [part + "\n" for part in parts[:-1]]
    if parts[-1]:
        lines.append(parts[-1])
    source_id = path.as_uri()
    result = {"source_id": source_id, "revision": revision, "total_chars": len(text),
              "total_lines": len(lines)}
    if value.get("expected_revision") not in (None, revision):
        return result | {"action": "restart", "reason": "source_changed_during_pagination",
                         "content": [], "coverage_spans": [], "coverage_sufficient": False,
                         "full_read_complete": False}
    if value.get("cursor") is not None and "expected_revision" not in value:
        raise ValueError("Pagination cursor requires expected_revision")
    start_line = integer(value.get("start_line", 1), "start_line", 1)
    end_line = integer(value.get("end_line", max(1, len(lines))), "end_line", 1)
    if end_line < start_line or start_line > max(1, len(lines)) or end_line > max(1, len(lines)):
        raise ValueError("Requested line range is outside the source")
    if value.get("required_full_read", False):
        start, end = 0, len(text)
    else:
        start = sum(map(len, lines[:start_line - 1]))
        end = sum(map(len, lines[:end_line]))
    known = value.get("loaded_spans", [])
    if not isinstance(known, list):
        raise ValueError("loaded_spans must be an array")
    for span in known:
        if not isinstance(span, list) or len(span) != 2:
            raise ValueError("Each loaded span must be [start, end)")
        if integer(span[1], "span end") < integer(span[0], "span start"):
            raise ValueError("Invalid loaded span")
    matching = (value.get("content_available", False) and value.get("loaded_source_id") == source_id
                and value.get("loaded_revision") == revision)
    if matching and any(right > len(text) for _, right in known):
        raise ValueError("Loaded span exceeds matching source length")
    known = merge(known) if matching else []
    # Forced passes keep independent coverage: old loaded content is not evidence
    # that the explicit reread happened. As with loaded_spans, callers must only
    # supply spans whose content is still available from this pass.
    reread = value.get("reread_spans", [])
    if not isinstance(reread, list):
        raise ValueError("reread_spans must be an array")
    for span in reread:
        if not isinstance(span, list) or len(span) != 2:
            raise ValueError("Each reread span must be [start, end)")
        if integer(span[1], "reread span end") < integer(span[0], "reread span start"):
            raise ValueError("Invalid reread span")
    if matching and any(right > len(text) for _, right in reread):
        raise ValueError("Reread span exceeds matching source length")
    reread = merge(reread) if matching and value.get("cursor") is not None else []
    sufficient = not missing(start, end, known)
    decision = assess({"source_id": source_id, "loaded_source_id": value.get("loaded_source_id"),
                       "loaded_revision": value.get("loaded_revision"), "current_revision": revision,
                       "content_available": value.get("content_available", False),
                       "coverage_sufficient": sufficient, "freshness_required": True,
                       "revision_verified": True, "access": "available"})
    if decision["action"] == "reuse" and not value.get("force_read", False):
        return result | {"action": "reuse", "content": [], "coverage_spans": known,
                         "coverage_sufficient": True, "full_read_complete": not missing(0, len(text), known)}
    cursor = integer(value.get("cursor", start), "cursor")
    if not start <= cursor <= end:
        raise ValueError("Cursor is outside the requested range")
    cursor_coverage = reread if value.get("force_read", False) else known
    if missing(start, cursor, cursor_coverage):
        raise ValueError("Cursor would skip unread content; include prior matching "
                         + ("reread_spans for this forced pass" if value.get("force_read", False)
                            else "coverage"))
    gaps = [[start, end]] if value.get("force_read", False) else missing(start, end, known)
    content, remaining = [], budget
    for left, right in gaps:
        left = max(left, cursor)
        if left >= right or remaining == 0:
            continue
        right = min(right, left + remaining)
        content.append({"start": left, "end": right, "text": text[left:right]})
        remaining -= right - left
    coverage = merge(known + [[item["start"], item["end"]] for item in content])
    pending = missing(start, end, coverage)
    # A forced reread must complete its newly emitted page sequence, even if old content exists.
    if value.get("force_read", False):
        reread = merge(reread + [[item["start"], item["end"]] for item in content])
        pending = missing(start, end, reread)
        result["reread_spans"] = reread
    return result | {"action": "read", "content": content, "coverage_spans": coverage,
                     "coverage_sufficient": not pending, "next_cursor": pending[0][0] if pending else None,
                     "full_read_complete": not missing(0, len(text), coverage)
                     and not (value.get("force_read", False) and pending)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path)
    args = parser.parse_args()
    try:
        raw = args.input.read_text(encoding="utf-8-sig") if args.input else sys.stdin.read()
        result = read_source(json.loads(raw, object_pairs_hook=unique))
    except (ValueError, OSError, TypeError) as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        return 2
    print(json.dumps(result, separators=(",", ":"), ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
