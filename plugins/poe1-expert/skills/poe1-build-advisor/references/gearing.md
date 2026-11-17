---
game: poe1
patch: 3.30.0
league: Covens of Umbra
as_of: 2026-11-17
sources:
  - https://www.pathofexile.com/forum/view-thread/4013680
  - https://www.pathofexile.com/forum/view-thread/3913392
  - repo:DBAggie/exiled-studio/schemas/mcp-tools.v1.json
verification: maintainer-approved
---

# Gearing progression and upgrade order

This is a general plan for gearing a PoE1 character from the campaign into the endgame. It is a common community approach, not a game rule. Specific bases, uniques, and mod values come from the knowledge MCP at answer time, never from this file.

## The order
1. **Cap elemental resistances and get enough life (or ES)** for the current content (`defensive-thresholds.md`).
2. **Fix ailment holes** with flasks, then gear or passives.
3. **Main skill links**: a 4-link early, then a 5-link, then a 6-link.
4. **Damage**: weapon (attacks) or flat added damage and gem levels (spells), then damage multipliers.
5. **Chaos resistance and extra layers** (armour, evasion, block, suppression) as content gets harder.
6. **Jewels**: life and resistances first, then damage or a specific notable.
7. **Cluster jewels and build-defining uniques**, when the build depends on them.

Go back to step 1 every time a new item changes the resistance totals. Swapping a ring often drops a resistance below cap.

## Campaign
- Wear anything with life and resistances. Movement speed boots matter a lot.
- Attack builds: replace the weapon often. A good leveling weapon is the biggest single damage gain.
- Spell builds: items with "+ level to gems" or added spell damage, plus gem levels.
- Keep links: buy or craft a 4-link chest or helmet for the main skill.
- Use the crafting bench on open affixes for life and resistances.

## Early maps
- Every armour slot and jewellery slot should carry life (or ES) and at least one resistance.
- A 5-link for the main skill.
- A weapon or gear set that kills white and yellow maps comfortably.
- Flasks: one life flask with a useful suffix, utility flasks with ailment removal.

## Red maps and bosses
- Rares with high life and two or three resistances, open affixes crafted.
- A 6-link for the main skill, or a strong 5-link with a better weapon.
- Chaos resistance on gear.
- Jewels with life and damage or defence mods; a watcher's eye or other build-defining jewels for richer builds.
- Cluster jewels if the build uses them (see below).

## What to look for per slot (general)
- **Weapon (attacks)**: base physical or elemental damage, attack speed, crit chance for crit builds. This is the build's floor.
- **Weapon (spells)**: added spell damage, "+ level" to gems, spell damage, cast speed, crit for crit spells.
- **Shield or offhand**: block, life, resistances, or spell modifiers depending on the build.
- **Body armour**: the item most often carrying the 6-link. Life or ES, and the defence type the build uses.
- **Helmet, gloves, boots**: life and resistances. Boots: movement speed. Gloves: attack speed or added damage for attacks. Helmets and gloves often carry enchantments or special implicits.
- **Amulet**: life, resistances, and the build's main stat or damage line ("+ level" for spells, crit multiplier, and so on). Anointments go here.
- **Rings**: life, resistances, attributes, added flat damage for attacks.
- **Belt**: life, resistances, flask modifiers.
- **Flasks**: the right suffixes matter more than the base. Instant recovery or bleed removal on life flasks; freeze or ailment removal on utility flasks.
- **Jewels**: life percent plus damage, or resistances when gear is short.

## Links: 5L and 6L
- A support in the main skill's link is often worth 20% to 40% more damage (a rule of thumb; the real value is the support's own numbers). Going from 5 to 6 links is one of the largest single damage steps.
- Before buying a 6-link, check the 5-link has the right supports. A wrong support in a 6-link is a waste.
- 3.28: a Greater support and its normal version do not work together; the Greater wins (3.28.0 notes).

## Jewels and cluster jewels
- Regular jewels: cheap life and resistances, or damage, in tree sockets. Good value early.
- Cluster jewels: large, medium, and small types in outer sockets; they add notables and small passives. Good when the right notables exist for the build, but expensive to roll and path to. Build guides usually name the notables.
- 3.30: cluster jewel modifiers whose small passives also grant attack speed and/or cast speed are now one mod family, so one jewel cannot roll several of them (3.30.0 notes; before, only a Refracting Fog could do it).

## Upgrade decisions
- Measure each upgrade, do not guess. Compare the item's effect on DPS and defences in Exiled Studio or PoB before buying.
- A cheap upgrade that fixes a resistance hole is worth more than an expensive damage item while the player still dies.
- On trade, filter for life plus total resistances plus open affixes. In SSF, plan crafting around the bench and essences.

## League and economy notes
- Prices and availability come from `poe1-economy` with its `as_of` date and league. Never quote prices from memory.
- 3.30: scarabs were removed and replaced with Threads, and ten league mechanics no longer spawn in maps on their own (3.30.0 notes). Older farming plans that paid for gear no longer apply as written.
- 3.30: Orbs of Chance are much rarer and no longer sold by vendors, Orbs of Binding no longer drop, and rare and magic items can now drop with an Item Tier that raises their modifier tiers (3.30.0 notes). Old vendor and currency habits may not hold.

## Tools to call

When the Exiled Studio app MCP is reachable:

1. `get_build` and `list_warnings`: what is equipped and which lines the app did not read.
2. `list_items`: all slots. Note empty slots and items with warnings.
3. `get_item` on each candidate slot: lines, open affixes, resolved stats.
4. `list_fields` then `get_breakdown` on the resistance, life, and damage fields to see what each item contributes.
5. `preview_item_edit` for each suggested change (a crafted line, a replaced line). It needs the current line text from `get_item` in `expect`. Quote its before and after.
6. `get_tree`, `find_tree_nodes`, `get_tree_node`, `preview_tree_change` when a jewel socket or passive is part of the plan.
7. `request_item_edit` only when the player asks to apply a change.

Rules:
- When the app is reachable, every number is checked with `get_breakdown` or `preview_item_edit` first.
- When it is not, label each number an estimate and say how to check it.
- A field in state `unsupported`, `indeterminate`, or `not-computed` is never read as zero. If an upgrade's effect sits in such a field, say the app cannot show it yet.

## Common mistakes
- Buying damage while resistances are uncapped.
- Upgrading one slot and losing a resistance cap without noticing.
- Buying a 6-link before checking the supports.
- Ignoring flasks, which are the cheapest defence upgrade.
- Listing specific mod values or unique stats from memory instead of the knowledge MCP.
- Recommending cluster jewels to a low-budget build that has no use for their notables.

## Verification (2026-11-17)

`engine-checked` here means: the folded-in game facts (the 3.28.0 Greater support rule and Intelligence ES; the 3.30.0 scarab removal and Threads, cluster jewel speed mods as one family, Orb of Chance and Item Tier changes) were checked against the official notes, and the tool names and the `expect` argument of `preview_item_edit` against Exiled Studio's `schemas/mcp-tools.v1.json`. The upgrade order itself is community advice, not a game rule.

Approved by the maintainer on 2026-11-17 (given in chat, recorded by the session). The checks named above are what was done before approval; nothing here was checked in game unless a line says so.
