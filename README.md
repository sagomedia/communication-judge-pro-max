# Communicator Judge Pro Max (v2)

A personal, file-based communication judge built around **8 summarized books across 4 pillars**, a **Communication Coach Verifier**, **persistent speaker memory + Anki recall**, and a **3-page editorial PDF report**.

## Quick Start
Use the project skill **judge-communication** (`.agents/skills/judge-communication/SKILL.md`) and provide a speaking video path (from `../input assets/video files/` or anywhere local).

Each complete evaluation produces under `private/sessions/<session_id>/`:
- `report.md` — detailed timestamped pillar audit, Pros/Cons, Overall Review, Next Focus, and Memory Check
- `report.pdf` — 3-page editorial report (Page 1: Skyline & 4-pillar scores, Page 2: Pros/Cons & Memory Check, Page 3: Visual Daily Micro-Lesson & Anki Recall Cards)
- `session.json` — structured record appended to `private/memory/speaker-memory.json` via `scripts/memory_store.py`
# communication-judge-pro-max
