#!/usr/bin/env python3
"""Bounded, read-only workspace metadata inventory; never classifies deletion safety."""
import argparse
import heapq
import json
import os
from pathlib import Path
import stat
import time


def linked(info):
    return stat.S_ISLNK(info.st_mode) or bool(
        getattr(info, "st_file_attributes", 0) & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 1024))


def inventory(root, *, top=10, max_entries=50000, max_seconds=5.0):
    if ".." in Path(root).parts:
        raise ValueError("Use an explicit project path without parent traversal")
    root = Path(os.path.abspath(root))
    if top < 1 or top > 100 or max_entries < 1 or not 0 < max_seconds <= 3600:
        raise ValueError("top must be 1-100; limits must be positive (seconds <= 3600)")
    # Check the supplied path before resolving it: resolving first would conceal a junction.
    for parent in (root, *root.parents):
        if linked(parent.lstat()):
            raise ValueError("Project path must not traverse a link or reparse point")
    if not root.is_dir() or root == root.parent:
        raise ValueError("Choose an existing project directory, not a filesystem root")
    started = time.monotonic()
    groups, largest, errors = {}, [], []
    counts = dict(entries=0, files=0, logical_bytes=0, skipped_links=0, skipped_special=0, error_count=0)
    limits = []
    # Keep open directory iterators only on the traversal stack, never a full-tree path list.
    stack = []

    def error(path, exc):
        counts["error_count"] += 1
        if len(errors) < 10:
            errors.append({"path": path, "error": type(exc).__name__})

    def open_dir(path, group):
        try:
            stack.append((os.scandir(path), group))
        except OSError as exc:
            error(os.path.relpath(path, root), exc)

    open_dir(root, None)
    try:
        while stack:
            if counts["entries"] >= max_entries:
                limits.append("max_entries")
                break
            if time.monotonic() - started >= max_seconds:
                limits.append("max_seconds")
                break
            iterator, group = stack[-1]
            try:
                entry = next(iterator)
            except StopIteration:
                iterator.close()
                stack.pop()
                continue
            except OSError as exc:
                error("." if group is None else group, exc)
                iterator.close()
                stack.pop()
                continue
            counts["entries"] += 1
            try:
                info = entry.stat(follow_symlinks=False)
                if linked(info):
                    counts["skipped_links"] += 1
                    continue
                bucket = entry.name if group is None else group
                if stat.S_ISDIR(info.st_mode):
                    groups.setdefault(bucket, {"logical_bytes": 0, "files": 0})
                    open_dir(entry.path, bucket)
                elif stat.S_ISREG(info.st_mode):
                    size = info.st_size
                    counts["files"] += 1
                    counts["logical_bytes"] += size
                    data = groups.setdefault(bucket, {"logical_bytes": 0, "files": 0})
                    data["logical_bytes"] += size
                    data["files"] += 1
                    item = (size, Path(entry.path).relative_to(root).as_posix())
                    if len(largest) < top:
                        heapq.heappush(largest, item)
                    elif item > largest[0]:
                        heapq.heapreplace(largest, item)
                else:
                    counts["skipped_special"] += 1
            except OSError as exc:
                error(Path(entry.path).relative_to(root).as_posix(), exc)
    finally:
        for iterator, _ in stack:
            iterator.close()
    return {"root": str(root), "status": "partial" if limits or counts["error_count"] else "complete",
            **counts, "limits": limits, "errors": errors,
            "largest_top_level_paths": [{"path": name, **data} for name, data in
                                        sorted(groups.items(), key=lambda row: (-row[1]["logical_bytes"], row[0]))[:top]],
            "largest_files": [{"path": name, "logical_bytes": size} for size, name in sorted(largest, reverse=True)],
            "measurement": "logical file bytes; hard links counted per path; skipped links excluded; no deletion advice"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path)
    parser.add_argument("--top", type=int, default=10)
    parser.add_argument("--max-entries", type=int, default=50000)
    parser.add_argument("--max-seconds", type=float, default=5.0)
    args = parser.parse_args()
    try:
        result = inventory(args.project, top=args.top, max_entries=args.max_entries, max_seconds=args.max_seconds)
    except (OSError, ValueError) as exc:
        print(json.dumps({"status": "error", "error": str(exc)}))
        return 2
    print(json.dumps(result, ensure_ascii=True))
    return 0 if result["status"] == "complete" else 1


if __name__ == "__main__":
    raise SystemExit(main())
