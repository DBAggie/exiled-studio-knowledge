# Follow-ups for the maintainer (2026-11-17)

Left by the autonomous session that verified and merged PRs #2 to #25. Everything here needs the maintainer: a check in game, a number only the maintainer gives, or a decision. Go through them top to bottom; each stands alone. `main` is at `3.30.0-kb.23`.

## What was done
- **Batch 1, mechanics (#4 to #6, #12 to #20):** verified and merged. 7 files `engine-checked`, 5 `unverified` (one open point each, section A).
- **Batch 2, build advisor (#7 to #11):** verified and merged. 4 files `engine-checked`; `defensive-thresholds.md` stays `unverified` (section B).
- **Batch 3, community (#21 to #25):** verified and merged. 4 files `engine-checked`; `crafting.md` stays `unverified` (section C).
- **Economy (#2):** merged with the meta summary (section D).
- **Eval questions (#3):** merged as drafts, keys empty (section E).
- Each PR has a comment with every checklist point, its result and the link it was checked against.

## A. In-game checks (mechanics)
Each test is written out on its PR. Report the result and a session sets the file to `in-game-checked`.

| File | Open point | Test saved on |
|---|---|---|
| `recovery.md` | Does leech keep running after the target dies? | PR #12 |
| `minions.md` | Does summoning past the cap always replace the oldest minion? | PR #15 |
| `auras-curses.md` | Which way does the game round the reserved total? | PR #16 |
| `totems-traps-mines.md` | The trap arm time | PR #17 |
| `ailments.md` | Does a player's ailment threshold include energy shield? | PR #19 |

Also not checked in game, but stated with their source in the files:
- `recovery.md`: PoB and poewiki disagree on whether "increased total recovery per second from leech" shortens leech instances. Both readings are in the file.
- `ailments.md`: PoB takes non-damaging ailment effect from the hit **after** enemy mitigation; poewiki does not say.
- `crit.md`: the 3.6.0 cap removal was confirmed from poewiki's version history, not from the 3.6.0 forum post.

## B. Numbers only the maintainer gives (build advisor)
- **`defensive-thresholds.md`**: every life, chaos resistance and max hit target per content tier is a rule of thumb written from memory. Give or approve the numbers, then the file can leave `unverified`.
- **`gearing.md` line 60**: "a support is often worth 20% to 40% more damage".
- **`trade-offs.md` line 42**: "below about 40% to 50% crit chance, crit multiplier gives little".
- **`budget-tiers.md`**: what each tier ("a few divines", "tens", "hundreds") buys.

## C. Crafting points no source confirmed
`crafting.md` stays `unverified` for these. The official notes (3.26 to 3.30) and the economy snapshot do not settle them:
- Resonators unchanged in 3.30 (the snapshot has no resonator category).
- Multimod still on the bench next to the new locks.
- The full list of Harvest reforge crafts in 3.30.
- How much fossil supply changed after Delve's atlas clusters left and Sulphite stopped spawning in maps at random.

A look at the in-game bench and Horticrafting station settles the first three.

## D. Approvals
- **Meta summary** in `snapshots/covens/2026-11-16.md` (read from the poe.ninja builds page on 2026-11-17, league day 4): approve or correct it (Q11). The snapshot stays `unverified` until then.
- **Promote to `maintainer-approved`**: only the maintainer does this. 15 references are `engine-checked` and ready for your skim: `damage`, `conversion`, `crit`, `charges`, `flasks`, `triggers`, `defences`; `diagnosis`, `gearing`, `reading-breakdowns`, `trade-offs`; `jargon`, `archetypes`, `budget-tiers`, `atlas`.
- **Merged while still `unverified`** (7 files): the five in section A, `defensive-thresholds.md` and `crafting.md`. Each says in its Verification section what is open. Say if you would rather these had waited.

## E. Evals
- **Answer keys**: all 58 cases have `key: null`. The maintainer writes or approves them (plan D8).
- **Diagnosis fixtures**: the 8 diagnosis cases say `"build": "fixture: TBD by maintainer"`.
- **`traps-007`** assumes the Blood Magic keystone was removed. poewiki's reservation page still describes a Blood Magic keystone, so the intent looks wrong; check before keying it.
- **Some mechanics drafts were written before batch 1's corrections.** When keying, use the corrected files: attack crits need a second accuracy check (`mechanics-012`), flask effect and duration raise life flask recovery, triggered skills pay their cost (`mechanics-017`), endurance charges give elemental damage reduction (`mechanics-007`).
- **The eval runner is not built.** Q5 says it runs on the workstation by hand. It needs a decision on how it calls Claude (which client, with and without the plugin) before a session builds it.

## F. Not started, needs a decision
- **Patch-note triage** (plan D7, rule 4): the tool that matches new patch notes to mechanics files and opens issues is not built. Useful now: 3.30 hotfixes keep landing (the references were checked up to 3.30.0b Hotfix 4).
- **Economy refresh cadence**: runs by hand (Q7). The only snapshot is 2026-11-16; league-start prices go stale in a day or two.
- **Hardcore, SSF and Standard** snapshots: not fetched.
- **Dev skill `exiled-studio-mcp`** (plan step 7) lives in the `exiled-studio` repo; this session could read that repo but not write to it.
- **The engine check used PoB only.** No session so far had Exiled Studio's MCP tools or `calc-run`. A session on the workstation with the app running could re-check the `engine-checked` numbers against the engine itself.

## G. Housekeeping
- `VERIFICATION-HANDOFF.md` is finished work now; this PR marks it done at the top. Delete it or keep it as a record.
- Sources: the references cite PoB files by GitHub link at tag `v2.67.2` and Exiled Studio schemas as `repo:DBAggie/exiled-studio/...` (dev branch at `b42e49f`).
