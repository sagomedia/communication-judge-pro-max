---
name: improve-communication
description: Create a personal speaking practice plan, repeatable drills, topic vocabulary, or an evidence-based progress review from this project's private communication sessions. Use when the user asks to improve, practice, test, or track their speaking.
---

# Improve communication

Work in this project. Read `AGENTS.md`, `README.md`, `context/profile.md`, `context/rubric-v1.md`, `context/personal-style/goal-v1.md`, `context/personal-style/rubric-v1.md`, `measurement/progress-v1.md`, `measurement/session-record-v1.md`, and `memory/approved-calibration.md`. Review actual private reports, speaker feedback and scores only if they exist; do not treat example records as the user's results. Keep all personal media and notes local unless explicitly authorized for an external service.

1. Identify the user's current goal and review only relevant session records. Run `python3 scripts/progress.py` when score records exist. Report raw per-criterion values, dates, sample sizes, version, reviewer statuses, missing evidence and comparability limitations; don't turn ordinal ratings into percentages or invent improvement. The script only groups comparable recorded metadata; it cannot establish score validity or guarantee equal difficulty. If there are no usable records, say so and propose a short baseline practice rather than a diagnosis.
2. Select one or at most two practice priorities using the user's goal, recurring evidence, listener feedback when available, and importance to meaning. Cite actual session IDs and timestamps for claimed patterns. Do not infer confidence, anxiety or personality from voice or appearance; preserve self-reported values as a separate metric.
3. Create a concrete exercise: context and audience, one instruction, a realistic first-take prompt, time/repetitions, what observable success looks like, and how to check it. Preserve first takes separately from rehearsals. Offer a fresh follow-up prompt and a simple next review date or cadence; do not set reminders or schedules unless explicitly requested and configured.
4. Suggest 3–5 useful words or phrases only when topic/audience is known. Give plain meaning, context-appropriate example and why useful; present them as options, not evidence of mistakes. Ask for a recording only if needed for further evaluation. Never manufacture listener feedback, performance or scores.
5. Save any requested plan or progress review as a new uniquely named file in `private/reviews/` and link it. Do not overwrite earlier results or silently change rubrics or scoring history. Use `workflows/calibrate.md` only when the user explicitly requests calibration, and obtain their explicit approval before changing scoring rules.
