# Evals

Eval suites measure what the pack adds: each case runs with and without the `poe1-expert` plugin (plan D8).

| Suite | Example | Graded by |
|---|---|---|
| `mechanics` | Increased vs more, conversion order, armour vs big hits | Answer key and sources |
| `traps` | PoE2-only or removed mechanics asked in a 3.30 context | Must catch the mismatch |
| `diagnosis` | Corpus builds with planted flaws | Expected findings list |
| `tool-discipline` | "DPS if I swap this ring?" | Must call `preview_item_edit` |
| `snapshot-honesty` | Price or meta questions | Must cite `as_of` and league |

## Rules
- **Answer keys are written or approved by the maintainer**, never by the sessions that write the knowledge. Sessions may draft questions (`key_status: draft-question`, `key: null`); the maintainer fills in the key and sets `maintainer-approved`.
- Judgment answers are graded against a rubric by a separate agent.
- Case format: `check_cases.py` (one JSON object per line in `suites/<suite>.jsonl`). CI runs it on every PR.

## v1 gates
- 0 cross-game contamination
- 100% date disclosure on snapshot answers
- At least 95% tool discipline when the app is reachable
- At least 90% mechanics accuracy
- A clear gain over plain Claude on build diagnosis

## Not built yet
The runner (each case with and without the plugin, then grading) and CI's fast subset. Both need a decision on how CI calls Claude (`REVIEW-QUEUE.md`).
