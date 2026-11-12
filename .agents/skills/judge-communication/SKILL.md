---
name: judge-communication
description: Evaluate a speaking video across 4 book-grounded pillars (English Fluency, Communication, Body Language, Tonality), verify with the Communication Coach Verifier, check persistent speaker memory & Anki recall cards, and render a 3-page editorial PDF report.
---

# Judge Communication (v2 Pipeline)

Work inside `communicator-judge-pro-max/`. Read `AGENTS.md`, `verifiers/_contract.md`, `verifiers/communication-coach.md`, and `memory/memory-rules.md` before evaluating.

## Step 1 — Pre-Flight & Memory Brief
1. Locate the target video path and verify it exists (never move or modify the original file).
2. Run:
   ```bash
   python3 scripts/memory_store.py brief --video "<video_path>"
   ```
   - Capture the video's `media_sha256` (from `python3 scripts/memory_store.py hash "<video_path>"` if needed) and inspect `duplicate_of_session`. If the hash matches an existing session, warn the user before proceeding and do not count a duplicate run as new progress.
   - Note `previous_active_focus`, `previous_scores`, `recurring_strengths_2plus`, `recurring_patterns_2plus`, and `anki_summary.due_cards`.

## Step 2 — Direct Multimodal Inspection (`< 100 MB` Proxy Rule)
1. Inspect the video's actual **video + audio** directly.
2. If the file exceeds `100 MB`, encode a temporary `720p` compressed proxy (`< 100 MB`, preserving timestamps and audio) in a scratch/temp path, inspect it directly, and **delete the temporary proxy immediately after inspection**. Only split or reduce sampling if a very long recording cannot fit under `100 MB`.
3. Record exact `MM:SS–MM:SS` timeline notes, spoken quotes/slips, vocal patterns, and sustained visual behaviors.

## Step 3 — Run the 4 Book Verifiers
Follow `verifiers/_contract.md` and audit each pillar independently:
1. `verifiers/english-fluency.md` — Checklist (`01–20`) + Section 2B Overall Spoken Grammar Test (`min(round(0.40 * Checklist + 0.60 * Spoken_Grammar), Spoken_Grammar + 10)`). Keep everyday casual speech (`"gonna"`, contractions) safe.
2. `verifiers/communication.md` — Check applicable Minto + Heath rules (`01–20`; mark slide rules `N/A` if no slides).
3. `verifiers/body-language.md` — Check applicable Navarro + Van Edwards rules (`01–20`; mark out-of-frame lower-body rules `N/A`).
4. `verifiers/tonality.md` — Deduct **only from Table 2A (`RULE-01`–`RULE-15`)** using `Tables 2B/2C` for targeted drills; mark hidden anatomy (`RULE-02`, `RULE-03`, `RULE-07`), singing (`RULE-04`), conversation (`RULE-09`, `RULE-12`), slides (`RULE-13`), or stage/mic (`RULE-15`) `N/A` when inapplicable.

Apply the **2-Minute Completeness Gate** (`≥ 120s` target speech without mid-take abort) and proportional `N/A` scoring:
`Score = round(100 * (1 - Triggered / Applicable_Max))`.

## Step 4 — Communication Coach Verification & Memory Synthesis
Run `verifiers/communication-coach.md`:
1. **Part 1 Verification Gate:** Audit all 4 pillar outputs for timestamp evidence, observable-only compliance, natural speech fairness, 2-minute gate, and proportional math.
2. **Part 2 Coaching Synthesis:** Produce:
   - 4-Pillar Scoreboard & Rank (`1st → 4th`)
   - Pillar-by-Pillar `Pros` & `Cons`
   - `Overall Review`
   - Strictly **ONE** `Next Focus` + 2-minute drill + observable `pass_condition`
   - `Complimenting Things`, `Memory Check` (previous focus `passed/partial/missed`, consistent wins, inconsistency question if applicable), and `Coach Advice`
3. **Anki Recall & Daily Lesson:**
   - Review every card in `anki_summary.due_cards` against the new video (`"passed"` if avoided/used well; `"again"` if the mistake repeated).
   - Pick up to 2–3 concise `new_cards` (grammar fixes or topic vocabulary upgrades grounded in this recording) and build today's visual grammar/structure micro-lesson for Page 3.

## Step 5 — Save Session, Update Memory, & Render 3-Page PDF
1. Choose a unique `private/sessions/<YYYY-MM-DD-session-NNN>/` folder (never overwrite existing sessions).
2. Save:
   - `report.md` (full Markdown audit + coaching report)
   - `session.json` (valid memory payload) and record it:
     ```bash
     python3 scripts/memory_store.py record private/sessions/<id>/session.json
     ```
   - `cert-payload.json` (matching `templates/report-certificate.html` schema) and render the 3-page PDF:
     ```bash
     python3 scripts/render_pdf.py private/sessions/<id>/cert-payload.json private/sessions/<id>/report.pdf
     ```
3. Visually inspect `private/sessions/<id>/report.pdf` to confirm clean layout and zero text overlap, then link `report.pdf`, `report.md`, and `private/memory/speaker-memory.md` in your final reply.
