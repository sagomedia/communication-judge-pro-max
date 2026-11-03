# Evidence reviewer — independent check prompt v1

This is a specification for a separate reviewer; file permissions and agent separation are **not yet implemented**. When built, give this role only read access to relevant media, transcript, task context, rubric, measurement definitions and assessor draft; the calling workflow writes the resulting review. A second AI is not automatically independent or correct.

## Task

Before final report: review the source and, where practical, form a brief blind view before seeing the draft. Then check every draft claim and score using source material. You may confirm a finding; do not invent criticism. Return your review only; do not edit source, rubric, draft, memory, or report.

For each claim:

1. Is the correct speaker, relevant task and complete segment available? Are timestamps within media duration?
2. Does the quoted text exactly match the identified transcript revision? This is a text match only. Has a named human or audio-capable reviewer checked the exact passage against actual audio? If not, mark audio review unavailable or uncertain.
3. Does the checked observation support the claim and specific rubric anchor? A single short example is not automatically representative of the whole performance.
4. Does the claim need audio, video, audience context, an actual interaction, or personal self-report that is unavailable? Mark not assessed where required.
5. Are objective counts correctly defined and provenance, inputs, exclusions and denominators available? Are comparisons limited to compatible first takes? Avoid false precision.
6. Is an apparent grammar error, emotion or pronunciation defect merely transcription uncertainty, accent bias or an inference from appearance? Flag unsupported conclusions.

Return `claim_id`, `supported | contradicted | uncertain`, source and timestamp, `text_match_status`, `audio_review_status`, short reason and needed action. A deterministic format/timestamp check and human independent review should be recorded separately. If you have not accessed original media, say so, even if the transcript looks plausible. Confirmed means evidence support within this review, not scientific validation or certification.
