#!/usr/bin/env python3
"""Summarize comparable first-take score records; never modify them."""
import argparse
import datetime as dt
import json
import math
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
CONTEXT_FIELDS = ("speaker", "language", "prompt_family", "audience", "format", "preparation_seconds", "conditions")
MODALITIES = {"audio", "video", "raw_asr", "reviewed_transcript"}
REVIEW_STATES = {"supported", "contradicted", "uncertain", "not_independently_reviewed"}


def text_value(value):
    return isinstance(value, str) and bool(value.strip()) and value.lower().strip() not in {"unknown", "unspecified", "n/a"}


def number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def load_record(path):
    with path.open(encoding="utf-8") as handle:
        record = json.load(handle)
    if not isinstance(record, dict) or record.get("schema_version") != 1:
        raise ValueError("unsupported or missing schema_version")
    if not text_value(record.get("session_id")):
        raise ValueError("missing session_id")
    try:
        date = record["date"]
        if not isinstance(date, str) or dt.date.fromisoformat(date).isoformat() != date:
            raise ValueError
    except (KeyError, TypeError, ValueError):
        raise ValueError("invalid session date") from None
    digest = record.get("media_sha256")
    if not isinstance(digest, str) or re.fullmatch(r"[0-9a-fA-F]{64}", digest) is None:
        raise ValueError("missing or invalid media_sha256")
    context = record.get("context")
    if not isinstance(context, dict):
        raise ValueError("missing context")
    if context.get("take_type") != "first":
        raise ValueError("not a recorded first take")
    for field in CONTEXT_FIELDS:
        value = context.get(field)
        if field == "preparation_seconds":
            if type(value) is not int or value < 0:
                raise ValueError("missing or invalid comparison field: " + field)
        elif not text_value(value):
            raise ValueError("missing comparison field: " + field)
    if not isinstance(record.get("scores"), list):
        raise ValueError("missing scores list")
    return record


def validate_score(score):
    if not isinstance(score, dict):
        return "score must be an object"
    for field in ("rubric", "criterion", "assessor"):
        if not text_value(score.get(field)):
            return "missing score field: " + field
    if score.get("review_status") not in REVIEW_STATES:
        return "invalid review_status"
    if score["review_status"] == "contradicted":
        return "contradicted score excluded"
    rating = score.get("rating")
    if rating is None:
        return "not assessed or not applicable"
    if type(rating) is not int or rating not in (1, 2, 3, 4):
        return "rating must be 1–4 or null"
    evidence = score.get("evidence")
    if not isinstance(evidence, list) or not evidence:
        return "rated entry has no evidence"
    for item in evidence:
        if not isinstance(item, dict):
            return "invalid evidence item"
        start, end = item.get("start_seconds"), item.get("end_seconds")
        if not number(start) or not number(end) or start < 0 or end <= start:
            return "invalid evidence times"
        if item.get("modality") not in MODALITIES or not text_value(item.get("note")):
            return "invalid evidence modality or note"
    return None


def summarize(session_root):
    groups, excluded, records = {}, [], []
    for path in sorted(session_root.glob("*/scores.json")):
        try:
            record = load_record(path)
            records.append((record, path))
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            excluded.append({"file": str(path), "reason": str(exc)})
    seen_media, seen_sessions = set(), set()
    for record, path in sorted(records, key=lambda pair: (pair[0]["date"], str(pair[1]))):
        sid, digest = record["session_id"], record["media_sha256"].lower()
        if sid in seen_sessions or digest in seen_media:
            excluded.append({"file": str(path), "reason": "duplicate session ID or media hash"})
            continue
        seen_sessions.add(sid)
        seen_media.add(digest)
        context = record["context"]
        seen_criteria = set()
        for score in record["scores"]:
            reason = validate_score(score)
            label = score.get("criterion", "unknown") if isinstance(score, dict) else "unknown"
            if not reason:
                identity = (score["rubric"], score["criterion"])
                if identity in seen_criteria:
                    reason = "duplicate rubric/criterion in session"
                else:
                    seen_criteria.add(identity)
            if reason:
                excluded.append({"file": str(path), "criterion": label, "reason": reason})
                continue
            key = tuple(context[field] for field in CONTEXT_FIELDS) + (score["rubric"], score["criterion"])
            group = groups.setdefault(key, {"context": {field: context[field] for field in CONTEXT_FIELDS}, "rubric": score["rubric"], "criterion": score["criterion"], "observations": []})
            group["observations"].append({"session_id": sid, "date": record["date"], "rating": score["rating"], "assessor": score["assessor"], "review_status": score["review_status"], "record_path": str(path)})
    output = sorted(groups.values(), key=lambda group: (group["rubric"], group["criterion"], json.dumps(group["context"], sort_keys=True)))
    for group in output:
        group["n"] = len(group["observations"])
    return {"groups": output, "excluded": excluded, "limitations": "Custom ordinal ratings; grouping does not validate evidence, reviewer independence, comparable difficulty, or improvement."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sessions-dir", type=Path, default=ROOT / "private" / "sessions", help="Session directory (default: project private/sessions)")
    args = parser.parse_args()
    if not args.sessions_dir.exists():
        print(json.dumps({"groups": [], "excluded": [], "message": "No session directory or scored sessions yet."}, indent=2))
        return 0
    if not args.sessions_dir.is_dir():
        print("Session path is not a directory", file=sys.stderr)
        return 2
    print(json.dumps(summarize(args.sessions_dir), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
