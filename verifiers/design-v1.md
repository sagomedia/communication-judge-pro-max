# Customized verifiers — design v1.0

Status: proposed design. The components below do not exist yet. A verifier reviews a specific claim; the degree of verification and the unresolved limitations must remain visible.

## Roles and controls

| Component | Input and task | Can establish | Cannot establish |
|---|---|---|---|
| **1. Input and coverage gate** | Inspect media, metadata, audible speech, duration, clipping, speaker attribution, context and complete/incomplete boundaries. | Which modalities and parts of the task are available. | The speaker's true ability from one short sample. |
| **2. Transcript integrity** | ASR with segments/times, then review relevant passages against audio by user or an audio-capable reviewer. Keep raw ASR and reviewed versions. | What a named reviewer heard at a given interval, with uncertainty. | An ASR confidence score is not proof the words were spoken. |
| **3. Structure and audience verifier** | Prompt, audience/goal if supplied, recording/transcript and custom anchors. Locate main point, progression and examples independently. | A supported coaching judgment about structure or task fit. | Actual audience understanding without listener evidence; audience fit without audience context. |
| **4. Language verifier** | Audio and verbatim transcript, with ASR uncertainty; identify grammar and word-choice examples and intended meaning. | Supported suggestions that preserve intended meaning and spoken register. | A certified CEFR/EF SET/IELTS level; grammar from uncertain words. |
| **5. Delivery verifier** | Original audio; replay relevant clips; optionally record repeatable acoustic measurements with measurement method. | Observable features and potential effects on intelligibility. | Native-like accent as a requirement, confidence, or exact filler counts from a cleaned transcript. |
| **6. Visual observation verifier** | Video and timestamps only if subject is visible and user enables it. | Descriptions of visible movements with limitations. | Personality, mental state, honesty, or claims based on audio alone. |
| **7. Deterministic evidence checker** | Evidence JSON, timestamps, transcript version, recording duration and schema. | Valid schema, timestamp bounds, stored version/hash consistency, exact match against the named transcript version. | Whether text matches what was actually said, the claim is relevant, or a score is fair. |
| **8. Independent evidence reviewer** | Original eligible media and task context; generate a blind initial assessment, then inspect the first assessor's claims and evidence. | `supported`, `contradicted`, or `uncertain` judgments, with reasons; can request replay or user review. | Guaranteed correctness or independence merely because a second AI was used. |
| **9. Change and calibration reviewer** | Rubric/model versions, comparable earlier sessions, user and human feedback. | Flags incompatible comparisons, recurring errors and proposed rubric changes. | A valid progress claim if the inputs, task or evidence changed materially. |

Separate assessor and reviewer instructions and outputs. The reviewer first reviews evidence without seeing the proposed conclusion where practical, then checks the claim. If different models are used, record both; shared biases remain possible. Disagreement stays visible; no silent majority vote or automatic promotion to high certainty. A human can correct a transcript, dispute a judgment, or have a qualified reviewer assess it.

## Proposed pipeline

1. Create a session manifest: media path and content hash, speaker, language, task, stated audience, start/end coverage, date, permission choices, and rubric version. Unsupported media or unclear speaker attribution blocks affected findings.
2. Produce versioned ASR and mark every timestamp and uncertain span. Original recording remains unchanged. Human correction produces a new transcript revision; it does not overwrite raw ASR.
3. Have the assessor find both strengths and limitations. Select eligible rubric criteria and identify direct timestamped supporting evidence. A negative claim based on absence requires inspection of the complete relevant portion.
4. Validate structure, timestamps, exact transcript text and provenance deterministically. Reject invalid claims or send them back for correction.
5. Independently inspect relevant media and evidence. Label each claim `supported`, `contradicted`, or `uncertain`. If only transcript is available, report transcript-only status; do not label audio-dependent conclusions supported. Unsupported findings are suppressed or flagged for review, not quietly polished into certainty.
6. Render per-criterion ratings only where input and evidence suffice, then a coaching summary and drill. Save proposed and checked results separately so there is an audit trail. Apply any user correction in a new revision.
7. Compare comparable recordings using the same rubric version and roughly similar task, duration, conditions and assistance. A changed version triggers a new baseline or explicit re-evaluation; keep old files intact.

### Provenance and confidence

Each claim includes: source modality (`audio`, `video`, `raw_asr`, `reviewed_transcript`), location, relevant excerpt or factual observation, transcript version, reviewer identity/type, and status. `confidence` is an uncalibrated qualitative reviewer judgment (`low`, `medium`, `high`), **not a probability**. Even `high` is not a certificate. Keep separate `text_match_status` and `audio_review_status`; no audio review can never be represented as verified audio.

## Output contract: illustrative JSON

The system should validate a versioned schema when implemented; this example is illustrative, not an implemented schema. All paths and quotes here are fictional.

```json
{
  "session_id": "example-001",
  "rubric_version": "1.0",
  "modality_available": ["audio", "video", "raw_asr"],
  "criterion": "main_point_and_purpose",
  "rating": 3,
  "rating_type": "custom_coaching_estimate",
  "assessment_status": "assessed",
  "claim": "The purpose becomes clear in the opening.",
  "evidence": [{
    "start_seconds": 8.2,
    "end_seconds": 15.1,
    "source": "raw_asr",
    "transcript_version": "asr-v1",
    "quote": "Today I will explain our proposed project.",
    "text_match_status": "matched",
    "audio_review_status": "not_reviewed"
  }],
  "independent_review": {"status": "uncertain", "reason": "Opening has not been checked against audio."},
  "confidence": "low",
  "coaching_action": "Replay the opening and confirm the exact words before finalizing."
}
```

For `not_assessed`, set the rating to `null`, provide the reason and omit unsupported evidence. For each assessed result, include observation, impact, supporting source, at least one appropriate next step, and reviewer status. Findings about a misheard or corrected quote must not survive as finalized criticisms.

## Example of a useful report

**Strength:** “At 00:12–00:20, you stated the purpose before giving details.” [only if checked]

**Opportunity:** “At 00:35–00:50, the transition between the problem and proposed solution is difficult to follow. Consider: ‘That is the problem; my proposal is…’” [interpretation, not fact]

**Next drill:** Re-record a 90-second explanation with a purpose, two supporting points, and a close. Review whether the listener can identify the purpose. Save both takes.

**Not assessed:** Interaction — the sample is a monologue. Confidence — record the speaker's own rating separately.
