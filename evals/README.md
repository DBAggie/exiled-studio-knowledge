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

## Running the suites
The runner is a local script, run by hand on the workstation (`REVIEW-QUEUE.md`, Q5). CI never calls a model; it only checks the case format and runs the runner's tests against a fake model.

```sh
python evals/run.py                      # every approved case, with and without the plugin
python evals/run.py --suite mechanics    # one suite
python evals/run.py --id traps-001 --arms plugin
python evals/run.py --dry-run            # list what would run; no model calls
python -m unittest discover -s evals     # the runner's own tests
```

- **How Claude is called:** the `claude` command line (Claude Code) in print mode, in an empty working directory. The `plugin` arm adds `--plugin-dir plugins/poe1-expert`; the `plain` arm adds nothing. `--model` and `--grader-model` choose models.
- **Grading:** a second, separate call with no tools and no plugin sees the question, the answer, the tools it called and the key, and returns a verdict per key item. A case passes when every `must` is met, no `must_not` is violated, and every tool in `expect_tools` was called (checked from the transcript, not by the grader). A grader reply that is not JSON, or that skips a key item, is an error, never a pass.
- **Cases that need the app** (`setup.app_mcp`, the whole `tool-discipline` suite) are skipped unless `--app-mcp-config <file>` points at a running Exiled Studio's MCP server.
- **Diagnosis fixtures** are not written yet. Those cases run from the prompt alone and are marked `no-fixture`.
- **Output:** `local/eval-runs/<time>/results.jsonl` and `summary.md` (pass rates per suite and arm, and the v1 gates). `local/` is ignored by git.
- **Cost:** each case is two model calls per arm (answer, grade): about 230 calls for the full set.

The runner was tested with a fake model only. Its first real run on the workstation is the check that the `claude` flags and output format match the installed version.
