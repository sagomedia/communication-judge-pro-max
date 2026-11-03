# Evidence and source collection

Checked 2026-11-03. Official frameworks inform the design; custom ratings, targets, verifier rules and implementation plans are not endorsed by the sources.

| Source | What it contributes | How we use it and limitations |
|---|---|---|
| [Council of Europe: CEFR Table 3](https://www.coe.int/en/web/common-european-framework-reference-languages/table-3-cefr-3.3-common-reference-levels-qualitative-aspects-of-spoken-language-use) | Spoken-language descriptors for range, accuracy, fluency, interaction and coherence. | Conceptual coverage for spoken English. A framework, not an automatic exam or numeric calculator. Interaction needs interaction evidence. |
| [Council of Europe: CEFR Companion Volume](https://rm.coe.int/cefr-companion-volume-with-new-descriptors-2020/16809ea0d4) | Published scales for speaking, phonological control, addressing audiences, and related skills. | Source for later descriptor-based human review; no automatic conversion from our 1–4 scale to CEFR. |
| [IELTS official Speaking band descriptors](https://ielts.org/cdn/ielts-guides/ielts-speaking-band-descriptors.pdf) | Public assessment dimensions: fluency/coherence, vocabulary, grammar, pronunciation. | Check that our language coverage is meaningful. We do not issue IELTS bands or reproduce the test. |
| [EF SET 4-skill test](https://www.efset.org/4-skill/) and [FAQ](https://www.efset.org/faq/) | Official description of the 90-minute test and its skills and policies. | An optional external proficiency anchor. Public information reviewed is insufficient to reconstruct EF SET's proprietary speaking scoring system; check current retake policy. It is not a complete presentation assessment. |
| [Toastmasters: How to Evaluate Effectively](https://www.toastmasters.org/Magazine/Magazine%20Issues/2018/July2018/Sidebars/Evaluate%20Effectively) | Consider the speaker's objectives and offer concrete, supportive feedback on the speech. | Shape practical, goal-focused feedback; our particular rating scale is custom. |
| [Koenecke et al., Careless Whisper](https://arxiv.org/abs/2402.08021) | Documents speech-to-text hallucinations in the studied audio. | Review material claims against original audio; do not assume the study's error rate applies to this user's recordings or a different system. |
| [Thakur et al., Judging the Judges](https://arxiv.org/abs/2406.12624) | Studies LLM judge disagreement and vulnerabilities on text-generation evaluation tasks. | Motivates auditing and human comparison; it does not measure accuracy of this proposed speaking coach. |
| [Shi et al., Position Bias in LLM-as-a-Judge](https://arxiv.org/abs/2406.07791) | Documents order effects in pairwise model judgments. | When comparing recordings, test order swaps and log instability; results on model-generated text do not directly quantify bias for this use case. |

## Inspiration and method

The user's video is [AI harness demonstration](https://youtu.be/QRFyNJnrHxM). Prior analysis used an automatically generated transcript and sampled frames, not a continuous watch. Its harness ideas inform the design: explicit context, scoped tools, structured output, separate verification, versioned memory and scheduled runs. This source inspires the architecture; it does not validate the custom communication rubric.
