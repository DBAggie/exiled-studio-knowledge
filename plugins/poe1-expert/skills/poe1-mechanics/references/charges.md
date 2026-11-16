---
game: poe1
patch: 3.30.0
as_of: 2026-11-15
sources:
  - https://maxroll.gg/poe/resources/charges
  - https://www.pathofexile.com/forum/view-thread/3924293
  - https://patchbot.io/games/path-of-exile/articles/2188-content-update-3300-path-of-exile-covens-of-umbra
  - https://poedb.tw/us/Version_3.29.0
  - https://poedb.tw/us/Version_3.28.0
  - https://poedb.tw/us/Version_3.26.0
verification: unverified
---

# Charges in PoE1

Charges are stacking buffs with a count, a maximum, and a shared duration. The three core types (power, frenzy, endurance) exist on every character. Other types exist only when a specific source grants them.

## The three core charges

Each charge gives its effect once per charge held. The per-charge values below are the character constants the Exiled Studio engine reads from game data (`docs/phase-3/config-inputs.md`, "Charges").

| Charge | Effect per charge |
|---|---|
| Power | 50% increased critical strike chance |
| Frenzy | 4% increased attack speed, 4% increased cast speed, 4% **more** damage |
| Endurance | 4% additional physical damage reduction, plus an elemental defence (see below) |

- The frenzy damage bonus is a "more" multiplier, so it multiplies with everything else; the speed bonuses are "increased" and add to other increased speed.
- The power charge bonus is "increased" crit chance, so it adds to other increased crit chance before multiplying the base.
- **Endurance elemental part.** Older patches gave +4% to all elemental resistances per endurance charge. Path of Building's current model (v2.67.2) treats it as elemental damage reduction per charge. Which form 3.30 uses is not confirmed; check before quoting.

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
- 3.28's Transfusion Support gives a minion charges from life spent on upfront costs.

## Other charge types

These start with a maximum of 0 and do nothing unless a source grants them. Each has its own rules; look up the source item or passive for effects and maxima.

| Type | Granted by (example) | Status for 3.30 |
|---|---|---|
| Absorption | Graven's Secret (replaces power charges) | not confirmed for 3.30 |
| Affliction | Olesya's Delight (replaces frenzy charges) | not confirmed for 3.30 |
| Brutal | Arn's Anguish (replaces endurance charges) | not confirmed for 3.30 |
| Challenger | a Gladiator notable | not confirmed for 3.30 |
| Blitz | the Berserker's Blitz notable | its passive was replaced in 3.26; probably no player source |
| Fanatic | Instruments of Zeal (Inquisitor) | still exists; 3.29 lowered its maximum |
| Siphoning | Disintegrator | still exists; 3.29 raised its per-charge reduction |
| Spirit | Lightpoacher, Hale Negator | not confirmed for 3.30 |
| Divinity | Garb of the Ephemeral | not confirmed for 3.30 |
| Void | Voidfletcher | not confirmed for 3.30 |
| Blood | Reap of Butchery (new in 3.29) | new, see the gem |
| Inspiration | Inspiration Support | not confirmed for 3.30 |

- **Replacement charges.** Absorption, affliction, and brutal charges are gained instead of a core type. The source converts the gain, so "gain a power charge" gives an absorption charge, and per-power-charge modifiers no longer see a charge.
- **Inspiration** comes from a support gem and is not a core charge; it builds from skill use and is spent automatically. Check the gem for its current rules.

## Rage

- Rage is a separate charge-like resource, not a charge. It builds from attacks or hits, is capped by a maximum, and decays when you stop gaining it.
- Its bonuses, maximum, and decay depend on the patch and the source; look them up. 3.26 added rage regenerated from life regeneration (Kaom's Spirit), and 3.29 moved some rage costs to "rage cost efficiency" (Hateforge).
- Rage carries through combat-area transitions since 3.28.0e.

## Monsters and minions

- Monsters with charges get much larger per-charge effects than players. Do not apply player values to monsters.
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

- `loom_calc::poe1::charges`: the count for each type comes from the `use<Kind>Charges` and `override<Kind>Charges` config inputs, the maximum, and the minimum. The calc breakdown shows each per-charge effect with its source.
- Crit chance and speed fields show the power and frenzy contributions as named effects.
- Endurance charge effects reach damage taken, which is not a slice field yet; say so when asked for a number.
- Absorption, affliction, and brutal conversions and "at maximum" flags are unmapped stats in the engine and show as reasons.
