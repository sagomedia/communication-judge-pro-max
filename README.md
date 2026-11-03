<img src="assets/icon.svg" width="64" height="64" alt="">

# Communicator Judge Pro Max

A personal, file-based communication coach for English presentations and everyday explanations. It separates speaking performance, a listener's understanding and your own confidence. Two project skills provide the instructions for an AI-assisted workflow; a local script summarizes comparable saved scores. Analysis uses whatever native video or audio capability the session provides; no scheduled automation is configured.

## Use the project skills

- **`$analyze-communication-video`** — provide your speaking video or audio and, if available, the topic, audience, objective and whether it is a first take. The skill gives the evaluation procedure to follow in a session that can view or listen to the media, such as Antigravity video analysis or Gemini, with your authorization. It guides evidence checks, tailored vocabulary and a private report. If media access or an independent review is unavailable, the result will say so.
- **`$improve-communication`** — ask for practice or a progress review. It uses actual saved sessions when available, proposes a focused drill and topic-specific vocabulary, and keeps comparisons and uncertainty visible.

The skills live in [`.agents/skills/`](.agents/skills/). They are instruction sets followed by an agent, not a stand-alone application or a guarantee that a separate verifier will run. A newly added project skill may require a new agent session to be discovered. To inspect recorded first-take results locally, run `python3 scripts/progress.py`; see the [record format](measurement/session-record-v1.md).

## Start here

1. Read [your goals and boundaries](context/profile.md), the [scoring system proposal](measurement/scoring-system-proposal.md), and [the measurement plan](measurement/progress-v1.md).
2. Select a comparable prompt in [practice prompts](context/prompts-v1.md). Before recording, copy [session template](templates/session.md) into your local `private/sessions/` folder and fill in the pre-recording questions.
3. Save a 1–2 minute first take under `private/inbox/`. Follow the [evaluation workflow](workflows/evaluate-session.md), using the [rubric](context/rubric-v1.md) and [report template](templates/report.md) in a session that can view or listen to the media.
4. Review the evidence using the [verifier instructions](verifiers/evidence-reviewer.md); optionally ask a listener to complete the [listener template](templates/listener.md). The skills apply these written procedures; a separate agent and enforced read-only access are not yet configured.
5. Record a weekly comparison with the [weekly review template](templates/weekly-review.md). Use [calibration workflow](workflows/calibrate.md) to propose changes based on mistakes.

## Your personal style goal

[Your north star](context/personal-style/goal-v1.md) captures the qualities you admire in different communicators. The [personal style rubric](context/personal-style/rubric-v1.md) and [creator reference library](context/personal-style/reference-library.md) translate them into draft, evidence-based coaching criteria. These supplement the general rubric; they do not score similarity to another person.

## Folder map

```text
.agents/skills/ reusable analysis and improvement skills
context/       goals, task prompts and scoring rules
examples/      fictional examples of good evidence; never personal results
workflows/     repeatable evaluation and calibration instructions
verifiers/     independent review procedures and verifier design
measurement/   definitions, comparisons and baseline protocol
research/      annotated psychology and measurement evidence
scripts/       local progress summary tool
templates/     reusable session, listener, report and weekly review forms
memory/        process log and approved calibration change-log templates
private/       your recordings and results; excluded from Git
```

`docs/` contains the original research/design notes and redirects for earlier links. [Source collection](docs/evaluation/sources.md) covers language frameworks; [psychology research](research/psychology-and-measurement.md) explains the new measures. [Video mapping](research/video-method.md) identifies which harness elements come from the inspiration video and what is still manual.

Treat a rating as an estimate for a particular performance, not a diagnosis, certification or fixed judgment of you. Never infer confidence from facial expression. Keep original media unchanged and obtain consent from other speakers before recording or sharing. Local ignore rules reduce accidental commits but don't encrypt files; verify privacy before sending anything to an external service.
