# Speaker Memory Rules (v2)

> **Purpose:** Builds a lightweight, persistent memory across speaking runs so the Communication Coach Verifier can recognize consistency, ask sharp questions when habits or quality shift inconsistently, give grounded compliments, and offer targeted advice.

---

## 1. Storage & Privacy
- **Tracked specification:** `memory/memory-rules.md` (this file) and `scripts/memory_store.py`.
- **Local private memory (gitignored under `/private/`):**
  - `private/memory/speaker-memory.json` — structured history of all runs (newest appended, never overwriting earlier entries).
  - `private/memory/speaker-memory.md` — human-readable summary automatically regenerated from `speaker-memory.json`.

---

## 2. What Each Session Saves
After a run passes the Communication Coach Verification Gate, record:
- `session_id`, `date`, `video_file`, `media_sha256`, `duration_seconds`, `take_status` (`Complete` or `Incomplete Take`)
- `scores`: `{ english_fluency, communication, body_language, tonality }` (`0–100`) and `tiers`
- `active_focus_checked`: `{ previous_focus, result: "passed" | "partial" | "missed" | "none", note }`
- `next_focus`: `{ focus, pass_condition }` (the ONE focus chosen for the *next* run)
- `pros_tags`: short canonical labels of strengths observed (e.g., `concrete_examples`, `steady_projection`, `counting_gestures`, `active_subjects`)
- `cons_tags`: short canonical labels of issues observed (e.g., `late_main_point`, `face_hair_touches`, `hidden_hands_10s`, `verb_agreement_slips`, `on_camera_stretch_yawn`)
- `grammar_slips`: exact broken phrases flagged in English Fluency Section 2B (e.g., `"I builded"`, `"a store have"`)
- `card_reviews`: list of `{ "id": "<card_id>", "result": "passed" | "again" }` evaluating due Anki cards against the new video
- `new_cards`: new 1–2 line grammar or topic-vocabulary recall cards created from this session's mistakes/placeholders (`{ id, kind, cue, answer, rule_short, visual_pair }`)

## 2B. Anki-Style Spaced Recall & Daily Micro-Lessons
- Every mistake or vague placeholder in a video generates a compact recall card stored in `anki_deck[]` inside `private/memory/speaker-memory.json`.
- Cards follow a **4-box Leitner schedule** across sessions:
  - **Box 1:** due next session (`+1` session)
  - **Box 2:** due in `+2` sessions
  - **Box 3:** due in `+4` sessions
  - **Box 4:** mastered (`+8` sessions)
- If the speaker uses the right form or avoids the mistake in a later video (`result: "passed"`), the card advances one box. If the mistake repeats (`result: "again"`), the card resets to **Box 1** so it immediately resurfaces in the next PDF's **Daily Lesson & Anki Recall Deck** page.

---

## 3. How the Coach Uses Memory During Each Run
Before writing **Part 2, Section 5 (Complimenting Things, Memory Check & Coach Advice)**:

1. **Duplicate Guard:** Compute the video's SHA-256 (`python3 scripts/memory_store.py hash <video>`). If that exact file hash was already recorded, warn the user before re-running and do **not** treat a re-evaluation of the same video as new progress.
2. **Pull Memory Brief (`python3 scripts/memory_store.py brief`):**
   - Check the **previous `next_focus` & `pass_condition`**. State plainly whether it was `passed`, `partial`, or `missed` in this new video.
   - Check **Consistency (`"He is so consistent"`)**: Highlight any `pros_tags` appearing in `2+` sessions, consecutive `Complete (≥ 120s)` takes, or steady/improving pillar scores. Turn this into a **specific compliment**.
   - Check **Inconsistency / Recurring Habit (`"Asking a question if inconsistent"`)**:
     - If a pillar score dropped sharply compared to the previous session, OR a previously flagged `cons_tag` / `grammar_slip` returned again (`2+` sessions), **ask 1 direct, supportive coaching question** referencing both sessions (e.g., *"You pushed all the way through a 3m 38s pitch this time after quitting at 00:37 earlier — what made the face/hair touches and end-of-take yawn still slip back in at 03:04–03:48?"*).
   - **Give Practical Advice:** 1–2 concrete, encouraging sentences connecting memory patterns to the speaker's next recording.
