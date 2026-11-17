---
game: poe1
patch: 3.30.0
league: Covens of Umbra
as_of: 2026-11-17
sources:
  - https://www.pathofexile.com/forum/view-thread/4013680
  - https://www.pathofexile.com/forum/view-thread/3913392
  - https://www.pathofexile.com/forum/view-thread/3869068
  - https://github.com/PathOfBuildingCommunity/PathOfBuilding/blob/v2.67.2/src/Modules/Data.lua
  - https://github.com/PathOfBuildingCommunity/PathOfBuilding/blob/v2.67.2/src/Modules/CalcDefence.lua
  - repo:DBAggie/exiled-studio/schemas/mcp-tools.v1.json
  - https://poe.ninja/poe1/builds/covens
verification: unverified
---

# Defensive thresholds by content tier

**Every number in this file is a community rule of thumb, not a game rule.** The game has no "required" life or resistance for any content. These ranges are what players commonly aim for so a typical build survives with ordinary play. Skilled players go lower; hardcore players go higher. Treat each number as a starting point and say so to the player.

Only the caps are game rules: elemental and chaos resistances default to a 75% maximum, raised by specific modifiers up to a hard cap of 90%. Block caps at 75% by default (raisable to 90%). Spell suppression chance caps at 100%.

PoE2 differs; do not apply this there.

## How to use the tiers
- Find the player's content, read the row, compare with the build.
- A build below a line is not "wrong". It has a risk to name.
- Layers matter more than one number. A build with average life and four layers often beats a build with huge life and none.
- League and mode change the bar: hardcore players take conservative numbers for safety (a simple way is to use the next tier's); SSF players often run lower while gearing.
- **Which tier is the player in?** Character level is a fair guide (maintainer, 2026-11-17): level 69 to 75 is usually white to yellow maps; pinnacle bosses start around level 80 to 85; above level 88 is usually red maps.
- **Pools differ by build.** Some builds top out on life and put the rest into energy shield or evasion. An ES build may have much less life and much more ES; compare the pool the build actually uses, and its layers, not life alone.

## What ladder characters actually had (Covens, league day 4)

Read from the poe.ninja builds page on 2026-11-17 (softcore trade, the first 100 characters shown at each level). These are observations, not targets: it was early in the league, and such characters are still gearing.

| Level | Likely content | Life, middle half | Life + ES, median |
|---|---|---|---|
| 75 | white to yellow maps | 2,500 to 3,400 | about 3,200 |
| 85 | pinnacle bosses begin | 3,000 to 4,000 | about 3,900 |
| 90 | red maps | 3,000 to 4,300 | about 4,200 |
| 95 | red maps and bosses | 2,900 to 4,800 | about 4,800 |

The life targets below sit above these figures. Treat the targets as where a build is comfortable and the table as where many players are early in a league. Later in a league, pools are higher.

## Campaign (Acts 1 to 10)
- **Resistances**: try to cap fire, cold and lightning after the Act 5 penalty (-30%) and again after Act 10 (another -30%, -60% in total). Many players are below cap mid-act; aim to be capped entering Act 6 and entering maps.
- **Chaos resistance**: anything is fine; negative is normal.
- **Life**: aim for life to go up by about 400 to 500 per act, give or take (maintainer, 2026-11-17). That is roughly 2,000 to 2,500 by the end of Act 5 and 4,000 to 5,000 by the end of Act 10 for a life build. ES builds may carry less life and more ES.
- **Ailments**: a flask with freeze or bleed removal helps; not required.
- **Movement**: a movement skill and a quicksilver flask help more than any number.

## Early maps (white and yellow tiers)
- **Resistances**: elemental at 75% each. Chaos at least near 0%.
- **Life**: around 3,500 to 4,500, or the ES equivalent.
- **Max hit**: no fixed number; it depends on the build and its layers. Scaling the red-map figure down by the life targets gives roughly 5,000 to 7,000 per element as an estimate.
- **Ailments**: one answer to freeze and one to bleed (flask suffixes are fine).
- **Layers**: at least one of armour, evasion, block, or spell suppression scaled on purpose. A guard skill if one fits.
- **Flasks**: very build dependent; a life flask with an instant or bleed-removal suffix and usually two utility flasks.

## Red maps (tiers 14 to 16, light juice)
- **Resistances**: elemental 75% each with some over-cap. Chaos 20% to 40% or more.
- **Life**: around 5,000 to 6,000, or the ES equivalent.
- **Ailments**: freeze immunity or near-total avoidance. Shock and stun answers become important. Bleed and corrupted blood handled.
- **Spell suppression**: not every build has it. A build that is working toward suppression should aim for 100% chance; below that, every unsuppressed spell hit is a surprise.
- **Block**: not every build has it. A build that uses block should aim for the default cap on attack block, and some for spell block too.
- **Max hit**: depends on the build and which layers it has; there is no one number. As a rough guide players aim several thousand per element above their life pool (for example 7,000 to 10,000).
- **Recovery**: a reliable leech, regeneration, or recoup source.
- 3.30: a corruption can add 2 explicit mods to a map, up to 9 in total (3.30.0 notes). Map mods that lower maximum resistances or reduce recovery make these lines worse; read the mods.
- 3.28: Voidstones raise the minimum map tier in their Atlas quadrant (3.28.0 notes). Players reach red maps sooner, often before their defences are ready.

## Pinnacle bosses (Shaper, Elder, Sirus, Maven, Eater of Worlds, Searing Exarch, and similar)
- **Resistances**: elemental 75% minimum; many players add maximum resistance (76% to 80%) for elemental-heavy bosses. Chaos 40% to 75% for chaos-heavy fights.
- **Life**: around 6,000 or more, or the ES equivalent.
- **Max hit**: build dependent; often cited around 10,000 or more per damage type.
- **Ailments**: freeze and stun handled; curse effect reduced or cleansed helps.
- **Recovery**: flasks, leech, or regeneration enough to recover between big hits.
- 3.30: in Deified areas (a map with a Divine Vessel applied) map bosses get 25% increased damage, 25% increased attack and cast speed and 100% increased toughness; the Cortex bosses now show as pinnacle Atlas bosses (3.30.0 notes). Check the boss in question through the knowledge MCP.

## Uber pinnacle bosses
- **Resistances**: capped, often with raised maximums. Chaos often 75% for some fights.
- **Life**: 7,000 to 10,000 or the ES equivalent is a common bar. Deep-defence builds go much higher.
- **Max hit**: build dependent; values above 15,000 for the main damage types are commonly cited. Treat as rough; it depends on which boss.
- **Ailments**: full freeze, stun, and shock answers.
- **Damage**: uber fights need enough damage to end phases before the arena fills. A too-defensive build can fail on timers.
- 3.28: uber fights need 4 fragments instead of 5 (3.28.0 notes). 3.30: Atziri moved to the Temple of Atzoatl; she and Uber Atziri use empowered abilities below 66% life, and the fight can no longer be paused (3.30.0 notes). Specific boss numbers change by patch; nothing beyond these notes was checked.

## What each defence does, briefly
- **Resistances**: reduce elemental and chaos hits and damage over time by the shown percent.
- **Armour**: reduces physical hits. Big against small hits, weak against huge hits:

```
damage reduction = armour / (armour + 5 x raw hit damage)
```

  The reduction caps at 90%. A hit 10 times the armour value gets about 2% reduction.
- **Chaos damage** bypasses energy shield by default, so chaos resistance matters more for ES builds without Chaos Inoculation.
- **Evasion**: chance to avoid attacks entirely. Does not stop spells.
- **Block**: chance to block hits (attack block, spell block). Blocked hits deal no damage unless a modifier says otherwise.
- **Spell suppression**: suppressed spell hits deal less damage (40% prevented by default since 3.27.0; it was 50%). It does not stop the hit.
- **Max hit**: the biggest single hit of one type the character survives with all layers. It is the best single number for one-shot risk.
- 3.28: Ultimatum gained a modifier that prevents player block (3.28.0 notes). Block builds must read that mod.
- 3.28: Intelligence now grants 1% increased maximum ES per 10 Intelligence, half the old rate (3.28.0 notes). ES pools from Intelligence alone are smaller than older guides show.

## Tools to call

When the Exiled Studio app MCP is reachable:

1. `get_build`: calc status and warnings count. Partial status means some numbers below the line may be missing.
2. `list_warnings`: unread lines (a lost resistance line changes the verdict).
3. `list_fields`: find each defence field and its state: life, energy shield, `resistance.fire`, `resistance.cold`, `resistance.lightning`, `resistance.chaos`, armour, evasion, block chance, spell suppression chance, and any max hit field if one exists.
4. `get_breakdown` on each field you compare with a threshold. Quote the tool's value.
5. For a suggested fix: `get_item` then `preview_item_edit`, or `find_tree_nodes`, `get_tree_node`, then `preview_tree_change`. Report the before and after.

Rules:
- When the app is reachable, every number is checked with `get_breakdown` or `preview_item_edit` first.
- When it is not, label each number an estimate and say how to check it.
- A field in state `unsupported`, `indeterminate`, or `not-computed` is never read as zero. If the app has no max hit field, say the app does not compute max hit yet; do not estimate it as zero.

## Common mistakes
- Presenting these ranges as game requirements.
- Quoting one-number targets without the player's content, mode, and build type.
- Comparing life alone when the build uses ES, block, or suppression.
- Forgetting the -60% campaign penalty when reading old screenshots.
- Treating spell suppression as evasion for spells (it reduces, it does not avoid).
- Expecting armour to stop big boss slams.
- Using old Intelligence-to-ES numbers after the 3.28 change.

## Verification (2026-11-17)

Game facts checked against the official 3.27.0, 3.28.0 and 3.30.0 notes and Path of Building 2.67.2: the caps, the campaign penalty, the armour formula, spell suppression (40%), the 3.28.0 lines and the 3.30.0 lines. Tool and field names checked against Exiled Studio's `schemas/mcp-tools.v1.json`.

Numbers, from the maintainer on 2026-11-17: the chaos resistance and elemental resistance figures are approved as written; life should rise about 400 to 500 per act; the level bands for each content tier; max hit is build dependent (the figures stay as rough guides, and the early-maps one is a scaled estimate); suppression and block targets apply only to builds that use those layers; hardcore takes conservative numbers; ES builds trade life for ES; two utility flasks is the usual early-maps count. The observed table was read by hand from the poe.ninja builds page.

Still `unverified`: the life targets for early maps, red maps, pinnacle and uber bosses are the original drafts. They sit above what ladder characters had on league day 4, and the maintainer has not yet said whether to keep them or lower them.
