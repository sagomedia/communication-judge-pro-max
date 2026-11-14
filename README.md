# Communicator Judge Pro Max (v2)

A personal, file-based communication judge built around **8 summarized books across 4 pillars**, a **Communication Coach Verifier**, **persistent speaker memory + Anki recall**, and a **3-page editorial PDF report**.

## Prerequisites (Fail-Closed Capability Gate)
This workflow **requires** an AI agent whose model has **native audio/voice + native video understanding** running in a harness whose media tool can read `.mp4` video+audio directly (plus `ffmpeg`, `ffprobe`, and `google-chrome` / Chromium on the host).

- **Step 0 (`scripts/preflight_check.py`) runs before everything:** Any text-only model, image-only model, ASR-only workaround, or harness that rejects `.mp4` media will **stop immediately with `UNSUPPORTED_ENVIRONMENT`** instead of hallucinating wrong scores or fake timestamps.
- Quick host + video check:
  ```bash
  python3 scripts/preflight_check.py "../input assets/video files/<video>.mp4" --probe-clip /tmp/cj_probe.mp4
  ```
  (Or `python3 scripts/preflight_check.py --tools-only` to check host dependencies without a video.)

## Quick Start
Use the project skill **judge-communication** (`.agents/skills/judge-communication/SKILL.md`) and provide a speaking video path (from `../input assets/video files/` or anywhere local).

Each complete evaluation produces under `private/sessions/<session_id>/`:
- `report.md` — detailed timestamped pillar audit, Pros/Cons, Overall Review, Next Focus, and Memory Check
- `report.pdf` — 3-page editorial report (Page 1: Skyline & 4-pillar scores, Page 2: Pros/Cons & Memory Check, Page 3: Visual Daily Micro-Lesson & Anki Recall Cards)
- `session.json` — structured record (including `capability_attestation`) appended to `private/memory/speaker-memory.json` via `scripts/memory_store.py`
