# Verification handoff: the 22 draft references

> **Status, 2026-11-17: all three batches and the meta summary are done and merged** (PRs #2 to #25, `3.30.0-kb.23`). What is left for the maintainer is in `FOLLOW-UPS.md`. The text below is kept as the record of how the work was done.

Decided in `REVIEW-QUEUE.md`, Q9 (maintainer, 2026-11-17). This note is the work list for the sessions that move PRs #4 to #25 from `unverified` toward `maintainer-approved`. Read it whole before starting a batch.

## How a verification session works

1. **One batch per session, one PR at a time**, in the batch order below. Check out the PR's branch, verify, push to the same branch. Do not open new PRs for this.
2. **Use Claude in Chrome** (the maintainer's real browser) for every web source. Automated fetches of poewiki were blocked; the browser is not. Load the `anthropic-skills:chrome-browser` skill first. Work in a new tab, read only, never sign in or post anything.
3. **Sources, in this order:**
   1. The official patch notes: the forum board https://www.pathofexile.com/forum/view-forum/patch-notes. Every post with **3.30.x** in its title (3.30.0 and each hotfix after it), read in full. Earlier patches (3.26 to 3.29) where a point names one: the same board, their own posts.
   2. poewiki (https://www.poewiki.net) for mechanics the notes do not state. Treat it as a secondary source; prefer the patch notes when they disagree, and record the disagreement.
   3. For mechanics files: the engine (Exiled Studio's MCP tools or `calc-run`, if the session has them) and the pinned PoB 2.67.2 checkout, read only. PoB is the oracle of what PoB does, not of what the game does.
   4. Copies (poedb, patchbot.io) only to find a passage, never as the evidence.
4. **For each point in the PR's checklist below:** confirm it, correct it, or mark it plainly as unconfirmed in the file with the reason. Write in your own words; cite by link. Never copy poewiki or poedb text.
5. **Then set the header:**
   - `sources`: replace copy links (poedb, patchbot.io) with the official thread links the point was checked against; keep poewiki links that were used.
   - `verification`: `engine-checked` when every numeric rule was checked against the engine or PoB and the patch notes; `in-game-checked` only when the maintainer checked something in game. Leave `unverified` if any checklist point is still open, and say which in the PR.
   - `as_of`: the day of the check.
6. **On the PR:** a comment listing each checklist point with its result (confirmed / corrected / still open) and the link it was checked against. Run `python tools/validate/validate.py` and give its result.
7. **The maintainer** reads that comment, merges, and later promotes files to `maintainer-approved`. Sessions never set `maintainer-approved` and never merge.

## Applies to every PR

- Each PR body says the 3.26 to 3.29 notes were not all read in full and the 3.30 notes were read through a copy cut off near the end. So besides the listed points, **read the full official 3.30.x posts once per batch** and check each file for anything they change in its topic.
- Keep `patch: 3.30.0`. If a hotfix changed a rule, say which (for example "3.30.0d").

## Cross-file conflicts found while writing this note

- **Crits and elemental ailments.** `ailments.md` (PR #19) line 68 says crits always apply ignite, chill, freeze and shock; `crit.md` (PR #6) line 96 says whether that still holds in 3.30 is not confirmed. Settle it once and make both files agree.
- **Endurance charges.** `charges.md` (PR #13) line 31 and `defences.md` (PR #20) line 122 both take PoB's model (elemental damage reduction per charge) against older guides' +4% resistances. Settle it once and make both files agree.

## Batch 1: mechanics (PRs #4 to #6, #12 to #20)

Files under `plugins/poe1-expert/skills/poe1-mechanics/references/`. Lines are on each PR's branch as of 2026-11-17.

| PR | File | Points to check |
|---|---|---|
| #4 | `damage.md` | Gem-level added damage effectiveness, the 3.25 change (line 69). The Arcane Might keyword, 3.29 (line 47). |
| #5 | `conversion.md` | Gained as extra taken from the amount before conversion and then converting again (PoB's model, not checked in game). Which stats count as skill conversion (lines 38 to 49). The 3.27 monster conversion rework (line 82 onward). No 3.26 to 3.30 change to the order, the 100% cap, or gained as extra (line 88). |
| #6 | `crit.md` | Crits and elemental ailments in 3.30 (line 96; see conflicts). 3.29 bifurcation wording and its ailment interaction (lines 63, 76). No second crit roll. Removal of the 5% and 95% caps in 3.6.0 (line 38). Resolute Technique unchanged (line 117). |
| #12 | `recovery.md` | Base mana regen 1.75% (line 29). ES recharge about 33% per second (line 97). ES leech cap 10% (lines 64, 65). Leech continuing after the target dies (line 72). Recoup on damage over time (line 90). Recovery rate scaling recoup and the leech cap (lines 92, 118). |
| #13 | `charges.md` | The endurance charge's elemental part (line 31; see conflicts). Sources of absorption, affliction, brutal, challenger, spirit, divinity, void, inspiration charges (table, lines 68 to 79). Any Blitz source left (lines 72, 102). Rage values (lines 84 to 88). |
| #14 | `flasks.md` | Separate life flask uses stacking (line 40). Flask effect scaling "during effect" mods (line 47). Tincture mana burn, cooldown, effect (lines 73, 75). |
| #15 | `minions.md` | Minion base resistances and the act penalty (lines 66 to 72). Summoning past the cap replacing the oldest, for every skill (lines 112, 113). |
| #16 | `auras-curses.md` | Marks using a curse slot (line 119). The boss curse-effect reduction (lines 131 to 133). The game's reservation rounding (line 65). Impending Doom and doom (line 128). Divine Blessing and aura effect (lines 86 to 89). |
| #17 | `totems-traps-mines.md` | Trap arm time (line 81). Base trap and mine limits (line 103). Which mines reserve mana (lines 100, 101). |
| #18 | `triggers.md` | Triggered spells costing no mana, per source (line 118). Cast when Damage Taken firing all linked spells (lines 37, 49). Cast on Melee Kill still in 3.30 (line 36). No energy-based meta gems in PoE1 3.30, stated as fact (lines 22 to 29). Trigger rotation for several spells (lines 96 to 100). |
| #19 | `ailments.md` | Scorch, brittle and sap coefficients (from PoB's code only; line 134). Whether a player's ailment threshold includes ES (line 105). Whether effect formulas use damage before or after mitigation. Bleed multipliers (left to the tools). The constants block (line 26). Crits and ailments (line 68; see conflicts). |
| #20 | `defences.md` | Endurance charges (line 122; see conflicts). A second accuracy check for enemy crits (line 76). The folded-in changes: 3.27 suppression to 40%, 3.28 Intelligence ES, 3.29 avoid-all adding to avoid-type. |

## Batch 2: build advisor (PRs #7 to #11)

Files under `plugins/poe1-expert/skills/poe1-build-advisor/references/`. Every threshold in these files is a community rule of thumb written from memory (life targets, chaos resistance bands, max hit, 40% to 50% crit chance). Patch notes cannot confirm those, so:

- Check only the **game facts** in them against the official notes (the list below).
- Mark each number plainly as a rule of thumb if it is not already, and leave it for the maintainer, who gives the numbers (#8 needs them most). Do not invent sources for them.
- Set `verification` no higher than `engine-checked`, and say in the PR comment which numbers wait for the maintainer.

| PR | File | Points to check |
|---|---|---|
| #7 | `diagnosis.md` | Chaos resistance guidance (lines 30, 31, 116). The life and ES checks (lines 35, 36). The MCP tool names and field names it uses (`list_warnings`, `list_fields`, `get_breakdown`, `resistance.cold`, `life`, `hit-dps`; lines 100 to 111) against Exiled Studio's `schemas/mcp-tools.v1.json`. |
| #8 | `defensive-thresholds.md` | The whole file's numbers, for the maintainer (line 15 says so). 3.28 uber fights needing 4 fragments, 3.30 Uber Atziri empowered skills below 66% life (line 66). |
| #9 | `gearing.md` | The folded-in changes: 3.28 Intelligence ES, Greater supports not working with their normal version (line 62), 3.30 scarab removal and Threads (line 76), 3.30 cluster jewel speed mods as one family (line 67). |
| #10 | `reading-breakdowns.md` | Field and tool names against Exiled Studio's MCP contract and the calc result schema (`schemas/calc-result.v1.schema.json`). |
| #11 | `trade-offs.md` | The crit chance rule of thumb (line 42) and any other numbers, marked as rules of thumb. |

## Batch 3: community (PRs #21 to #25)

Files under `plugins/poe1-expert/skills/poe1-community/references/`. The 3.28 notes were read on pathofexile.com; 3.30 through a copy; 3.26, 3.27, 3.29 through poedb. The scarab removal (Threads replace scarabs) agrees with poe.ninja's empty Scarab overview.

| PR | File | Points to check |
|---|---|---|
| #21 | `jargon.md` | Terms that name removed or renamed content (scarabs, anything 3.26 to 3.30 removed). |
| #22 | `archetypes.md` | The 3.29 self-cast changes (line 26) and the 3.29 totem and mine support nerfs (line 47), both from third-party summaries. |
| #23 | `budget-tiers.md` | Prices or items that 3.30 removed or changed; cross-check with the economy snapshot in PR #2. |
| #24 | `crafting.md` | Eldritch implicits and currency (lines 105 to 112). Resonators (lines 56, 57). The Harvest reforge list and the 3.30 Harvest rework (lines 59 to 65). Old meta-crafts next to the new bench locks (line 93). Foulborn orbs (line 116). Influence and awakener crafts (line 122). Bench lock costs (the summary gave two figures, so none are given). Fossil supply (line 54). |
| #25 | `atlas.md` | Fossil supply after Delve clusters left. The Phantom Anomalies keystone (line 53). The folded-in 3.30 atlas changes: tree from the centre, 150 points, Atlas Drops, Threads, item tiers, core mechanics no longer spawning on their own. |

## Meta summaries (Q11)

Separate from the batches: a session with the poe.ninja builds page open in Chrome writes each snapshot's meta and popularity summary (top ascendancies and skills, their trend, the main archetypes), on the snapshot's PR, and the maintainer approves it. It reads the page only; no unsupported endpoints.
