# Follow-ups for the maintainer (2026-11-17)

Left by the autonomous session that verified and merged PRs #2 to #25. Everything here needs the maintainer: a check in game, a number only the maintainer gives, or a decision. Go through them top to bottom; each stands alone. `main` is at `3.30.0-kb.31`.

## What was done
- **Batch 1, mechanics (#4 to #6, #12 to #20):** verified and merged. all 12 files `engine-checked` after later passes (section A).
- **Batch 2, build advisor (#7 to #11):** verified and merged. all 5 files `engine-checked` after later passes (section B).
- **Batch 3, community (#21 to #25, #28):** verified and merged. All 5 files `engine-checked` (section C).
- **Economy (#2):** merged with the meta summary (section D).
- **Eval questions (#3):** merged as drafts, keys empty (section E).
- Each PR has a comment with every checklist point, its result and the link it was checked against.

## A. Mechanics: all five open points closed
Closed on 2026-11-17: leech after the enemy dies and oldest-minion replacement (the maintainer's confirmation, PR #32), trap arm time (near-instant, no published number, PR #32), reservation rounding (PoB and the engine, PR #31), and the player's ailment threshold (life only, energy shield does not count; for Chaos Inoculation the life before the keystone applies; the maintainer and poewiki, PR #33). All 12 mechanics files are `engine-checked`. None of the five was tested in game by a session; if any answer came from an in-game test, say so and that file can become `in-game-checked`.

Not checked in game, but stated with their source in the files:
- `ailments.md`: PoB takes non-damaging ailment effect from the hit **after** enemy mitigation; poewiki does not say.
- `crit.md`: the 3.6.0 cap removal was confirmed from poewiki's version history, not from the 3.6.0 forum post.

Community sources the maintainer added on 2026-11-17: poedb and Craft of Exile (used for `crafting.md`), Mobalytics and PoE Vault guides (no mechanics explainers for these points; useful for the community and build-advisor files, with ideas credited and no text copied).

## B. Numbers only the maintainer gives (build advisor)
- **`defensive-thresholds.md`** (PRs #34, #35): done. Life and ES targets now follow observed pools by level (the maintainer's decision), and the file is `engine-checked`. The 10,000 and 15,000 max hit figures for bosses are still commonly cited values with no source. The observed table is from league day 4; re-read it later in the league.
- **`gearing.md` line 60**: "a support is often worth 20% to 40% more damage".
- **`trade-offs.md` line 42**: "below about 40% to 50% crit chance, crit multiplier gives little".
- **`budget-tiers.md`**: what each tier ("a few divines", "tens", "hundreds") buys.

## C. Crafting points (closed 2026-11-17, PR #28)
Resonators, multimod and the type-guaranteed Harvest reforges were confirmed from poedb's current game data (the maintainer pointed to it), and `crafting.md` is now `engine-checked`. Fossil supply is a market question and is left to economy snapshots. Craft of Exile (3.29 data, accepted by the maintainer for general crafting) agrees and was added as a second source in PR #29.

poedb was also searched for the five section A points (trap arm time, leech after death, minion replacement, reservation rounding, player ailment threshold). It does not state any of them; they still need the in-game tests.

## D. Approvals
- **Meta summary** in `snapshots/covens/2026-11-16.md`: approved by the maintainer on 2026-11-17; the snapshot is `maintainer-approved` (PR #39).
- **Promoted to `maintainer-approved`**: all 22 references, on the maintainer's approval of 2026-11-17 (PR #39, `3.30.0-kb.32`). None was checked in game.
- Nothing in the pack is `unverified` or `engine-checked` any more.

## E. Evals
- **Answer keys**: all 58 are approved: traps, tool discipline and snapshot honesty (PR #36), the 20 mechanics keys (PR #37) and the 8 diagnosis keys (PR #38), the last two suites dictated by the maintainer. Still open: the 8 diagnosis build fixtures (`fixture: TBD by maintainer`).
- **Diagnosis fixtures**: the 8 diagnosis cases say `"build": "fixture: TBD by maintainer"`.
- `traps-007` was replaced with a scarab question (PR #36). Still to fix when keying: `diagnosis-008` now says Warden and `diagnosis-001` states its fire resistance unambiguously (PR #38). `mechanics-015` now states +1 curse (PR #37). Points where a dictated answer differed from the verified files, for the maintainer to confirm: chill cap 30% and suppression 40% (keys follow the files); Juggernaut node texts in `diagnosis-007` were not checked, so the key names no node.
- **Some mechanics drafts were written before batch 1's corrections.** When keying, use the corrected files: attack crits need a second accuracy check (`mechanics-012`), flask effect and duration raise life flask recovery, triggered skills pay their cost (`mechanics-017`), endurance charges give elemental damage reduction (`mechanics-007`).
- **Eval runner**: built (`evals/run.py`, PR #40). It calls the `claude` command line with and without the plugin, grades with a separate call, and writes the v1 gate table. Tested with a fake model only; **the first real run on the workstation is still to do** (`python evals/run.py --suite traps` is a small first check). The `tool-discipline` suite needs `--app-mcp-config` and a running app.

## F. Not started, needs a decision
- **Patch-note triage**: built (`tools/refresh/triage.py`, PR #40). Keyword matching only; no stat IDs. Not yet run on real notes: the references were checked up to 3.30.0b Hotfix 4, so run it on the next hotfix or patch.
- **Economy refresh cadence**: stays by hand (Q7). `tools/refresh/due.py` says when a league is due (PR #40). The only snapshot is still 2026-11-16: the session cannot fetch one (poe.ninja is not reachable from it, and sessions must not call it). **The maintainer runs the refresh.**
- **Hardcore and Standard** snapshots: not fetched, for the same reason. One command now does all three: `pwsh tools/refresh/run-economy.ps1 -League Covens, "Hardcore Covens", Standard` (edited in PR #40, not run; check the league ids against what `economy.py` prints). **SSF** has no market, so there is nothing to fetch.
- **Dev skill `exiled-studio-mcp`**: already done. It was merged into the Exiled Studio repo's `dev` branch as its PR #124 on 2026-11-16 (`.claude/skills/exiled-studio-mcp/SKILL.md`); this list was out of date.
- **Engine source reviewed (PR #31):** the "Check with the engine" sections of the 12 mechanics files now come from `crates/loom-calc` (dev `b42e49f`). The engine could not be built or run in the session, so nothing was checked by running `calc-run`; a session on the workstation could do that.

## G. Housekeeping
- `VERIFICATION-HANDOFF.md` is finished work now; this PR marks it done at the top. Delete it or keep it as a record.
- Sources: the references cite PoB files by GitHub link at tag `v2.67.2` and Exiled Studio schemas as `repo:DBAggie/exiled-studio/...` (dev branch at `b42e49f`).
