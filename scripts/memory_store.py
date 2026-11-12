#!/usr/bin/env python3
"""Manage persistent speaker memory and Anki-style recall cards for Communicator Judge v2."""

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_JSON = ROOT / "private" / "memory" / "speaker-memory.json"
DEFAULT_MD = ROOT / "private" / "memory" / "speaker-memory.md"
PILLARS = ("english_fluency", "communication", "body_language", "tonality")
BOX_INTERVALS = {1: 1, 2: 2, 3: 4, 4: 8}


def sha256_file(path: Path) -> str:
    """Compute hex SHA-256 digest of a file in chunks."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def empty_store() -> dict:
    """Return a fresh speaker-memory structure."""
    return {
        "schema_version": 2,
        "speaker": "Gokulakrishnan",
        "sessions": [],
        "active_focus": None,
        "recurring_strengths": {},
        "recurring_patterns": {},
        "anki_deck": [],
    }


def load_store(path: Path) -> dict:
    """Load existing memory JSON or return a fresh store if missing."""
    if not path.exists():
        return empty_store()
    with path.open(encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict) or "sessions" not in data:
        raise ValueError(f"Invalid memory file structure: {path}")
    data.setdefault("anki_deck", [])
    return data


def recompute_aggregates(store: dict) -> None:
    """Rebuild recurring strengths, patterns, and active focus from session history."""
    strengths = Counter()
    patterns = Counter()
    for session in store["sessions"]:
        for tag in dict.fromkeys(session.get("pros_tags", [])):
            strengths[tag] += 1
        for tag in dict.fromkeys(session.get("cons_tags", [])):
            patterns[tag] += 1
    store["recurring_strengths"] = dict(sorted(strengths.items(), key=lambda item: (-item[1], item[0])))
    store["recurring_patterns"] = dict(sorted(patterns.items(), key=lambda item: (-item[1], item[0])))
    store["active_focus"] = store["sessions"][-1].get("next_focus") if store["sessions"] else None


def update_anki_deck(store: dict, payload: dict, session_index: int) -> None:
    """Apply spaced-repetition reviews and register new recall cards."""
    deck_by_id = {card["id"]: card for card in store.setdefault("anki_deck", []) if "id" in card}

    for review in payload.get("card_reviews", []):
        cid = review.get("id")
        result = review.get("result")
        card = deck_by_id.get(cid)
        if not card or result not in ("passed", "again"):
            continue
        if result == "passed":
            card["box"] = min(card.get("box", 1) + 1, 4)
            card["streak"] = card.get("streak", 0) + 1
        else:
            card["box"] = 1
            card["streak"] = 0
            card["lapses"] = card.get("lapses", 0) + 1
        card["last_result"] = result
        card["last_reviewed_session"] = payload["session_id"]
        card["due_session_index"] = session_index + BOX_INTERVALS[card["box"]]

    for raw_card in payload.get("new_cards", []):
        cid = raw_card.get("id")
        if not cid:
            continue
        if cid in deck_by_id:
            existing = deck_by_id[cid]
            existing["box"] = 1
            existing["streak"] = 0
            existing["lapses"] = existing.get("lapses", 0) + 1
            existing["last_result"] = "again"
            existing["due_session_index"] = session_index + 1
            continue
        new_card = {
            "id": cid,
            "kind": raw_card.get("kind", "grammar"),
            "cue": raw_card["cue"],
            "answer": raw_card["answer"],
            "rule_short": raw_card["rule_short"],
            "visual_pair": raw_card.get("visual_pair"),
            "box": 1,
            "streak": 0,
            "lapses": 0,
            "last_result": "new",
            "created_session": payload["session_id"],
            "due_session_index": session_index + 1,
        }
        store["anki_deck"].append(new_card)
        deck_by_id[cid] = new_card


def select_due_cards(store: dict, max_cards: int = 5) -> list[dict]:
    """Return due Anki recall cards ordered by lowest box / highest lapses."""
    next_index = len(store.get("sessions", []))
    due = [
        card for card in store.get("anki_deck", [])
        if card.get("due_session_index", 0) <= next_index
    ]
    due.sort(key=lambda c: (c.get("box", 1), -c.get("lapses", 0), c.get("kind", "grammar"), c["id"]))
    return due[:max_cards]


def render_markdown(store: dict) -> str:
    """Render a concise human-readable memory summary from the JSON store."""
    sessions = store.get("sessions", [])
    lines = [
        "# Speaker Memory",
        "",
        f"- **Speaker:** {store.get('speaker', 'Unknown')}",
        f"- **Recorded sessions:** {len(sessions)}",
    ]
    active = store.get("active_focus")
    if active:
        lines.append(f"- **Current Active Focus:** {active.get('focus', '')}")
        lines.append(f"- **Next Pass Condition:** {active.get('pass_condition', '')}")
    else:
        lines.append("- **Current Active Focus:** None yet")

    recurring_pros = {k: v for k, v in store.get("recurring_strengths", {}).items() if v >= 2}
    recurring_cons = {k: v for k, v in store.get("recurring_patterns", {}).items() if v >= 2}

    lines.extend(["", "## Recurring Strengths (2+ sessions)"])
    lines.extend(f"- `{tag}` ({count}x)" for tag, count in recurring_pros.items()) if recurring_pros else lines.append("- None confirmed across 2+ sessions yet.")

    lines.extend(["", "## Recurring Habits / Cons (2+ sessions)"])
    lines.extend(f"- `{tag}` ({count}x)" for tag, count in recurring_cons.items()) if recurring_cons else lines.append("- None confirmed across 2+ sessions yet.")

    due = select_due_cards(store, max_cards=8)
    lines.extend(["", f"## Active Anki Recall Deck ({len(store.get('anki_deck', []))} cards, {len(due)} due next)"])
    if due:
        for card in due:
            lines.append(f"- **[Box {card.get('box', 1)} · {card.get('kind', 'grammar')}]** `{card['id']}` — {card['cue']} → **{card['answer']}** (*{card['rule_short']}*)")
    else:
        lines.append("- No cards due right now.")

    lines.extend([
        "",
        "## Session Timeline",
        "",
        "| Session ID | Date | Status | Fluency | Comm | Body | Tonality | Focus Result |",
        "|---|---|---|---:|---:|---:|---:|---|",
    ])
    for s in sessions:
        scores = s.get("scores", {})
        focus_check = (s.get("active_focus_checked") or {}).get("result", "none")
        lines.append(
            f"| `{s.get('session_id', '')}` | {s.get('date', '')} | {s.get('take_status', '')} | "
            f"{scores.get('english_fluency', '-')} | {scores.get('communication', '-')} | "
            f"{scores.get('body_language', '-')} | {scores.get('tonality', '-')} | {focus_check} |"
        )
    lines.append("")
    return "\n".join(lines)


def build_brief(store: dict, video_hash: str | None = None) -> dict:
    """Create a compact memory brief for the Communication Coach Verifier."""
    sessions = store.get("sessions", [])
    duplicate_of = None
    if video_hash:
        for s in sessions:
            if s.get("media_sha256", "").lower() == video_hash.lower():
                duplicate_of = s.get("session_id")
                break

    last_session = sessions[-1] if sessions else None
    complete_streak = 0
    for s in reversed(sessions):
        if s.get("take_status") == "Complete":
            complete_streak += 1
        else:
            break

    deck = store.get("anki_deck", [])
    return {
        "session_count": len(sessions),
        "duplicate_of_session": duplicate_of,
        "complete_take_streak": complete_streak,
        "previous_active_focus": store.get("active_focus"),
        "previous_scores": last_session.get("scores") if last_session else None,
        "previous_session_id": last_session.get("session_id") if last_session else None,
        "recurring_strengths_2plus": {k: v for k, v in store.get("recurring_strengths", {}).items() if v >= 2},
        "recurring_patterns_2plus": {k: v for k, v in store.get("recurring_patterns", {}).items() if v >= 2},
        "anki_summary": {
            "total_cards": len(deck),
            "mastered_box4": sum(1 for c in deck if c.get("box") == 4),
            "due_cards": select_due_cards(store, max_cards=5),
        },
    }


def validate_session_payload(payload: dict) -> None:
    """Validate required fields before appending a session record."""
    for field in ("session_id", "date", "video_file", "media_sha256", "take_status", "scores", "next_focus"):
        if field not in payload:
            raise ValueError(f"Missing required field: {field}")
    scores = payload["scores"]
    for pillar in PILLARS:
        val = scores.get(pillar)
        if not isinstance(val, int) or not (0 <= val <= 100):
            raise ValueError(f"Invalid score for {pillar}: {val}")


def save_store(store: dict, json_path: Path, md_path: Path) -> None:
    """Write JSON store and regenerated Markdown summary."""
    json_path.parent.mkdir(parents=True, exist_ok=True)
    with json_path.open("w", encoding="utf-8") as handle:
        json.dump(store, handle, indent=2, ensure_ascii=False)
        handle.write("\n")
    with md_path.open("w", encoding="utf-8") as handle:
        handle.write(render_markdown(store))


def cmd_hash(args: argparse.Namespace) -> int:
    print(json.dumps({"video": str(args.video), "media_sha256": sha256_file(args.video)}, indent=2))
    return 0


def cmd_brief(args: argparse.Namespace) -> int:
    store = load_store(args.memory_json)
    video_hash = sha256_file(args.video) if args.video else None
    print(json.dumps(build_brief(store, video_hash), indent=2, ensure_ascii=False))
    return 0


def cmd_record(args: argparse.Namespace) -> int:
    with args.session_json.open(encoding="utf-8") as handle:
        payload = json.load(handle)
    validate_session_payload(payload)
    store = load_store(args.memory_json)

    if args.speaker:
        store["speaker"] = args.speaker
    sid = payload["session_id"]
    digest = payload["media_sha256"].lower()
    for existing in store["sessions"]:
        if existing.get("session_id") == sid:
            raise ValueError(f"Duplicate session_id: {sid}")
        if existing.get("media_sha256", "").lower() == digest and not args.allow_duplicate_hash:
            raise ValueError(f"Duplicate media_sha256 already recorded in {existing.get('session_id')}")

    session_index = len(store["sessions"])
    store["sessions"].append(payload)
    update_anki_deck(store, payload, session_index)
    recompute_aggregates(store)
    save_store(store, args.memory_json, args.memory_md)
    print(json.dumps({"recorded": sid, "total_sessions": len(store["sessions"]), "anki_cards": len(store["anki_deck"])}, indent=2))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--memory-json", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--memory-md", type=Path, default=DEFAULT_MD)
    sub = parser.add_subparsers(dest="command", required=True)

    p_hash = sub.add_parser("hash", help="Print SHA-256 hash of a video file.")
    p_hash.add_argument("video", type=Path)
    p_hash.set_defaults(func=cmd_hash)

    p_brief = sub.add_parser("brief", help="Print memory brief for the coach verifier.")
    p_brief.add_argument("--video", type=Path, default=None, help="Optional video path to check for duplicate hash.")
    p_brief.set_defaults(func=cmd_brief)

    p_rec = sub.add_parser("record", help="Append a verified session JSON into speaker memory.")
    p_rec.add_argument("session_json", type=Path)
    p_rec.add_argument("--speaker", type=str, default=None)
    p_rec.add_argument("--allow-duplicate-hash", action="store_true")
    p_rec.set_defaults(func=cmd_record)

    args = parser.parse_args()
    try:
        return args.func(args)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
