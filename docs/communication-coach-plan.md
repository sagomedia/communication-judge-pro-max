# Communicator Judge Pro Max: research and first implementation plan

Status: proposal for discussion, not a working automation. The user's priority is presentations and general speaking confidence.

## Outcome

Turn a short recording into evidence-backed coaching: what worked, what made the message harder to follow, and one exercise to try next. Track performance over time on comparable tasks. The first version focuses on one speaker, spoken English, and recordings the user chooses to analyze.

## The inspiration video and its six layers

The [inspiration video](https://youtu.be/QRFyNJnrHxM), “Stop Upgrading Your AI Model (Build A Harness Instead),” demonstrates six harness layers using a résumé-screening example. This revision draws on a locally generated, uncorrected transcript of the video's audio and sampled video frames; transcript errors are possible, and the frames are not a continuous visual review.

| Video layer | Application to this coach |
| --- | --- |
| Context | Personal goals, presentation audience, prompt, rubric and prior practice. |
| Tool access | Explicitly authorized local file access, media extraction and transcription; optional model access with a clear privacy choice. |
| Output | A consistent session report and structured, timestamped findings. |
| Verification | Mechanical evidence checks, a separate claim review, user corrections and occasional human listening. |
| Memory | Preserve reviewed sessions, user preferences, goal history and rubric versions in files. |
| Automation | Trigger a repeatable processing pipeline on request; consider folder watching after the manual flow works. |

These layers help structure the system, but they do not themselves validate the accuracy of its assessments. The checks below and comparison with human judgment remain necessary.

### Specific mechanisms to adapt from the demonstration

- **Context (about 02:13):** put the user's goal, rubric and worked examples in separate files, plus a project instruction file that points the workflow to them. Define score anchors and require evidence for every finding; examples demonstrate reasoning and must not be copied into a report.
- **Tool access (about 05:56):** scope access to the recording and session files needed for the task. Never move or delete an original, and use an explicit privacy choice for any cloud service.
- **Output (about 07:55):** create one report template and one repeatable analysis procedure. The video packages its procedure as a Claude skill; our implementation can use an equivalent command or workflow in the chosen environment.
- **Verification (about 10:15):** send the source evidence, rubric and draft findings to a fresh, read-only checker before finalizing. The checker may confirm a finding, flag a problem, or say there is insufficient evidence. It must be allowed to confirm, rather than invent issues. Check timestamps and quotes mechanically as well. A separate AI pass can still share the same biases or make errors; it is not proof of independence or correctness.
- **Memory and calibration (about 12:33):** keep a processed-session log to avoid accidental duplicates. Keep the user's corrections separately. On an explicit calibration request, propose a general rubric change and show its effects on past examples; apply the change only if the user approves it. Version the rubric, preserve original reports, and label any reanalysis as a new result.
- **Automation (about 15:57):** the demonstration schedules its local workflow. For this coach, first make the user-triggered process reliable; later add an optional schedule or folder watcher with clear failure messages and no duplicate processing.

A transcript is evidence about words, not a complete record of delivery. Video of a solo speaker cannot establish listening, conversation skills, confidence, or intent. Mark a criterion **not assessed** when its required evidence is absent.

## What to borrow from established assessments

- [EF SET's four-skill test](https://www.efset.org/4-skill/) takes 90 minutes and reports speaking, writing, reading and listening. The [two-skill test](https://www.efset.org/english-certificate/) covers reading and listening only. EF describes automated scoring and an adaptive design; its [FAQ](https://www.efset.org/faq/) says certifying exams are limited to one session per 90 days. Record an official speaking result as an external reference if the user takes the four-skill test.
- The sources reviewed do not specify enough detail to reproduce EF SET's speaking model, calibration, or scoring formula. Our coaching scores are independent; they are not EF SET scores or certificates. No numerical conversion is justified.
- The Council of Europe's [CEFR companion volume](https://rm.coe.int/cefr-companion-volume-with-new-descriptors-2020/16809ea0d4) offers can-do descriptors. Use these for qualitative comparisons only, with uncertainty; a single short recording cannot establish a certified level.
- The Council's [spoken-language reference table](https://www.coe.int/en/web/common-european-framework-reference-languages/table-3-cefr-3.3-common-reference-levels-qualitative-aspects-of-spoken-language-use) separates range, accuracy, fluency, interaction and coherence. Its companion volume also includes addressing an audience, which is relevant to the user's presentation goal. Treat these as reference descriptors rather than automatic level assignments.
- [IELTS speaking descriptors](https://ielts.org/cdn/ielts-guides/ielts-speaking-band-descriptors.pdf) give four useful categories: fluency and coherence, vocabulary, grammar, and pronunciation. Adapt their ideas to coaching, without claiming an IELTS band. The Council of Europe emphasizes [intelligibility over accent imitation](https://www.coe.int/en/web/common-european-framework-reference-languages/phonological-competence).

## Proposed rubric: one score per dimension

Use a personal 1–4 scale only on sufficient evidence. A general anchor: **1** = frequent barriers to the task; **2** = message partly succeeds with recurring barriers; **3** = generally effective with some lapses; **4** = consistently effective for this task. Each score must have criterion-specific observations, timestamps, and a reason. Intermediate scores and averages are unnecessary initially. Review anchors after trial recordings with a human listener.

| Dimension | Evidence and verifier | What to look for |
| --- | --- | --- |
| Message and structure | Transcript plus prompt; evaluator checks against the stated goal. | Main point, relevant support or example, and a clear ending or requested action when the task calls for it. |
| Fluency and coherence | Audio and time-aligned transcript; counts are supporting context. | Whether pauses, repetitions, and transitions disrupt understanding. Do not penalize all pauses or reward speed alone. |
| Vocabulary | Verified transcript and prompt. | Whether word choice communicates the intended meaning and whether the speaker can explain an idea another way. Recommend useful phrases drawn from the speaker's topic. |
| Grammar | Verified transcript and audio where ambiguous. | Recurring patterns and their effect on meaning. Preserve natural spoken language; do not label every informal expression an error. |
| Intelligibility | Audio and ideally an independent listener. | A short span the listener could not understand and whether stress or articulation could be practiced. No native-accent target. |
| Interaction | Audio/video with both sides and consent, when available. | Responding to the other person's question, allowing turns, and clarifying misunderstandings. Otherwise not assessed. |

Camera presentation is a separate, optional observation, initially unscored: e.g., face visible or off-frame, gestures visible at a timestamp, and camera framing. An image cannot prove confidence, attention, honesty, personality, or emotion. A [review of facial expression research](https://journals.sagepub.com/doi/abs/10.1177/1529100619832930) explains why inferring emotion from facial movements is unreliable across contexts and people. Eye contact and gesture norms vary by individual, culture, disability, and task; don't prescribe constant eye contact or movement. Audio-only inputs skip this section.

### Evidence contract

For each finding store: criterion, strength or opportunity, time range, exact quote or audible/visible observation, explanation and effect, suggested alternative or exercise, confidence, and evidence source. A second verifier checks that timestamps exist, quotes match the reviewed transcript, claims follow from evidence, audio/video claims use the appropriate source, and advice is actionable. Unsupported or conflicting findings are removed or marked uncertain; no evidence means no score. A second model is a consistency check, not independent proof of correctness.

Prioritize opportunities by the likely effect on the speaker's stated goal, how often the pattern appears across comparable attempts, and whether it has a practical drill. Show at most two priorities per session alongside at least one evidenced strength. Treat these as coaching judgments, not objective rankings; the user can dismiss or change them. A low-confidence observation is never silently promoted into a high-priority recurring problem.

Automated speech recognition (ASR) can omit fillers, normalize grammar or mishear accents. Preserve the raw transcript and a separate user-corrected transcript, include timestamps, and allow the user to reject findings. Grammar judgments require especially careful transcript review. Pronunciation requires audio; text alone is insufficient.

## Baseline and initial target

Suggested starting hypothesis for presentations and general speaking confidence: **in four weeks, deliver a two-minute presentation with a main point, two supporting details and a short conclusion in at least two of three fresh practice prompts**, judged using the same checklist by the user and, if available, an independent listener. After each attempt, the user can separately rate their own comfort from 1–5 and add a note; this is self-reported experience, not a camera-detected confidence score. This is a practice target, not a prediction of a CEFR level.

1. In week 1 record three unscripted 1–2 minute prompts in similar conditions: explain a familiar project, describe a problem and solution, and express a preference with a reason. Save prompt, audience, preparation time, language, whether the speech was scripted, and recording conditions. Assess each independently and record the baseline and uncertainty. Select one repeated strength and one high-impact opportunity. Compare scripted and unscripted sessions separately.
2. For 10–15 minutes on most days: speak to a fresh prompt; review one timestamped strength and one opportunity; practice one short drill; record a revised version. Keep first and second attempts distinct; revised takes are practice, not the baseline.
3. Weekly, assess three fresh but comparable prompts using the same rubric, task conditions, and first-take rule. Compare results by dimension with the baseline, retaining mixed outcomes. Do not infer progress from one small score change.
4. At week 4 review the target and user/listener judgments, then adjust the target. If available, take EF SET 4-skill as a separate baseline and retake only when permitted and enough time has passed. Store official result and date separately from coaching.

If the priority is dialogue, include a separate short conversation task; a monologue cannot measure interaction. Ask a listener to summarize the main point before seeing the transcript: compare their summary to the speaker's intended message, while recognizing that one listener is only one observation.

## Proposed file-based workflow

```text
communication-coach/
  config/profile.yaml             # goal, language, consent, model and privacy preferences
  prompts/                        # versioned prompts and task conditions
  inbox/                          # user-added videos or audio
  sessions/YYYY-MM-DD-id/
    source/                       # original recording; never overwrite
    metadata.yaml                 # prompt, task, attempt, consent, software versions
    transcript.raw.json           # time-aligned ASR output
    transcript.reviewed.json      # optional corrections, separate from raw
    metrics.json                  # observations with method and units
    findings.json                 # evidence-linked findings and verification status
    report.md                     # strengths, opportunities, drills and limitations
  progress/weekly.md              # comparable first attempts only
  benchmarks/                     # optional official external results
```

A command or watched folder can create a session when a file arrives. First validate file type, duration and audio quality; extract audio locally; transcribe with timestamps; optionally let the user correct the transcript; calculate transparent metrics; evaluate only supported dimensions; validate findings; generate the report. Write outputs to a temporary session and finalize only on success. Preserve originals, report failures clearly, and prevent duplicate processing. Record model and rubric versions so changes do not masquerade as progress. Video frame sampling, if later added, is opt-in and only for observable presentation facts.

**Report example (illustrative, not your result):**

- Strength — 00:20–00:34: you gave a concrete example after the main point; this helped explain the idea.
- Opportunity — 00:47–01:01: the answer changed topics before completing the reason. Try “The main reason is … For example …”.
- Drill — Explain a familiar idea in three sentences: point, reason, example. Record it once again.
- Not assessed — interaction, because the recording was a solo explanation. Pronunciation remains unscored if the evaluator could not review audio.

## Verification and rollout

1. **Manual prototype:** run 3–5 recordings through a repeatable rubric; review timestamps and transcript with the user. Check that findings include actual strengths and useful changes, and that missing evidence is marked unavailable.
2. **Automation MVP:** single-user local folder/CLI, audio extraction, timestamped transcription, report generation and evidence checks. User-triggered processing first; add a watcher only after reliability is established. Confirm the transcription and assessment models, their costs, and whether any audio or text leaves the machine before selection.
3. **Reliability check:** rescore a small held-out set without seeing previous results; compare dimension-level agreement and inspect disagreements. Have a human listener review a sample, including clips with unfamiliar accents and low-quality audio. Do not report invented accuracy or calibrated confidence.
4. **Progress:** weekly summaries only across matching task types and rubric/model versions; show individual results and uncertainty rather than a single leaderboard. Re-baseline or explicitly mark a change when the evaluation method changes.
5. **Later additions:** optional conversation assessment, user-approved vocabulary review, reminders, presentation observations, and a lightweight dashboard if useful.

Privacy: default to local storage and user-initiated processing. Require consent from other speakers before analyzing shared recordings. Make retention, deletion and any cloud upload explicit in settings. Do not send a recording to a service silently.

## Decisions to make together

- Which presentation topics and audiences matter most to the user?
- Will a human listener be available to review occasional clips? Is local-only processing required, or is an explicitly approved cloud model acceptable?
- Preferred daily practice time, recording format, and operating system constraints?
