---
game: poe1
patch: 3.30.0
league: Covens of Umbra
as_of: 2026-11-17
sources:
  - https://www.pathofexile.com/forum/view-thread/3913392
  - https://www.pathofexile.com/forum/view-thread/4013680
  - https://www.poewiki.net/wiki/Energy_shield
  - repo:DBAggie/exiled-studio/schemas/mcp-tools.v1.json
verification: maintainer-approved
---

# Common trade-offs

Build choices rarely have one right answer. For each trade-off below: what is traded, and how to decide for this player. Always tie the decision to their content, budget, league, and play style. Measure the options with the app when it is reachable.

## Damage versus defence
- **The trade**: passive points, item affixes, and link slots go to damage or to survival.
- **How to decide**:
  - If the player dies in the content they want, defence first until deaths stop. A dead character deals no damage.
  - If they survive but kill slowly, damage next.
  - Check against the tier's rule-of-thumb lines (`defensive-thresholds.md`). Below the line: defence. Well above: move points to damage.
  - Hardcore: lean defence. Softcore farming: a little more damage often earns more per hour.
- Show both: a passive change's effect on DPS and on life or resistances in one `preview_tree_change`.

## Life versus energy shield (and hybrid)
- **Life**: works with most defences, gear is cheap, recovers through leech, regeneration, and flasks.
- **Energy shield**: recharges on its own after a delay, scales from Intelligence-based gear, pairs with Chaos Inoculation (chaos immunity at the cost of life set to 1). Without it, chaos damage bypasses energy shield by default.
- **Hybrid**: both pools; needs gear with both, more expensive.
- **How to decide**:
  - Follow the class and the build's keystones. Do not mix half-heartedly.
  - Budget: life is usually cheaper to start.
  - Content with constant damage (degens) hurts ES recharge more than life.
  - 3.28: Intelligence's built-in ES bonus was halved (1% increased per 10 Intelligence; 3.28.0 notes). Older ES-stacking plans give less now; measure, do not assume.
- PoE2 differs; do not apply this there.

## Crit versus non-crit
- **Crit**: needs base crit (skill or weapon), crit chance, and crit multiplier. Strong scaling, high cost, and needs accuracy for attacks.
- **Non-crit**: points go to flat damage, more multipliers, and defence. Often uses a keystone that gives up crits for a benefit (for example Resolute Technique on attacks, or Elemental Overload for elemental crits at low chance).
- **How to decide**:
  - Low-base-crit skills and low budgets: non-crit.
  - High-base-crit skills with a budget for crit gear: crit.
  - Check the crit chance field. Below about 40% to 50% chance, crit multiplier gives little. This line is a rule of thumb.
  - Non-crit builds should not invest in crit; crit builds should not ignore accuracy.

## Clear versus bossing
- **Clear**: area, projectiles, chains, movement, on-kill effects.
- **Bossing**: single-target multipliers, penetration, curses, sustained uptime.
- **How to decide**:
  - Ask what they want to farm. Mapping builds need clear; boss farmers need single target.
  - Swap gems or a weapon for a boss (a "boss setup") when it is cheap.
  - Compare the main skill's DPS against a boss enemy (set in the configuration) and a normal one.

## Budget versus ceiling
- **Budget builds**: work with cheap rares and few key items. Low ceiling.
- **High-ceiling builds**: scale with expensive uniques, cluster jewels, or rare craft lines; weak until funded.
- **How to decide**:
  - Ask the budget and league. SSF and new leagues favour budget builds.
  - A build that "starts at 50 divines" is not a starter (the figure is only an illustration).
  - Prices come from `poe1-economy` with its `as_of` date. Never from memory.

## Links: which skills get the best links
- **The trade**: the 6-link goes to the main damage skill; 4-links to utilities (curse, guard, movement, auras).
- **How to decide**:
  - Main skill gets the most links. Single-target and clear setups can share links with gem swaps.
  - A 5-link with the right supports beats a 6-link with a wrong one.
  - 3.28: a Greater support does not stack with its normal version (3.28.0 notes).

## Reservation: auras and heralds versus mana or life
- **The trade**: reserved mana or life cannot be spent; more auras mean less pool or less skill-cost room.
- **How to decide**: reserve when the build has the efficiency for it; check the unreserved mana and life fields after a change.

## Flask uptime versus slot choice
- **The trade**: flask slots (or tinctures for some builds) compete with each other.
- **How to decide**: cover ailments first, then the build's damage or defence flasks. Keep at least one recovery answer.

## Speed versus safety
- Movement speed and cast speed feel good; they also let the player dodge. Slow tanky builds survive hits, fast builds avoid them. Ask how the player plays.

## Tools to call

When the Exiled Studio app MCP is reachable:

1. `get_build`: class, main skill, calc status.
2. `list_warnings`: anything that skews the comparison.
3. `list_fields`, then `get_breakdown` on the fields each side of the trade-off touches (damage fields and defence fields).
4. Option A and option B each through `preview_item_edit` (item lines) or `preview_tree_change` (passives, masteries). Use `get_item`, `get_tree`, `find_tree_nodes`, and `get_tree_node` to build the change.
5. Present the before and after for both options side by side. Let the player pick.
6. `request_item_edit` only when the player asks to apply the chosen option.

Rules:
- When the app is reachable, every number is checked with `get_breakdown` or `preview_item_edit` (or `preview_tree_change`) first.
- When it is not, label each number an estimate and say how to check it.
- A field in state `unsupported`, `indeterminate`, or `not-computed` is never read as zero. If one side of the trade-off sits in such a field, say the app cannot measure that side yet.

## Common mistakes
- Giving one answer without asking about content, budget, and league.
- Recommending crit to a skill with low base crit on a low budget.
- Moving a life build to ES (or the reverse) for a small gain; it costs a full regear.
- Calling a build "better" from one number (DPS) and ignoring defence.
- Using old Intelligence-to-ES assumptions after 3.28.
- Quoting prices or meta from memory.

## Verification (2026-11-17)

`engine-checked` here means: the game facts (the 3.28.0 Intelligence ES and Greater support rules, chaos damage and energy shield, tinctures using flask slots) were checked against the official notes and poewiki, and the tool names against Exiled Studio's `schemas/mcp-tools.v1.json`. The crit chance line (about 40% to 50%) is a rule of thumb and is marked so; it waits for the maintainer. The rest is advice, not game rules.

Approved by the maintainer on 2026-11-17 (given in chat, recorded by the session). The checks named above are what was done before approval; nothing here was checked in game unless a line says so.
