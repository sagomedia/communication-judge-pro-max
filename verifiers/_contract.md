# Verifier Execution & Scoring Contract (v2)

Every pillar verifier (`english-fluency.md`, `communication.md`, `body-language.md`, `tonality.md`) follows these rules when auditing a video:

1. **Direct Media Grounding & Proxy Compression (`< 100 MB`):** Watch and listen to the actual video/audio. Cite exact `MM:SS–MM:SS` timestamps and concrete words/visuals/sounds for every Pro and Con. Never invent observations for frames, body parts, or words you cannot clearly see or hear.
   - **Proxy rule:** If the original video exceeds `100 MB`, create a temporary compressed `720p` proxy under `100 MB` (preserving timestamps and audio) for full multimodal inspection, then delete the proxy afterward. Only split or reduce frame sampling if a very long video still cannot fit under `100 MB`.
   - **Observable-only guard (Tonality/Body):** Do not guess invisible body mechanics (e.g., hidden abdominal tension under clothing, `0.33 in` Adam's apple movement, tongue-tip position, or unmeasured Hz/dB figures); mark those `N/A — not observable on video` unless unmistakable in the audio or frame.
2. **Minimum Completeness & Length Gate (`Incomplete Take`):**
   - A full benchmark evaluation requires a **complete speaking take of at least 2 minutes (`120s`)** without mid-take abandonment.
   - If the recording is shorter than **2 minutes (`< 120s`)**, contains `< 120s` of actual speaking attempt, or is **aborted mid-take**, mark the status directly as **`Incomplete Take`** (do **not** assign a finalized CEFR/EF SET benchmark rank; show provisional proportional scores alongside observed Pros and Cons as coaching feedback).
3. **Format & Visibility Applicability (`N/A` Rule):** Before evaluating a rule, check whether it applies to this recording:
   - **No slides/charts:** Mark slide-text and exhibit-title rules `N/A — no slides used`.
   - **Solo monologue (no live partner/audience):** Mark conversational turn-taking/listening-interruption rules `N/A — solo recording`.
   - **Cropped camera framing:** Mark rules requiring unseen body parts (e.g., feet/ankles/chair armrests when framed waist-up) `N/A — out of frame`.
   - **Speaking vs. singing / physical self-tests:** Mark singing-only vibrato/riffing rules and in-person physical touch self-tests (e.g., pinching nose, finger on Adam's apple) `N/A — not observable in video`.
4. **Proportional Scoring Math (`0–100`):**
   - Evaluate only **applicable** rules. Deduct **at most once per violated Rule ID** (`-2` Minor, `-5` Moderate, `-10` Critical); if a violation recurs, list multiple timestamps in that Con entry without stacking extra deductions.
   - Normalize proportionally against the maximum possible deductions of the **applicable** rules so `N/A` rules never act as free passes:
     $$\text{Score} = \text{round}\left(100 \times \left(1 - \frac{\sum \text{Triggered Deductions}}{\sum \text{Max Deductions of Applicable Rules}}\right)\right)$$
   - Clamp final score to `0–100` and map to the unified tier (on complete takes `≥ 120s`):
     - **A1–A2:** `1–40`
     - **B1–B2:** `41–60`
     - **C1:** `61–70`
     - **C2:** `71–100`
5. **Required Output Structure per Verifier:**
   - **Take Status:** `Complete (≥ 120s)` or `Incomplete Take (Provisional)`
   - **Score & Tier:** `Triggered X / Applicable Max Y pts -> Score Z/100 (Tier or Provisional)`
   - **Pros (2–4 items):** Specific moments where the speaker demonstrated the pillar's book principles well, with timestamps and rule references.
   - **Cons (all triggered violations):** `Rule ID | Severity | Timestamp(s) | Observed Evidence | Exact Fix`
   - **Not Applicable (`N/A`):** Rule IDs skipped due to recording format or framing.
