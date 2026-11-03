# Private session scores: machine-readable format v1

This is an interchange format for the project skills and `scripts/progress.py`. Store one UTF-8 JSON file named `scores.json` in each unique `private/sessions/<session-id>/` directory, together with the separately written report, manifest and review. Do not create records without an actual analysis. Keep personal data out of Git and do not upload it without authorization. Never overwrite a prior session; corrections use a new session folder and state what was superseded.

```json
{
  "schema_version": 1,
  "session_id": "2026-11-03-example",
  "date": "2026-11-03",
  "media_sha256": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
  "context": {
    "speaker": "user",
    "language": "en",
    "prompt_family": "explain-project-v1",
    "audience": "colleague",
    "format": "solo-camera",
    "preparation_seconds": 60,
    "take_type": "first",
    "conditions": "same-microphone-and-room"
  },
  "scores": [
    {
      "rubric": "general-v1",
      "criterion": "structure_and_transitions",
      "rating": 2,
      "assessor": "local evaluator",
      "review_status": "not_independently_reviewed",
      "evidence": [{"start_seconds": 12, "end_seconds": 25, "modality": "reviewed_transcript", "note": "Example observation; replace with real evidence."}]
    }
  ]
}
```

The example is fictional; the all-`a` hash and rating do not describe a real recording. Names are case-sensitive. `context` values describe actual conditions, not assumptions. Unknown values must be JSON `null`; the progress tool excludes records with unknown comparison fields rather than guessing. `preparation_seconds` is a nonnegative integer. Use `take_type` `first`, `rehearsal`, or `unknown`. Use stable criterion IDs consistently; examples include `main_point_and_purpose`, `structure_and_transitions`, and personal `narrative_movement`. Scope each ID to `general-v1` or `personal-v1`; don't rename rubric IDs without versioning.

Each score entry has `rubric`, `criterion`, `rating` (integer 1–4 or JSON null), `assessor`, `review_status` (`supported`, `contradicted`, `uncertain`, or `not_independently_reviewed`), and `evidence` (a list). A rated entry needs at least one evidence object containing actual start/end seconds, a modality (`audio`, `video`, `raw_asr`, or `reviewed_transcript`), and a nonempty description. A null rating should have a `reason` explaining `not_assessed` or `not_applicable`; its evidence can be empty. Do not publish contradicted scores; revise or store null pending review. The schema cannot prove the cited evidence is valid. Record real transcript revision and audio review state in the report; an exact transcript match never proves the audio.

`python3 scripts/progress.py` reads these records and prints grouped JSON to standard output. It excludes malformed files, non-first takes, incomplete comparison metadata, duplicate media and unusable scores, with reasons. Grouping uses speaker, language, prompt family, audience, format, preparation time and conditions, plus rubric version and criterion. A missing field is not a match. Treat scores with different reviewer status or other material conditions cautiously; inspect source reports. Topic difficulty can differ despite matching fields. It does not verify media, rubric validity, listener comprehension, audio, reviewer independence, calibration, or causal progress. Never mix or average confidence self-reports with skill scores.
