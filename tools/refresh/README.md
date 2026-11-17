# Refresh jobs

Run on the maintainer's workstation, by hand (plan D7; `REVIEW-QUEUE.md`, Q7). Each run opens a PR to this repository; nothing is committed directly, and every refresh goes through the maintainer's review.

- **Economy** (`economy.py`, plan step 8): fetches poe.ninja's supported economy-overview endpoints for one league, low volume and cached, with a plain User-Agent, and writes `plugins/poe1-expert/skills/poe1-economy/snapshots/<league-slug>/<date>.json`. Claude sessions never call poe.ninja.
- **Patch-note triage** (`triage.py`): matches the lines of new patch notes to the references they may touch, by keyword (`triage-keywords.json`), and writes one review note per reference to `local/triage/`. With `--open-issues` it opens one GitHub issue per reference. It never rewrites a reference. Stat-ID matching is not done: stat IDs live in the app's game data, not here.

  ```sh
  python tools/refresh/triage.py --title "3.30.1" --file notes.txt --source <forum link>
  python tools/refresh/triage.py --title "3.30.1" --url <forum link> --open-issues
  ```

  When a reference gains a topic, add its keywords to `triage-keywords.json`; a test fails if a reference has no entry.

## Cadence
Refreshes run by hand; no scheduled task is registered (`REVIEW-QUEUE.md`, Q7), and `register-task.ps1` stays unused.

- League-start week: every 1 to 2 days. Then weekly to every two weeks. Stop at league end and mark that league's snapshots `historical`.
- `python tools/refresh/due.py --max-age 2` (first week) or `--max-age 7` (later) lists each league's newest snapshot and says which are due. It reads only this repository.
- One command refreshes several leagues as one PR:

  ```powershell
  pwsh tools/refresh/run-economy.ps1 -League Covens, "Hardcore Covens", Standard
  ```

  League names are poe.ninja's league ids; `economy.py` prints the known ids when a name is wrong. SSF leagues have no market, so there are no SSF prices to fetch; SSF questions get no price answer.
- After the PR opens, add the hand-written summary (`<date>.md`) for the leagues you want one for, then merge.

Tests: `python -m unittest discover -s tools/refresh`.
