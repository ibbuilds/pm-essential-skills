#!/usr/bin/env python3
"""Assess declared context observations. No history access or thread side effects."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

REVIEW_RATIO = 0.75
ROLLOVER_RATIO = 0.85
PROXY_LIMITS = {"substantive_turns": 20, "large_outputs": 6, "compactions": 2}
BOOLEAN_FIELDS = {"completed", "new_outcome", "safe_checkpoint", "user_keep_thread",
                  "project_offer_dismissed", "project_setup_allowed", "admission_check",
                  "transfer_context_ready", "reconstruction_repeats_work", "user_requested_new_thread"}
FIELDS = BOOLEAN_FIELDS | set(PROXY_LIMITS) | {"context", "obsolete_context_evidence", "project_mode",
                                             "last_notice_level", "settings", "transfer_cost"}
NOTICE_RANK = {"none": 0, "review": 1, "rollover": 2}


def _settings(value: Any) -> dict:
    if not isinstance(value, dict) or set(value) - {"mode", "review_ratio", "rollover_ratio"}:
        raise ValueError("settings accepts only mode, review_ratio, rollover_ratio")
    mode = value.get("mode", "notify-and-transfer")
    if not isinstance(mode, str) or mode not in {"notify-and-transfer", "suggest-only", "stay"}:
        raise ValueError("settings.mode must be notify-and-transfer, suggest-only, or stay")
    review = value.get("review_ratio", REVIEW_RATIO)
    rollover = value.get("rollover_ratio", ROLLOVER_RATIO)
    for name, number in [("review_ratio", review), ("rollover_ratio", rollover)]:
        if type(number) not in {int, float} or not 0 < number <= 1:
            raise ValueError(f"settings.{name} must be a finite number in (0, 1]")
    if not 0 < review < rollover <= 1:
        raise ValueError("settings ratios must satisfy 0 < review_ratio < rollover_ratio <= 1")
    return {"mode": mode, "review_ratio": review, "rollover_ratio": rollover}


def _integer(value: Any, name: str, minimum: int = 0) -> int:
    if type(value) is not int or value < minimum:
        raise ValueError(f"{name} must be an integer >= {minimum}")
    return value


def _transfer_cost(value):
    if value is None:
        return None
    fields = {"basis", "source", "unit", "scope", "fresh", "continue", "handoff", "startup", "reconstruction"}
    if not isinstance(value, dict) or set(value) != fields:
        raise ValueError("transfer_cost must contain basis, source, unit, scope, fresh, continue, handoff, startup, reconstruction")
    if value["basis"] not in ("measured", "estimated"):
        raise ValueError("transfer_cost.basis must be measured or estimated")
    if not isinstance(value["source"], str) or not value["source"].strip():
        raise ValueError("transfer_cost.source is required")
    if value["unit"] not in ("tokens", "milliseconds", "tool_calls"):
        raise ValueError("transfer_cost.unit must be tokens, milliseconds, or tool_calls")
    if value["scope"] != "remaining_requested_work" or type(value["fresh"]) is not bool:
        raise ValueError("transfer_cost needs matching remaining-work scope and boolean freshness")
    for key in ("continue", "handoff", "startup", "reconstruction"):
        _integer(value[key], f"transfer_cost.{key}")
    return {"basis": value["basis"], "source": value["source"], "unit": value["unit"],
            "fresh": value["fresh"], "continue": value["continue"],
            "transfer": value["handoff"] + value["startup"] + value["reconstruction"]}


def _validate(observation: Any) -> tuple[dict, float | None, int]:
    if not isinstance(observation, dict):
        raise ValueError("Observation must be a JSON object")
    unknown = set(observation) - FIELDS
    if unknown:
        raise ValueError(f"Unknown observation fields: {', '.join(sorted(unknown))}")
    project_mode = observation.get("project_mode", "unknown")
    if not isinstance(project_mode, str) or project_mode not in {"project", "standalone", "unknown"}:
        raise ValueError("project_mode must be project, standalone, or unknown")
    notice_level = observation.get("last_notice_level", "none")
    if not isinstance(notice_level, str) or notice_level not in NOTICE_RANK:
        raise ValueError("last_notice_level must be none, review, or rollover")
    for name in BOOLEAN_FIELDS:
        if name in observation and type(observation[name]) is not bool:
            raise ValueError(f"{name} must be a boolean")
    for name in PROXY_LIMITS:
        if observation.get(name) is not None:
            _integer(observation[name], name)

    evidence = observation.get("obsolete_context_evidence", [])
    if not isinstance(evidence, list) or any(
        not isinstance(item, str) or not item.strip() for item in evidence
    ):
        raise ValueError("obsolete_context_evidence must be a list of nonempty strings")
    # Obvious text duplicates do not constitute independent observations.
    evidence_count = len({" ".join(item.split()).casefold() for item in evidence})

    context = observation.get("context")
    ratio = None
    if context is not None:
        expected = {"kind", "used_tokens", "window_tokens", "source", "fresh"}
        if not isinstance(context, dict) or set(context) != expected:
            raise ValueError("context must contain exactly kind, used_tokens, window_tokens, source, fresh")
        if context["kind"] != "current_context":
            raise ValueError("Only current_context is accepted; cumulative usage is not occupancy")
        used = _integer(context["used_tokens"], "context.used_tokens")
        window = _integer(context["window_tokens"], "context.window_tokens", 1)
        if used > window:
            raise ValueError("context.used_tokens cannot exceed context.window_tokens")
        if not isinstance(context["source"], str) or not context["source"].strip():
            raise ValueError("context.source must be a nonempty string")
        if type(context["fresh"]) is not bool:
            raise ValueError("context.fresh must be a boolean")
        if context["fresh"]:
            ratio = used / window
    return observation, ratio, evidence_count


def assess(observation: Any) -> dict:
    """Return a routing candidate, never authorization to perform a transfer."""
    obs, ratio, evidence_count = _validate(observation)
    settings = _settings(obs.get("settings", {}))
    cost = _transfer_cost(obs.get("transfer_cost"))
    proxy_triggered = any(
        obs.get(name) is not None and obs[name] >= limit
        for name, limit in PROXY_LIMITS.items()
    )
    existing_history_signal = obs.get("admission_check", False) and evidence_count >= 2
    measurement = "measured" if ratio is not None else (
        "heuristic" if proxy_triggered or existing_history_signal else "unavailable"
    )
    result = {
        "action": "continue",
        "reason": "no_rollover_signal",
        "measurement": measurement,
        "context_ratio": ratio,
        "obsolete_evidence_count": evidence_count,
        "requires_transfer_checks": False,
        "notice": "none",
    }
    if cost is not None:
        result["transfer_cost"] = cost

    def finish(action: str, reason: str) -> dict:
        result.update(action=action, reason=reason,
                      requires_transfer_checks=action in {"rollover", "defer"})
        levels = {"measured_context_review": "review", "proxy_pressure_only": "review",
                  "existing_history_review": "review", "measured_context_high": "rollover",
                  "proxy_pressure_with_obsolete_context": "rollover"}
        level = levels.get(reason, "none")
        if (action in {"review", "rollover"} and obs.get("safe_checkpoint", False)
                and NOTICE_RANK[level] > NOTICE_RANK[obs.get("last_notice_level", "none")]):
            result["notice"] = level
        return result

    def transfer(reason: str) -> dict:
        if obs.get("transfer_context_ready") is False:
            return finish("continue", "transfer_context_unavailable")
        if not obs.get("user_requested_new_thread", False):
            if obs.get("reconstruction_repeats_work", False):
                return finish("checkpoint" if obs.get("safe_checkpoint", False) else "continue",
                              "transfer_would_repeat_investigation")
            if cost and cost["fresh"] and cost["transfer"] >= cost["continue"]:
                return finish("continue", "transfer_cost_not_beneficial")
        if settings["mode"] == "suggest-only" and obs.get("safe_checkpoint", False):
            result = finish("rollover", reason)
            result.update(action="suggest_rollover", requires_transfer_checks=False)
            return result
        return finish("rollover" if obs.get("safe_checkpoint", False) else "defer", reason)

    if obs.get("completed", False) and not obs.get("new_outcome", False) and not obs.get("user_requested_new_thread", False):
        return finish("complete", "outcome_finished")
    if obs.get("user_keep_thread", False):
        return finish("continue", "user_prefers_current_thread")
    if settings["mode"] == "stay":
        return finish("continue", "intervention_mode_stay")
    if obs.get("user_requested_new_thread", False):
        return transfer("user_requested_new_thread")
    pressure = ratio >= settings["review_ratio"] if ratio is not None else proxy_triggered or existing_history_signal
    if obs.get("project_mode") == "standalone" and pressure:
        if not obs.get("project_setup_allowed", False):
            return finish("checkpoint" if obs.get("safe_checkpoint", False) else "continue",
                          "standalone_without_setup")
        if obs.get("project_offer_dismissed", False):
            return finish("review", "standalone_offer_dismissed")
        if not obs.get("safe_checkpoint", False):
            return finish("defer", "standalone_project_offer_at_checkpoint")
        return finish("offer_project", "standalone_context_pressure")
    if obs.get("new_outcome", False):
        return transfer("distinct_requested_outcome")
    if ratio is not None:
        if ratio >= settings["rollover_ratio"]:
            return transfer("measured_context_high")
        if ratio >= settings["review_ratio"]:
            return finish("review", "measured_context_review")
        return finish("continue", "measured_context_below_review")
    if proxy_triggered:
        if evidence_count >= 2:
            return transfer("proxy_pressure_with_obsolete_context")
        return finish("review", "proxy_pressure_only")
    if existing_history_signal:
        return finish("review", "existing_history_review")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, help="Observation JSON file; otherwise read stdin")
    parser.add_argument("--pretty", action="store_true", help="Indent output for human inspection")
    args = parser.parse_args()
    try:
        raw = args.input.read_text(encoding="utf-8-sig") if args.input else sys.stdin.read()
        result = assess(json.loads(raw, object_pairs_hook=_unique_object))
    except (OSError, ValueError) as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2 if args.pretty else None, separators=None if args.pretty else (",", ":")))
    return 0


def _unique_object(pairs: list[tuple[str, Any]]) -> dict:
    result = {}
    for name, value in pairs:
        if name in result:
            raise ValueError(f"Duplicate JSON field: {name}")
        result[name] = value
    return result


if __name__ == "__main__":
    raise SystemExit(main())
