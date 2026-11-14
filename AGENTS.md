# Communicator Judge Pro Max (v2)

This repository is a file-based communication coaching harness. It evaluates spoken English recordings across **4 book-grounded pillars** (`English Fluency`, `Communication`, `Body Language`, `Tonality`), verifies findings through a **Communication Coach Verifier**, tracks **cross-session memory + Anki spaced recall**, and renders a **3-page editorial PDF report**.

## Step 0 — Mandatory Fail-Closed Capability Gate ("Before Everything")
**STOP AND CHECK BEFORE DOING ANYTHING ELSE.** This job requires simultaneous perception of spoken voice/audio AND continuous moving video. Many models are text-only or image-only, and many harnesses block `.mp4` media reading. Attempting to evaluate without native audio + video produces **wrong, hallucinated results** and is strictly forbidden.

Before reading speaker memory or scoring any pillar:
1. **Run `python3 scripts/preflight_check.py "<video_path>" --probe-clip /tmp/cj_probe.mp4`** (or `--tools-only` if no video path is provided yet). Verify `environment_ok: true` and `media_ok: true` (both real video AND audio streams exist).
2. **Test direct `.mp4` video+audio perception on the tiny probe clip** (or directly on the video if `<= 25 MB` and `<= 240s`) using your harness's media-reading tool (`read_file` or native multimodal attachment), then delete `/tmp/cj_probe.mp4`.
3. **Confirm all 3 capabilities hold simultaneously:**
   - **Harness `.mp4` support:** Your tool reads `.mp4` with video + audio (does NOT reject as binary/unsupported MIME).
   - **Native voice/audio understanding:** You directly hear exact spoken words, fillers, pauses, pitch, and vocal tone.
   - **Native video understanding:** You directly see continuous posture, hand gestures, gaze, and facial expressions across timestamps.
4. **No fake workarounds:** Never simulate missing modalities with external ASR/Whisper transcripts, extracted PNG frame strips without audio, `ffprobe` loudness guesses, or fabricated timestamps.
5. **Fail-Closed Abort:** If ANY check above fails or is uncertain, **delete any temporary probe clip, STOP IMMEDIATELY**, do NOT write `report.md`/`report.pdf`/`session.json`, and output:
   - Status: `UNSUPPORTED_ENVIRONMENT — CAPABILITY GATE BLOCKED`
   - Exact blocker (`Harness lacks .mp4 media reader`, `Model lacks native voice/audio understanding`, `Model lacks native video understanding`, or `Missing tools/stream`)
   - What is required instead (an AI model with native **audio + video** understanding running inside a harness that passes `.mp4` video+audio directly to the model).

## Core Rules
- **Never overwrite originals:** Keep source videos in `input assets/` untouched and never edit prior session outputs.
- **Direct media grounding & chunking:** Always inspect actual video + audio directly. Keep each inspected `.mp4` segment `<= 4 min` (`240s`) and `<= 25 MB` (for longer/larger files, encode temporary `720p` chunked proxies in `/tmp`, inspect all chunks in order, then delete the proxies immediately).
- **2-minute completeness gate:** A full benchmark evaluation requires a complete speaking take of **≥ 120 seconds** without mid-take abandonment (`verifiers/_contract.md`).
- **Natural spoken English:** Never penalize normal casual speech (`"gonna"`, contractions, conversational fragments); flag only genuinely broken/unnatural grammar (`verifiers/english-fluency.md` Section 2B).
- **Observable-only guard:** Never guess hidden internal mechanics (e.g., invisible Valsalva tension under clothing, larynx height in inches, tongue position, unmeasured Hz/dB) or rules inapplicable to the format (`N/A` proportional scaling).
- **Attested private outputs:** Store session reports, PDFs, and speaker memory strictly under `private/` (excluded from Git via `.gitignore`), and include `capability_attestation` with verified probe observations in `session.json`.

## Project Map
- `.agents/skills/judge-communication/SKILL.md` — master workflow skill binding Step 0 + Steps 1–5
- `scripts/preflight_check.py` — Step 0 host tooling, video/audio stream check, SHA-256, and probe generator
- `verifiers/` — `_contract.md`, `english-fluency.md`, `communication.md`, `body-language.md`, `tonality.md`, and `communication-coach.md`
- `memory/memory-rules.md` — cross-session consistency & 4-box Anki recall rules
- `templates/report-certificate.html` — 3-page A4 editorial HTML/SVG report template
- `scripts/memory_store.py` — SHA-256 deduplication, attestation enforcement, memory briefs, and Anki deck state
- `scripts/render_pdf.py` — headless Chrome HTML → PDF renderer
- `private/` — gitignored local sessions (`private/sessions/`), memory (`private/memory/`), and reviews
