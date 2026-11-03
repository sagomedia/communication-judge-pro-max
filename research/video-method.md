# Mapping the inspiration video's method

[Video](https://youtu.be/QRFyNJnrHxM). This mapping is based on the available automatic transcript and sampled frames, not continuous visual viewing. The video builds a résumé-screening harness; the communication workflow is our adaptation.

| Approximate timestamp | The video's mechanism | This project | Status |
|---|---|---|---|
| 03:00–04:52 | `context/` includes role, anchored rubric, ideal example and project instructions | `context/`, `examples/evidence.md`, `AGENTS.md` | Files provided; no claim of a trained or validated model |
| 06:28–07:39 | Connect source and limit tool access | `private/inbox/`, permission rules | Local folders and instructions only; no enforced scoped agent tools, watcher or cloud integration |
| 08:41–10:03 | Report template plus repeatable screening skill | `templates/report.md`, `workflows/evaluate-session.md` | Manual workflow; not an installed skill or slash command |
| 10:50–12:13 | Separate read-only verifier before reporting; can confirm | `verifiers/evidence-reviewer.md` | Reviewer prompt only; separate agent, access controls and automatic invocation not implemented |
| 13:04–13:34 | Processing memory prevents duplicate work | `memory/process-template.md` and a local copy | Manual log; hashing and automatic duplicate detection not implemented |
| 13:38–15:00 | User-invoked calibration, approval before rules change | `workflows/calibrate.md`, `memory/approved-calibration.md` | Manual procedure; versioning and enforcement not automated |
| 16:27–17:17 | Schedule automatic runs | Future integration | No schedule configured; do not claim it runs automatically |

This layout adapts the method to personal video, self-reports, and listener evidence; the video does not validate our psychology measurements or scoring reliability.
