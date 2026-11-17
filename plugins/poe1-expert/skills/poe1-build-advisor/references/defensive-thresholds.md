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
verification: maintainer-approved
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

## Life and energy shield by character level

The maintainer's decision (2026-11-17): life and ES targets follow what players actually have, by level. The ranges below are the middle half of ladder characters at each level, read by hand from the poe.ninja builds page on 2026-11-17 (Covens softcore trade, league day 4, the first 100 characters shown at each level). A build inside its range is normal for its level; below it, the pool is a risk to name; above it is comfortable. Pools rise as a league goes on, so re-read these with a newer snapshot.

| Level | Likely content | Life builds: life | Life + ES, typical |
|---|---|---|---|
| 70 | end of campaign, first maps | 2,100 to 2,800 | about 2,700 |
| 75 | white to yellow maps | 2,500 to 3,400 | about 3,200 |
| 80 | yellow maps, pinnacle bosses begin | 2,800 to 3,600 | about 3,500 |
| 85 | pinnacle bosses | 3,000 to 4,000 | about 3,900 |
| 90 | red maps | 3,200 to 4,400 | about 4,200 |
| 93 | red maps | 3,300 to 4,200 | about 4,400 |
| 95 and up | red maps, bosses, ubers | 3,600 to 5,000 | about 4,800 |

**ES builds** (more ES than life) are rare before level 90 (about 1 in 100) and grow to roughly 1 in 5 by level 97. Their ES, middle half: about 2,800 to 5,700 at level 90, and about 3,500 to 7,200 from level 93 up (typically 5,500 to 5,900). Many are Chaos Inoculation with 1 life. So an ES build carries a larger pool than a life build of the same level, with little or no life.

## Campaign (Acts 1 to 10)
- **Resistances**: try to cap fire, cold and lightning after the Act 5 penalty (-30%) and again after Act 10 (another -30%, -60% in total). Many players are below cap mid-act; aim to be capped entering Act 6 and entering maps.
- **Chaos resistance**: anything is fine; negative is normal.
- **Life**: keep adding life every act. The maintainer's guide is about 400 to 500 per act, give or take, as the aim; most characters end the campaign around level 70 with 2,100 to 2,800 life, so treat the guide as the upper end. ES builds may carry less life and more ES.
- **Ailments**: a flask with freeze or bleed removal helps; not required.
- **Movement**: a movement skill and a quicksilver flask help more than any number.

## Early maps (white and yellow tiers)
- **Resistances**: elemental at 75% each. Chaos at least near 0%.
- **Life**: about 2,500 to 3,400 at level 75 (see the table), or the ES equivalent.
- **Max hit**: no fixed number; it depends on the build and its layers.
- **Ailments**: one answer to freeze and one to bleed (flask suffixes are fine).
- **Layers**: at least one of armour, evasion, block, or spell suppression scaled on purpose. A guard skill if one fits.
- **Flasks**: very build dependent; a life flask with an instant or bleed-removal suffix and usually two utility flasks.

## Red maps (tiers 14 to 16, light juice)
- **Resistances**: elemental 75% each with some over-cap. Chaos 20% to 40% or more.
- **Life**: about 3,200 to 4,400 at level 90 (see the table). ES builds: about 4,000 to 6,000 ES.
- **Ailments**: freeze immunity or near-total avoidance. Shock and stun answers become important. Bleed and corrupted blood handled.
- **Spell suppression**: not every build has it. A build that is working toward suppression should aim for 100% chance; below that, every unsuppressed spell hit is a surprise.
- **Block**: not every build has it. A build that uses block should aim for the default cap on attack block, and some for spell block too.
- **Max hit**: depends on the build and which layers it has; there is no one number. As a rough guide players aim for a max hit a few thousand per element above their pool.
- **Recovery**: a reliable leech, regeneration, or recoup source.
- 3.30: a corruption can add 2 explicit mods to a map, up to 9 in total (3.30.0 notes). Map mods that lower maximum resistances or reduce recovery make these lines worse; read the mods.
- 3.28: Voidstones raise the minimum map tier in their Atlas quadrant (3.28.0 notes). Players reach red maps sooner, often before their defences are ready.

## Pinnacle bosses (Shaper, Elder, Sirus, Maven, Eater of Worlds, Searing Exarch, and similar)
- **Resistances**: elemental 75% minimum; many players add maximum resistance (76% to 80%) for elemental-heavy bosses. Chaos 40% to 75% for chaos-heavy fights.
- **Life**: about 2,800 to 4,000 at levels 80 to 85, where these fights begin, and 3,600 to 5,000 by level 95 (see the table). ES builds: about 5,500 to 7,000 ES at high level.
- **Max hit**: build dependent. A figure of 10,000 or more per damage type is often cited for these fights; it is well above what a typical pool gives, so it comes from layers, not life alone.
- **Ailments**: freeze and stun handled; curse effect reduced or cleansed helps.
- **Recovery**: flasks, leech, or regeneration enough to recover between big hits.
- 3.30: in Deified areas (a map with a Divine Vessel applied) map bosses get 25% increased damage, 25% increased attack and cast speed and 100% increased toughness; the Cortex bosses now show as pinnacle Atlas bosses (3.30.0 notes). Check the boss in question through the knowledge MCP.

## Uber pinnacle bosses
- **Resistances**: capped, often with raised maximums. Chaos often 75% for some fights.
- **Life**: the top of the level 95 range or above (5,000 or more life, or 7,000 or more ES). Few ladder characters have more this early in a league; deep-defence builds go much higher.
- **Max hit**: build dependent; values above 15,000 for the main damage types are commonly cited. Treat as rough; it depends on which boss, and it needs layers well beyond the pool.
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

Numbers, from the maintainer on 2026-11-17: the chaos resistance and elemental resistance figures are approved as written; the level bands for each content tier; life about 400 to 500 per act as the campaign aim; max hit is build dependent; suppression and block targets apply only to builds that use those layers; hardcore takes conservative numbers; ES builds trade life for ES; two utility flasks is the usual early-maps count. The maintainer also decided that life and ES targets follow what players actually have by level, so the old draft targets (3,500 to 4,500, 5,000 to 6,000, 6,000 or more, 7,000 to 10,000) were replaced by the observed ranges in the table, read by hand from the poe.ninja builds page (100 characters each at levels 70, 75, 80, 85, 90, 93, 95 and 97; the ES figures come from 8 to 23 characters per level, so they are rough).

`engine-checked` here means the game facts were checked as above and every number is either the maintainer's or an observation with its date and source. The max hit figures remain commonly cited values with no source.

Approved by the maintainer on 2026-11-17 (given in chat, recorded by the session). The checks named above are what was done before approval; nothing here was checked in game unless a line says so.
