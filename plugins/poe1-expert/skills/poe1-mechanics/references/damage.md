---
game: poe1
patch: 3.30.0
as_of: 2026-11-17
sources:
  - https://www.pathofexile.com/forum/view-thread/3531661
  - https://www.pathofexile.com/forum/view-thread/3985332
  - https://www.pathofexile.com/forum/view-thread/4013680
  - https://www.poewiki.net/wiki/Critical_strike
  - https://www.poewiki.net/wiki/Evasion
  - https://github.com/PathOfBuildingCommunity/PathOfBuilding/blob/v2.67.2/src/Modules/CalcOffence.lua
  - https://github.com/PathOfBuildingCommunity/PathOfBuilding/blob/v2.67.2/src/Modules/CalcDefence.lua
verification: engine-checked
---

# Damage: how hit damage is built and combined (PoE1)

PoE2 uses some of the same words with different rules. Do not apply this file there.

## Increased vs more

There are two kinds of percentage modifier, and they combine differently.

- **Increased / reduced**: all of them that apply to a hit are summed into one number. Reduced counts as negative.
- **More / less**: each one is its own multiplier. Less is a multiplier below 1.

```
damage = base x (1 + sum(increased) - sum(reduced)) x product(1 + more_i) x product(1 - less_j)
```

Example: 50% increased and 30% increased give x1.8, not x1.5 x 1.3. Two separate 30% more give x1.69.

Because increases are pooled, each new increase is worth less as the pool grows. A more multiplier is worth its full value no matter what else you have. That is why support gems (mostly "more") matter so much.

A total below zero (more reduced than increased) leaves the damage at zero, not negative.

## Damage types and keywords

There are five damage types: **physical, lightning, cold, fire, chaos**. Lightning, cold and fire together are **elemental**.

A hit also carries keywords (flags) from the skill and the source: attack or spell, melee, projectile, area, hit or damage over time, the weapon type, minion, totem, trap, mine, brand, and the skill's own keywords (for example "Cold Skills").

A modifier applies when every condition it names is true for that damage. So:

- "increased Damage" applies to all damage of every type.
- "increased Spell Damage" applies only to spells; "increased Attack Damage" only to attacks.
- "increased Projectile Damage" applies to projectile hits of either kind.
- "increased Cold Damage" applies to cold damage, including cold that came from conversion (see `conversion.md`).
- "increased Damage with Hits" does not touch damage over time, and "increased Damage over Time" does not touch hits.

Since 3.29 some skills and passives use the keyword **Arcane Might** for "increases and reductions to spell damage also apply to attack damage". The official 3.29.0 notes (Player Changes) call it a purely descriptive change: the rule is the same as the old wording.

## Flat added damage and its effectiveness

Flat added damage ("Adds 10 to 20 Cold Damage") goes into the **base**, before any percentage modifier. So every increase and more multiplies it.

Where the base comes from:

- **Spells**: the skill gem's own base damage, plus added damage that names spells (or no skill kind).
- **Attacks**: the weapon's damage (after its local mods), plus added damage that names attacks (or no skill kind). Unarmed attacks use a fixed unarmed base.

**Effectiveness of added damage** scales the flat added damage from other sources (gear, tree, auras, supports) before it joins the skill's base:

```
spell base  = skill base damage + added damage x effectiveness
attack base = weapon damage x attack damage multiplier + added damage x effectiveness
```

- The skill's own base damage is not scaled by effectiveness.
- Fast or multi-hit skills usually have low effectiveness; slow, single big hits usually have high effectiveness.
- For attacks, the gem's "attack damage" percentage scales the weapon's damage. For most attack gems the two values are the same, but read them separately.

**3.25 change**: many gems moved from one fixed effectiveness to an effectiveness that grows with gem level (the official 3.25.0 notes list, for example, Absolution, Prismatic Burst and Impending Doom's Doom Blast going from a single value to a range over gem levels 1 to 20). 3.29 retuned many spells again, including their effectiveness. Look the value up per gem and level; never assume one number for a gem.

## The hit damage pipeline

For each damage type, in this order:

1. **Base**: skill or weapon damage, plus flat added damage times effectiveness.
2. **Conversion and "gained as extra"** move or copy damage along the chain physical > lightning > cold > fire > chaos (`conversion.md`).
3. **Increased / reduced**: one sum of every increase that applies to the damage, counting each type the damage passed through.
4. **More / less**: every multiplier that applies.
5. **Roll**: the hit rolls a value between its min and max for each type.
6. **Critical strike**: if the hit crits, its damage is multiplied by the crit multiplier (`crit.md`). Lucky damage and double damage, if any, apply around here.
7. **The enemy's mitigation**, per type:
   - physical: the enemy's armour and any physical damage reduction;
   - elemental and chaos: the enemy's resistance, lowered by your penetration (hits only) and by curses or exposure applied to the enemy;
   - damage-taken modifiers on the enemy (see below).

Hits are rounded at a few points in the game and in Path of Building. The engine reproduces PoB's rounding; small differences of 1 point are normal between tools.

## Damage taken vs damage dealt

Modifiers on **you** ("you deal increased damage") and modifiers on **the enemy** ("enemy takes increased damage") are separate pools.

```
final = your damage x (1 + sum(enemy increased damage taken)) x product(enemy more damage taken) x enemy mitigation
```

- Shock is an "increased damage taken" effect on the enemy. It does not add to your own increased damage pool.
- "Enemy takes increased damage" from several sources sums among itself, then multiplies with your damage.
- Lowering resistance (curses, exposure) and penetration are not damage-taken effects. They change the resistance number.
- Penetration works only on hits. Damage over time ignores it.

## Global vs local modifiers

A **local** modifier changes the item it is on, not the character.

- On a weapon: added damage, increased physical damage, attack speed, crit chance and accuracy lines are local. They change the weapon's own numbers, and only attacks made with that weapon use them.
- On armour: increased armour, evasion or energy shield are local to that piece.

A **global** modifier applies to the character (subject to its conditions).

- "Adds X to Y Physical Damage to Attacks" on a ring or amulet is global: it adds to attacks with both hands.
- Local increased physical damage on a weapon is applied to the weapon's base first; then global increased physical damage applies again in the character's pool. The two do not sum together, so they effectively multiply.

## DPS

For a single target:

```
average hit  = sum over types of (min + max) / 2, after all modifiers
crit factor  = 1 + crit chance x (crit multiplier - 1)
DPS          = average hit x crit factor x rate x hit chance
```

- **Rate**: attacks or casts per second. Many tools cap a skill's rate near 30 per second (one action per server tick).
- **Hit chance** (attacks only) comes from your accuracy against the enemy's evasion:

```
hit chance = 1.25 x A / (A + (E / 5) ^ 0.9), clamped to 5%..100%
```

  A is your accuracy rating, E the enemy's evasion. Spells do not use accuracy; they can still be blocked or suppressed.
- For attacks, a crit must pass the accuracy check a second time; if that second check fails, the hit lands as a normal hit. So the chance that a landed attack is a crit is crit chance x hit chance, and that is the value to use in the crit factor (PoB does the same). Spells skip both checks.
- Area skills, projectiles that hit more than once, and skills with several hits multiply DPS by how many times they hit the target. That is skill-specific; read the skill.
- Damage over time (ailments, degen) is a separate DPS number that is added for a combined total.

## Worked example

A cold spell, numbers chosen for the example only:

- base cold damage 100 to 200; added 10 to 20 cold from gear; effectiveness 150%
- 100% increased spell damage, 50% increased cold damage
- two supports: 30% more and 20% more
- 20% crit chance, 250% crit multiplier
- enemy cold resistance 40%, your penetration 10%
- 2 casts per second

```
base       = (100 + 10 x 1.5) to (200 + 20 x 1.5) = 115 to 230, average 172.5
increased  = x (1 + 1.00 + 0.50) = x 2.5      -> 431.25
more       = x 1.3 x 1.2 = x 1.56             -> 672.75
crit       = x (1 + 0.20 x (2.50 - 1)) = x 1.3 -> 874.58
resistance = x (1 - (0.40 - 0.10)) = x 0.7    -> 612.20
DPS        = 612.20 x 2 = 1224.4
```

## Common mistakes

- Multiplying increases together. They sum; only more and less multiply.
- Treating "increased damage taken" on the enemy as part of your increased damage pool.
- Scaling the skill's own base damage by effectiveness. Effectiveness only scales added flat damage.
- Assuming a gem's effectiveness is one fixed number after 3.25.
- Applying weapon-local added damage to spells, or to the other hand.
- Letting penetration reduce damage over time.
- Forgetting hit chance for attacks, or applying accuracy to spells.
- Using PoE2 rules for any of the above. PoE2 differs; do not apply this there.

## Check with the engine

The Exiled Studio calc result has per-skill fields for average damage, crit chance, crit multiplier, speed, hit chance and total DPS, each with a provenance graph. Expand the average damage node to see the base, the summed increases, each more multiplier and the enemy's resistance step. Use it to confirm a hand calculation, and to see which modifiers did or did not apply to a hit.

## Verification (2026-11-17)

`engine-checked` here means: checked against the pinned Path of Building 2.67.2 (`CalcOffence.lua` for effectiveness, conversion order, the crit factor and the crit-times-hit-chance step; `CalcDefence.lua` for the hit chance formula, which PoB rounds to a whole percent) and against the official 3.25.0, 3.29.0 and 3.30.x patch notes. Nothing in 3.30.0 or its hotfixes changes these rules. Not checked in game.
