---
game: poe1
patch: 3.30.0
as_of: 2026-11-15
sources:
  - https://poedb.tw/us/Version_3.6.0
  - https://poedb.tw/us/Version_3.27.0
  - https://poedb.tw/us/Version_3.29.0
  - https://patchbot.io/games/path-of-exile/articles/2188-content-update-3300-path-of-exile-covens-of-umbra
verification: unverified
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

**Caps**: the old 5% minimum and 95% maximum were removed in 3.6.0. Crit chance now runs from 0% to 100%.

## Effective crit chance

A crit can only happen on a hit that lands. For attacks:

```
chance an attack crits = hit chance x crit chance
```

There is no second accuracy roll to confirm a crit in current PoE1. Spells do not use accuracy, so their crit chance is the chance per cast that hits.

## Lucky and unlucky crits

"Critical Strike Chance is Lucky" rolls the chance twice and keeps the better result:

```
lucky   = 1 - (1 - c)^2
unlucky = c^2
```

c is the capped crit chance. At 50% lucky gives 75%; at 90% it gives 99%.

## Bifurcation (new in 3.29)

Some effects make crit chance **bifurcate**. As the 3.29 notes describe it (read in a copy of the notes; the exact in-game wording is not confirmed here), the chance is rolled twice for that hit:

- one success: a normal crit;
- two successes: the crit's **extra** damage is doubled. With multiplier M, the hit uses `1 + 2 x (M - 1)` instead of M. A 300% multiplier becomes 500%.
- Lucky or unlucky applies to each of the two rolls separately.
- A hit that always crits never rolls, so it cannot bifurcate.

Expected crit factor with bifurcation and chance c (no luck):

```
factor = 1 + 2c(1 - c) x (M - 1) + c^2 x 2 x (M - 1) = 1 + 2c x (M - 1)
```

So on average bifurcation doubles the value of each point of crit chance, up to the cap. How bifurcated crits interact with ailments is not stated in the notes read; not confirmed for 3.30.

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
- Older patches made crits always inflict some elemental ailments. Whether any part of that still holds in 3.30 is **not confirmed here**. Check the skill and the tooltip, and use ailment chance as stated.

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

No change to the keystone was found in the 3.26 to 3.30 notes read; not confirmed for 3.30.

## Other PoE1 rules

- Accuracy does not affect crit chance except through hit chance.
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
per attack    = 0.376 x 0.90 = 33.8% of attacks crit
crit factor   = 1 + 0.376 x (2.5 - 1) = 1.564   (per landed hit)
lucky instead = 1 - (1 - 0.376)^2 = 61.1%; factor 1 + 0.611 x 1.5 = 1.916
```

## Common mistakes

- Adding "+% to crit chance" after the increases instead of to the base.
- Summing local and global increased crit. Local changes the weapon first.
- Treating crit multiplier as a pool of "increased" mods, or applying "reduced extra damage from crits" to the whole hit.
- Forgetting the 150% base multiplier, or the hit chance for attacks.
- Assuming the old 5% / 95% caps still exist.
- Using the crit multiplier on damage over time directly. It only reaches ailments through the crit hit's damage, or through modifiers that say so.
- Giving Resolute Technique builds any crit benefit.
- Using PoE2 "critical hit" rules. PoE2 differs; do not apply this there.

## Check with the engine

The Exiled Studio calc result has a crit chance field (already multiplied by hit chance for attacks), a crit multiplier field, a hit chance field and the average damage field, which weighs the crit and non-crit passes. Their provenance graphs show the base, flat additions, summed increases and each more multiplier. Resolute Technique is modelled. Lucky crit chance and bifurcation may show as "not modelled" reasons; then the engine cannot confirm those parts.
