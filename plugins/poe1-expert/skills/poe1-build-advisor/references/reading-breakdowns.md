---
game: poe1
patch: 3.30.0
as_of: 2026-11-17
sources:
  - https://www.pathofexile.com/forum/view-thread/3913392
  - https://www.pathofexile.com/forum/view-thread/4013680
  - https://github.com/PathOfBuildingCommunity/PathOfBuilding/blob/v2.67.2/src/Modules/CalcOffence.lua
  - https://github.com/PathOfBuildingCommunity/PathOfBuilding/blob/v2.67.2/src/Modules/CalcDefence.lua
  - repo:DBAggie/exiled-studio/schemas/mcp-tools.v1.json
  - repo:DBAggie/exiled-studio/schemas/calc-result.v1.schema.json
  - repo:DBAggie/exiled-studio/docs/parity/divergence-register.json
verification: maintainer-approved
---

# Reading a calculation breakdown

How to read a damage or defence breakdown in Exiled Studio or Path of Building (PoB), and how to explain one to a player. The formulas are long-standing PoE1 rules; they were checked against Path of Building 2.67.2 on 2026-11-17, and no official 3.26 to 3.30 note changes them. The mechanics references (`poe1-mechanics`) hold the detail.

PoE2 differs (for example its accuracy and armour rules); do not apply this there.

## The shape of a hit
For a hit, the game builds damage in this order:

```
1. base damage (gem base for spells, weapon base for attacks)
2. + added flat damage x damage effectiveness (of the skill)
3. conversion and "gained as extra" (per damage type)
4. x (1 + sum of all increased and reduced, as one number)
5. x product of every more and less multiplier, each on its own
6. critical strike (if it crits)
7. enemy side: resistance, penetration, armour, damage taken
```

Key points for the player:
- **Increased and reduced add together.** 50% increased and 30% increased make 80% increased, a 1.8 multiplier.
- **More and less multiply.** 30% more and 20% more make 1.3 x 1.2 = 1.56.
- That is why "more" multipliers grow in value as "increased" stacks up.

## Conversion
- Damage converts in a fixed order: physical, then lightning, then cold, then fire, then chaos. It never converts backwards.
- Converted damage benefits from modifiers to every type it has been. Physical converted to cold is scaled by physical and by cold modifiers.
- "Gained as extra" adds damage of another type and leaves the original.
- If conversion from one type totals more than 100%, the game scales it down to 100%.

## Critical strikes
```
average hit = non-crit hit x (1 - crit chance) + crit hit x crit chance
crit hit    = non-crit hit x crit multiplier
```
- Crit chance caps at 100%. Base crit comes from the gem (spells) or weapon (attacks).
- For attacks, a crit must pass the accuracy check a second time, so the shown crit chance is already multiplied by hit chance.
- A breakdown shows base crit, increased crit, and the final chance. Check the final.

## Rate and DPS
```
hit DPS = average hit x hits per second x hit chance (attacks only)
```
- Cast or attack rate: base time from the gem or weapon, then increased speed (additive), then more or less.
- Exiled Studio floors a weapon's own attack time in milliseconds, as the game does (a game-truth difference from PoB, registered in the app's divergence register).

## Hit chance (attacks)
```
hit chance = 1.25 x accuracy / (accuracy + (enemy evasion x 0.2) ^ 0.9)
```
- Clamped between 5% and 100%. Spells always hit unless the enemy has a specific avoidance.
- An attack build with a low hit chance loses DPS on every hit.

## Enemy resistance and penetration
```
effective resistance = enemy resistance after curses and exposure, then minus penetration
damage taken         = damage x (1 - effective resistance)
```
- Curses and exposure lower the resistance itself; this can go below zero.
- Penetration applies only to hits and only when you deal the hit. It does not affect damage over time.
- The default enemy matters. Exiled Studio and PoB both let the user set the enemy (resistances, level, boss type) in the configuration. A low default resistance makes DPS look higher than against a boss. Always say which enemy the number is for.

## Armour (enemy and player)
```
physical damage reduction = armour / (armour + 5 x raw hit damage)
```
Capped at 90%. Bigger hits get less reduction.

## Defence fields
- **Resistances**: the breakdown shows the total from all sources and the capped value. The capped value is what counts; the total minus the cap is over-cap.
- **Life and ES**: base from level and attributes, then flat additions, then increased (additive), then more. 3.28 halved ES from Intelligence (1% increased per 10 Intelligence; 3.28.0 notes).
- **Block, suppression**: chance from sources, then the cap.

## Reading Exiled Studio breakdowns
- Each field has a **state**:
  - `complete`: the value is the full calculation.
  - `partial`: the value is computed, but some inputs are not modelled. The breakdown names what is missing. Treat the number as a floor or a rough value and say so.
  - `unsupported`: the app has no calculation for this. There is no value. Never read it as zero.
  - `indeterminate`: the value cannot be settled (for example a choice the build does not make). There is no single value.
  - `not-computed`: the field has no value. Never read it as zero.
- `get_breakdown` returns the field and the graph of nodes it depends on. Each contribution names its source: an item line, a passive, a gem, the config, a custom modifier.
- Unread item lines (`list_warnings`) never count. If a line is missing, the field is lower than the game shows.

## Reading PoB breakdowns
- The sidebar shows totals. The Calcs tab shows each section; hover a value to see its breakdown and its sources.
- PoB also has a configuration tab for the enemy and conditions. Check it before trusting DPS.
- PoB is the pinned regression oracle for Exiled Studio. A difference between the two needs a reason (a registered divergence, a missing input, an unread line).

## Explaining a breakdown to a player
1. Start with the result: "your hit DPS against this enemy is X" (quoted from the tool).
2. Name the two or three biggest multipliers and where each comes from.
3. Show the weak part: low base, few more multipliers, low hit chance, high enemy resistance.
4. Give one change and its measured effect (`preview_item_edit` or `preview_tree_change`).
5. Avoid jargon or define it once: "increased adds up; more multiplies".

## Tools to call

When the Exiled Studio app MCP is reachable:

1. `get_build`: calc status. If not complete, say which fields are partial.
2. `list_fields`: field names, values, and states.
3. `get_breakdown` with the field name exactly as `list_fields` gives it (for example `life`, `resistance.fire`, `hit-dps`). Walk the nodes from the result down to the sources.
4. `list_warnings` and `get_item`: lines that did not count.
5. `preview_item_edit` or `preview_tree_change` to show what a change does to the field.
6. `get_tree_node` or `find_tree_nodes` to name a passive source.

Rules:
- When the app is reachable, every number is checked with `get_breakdown` or `preview_item_edit` first.
- When it is not, label each number an estimate and say how to check it.
- A field in state `unsupported`, `indeterminate`, or `not-computed` is never read as zero.

## Common mistakes
- Multiplying "increased" modifiers together instead of adding them.
- Adding "more" modifiers together instead of multiplying them.
- Forgetting converted damage keeps the earlier type's modifiers.
- Applying penetration to damage over time.
- Quoting DPS without saying which enemy it was against.
- Reading `partial` as `complete`, or `unsupported` as zero.
- Treating a PoB and Exiled Studio difference as a bug without checking the divergence register and warnings.

## Verification (2026-11-17)

`engine-checked` here means: the tool names against Exiled Studio's `schemas/mcp-tools.v1.json`; the five field states (`complete`, `partial`, `unsupported`, `indeterminate`, `not-computed`) and the example field names against `schemas/calc-result.v1.schema.json`; the attack-time flooring against `docs/parity/divergence-register.json` (dev branch, 2026-11-17); the formulas against Path of Building 2.67.2.

Approved by the maintainer on 2026-11-17 (given in chat, recorded by the session). The checks named above are what was done before approval; nothing here was checked in game unless a line says so.
