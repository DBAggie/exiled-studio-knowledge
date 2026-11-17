---
game: poe1
patch: 3.30.0
as_of: 2026-11-17
sources:
  - https://www.pathofexile.com/forum/view-thread/3913392
  - https://www.pathofexile.com/forum/view-thread/3985332
  - https://www.pathofexile.com/forum/view-thread/4013680
  - https://www.poewiki.net/wiki/Critical_strike
  - https://www.poewiki.net/wiki/Evasion
  - https://www.poewiki.net/wiki/Ailment
  - https://github.com/PathOfBuildingCommunity/PathOfBuilding/blob/v2.67.2/src/Modules/CalcOffence.lua
  - repo:DBAggie/exiled-studio/crates/loom-calc/src/poe1/hit.rs
  - repo:DBAggie/exiled-studio/crates/loom-calc/src/poe1/keystones.rs
verification: maintainer-approved
---

# Critical strikes (PoE1)

PoE1 calls them "critical strikes". PoE2 calls them "critical hits" and its numbers and rules differ. Do not apply this file there.

## Base crit chance

Every hit has a base critical strike chance:

- **Attacks** use the weapon's crit chance, after the weapon's local crit mods.
- **Spells** use the skill gem's own base crit chance.
- Some skills, passives or ascendancy nodes replace the base (for example, setting a spell's base from something else). Read the exact wording.

The base differs a lot between weapons and spells. Look it up; never assume.

## Increased crit chance

```
crit chance = (base + flat additions) x (1 + sum(increased)) x product(more), then capped to 0%..100%
```

- "+X% to Critical Strike Chance" adds to the base before increases. Small flat additions are strong on low-base skills because every increase multiplies them.
- "X% increased Critical Strike Chance" sums with all other increases (global, spell, with a weapon type, and so on).
- More and less multiply.
- A weapon's local "increased Critical Strike Chance" changes the weapon's base first; global increases then apply on top. They multiply, not sum.

**Caps**: the old 5% minimum and 95% maximum were removed in 3.6.0 (poewiki's version history for critical strikes; the 3.6.0 forum post was not opened). Crit chance now runs from 0% to 100%.

## Effective crit chance

A crit can only happen on a hit that lands. For attacks there is a **second accuracy check**: when an attack rolls a crit, it must pass the hit check again, and if that second check fails the hit lands as a normal hit. So:

```
chance a landed attack is a crit = crit chance x hit chance
chance an attack attempt crits   = crit chance x hit chance x hit chance
```

PoB applies the same step (it multiplies crit chance by hit chance for attacks). Against players, evasion's "entropy" does not cover this second check; it is a plain random roll. Spells do not use accuracy, so their crit chance is the chance per cast that hits.

## Lucky and unlucky crits

"Critical Strike Chance is Lucky" rolls the chance twice and keeps the better result:

```
lucky   = 1 - (1 - c)^2
unlucky = c^2
```

c is the capped crit chance. At 50% lucky gives 75%; at 90% it gives 99%.

## Bifurcation (new in 3.29)

Some effects make crit chance **bifurcate** (3.29.0 added it on the Assassin's Mystical Infusion, with 30% less spell crit chance). The official 3.29.0 notes describe it this way; the chance is rolled twice for that hit:

- one success: a normal crit;
- two successes: the crit's **extra** damage is doubled. With multiplier M, the hit uses `1 + 2 x (M - 1)` instead of M. A 300% multiplier becomes 500%.
- Lucky or unlucky applies to each of the two rolls separately.
- A hit that always crits never rolls, so it cannot bifurcate.

Expected crit factor with bifurcation and chance c (no luck):

```
factor = 1 + 2c(1 - c) x (M - 1) + c^2 x 2 x (M - 1) = 1 + 2c x (M - 1)
```

So on average bifurcation doubles the value of each point of crit chance, up to the cap.

**Bifurcation and ailments.** The notes say nothing about ailments, so the normal crit rules apply: a hit that passes either roll is a crit, so it gets the crit's inherent ignite, freeze and shock and the +50% damage-over-time multiplier for damaging ailments. The doubled extra damage makes the hit bigger, which strengthens non-damaging ailments (they scale with the hit). Damaging ailments do not use the crit multiplier, so the doubling does not reach them. PoB (2.67.2) models it so: it uses the bifurcated crit chance for crit ailments and does not double the Perfect Agony multiplier. Not checked in game.

## Crit multiplier

- Players have a base crit multiplier of **150%**: a crit deals 1.5 times the hit's damage.
- "+X% to Critical Strike Multiplier" adds to it. The multiplier sums all such sources; there is no separate "increased crit multiplier" pool.
- The part above 100% is the crit's **extra damage**. "Reduced extra damage from critical strikes" (a defence) cuts that extra part only.
- The multiplier cannot drop below 100% (a crit never deals less than a non-crit).

```
crit factor (average) = 1 + c x (M - 1)
```

c is the effective crit chance, M the multiplier as a decimal (2.5 for 250%).

## Crits and ailments

- **Damaging ailments** (ignite, bleed, poison) from a crit take their base from the crit hit's damage, so the crit multiplier makes them stronger.
- Some modifiers apply only to ailments from crits (for example a damage-over-time multiplier for ailments inflicted by crits).
- **Non-damaging ailments** (shock, chill, freeze, and the others) scale with the hit's damage against the enemy's ailment threshold. A crit's bigger hit gives a stronger or longer ailment.
- **Crits inherently ignite, freeze and shock** (100% chance), as long as the hit has the matching damage and the ailment reaches the target's threshold. Chill needs no chance at all. Bleeding, poison, scorch, brittle and sap are not guaranteed by a crit. This still holds in 3.30: no 3.26 to 3.30 note changes it, the 3.28.0 notes refer to the stat that turns it off ("critical strikes against you do not inherently inflict elemental ailments"), and both poewiki and PoB 2.67.2 apply it. Some items turn it off (for example "critical strikes do not inherently inflict non-damaging ailments"). `ailments.md` says the same.

See `ailments.md` for the ailment rules themselves.

## Non-crit damage

Some modifiers affect hits that do not crit:

- "Non-critical strikes deal X% less damage" applies to every hit that fails to crit.
- Elemental Overload-style effects remove the crit's extra damage (the multiplier counts as 100%) and pay you back in another way.

Model these as a separate pass: average = non-crit hit x (1 - c) + crit hit x c.

## Resolute Technique

The keystone makes your hits impossible to evade and stops them from ever being critical strikes.

- Hit chance becomes 100% against evasion (block and similar avoidance still apply).
- Crit chance is 0. Crit multiplier, lucky crits and "on crit" effects do nothing for those hits.
- Ailments from crits never happen; ailments from non-crit hits still do.

No 3.26 to 3.30 note mentions the keystone (3.30.x posts read in full; 3.25 to 3.29 posts searched for it). Not checked in game.

## Other PoE1 rules

- Accuracy does not affect crit chance except through hit chance (which, for attacks, applies twice: see above).
- Effects that make a hit "always crit" skip the roll entirely (so they also skip luck and bifurcation).
- Crit chance against a specific enemy (for example, from a debuff on that enemy) adds to the same calculation for hits against that enemy only.

## Worked example

An attack, numbers for the example only:

- weapon base crit 7%, 20% local increased crit on the weapon
- +1% to crit chance from a global source
- 300% global increased crit chance
- 90% hit chance
- crit multiplier 150% base + 100% added = 250%

```
weapon crit   = 7 x 1.20 = 8.4%
with flat     = 8.4 + 1 = 9.4%
increased     = 9.4 x (1 + 3.00) = 37.6%
landed crit   = 0.376 x 0.90 = 33.8% of landed attacks crit
crit factor   = 1 + 0.3384 x (2.5 - 1) = 1.508  (per landed hit)
lucky instead = 1 - (1 - 0.376)^2 = 61.1%; x 0.90 = 55.0%; factor 1 + 0.5496 x 1.5 = 1.824
```

## Common mistakes

- Adding "+% to crit chance" after the increases instead of to the base.
- Summing local and global increased crit. Local changes the weapon first.
- Treating crit multiplier as a pool of "increased" mods, or applying "reduced extra damage from crits" to the whole hit.
- Forgetting the 150% base multiplier, or the second accuracy check on attack crits.
- Assuming the old 5% / 95% caps still exist.
- Using the crit multiplier on damage over time directly. It only reaches ailments through the crit hit's damage, or through modifiers that say so.
- Giving Resolute Technique builds any crit benefit.
- Using PoE2 "critical hit" rules. PoE2 differs; do not apply this there.

## Check with the engine

The engine facts below were read from Exiled Studio's source (`crates/loom-calc`, dev branch at `b42e49f`, 2026-11-17; the 0.9 line). The engine follows Path of Building 2.67.2's order of operations and rounding, so a number the engine marks `complete` is PoB's number, apart from registered divergences. It computes 24 fields: `strength`, `dexterity`, `intelligence`, `life`, `mana`, `life-unreserved`, `mana-unreserved`, `energy-shield`, `armour`, `evasion`, `resistance.fire`, `resistance.cold`, `resistance.lightning`, `resistance.chaos`, `block-chance`, `spell-block-chance`, `spell-suppression-chance`, `average-damage`, `speed`, `hit-speed`, `hit-chance`, `crit-chance`, `crit-multiplier` and `hit-dps`. The hit fields exist only when the main skill is a self-cast spell hit or a main-hand attack: not channelled, triggered, a totem, trap, mine, minion or brand skill, not a skill with a cooldown, and not dual wielding. For any other main skill they are `not-computed`.

- `crit-chance` is `min((base + added) x increased x more, 100)`, then **times hit chance** for attacks, exactly the second accuracy check described above. `crit-multiplier` is its own field. `average-damage` weighs the non-crit and crit passes.
- Resolute Technique and Elemental Overload are modelled (keystones). Power charges enter `crit-chance` as a named per-charge effect.
- Lucky crit chance and bifurcation are not modelled. A build with them shows `partial` fields with a reason; say the engine cannot confirm those parts.

## Verification (2026-11-17)

`engine-checked` here means: the crit chance formula, the base multiplier (150%, a character constant in PoB's data), the second accuracy check, luck and bifurcation were checked against the pinned Path of Building 2.67.2 (`CalcOffence.lua`) and the official 3.28.0, 3.29.0 and 3.30.x notes; poewiki's critical strike, evasion and ailment pages agree. The worked example was recomputed. Not checked in game.

Approved by the maintainer on 2026-11-17 (given in chat, recorded by the session). The checks named above are what was done before approval; nothing here was checked in game unless a line says so.
