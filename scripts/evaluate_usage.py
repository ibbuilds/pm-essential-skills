#!/usr/bin/env python3
"""Compare supplied complete-task usage exports; no logging or model calls.

Only host-supplied per-request total_tokens are summed. Input, cached-input,
output, and reasoning subtotals must not be added to these totals again.
"""

import argparse
import json
from pathlib import Path
import sys

QUALITY = ("completed", "coverage_met", "constraints_preserved", "accepted")
RUN_FIELDS = {"task_id", "conditions_id", "model", "effort", "variant", "quality", "usage", "observations"}
METRICS = {"tool_calls", "repeated_reads", "user_interventions", "elapsed_ms"}


def integer(value, label):
    if type(value) is not int or value < 0:
        raise ValueError(f"{label} must be a nonnegative integer")


def run(value):
    if not isinstance(value, dict) or set(value) - RUN_FIELDS:
        raise ValueError("Invalid run fields")
    for key in ("task_id", "variant"):
        if not isinstance(value.get(key), str) or not value[key].strip():
            raise ValueError(f"{key} is required")
    if value["variant"] not in ("baseline", "suite"):
        raise ValueError("variant must be baseline or suite")
    for key in ("conditions_id", "model", "effort"):
        if value.get(key) is not None and (not isinstance(value[key], str) or not value[key].strip()):
            raise ValueError(f"{key} must be nonempty text or null")
    quality = value.get("quality", {})
    if not isinstance(quality, dict) or set(quality) - set(QUALITY):
        raise ValueError("Invalid quality fields")
    for key, flag in quality.items():
        if type(flag) is not bool:
            raise ValueError(f"quality.{key} must be boolean")
    observations = value.get("observations", {})
    if not isinstance(observations, dict) or set(observations) - METRICS:
        raise ValueError("Invalid observation fields")
    for key, number in observations.items():
        if number is not None:
            integer(number, key)
    usage = value.get("usage")
    totals, ids, complete = [], set(), False
    if usage is not None:
        if not isinstance(usage, dict) or set(usage) - {"source", "scope", "complete", "requests"}:
            raise ValueError("Invalid usage fields")
        if not isinstance(usage.get("source"), str) or not usage["source"].strip():
            raise ValueError("usage.source must identify the host export")
        if usage.get("scope") != "complete_task" or type(usage.get("complete")) is not bool:
            raise ValueError("usage needs complete_task scope and a boolean complete flag")
        requests = usage.get("requests")
        if not isinstance(requests, list):
            raise ValueError("usage.requests must be an array")
        known = True
        for request in requests:
            if not isinstance(request, dict) or set(request) != {"request_id", "total_tokens"}:
                raise ValueError("Requests contain only request_id and host total_tokens")
            identity = request["request_id"]
            if not isinstance(identity, str) or not identity.strip() or identity in ids:
                raise ValueError("Request IDs must be nonempty and unique within a run")
            ids.add(identity)
            total = request["total_tokens"]
            if total is None:
                known = False
            else:
                integer(total, "total_tokens")
                totals.append(total)
        complete = usage["complete"] and known and bool(requests)
    return {"task_id": value["task_id"], "variant": value["variant"],
            "conditions": tuple(value.get(key) for key in ("conditions_id", "model", "effort")),
            "quality": "failed" if any(flag is False for flag in quality.values()) else
                       "passed" if all(quality.get(key) is True for key in QUALITY) else "unknown",
            "total_tokens": sum(totals) if complete else None, "request_ids": ids,
            "observations": observations}


def compare(value):
    if not isinstance(value, dict) or set(value) != {"runs"} or not isinstance(value["runs"], list):
        raise ValueError("Input must contain a runs array")
    grouped, seen_requests = {}, set()
    for item in value["runs"]:
        record = run(item)
        if seen_requests & record["request_ids"]:
            raise ValueError("A model request cannot be counted in multiple runs")
        seen_requests.update(record["request_ids"])
        pair = grouped.setdefault(record["task_id"], {})
        if record["variant"] in pair:
            raise ValueError("Duplicate task/variant; use distinct task IDs for repeated pairs")
        pair[record["variant"]] = record
    pairs = []
    baseline_total = suite_total = 0
    all_measured = bool(grouped)
    all_quality = bool(grouped)
    for task, pair in grouped.items():
        result = {"task_id": task, "token_delta": None, "relative_token_change": None}
        if set(pair) != {"baseline", "suite"}:
            result.update(status="unpaired", quality="unknown")
        else:
            baseline, suite = pair["baseline"], pair["suite"]
            same = (all(item is not None for item in baseline["conditions"])
                    and baseline["conditions"] == suite["conditions"])
            if baseline["request_ids"] & suite["request_ids"]:
                raise ValueError("Baseline and suite cannot reuse the same model request")
            quality = "failed" if "failed" in (baseline["quality"], suite["quality"]) else (
                "passed" if baseline["quality"] == suite["quality"] == "passed" else "unknown")
            result["quality"] = quality
            result["observation_deltas"] = {
                key: suite["observations"][key] - baseline["observations"][key]
                for key in METRICS if baseline["observations"].get(key) is not None
                and suite["observations"].get(key) is not None and same}
            if not same:
                result["status"] = "conditions_unmatched_or_unknown"
            elif baseline["total_tokens"] is None or suite["total_tokens"] is None:
                result["status"] = "usage_incomplete_or_unavailable"
            else:
                left, right = baseline["total_tokens"], suite["total_tokens"]
                baseline_total += left
                suite_total += right
                result.update(status="measured", baseline_tokens=left, suite_tokens=right,
                              token_delta=right - left,
                              relative_token_change=(right - left) / left if left else None)
        all_measured = all_measured and result["status"] == "measured"
        all_quality = all_quality and result["quality"] == "passed"
        pairs.append(result)
    # Do not cherry-pick complete or successful pairs into an aggregate savings claim.
    delta = suite_total - baseline_total if all_measured else None
    return {"pairs": pairs, "all_pairs_measured": all_measured,
            "all_quality_passed": all_quality, "total_token_delta": delta,
            "relative_token_change": delta / baseline_total if all_measured and baseline_total else None,
            "observed_improvement": all_measured and all_quality and delta < 0,
            "interpretation": "supplied observations only; no causal or statistical guarantee"}


def unique(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate field: {key}")
        result[key] = value
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path)
    args = parser.parse_args()
    try:
        raw = args.input.read_text(encoding="utf-8-sig") if args.input else sys.stdin.read()
        try:
            value = json.loads(raw, object_pairs_hook=unique)
        except RecursionError as exc:
            raise ValueError(str(exc)) from exc
        result = compare(value)
    except (ValueError, OSError, TypeError) as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        return 2
    print(json.dumps(result, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
