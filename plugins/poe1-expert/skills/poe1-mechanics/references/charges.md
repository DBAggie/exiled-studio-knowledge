---
game: poe1
patch: 3.30.0
as_of: 2026-11-17
sources:
  - https://maxroll.gg/poe/resources/charges
  - https://www.pathofexile.com/forum/view-thread/3924293
  - https://www.pathofexile.com/forum/view-thread/3531661
  - https://www.pathofexile.com/forum/view-thread/3787013
  - https://www.pathofexile.com/forum/view-thread/3913392
  - https://www.pathofexile.com/forum/view-thread/3985332
  - https://www.pathofexile.com/forum/view-thread/4013680
  - https://www.poewiki.net/wiki/Charge
  - https://www.poewiki.net/wiki/Challenger_Charge
  - https://github.com/PathOfBuildingCommunity/PathOfBuilding/blob/v2.67.2/src/Data/Misc.lua
  - repo:DBAggie/exiled-studio/crates/loom-calc/src/poe1/charges.rs
  - repo:DBAggie/exiled-studio/crates/loom-calc/src/poe1/stacks.rs
verification: maintainer-approved
---

# Charges in PoE1

Charges are stacking buffs with a count, a maximum, and a shared duration. The three core types (power, frenzy, endurance) exist on every character. Other types exist only when a specific source grants them.

## The three core charges

Each charge gives its effect once per charge held. The per-charge values below are the character constants the Exiled Studio engine reads from game data (`docs/phase-3/config-inputs.md`, "Charges").

| Charge | Effect per charge |
|---|---|
| Power | 50% increased critical strike chance |
| Frenzy | 4% increased attack speed, 4% increased cast speed, 4% **more** damage |
| Endurance | 4% additional physical damage reduction and 4% additional elemental damage reduction |

- The frenzy damage bonus is a "more" multiplier, so it multiplies with everything else; the speed bonuses are "increased" and add to other increased speed.
- The power charge bonus is "increased" crit chance, so it adds to other increased crit chance before multiplying the base.
- **Endurance elemental part.** Since **3.25.0**, each endurance charge on players and minions gives 4% additional **elemental damage reduction**, not +4% to all elemental resistances (official 3.25.0 notes, Player Balance). Guides from before 3.25 still say +4% resistances; they are out of date. No later note changes it, and PoB 2.67.2's game data and poewiki agree. Monsters still get resistances from endurance charges (see below). `defences.md` says the same.

### Maximum, minimum, and duration

- **Default maximum:** 3 of each type. Modifiers add or remove maximum charges (3.30 example: Malachai's Loop gives fewer extra power charges; Ralakesh's Impatience rolls a lower maximum of one type).
- **Minimum charges:** some sources give a minimum. You always have at least that many, they cannot be spent below the minimum, and the minimum cannot exceed the maximum.
- **Duration:** 10 seconds by default. Gaining a charge of a type refreshes the timer for that type. When the timer runs out, all charges of that type are lost at once.
- "Increased charge duration" modifiers lengthen the timer for their type.
- **Area transitions (3.28.0e):** most charges now carry over through combat-area transitions, as temporary minions do. Rage, fortify, and shrines changed the same way.

### Count used in calculations

```
count = clamp(current charges, minimum, maximum)
effect = per-charge value x count
```

## Generating charges

- "Chance to gain a [type] charge on hit / on kill / on crit" (gems such as Power Charge On Critical Support, passives, and items).
- Charge-generating skills (for example Enduring Cry for endurance charges, or Blood Rage for frenzy on kill). Check current gem text; these change often.
- Ascendancy notables that grant charges on conditions. 3.29 examples: Deathmarked (Assassin) scales with maximum power charges.
- Shrines: 3.28 changed the Resonating Shrine to grant +1 maximum of each core charge, and still generates charges.

## Spending charges

- Some skills consume charges for a bonus (Discharge, Holy Hammers of Spirals in 3.29, Tectonic Slam). A consumed charge is gone until you gain it again.
- "Per charge" modifiers on items and passives ("X% increased cast speed per power charge") scale with the current count, not the maximum.
- "While at maximum [type] charges" conditions check that the count equals the current maximum.
- 3.30.0 changed Transfusion Support: a minion near you gains a power, frenzy or endurance charge for every 400 life you spend on upfront costs with supported spells (it used to give a soul per 200 life), and it no longer supports instant spells.

## Other charge types

These start with a maximum of 0 and do nothing unless a source grants them. Each has its own rules; look up the source item or passive for effects and maxima.

| Type | Granted by (example) | Status for 3.30 |
|---|---|---|
| Absorption | Graven's Secret, a Maven belt (replaces power charges) | current |
| Affliction | Olesya's Delight, a Maven belt (replaces frenzy charges) | current |
| Brutal | Arn's Anguish, a Maven belt (replaces endurance charges) | current |
| Brine | Tidebreaker (3.29.0: a chance to gain brine instead of endurance charges) | current |
| Challenger | was the Gladiator's Arena Challenger | gone: the notable was reworked in 3.25 and the charges can no longer be gained |
| Blitz | was the Berserker's Blitz notable | gone: 3.26.0 replaced Blitz with Gore Dancer; no player source left |
| Fanatic | Instruments of Zeal (Inquisitor) | still exists; 3.29 lowered its maximum |
| Siphoning | Disintegrator | still exists; 3.29 raised its per-charge reduction |
| Spirit | Lightpoacher, Hale Negator | current |
| Divine | Garb of the Ephemeral (reaching the maximum gives Divinity) | current |
| Void | Voidfletcher (3.29.0 moved it to another quiver base) | current |
| Blood | Reap of Butchery (new in 3.29) | new, see the gem |
| Inspiration | Inspiration Support | current |

- **Replacement charges.** Absorption, affliction, and brutal charges are gained instead of a core type. The source converts the gain, so "gain a power charge" gives an absorption charge, and per-power-charge modifiers no longer see a charge.
- **Inspiration** comes from a support gem and is not a core charge; it builds from skill use and is spent automatically. Check the gem for its current rules.

## Rage

- Rage is a separate charge-like resource, not a charge. It builds from attacks or hits, is capped by a maximum, and decays when you stop gaining it.
- Since the **3.25.0** rework: each rage gives 1% **more** attack damage (scaled by "rage effect"), and rage no longer gives attack or movement speed by itself. The base maximum is 30. If you have not been hit or gained rage for 2 seconds, you lose 10 rage per second. Rage on hit has a shared limit of once per 0.5 seconds. (Official 3.25.0 notes; PoB 2.67.2's game data has the same 30 maximum and 2-second delay.)
- Sources and extra effects change often; look them up. 3.26 added rage regenerated from life regeneration (Kaom's Spirit), and 3.29 moved some rage costs to "rage cost efficiency" (Hateforge).
- Rage carries through combat-area transitions since 3.28.0e.

## Monsters and minions

- Monsters with charges get much larger per-charge effects than players (for example, endurance charges give monsters elemental resistances and more physical damage reduction). Do not apply player values to monsters.
- Minions can have charges of their own but do not share the player's.

## Common mistakes

- Using the old power charge value (it is 50% increased crit chance per charge, not 40%).
- Treating the frenzy damage as "increased". It is "more".
- Assuming charges expire one at a time. The whole type is lost when its timer ends.
- Counting a power charge for per-power-charge modifiers while a source converts it to absorption charges.
- Giving the player monster charge values.
- Listing Blitz charges as a current Berserker option. The passive was replaced in 3.26.
- PoE2 differs (charges have different effects and durations there); do not apply this there.

## Check with the engine

The engine facts below were read from Exiled Studio's source (`crates/loom-calc`, dev branch at `b42e49f`, 2026-11-17; the 0.9 line). The engine follows Path of Building 2.67.2's order of operations and rounding, so a number the engine marks `complete` is PoB's number, apart from registered divergences. It computes 24 fields: `strength`, `dexterity`, `intelligence`, `life`, `mana`, `life-unreserved`, `mana-unreserved`, `energy-shield`, `armour`, `evasion`, `resistance.fire`, `resistance.cold`, `resistance.lightning`, `resistance.chaos`, `block-chance`, `spell-block-chance`, `spell-suppression-chance`, `average-damage`, `speed`, `hit-speed`, `hit-chance`, `crit-chance`, `crit-multiplier` and `hit-dps`. The hit fields exist only when the main skill is a self-cast spell hit or a main-hand attack: not channelled, triggered, a totem, trap, mine, minion or brand skill, not a skill with a cooldown, and not dual wielding. For any other main skill they are `not-computed`.

- `loom_calc::poe1::charges`: the count per type is PoB's rule, `max(use ? (override or maximum) : 0, min(maximum, minimum))`, from the `use<Kind>Charges` and `override<Kind>Charges` config inputs. A minimum gives charges even with the `use` input off.
- Power charges show in `crit-chance`; frenzy charges in `speed` (increased attack and cast speed) and as a more multiplier in `average-damage`. Each is a named per-charge effect with its source.
- Endurance charges' own effects (physical and elemental damage reduction) reach no computed field: the engine has no damage-taken field for the player. Say so when asked for a number.
- Rage and Inspiration charges are counted as stacks for modifiers that read them.
- "At maximum charges" flags and conversions to absorption, affliction or brutal charges are not mapped; they show as an `unmapped-stat` reason.

## Verification (2026-11-17)

`engine-checked` here means: the per-charge values, the default maximum of 3, the endurance charge's elemental damage reduction and the rage constants were checked against the game-data constants in the pinned Path of Building 2.67.2 (`Data/Misc.lua`) and the official 3.25.0 to 3.30.x notes; the charge list was checked against poewiki's charge pages. Not checked in game.

Approved by the maintainer on 2026-11-17 (given in chat, recorded by the session). The checks named above are what was done before approval; nothing here was checked in game unless a line says so.
