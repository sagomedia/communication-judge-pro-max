# Communicator Judge Pro Max (v2)

This repository is a file-based communication coaching harness. It evaluates spoken English recordings across **4 book-grounded pillars** (`English Fluency`, `Communication`, `Body Language`, `Tonality`), verifies findings through a **Communication Coach Verifier**, tracks **cross-session memory + Anki spaced recall**, and renders a **3-page editorial PDF report**.

## Core Rules
- **Never overwrite originals:** Keep source videos in `input assets/` untouched and never edit prior session outputs.
- **Direct media grounding:** Always inspect the actual video + audio (`< 100 MB`; if larger, encode a temporary compressed `720p` proxy preserving timestamps and audio, inspect it, then delete the proxy).
- **2-minute completeness gate:** A full benchmark evaluation requires a complete speaking take of **≥ 120 seconds** without mid-take abandonment (`verifiers/_contract.md`).
- **Natural spoken English:** Never penalize normal casual speech (`"gonna"`, contractions, conversational fragments); flag only genuinely broken/unnatural grammar (`verifiers/english-fluency.md` Section 2B).
- **Observable-only guard:** Never guess hidden internal mechanics (e.g., invisible Valsalva tension under clothing, larynx height in inches, tongue position, unmeasured Hz/dB) or rules inapplicable to the format (`N/A` proportional scaling).
- **Private local outputs:** Store session reports, PDFs, and speaker memory strictly under `private/` (excluded from Git via `.gitignore`).

## Project Map
- `.agents/skills/judge-communication/SKILL.md` — master workflow skill binding the full v2 pipeline
- `verifiers/` — `_contract.md`, `english-fluency.md`, `communication.md`, `body-language.md`, `tonality.md`, and `communication-coach.md`
- `memory/memory-rules.md` — cross-session consistency & 4-box Anki recall rules
- `templates/report-certificate.html` — 3-page A4 editorial HTML/SVG report template
- `scripts/memory_store.py` — SHA-256 deduplication, memory briefs, and Anki deck state
- `scripts/render_pdf.py` — headless Chrome HTML → PDF renderer
- `private/` — gitignored local sessions (`private/sessions/`), memory (`private/memory/`), and reviews
