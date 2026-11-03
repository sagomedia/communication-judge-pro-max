# Personal communication scoring system — proposal v1

**Status:** Design for the user to review. This extends the existing [rubric v1](../context/rubric-v1.md) as a practical scorecard; it does not change the rubric or make the automation operational. The categories and 1–4 scores are custom coaching judgments. They are not validated exam scores, diagnostic measurements or evidence about your general worth or intelligence.

## Goal and scope

For an English presentation or an everyday explanation, identify (a) what is working, (b) what most affects the listener, and (c) one practical action. Evaluate the task the speaker actually chose; a 60-second answer does not need the structure of a formal presentation. Confidence and nervousness are self-reports, not visual judgments.

## Part 1: score the performance

For each applicable criterion, choose the closest anchor in [the full rubric](../context/rubric-v1.md), based on the whole available performance. **1 = major difficulty; 2 = developing; 3 = mostly effective; 4 = consistently effective for this task.** Every score needs evidence, timestamp, source modality, reviewer and uncertainty. Use `not assessed` when the relevant evidence is missing or insufficient; do not enter 0.

| Area | What the score considers | Minimum evidence | Main reference or basis |
|---|---|---|---|
| **Main point** | Whether the listener can identify the purpose or message | Enough speech and the speaker's task/goal | Custom presentation criterion; CEFR coherence informs design |
| **Structure** | Whether ideas follow a useful sequence and transitions make their relationships clear | Enough of the full recording | CEFR coherence; custom task-specific anchors |
| **Supporting points** | Whether relevant reasons, examples or explanations make the message understandable | A task where support is appropriate and enough of the talk | Custom presentation criterion; audience purpose |
| **Audience fit** | Whether wording and context suit the intended audience | Stated audience and goal, plus relevant speech | CEFR addressing audiences; custom judgment |
| **Fluency** | Whether speech continues in a way that supports understanding, allowing natural pauses | Original audible speech | CEFR spoken fluency; custom anchors |
| **Intelligibility and delivery** | Whether speech can be understood and pacing/emphasis support the message | Original audio of adequate quality | CEFR phonological control; custom anchors |
| **Vocabulary** | Whether words communicate the intended distinctions and meaning | Audible or reviewed verbatim words and enough context | IELTS lexical resource and CEFR vocabulary inform design |
| **Grammar and sentence clarity** | Whether sentence choices communicate the intended meaning | Audible or reviewed verbatim speech and enough context | IELTS grammatical range/accuracy and CEFR accuracy inform design |

See [source collection](../docs/evaluation/sources.md) for original frameworks and their scope. Each mapped criterion is our adaptation, not the original institution's score or scale. Rate individually rather than averaging the eight numbers into an overall score before we establish whether that is useful. This also prevents missing evidence from being hidden by an attractive total.

### Example: how one criterion is decided

**Structure, fictional example:** A speaker presents the topic, gives relevant details, but jumps between points before a short close. Under the rubric, an evaluator may propose **2/4** if the jumps make the sequence difficult to follow. They must cite where that occurred and identify a strength, such as a clear opening. The evidence reviewer can confirm, disagree, or mark the conclusion uncertain. The number is an estimate for that recording, not the speaker's permanent ability.

## Part 2: record outcomes that are not performance ratings

- **Self-confidence:** speaker's own 0–10 response before the talk, using the exact task-specific question in [progress-v1.md](progress-v1.md).
- **Nervousness:** speaker's separate optional 0–10 response before the talk. A nervous person can still speak effectively.
- **Listener understanding:** record whether a listener, without seeing the intended answer, captures the speaker's previously written main point: matched / partly matched / not matched / unable to judge. Record who judged the match.
- **Task completion:** when applicable, record presence of a main point, two relevant supports and a close, each `yes` / `no` / `uncertain` with evidence. This checks the practice task, not every form of good communication.
- **Visible delivery:** optionally describe specific gestures or positioning with timestamps. Never convert them into an inferred confidence or personality score.

Keep these measures and the eight ratings separate. Do not infer a listener result if nobody responded. The custom self-report questions are not validated psychology scales and must not be interpreted as diagnoses.

## Part 3: verify each finding

The evaluator proposes a score and locates relevant evidence. The [evidence reviewer](../verifiers/evidence-reviewer.md) checks the original media when available, the cited timestamps, whether the observation supports the specific anchor, and whether the needed context exists. A second AI is not automatically independent or accurate. Record `supported`, `contradicted`, `uncertain`, or `not independently reviewed`. Exact transcript matching checks the text version only; it does not prove the words were spoken. If the relevant audio is inaccessible, mark audio-dependent criteria not assessed.

Each scorecard entry should contain:

```text
Criterion: Structure
Rating: [1–4 or not assessed]
Observation: [what happened, its effect, and at least one positive or limiting example]
Evidence: [timestamp + audio / reviewed transcript / video]
Audio checked by: [reviewer, or not reviewed]
Review result: [supported / contradicted / uncertain / not independently reviewed]
Next action: [one small exercise, if this criterion is the priority]
```

If a reviewer contradicts a claim, do not present the disputed score as verified; revise it with evidence or leave it uncertain. Avoid reporting numerical certainty percentages.

## Part 4: measure progress

1. Record three comparable first takes on different prompts with the same approximate duration, audience, preparation and language. Keep topic familiarity and recording conditions. This is an initial personal baseline, not a statistically reliable proficiency test.
2. Continue with fresh comparable first takes; label rehearsals separately. Record each criterion's individual rating, source and reviewer; do not mix rubric versions or conditions silently.
3. Compare criterion-by-criterion ratings and cited examples across recordings, alongside confidence, nervousness and listener outcomes. Report the count and all raw values; acknowledge small samples, topic differences and rater disagreement.
4. Choose one priority based on the speaker's goal, impact on the listener, repetition across recordings, and reliability of evidence. Describe why rather than applying an unvalidated formula. Practice, then look for supporting evidence in future first takes.

Suggested task-specific target: in two of three comparable fresh first takes within four weeks, clearly include a main point, two relevant supports and a brief close. Record the evidence and who assessed it. This is a proposal, not a finding about your current ability.

## Special tasks

For an interview or conversation, create a separate interaction rubric after sufficient research and context; a monologue cannot establish listening or turn-taking. For pronunciation-specific concerns, ask which sounds/words matter and check actual audio. For formal English proficiency, record an external EF SET four-skill result or appropriate qualified assessment separately; do not translate these custom ratings into CEFR/EF SET/IELTS scores.

## Decisions for personalization

- Which speaking task matters first: a project presentation, a short everyday explanation, or something else?
- Which two areas matter most for the first month? Possible options: main point and structure; fluency and intelligibility; vocabulary and grammar; or another combination.
- Optional after a pilot: consider whether a single summary number is helpful. It would need explicitly chosen weights, a clear missing-data rule, and testing against useful decisions; it must never be confused with a validated proficiency score.
