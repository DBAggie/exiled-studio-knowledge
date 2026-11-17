---
game: poe1
patch: 3.30.0
league: Covens of Umbra
as_of: 2026-11-17
sources:
  - https://www.pathofexile.com/forum/view-thread/4013680
  - https://www.pathofexile.com/forum/view-thread/3913392
  - https://github.com/PathOfBuildingCommunity/PathOfBuilding/blob/v2.67.2/src/Modules/CalcSetup.lua
  - https://www.poewiki.net/wiki/Energy_shield
  - repo:DBAggie/exiled-studio/schemas/mcp-tools.v1.json
  - repo:DBAggie/exiled-studio/schemas/calc-result.v1.schema.json
verification: engine-checked
---

# Diagnosis checklist

Use this when a player asks "why do I die" or "why is my damage low". Work top to bottom. Stop at the first clear problem, fix it, then look again. Most characters have one or two big holes, not ten small ones.

## Before you start
- Get the build: Exiled Studio open (app MCP), a PoB code, or a full description.
- Ask what content they run (campaign act, map tier, which boss), their league (softcore or hardcore, trade or SSF) and their budget.
- Ask how they die: one big hit, slow drain, a specific boss skill, frozen or stunned, degen ground. The answer points to the hole.
- Ask what the damage problem looks like: bosses take forever, or packs survive, or both.

## "Why do I die": check in this order

### 1. Elemental resistances
- Fire, cold and lightning should each be at their maximum (75% by default) for the content. After the campaign the player has a -60% penalty in total (-30% after Act 5 and -30% after Act 10; PoB 2.67.2 applies the same penalty, and no 3.26 to 3.30 note changes it).
- One uncapped resistance is the most common cause of sudden deaths. 60% instead of 75% means taking 40% instead of 25% of the hit: 60% more damage from that element.
- Check the shown value, not the total before the cap. Over-capping (total above the maximum) is a buffer against curses and map mods that lower resistances.

### 2. Chaos resistance
- Negative chaos resistance makes chaos damage hurt more than the hit shows. Many endgame bosses and degens deal chaos. Chaos damage also bypasses energy shield by default, so an ES pool does not cover it.
- Exception: Chaos Inoculation (CI) characters ignore this, since chaos damage cannot reach them that way.

### 3. Pool size
- Life (or energy shield, or the mix) too low for the tier. Compare with `defensive-thresholds.md`.
- Check that the "increased maximum life" total is reasonable for the stage. A mid-map character with very little increased life is common.

### 4. Ailments
- Freeze, stun, and shock cause most "I could not move and died" reports.
- Look for: a freeze answer (immunity, avoidance, or a flask), a bleed and corrupted blood answer (a flask with the right suffix, or immunity), and a shock answer for red maps.
- 3.30: the Master Alchemist ascendancy notable's ailment removal on flask use now covers all ailments, not only elemental ones (3.30.0 notes). Look such notables up through the knowledge MCP; do not rely on memory.

### 5. Flasks and uptime
- Are utility flasks used at all? Are they kept running (charge gain, duration, or a utility that automates them)?
- A life flask with no instant or bleed-removal suffix is a wasted slot in maps.

### 6. Missing layers
- No armour or evasion at all, no block, no spell suppression on a dex build, no guard skill, no movement skill to dodge.
- No defensive aura or buff where the build has spare mana or life to reserve.
- No curse on the enemy where the build could fit one cheaply.
- Pantheon not set, or not upgraded. Pantheon choices are free and often fix a specific death (for example a freeze or bleed problem).

### 7. Mechanics, not numbers
- Some deaths are from mechanics the player must dodge (boss slams, ground effects). Ask before buying gear.
- Map mods: reflect, no regeneration, less recovery, reduced maximum resistances. Since 3.30.0 a corruption can add 2 explicit mods to a map, up to 9 in total, so read them.

## "Why is my damage low": check in this order

### 1. The main skill links
- Is the main skill in the item with the most links? Does it have its right supports?
- Wrong supports are common: a support that does not apply (for example an attack support on a spell), two supports that scale the same thing, a support for a damage type the skill no longer deals after conversion.
- 3.28: a Greater support and its normal version no longer stack; the Greater one wins (3.28.0 notes). Two of them in one link wastes a socket.

### 2. Gem levels and quality
- A low-level main skill gem loses a large share of damage. Check level and quality early.

### 3. Damage multipliers
- "More" multipliers come from supports, some keystones, curses, exposure, and some ascendancy nodes. A build with only "increased" damage scales poorly.
- Look for missing: a curse, an exposure source, a damage aura or herald, a shock or chill effect the build could apply.

### 4. Enemy resistance and penetration
- Elemental builds without penetration, exposure, or curses lose a lot on bosses with high resistances.

### 5. Weapon or base damage
- Attack builds: the weapon's base damage and attack speed set the floor. A weak weapon caps everything else.
- Spell builds: added flat damage from gear, and gem level.

### 6. Hit chance and crit
- Attack builds with low accuracy miss. Check hit chance in the breakdown.
- Crit builds with low crit chance get little from multiplier. Non-crit builds often waste points on crit.

### 7. Rate
- Attack or cast speed too low makes clear feel slow even with high average hit.

## Ranking fixes by cost
Order every suggestion this way and say which tier each fix is in.

1. **Free**: gem swaps and link order, flask choice and setup, pantheon, mastery choices, aura and curse choices, a few passive respecs, the bench craft on an open affix (cheap currency).
2. **Cheap**: crafting resistances or life on gear with an open affix, a better flask, buying a base-level gem, a jewel with life and resistances.
3. **Moderate**: replacing a weak item (rare with life and two resistances), a 5-link, a better weapon.
4. **Expensive**: 6-link, key uniques, high-end rares, cluster jewels with the right notables.

Fix defence holes before damage if the player dies; a dead character deals no damage. Fix the cheapest large gain first.

## Tools to call

When the Exiled Studio app MCP is reachable:

1. `get_build`: class, level, main skill, calc status, warning counts. If the calc status is not complete, say so before any verdict.
2. `list_warnings`: item lines the app could not read. A missing life or resistance line changes the diagnosis.
3. `list_fields`: every computed field and its state. Find life, energy shield, each resistance, block, suppression, hit DPS, hit chance, and the like.
4. `get_breakdown` on each field you plan to talk about (for example `resistance.cold`, `life`, `hit-dps`). Quote its number and name its biggest sources.
5. `list_items` and `get_item` to find open affixes or weak slots.
6. `preview_item_edit` to show the effect of a suggested item change before you claim it. `get_tree`, `find_tree_nodes`, `get_tree_node`, then `preview_tree_change` for a passive change.
7. `request_item_edit` only when the player asks you to apply a change; they approve it in the app.

Rules:
- When the app is reachable, every number is checked with `get_breakdown` or `preview_item_edit` (or `preview_tree_change`) first. Quote the tool, not your own math.
- When it is not reachable, label each number an estimate and say how to check it (Exiled Studio or Path of Building).
- A field in state `unsupported`, `indeterminate`, or `not-computed` (no value) is never zero. Say the app does not compute it yet.
- If `list_fields` has no field for a quantity (for example a max hit or an ailment DPS), the app does not report it. Do not invent one.

## Common mistakes
- Suggesting damage upgrades to a player who dies to one hit.
- Reading resistance totals before the cap, or forgetting the campaign penalty.
- Treating negative chaos resistance as fine on a non-CI build.
- Calling a field with no value "0 DPS" or "0 life".
- Blaming numbers for a mechanic death (an undodged boss slam).
- Recommending expensive items when a free respec or flask fix covers it.
- Assuming Greater and normal versions of a support stack (changed in 3.28).

## Verification (2026-11-17)

`engine-checked` here means: the game facts (campaign penalty, the 3.28.0 Greater support rule, the 3.30.0 Master Alchemist and map corruption changes) were checked against the official notes and Path of Building 2.67.2, and every tool name, field name and field state against Exiled Studio's `schemas/mcp-tools.v1.json` and `schemas/calc-result.v1.schema.json` (dev branch, 2026-11-17). The check order and the cost tiers are advice, not game rules.
