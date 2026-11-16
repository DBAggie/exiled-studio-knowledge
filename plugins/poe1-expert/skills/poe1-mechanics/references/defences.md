---
game: poe1
patch: 3.30.0
as_of: 2026-11-15
sources:
  - https://patchbot.io/games/path-of-exile/articles/2188-content-update-3300-path-of-exile-covens-of-umbra
  - https://poedb.tw/us/Version_3.29.0
  - https://poedb.tw/us/Version_3.28.0
  - https://poedb.tw/us/Version_3.27.0
  - https://poedb.tw/us/Spell_Suppression
verification: unverified
---

# Defences (PoE1 3.30)

This file explains how each defence works and the order in which the game applies them to a hit. Constants match Path of Building's data (pinned PoB v2.67.2, tracking 3.29) plus the 3.27 to 3.30 patch notes we read. They are not confirmed in game for 3.30.

PoE2 differs; do not apply this there.

## The order a hit goes through

```
1. Avoidance        evasion (attacks), "avoid all damage from hits",
                    "avoid <type> damage from hits"
2. Block / suppress attack block or spell block; then, for spells,
                    spell suppression
3. "Taken as"       e.g. "physical damage taken as fire" moves part of
                    the hit to another type
4. Mitigation       per type: armour and physical damage reduction
                    (physical); resistances (elemental, chaos);
                    elemental damage reduction
5. Damage taken     increased/reduced damage taken, then "less damage
                    taken" (fortification, suppression's prevented share,
                    and others), each multiplying
6. Pools            damage taken by allies first (e.g. Frost Shield,
                    Soul Link style effects), guard skills, ward,
                    energy shield, Mind over Matter's mana share, life
```

Avoidance and block are all-or-nothing rolls: the hit either lands or it does not. Suppression is also a roll, but a suppressed hit still lands, reduced. Steps 3 to 5 shrink the hit. Step 6 decides which pool pays.

"Taken as" happens **before** mitigation. If 20% of physical is taken as fire, that 20% then meets your fire resistance, not your armour.

Damage over time skips steps 1 to 3 (no evasion, block, suppression or armour). It meets resistances, damage-over-time taken modifiers, then energy shield and life.

Since **3.29**, chance to "avoid all damage from hits" and chance to avoid damage of a specific type from hits are **additive** with each other (patch notes). Earlier they rolled separately.

## Armour

Armour reduces physical damage from hits. The reduction depends on the size of the hit.

```
reduction = A / (A + 5 x D)
A = your armour, D = the raw physical damage of the hit
capped at 90% physical damage reduction for players
```

Why armour is weak against big hits: for 50% reduction you need armour equal to five times the hit. A hit of 2,000 needs 10,000 armour for 50%. A hit of 20,000 needs 100,000. Against many small hits, the same armour does much more.

Armour's reduction adds to other "physical damage reduction" (endurance charges, some flasks and passives) before the 90% cap. Some effects let a share of your armour also apply to elemental hits; the formula is the same, computed for that type.

Armour never affects damage over time (bleeding, physical degens).

## Evasion

Evasion gives a chance for an enemy's attack to miss. It does nothing against spells unless a modifier says it does.

```
chance to be hit = 125 x acc / (acc + (E / 5)^0.9)    in %, clamped 5% to 100%
acc = attacker's accuracy, E = your evasion rating
evade chance = 100% - chance to be hit                 (so at most 95%)
```

**Entropy:** for players, evasion is not a fresh random roll each time. The game keeps a running counter that makes evades happen at a steady rate (for example, about every other hit at 50%). Long streaks of hits or evades do not happen.

Evasion against critical strikes: a crit from an enemy must pass the accuracy check a second time, so evasion lowers how often you take crits. This is long-standing PoE1 behaviour; not confirmed for 3.30.

## Block

Block stops all damage from a hit. Blocked hits do not apply on-hit effects such as ailments.

- **Attack block** and **spell block** are separate chances.
- Both have a default maximum of 75%. Modifiers can raise the maximum, to a hard cap of 90%.
- Block chance comes mostly from shields, dual wielding (a small inherent amount), staves and passives.
- Some keystones change block (for example Glancing Blows, where blocked hits deal part of their damage). Read their text through the tools.

3.30 change: Gladiator's shield block notable gives less block than before (patch notes; value through the tools).

## Spell suppression

Suppression works only against spell hits (and the ailments those hits apply).

```
suppressed spell hit: damage x (1 - P)
P = 40% by default, raised by "prevent +X% of suppressed spell damage"
suppression chance is capped at 100%
```

Changed in **3.27**: the base prevented share is now **40%** (previously 50%). Ailments inflicted by a suppressed hit are reduced by the same share.

Suppression is rolled after spell block. A blocked spell is not also suppressed.

## Resistances

Each resistance reduces damage of its type, from hits and over time.

```
damage taken = damage x (1 - R / 100)
R = your resistance, after max-res cap, floored at -200%
```

- **Maximum resistance:** 75% by default for fire, cold, lightning and chaos. "+X% to maximum resistance" raises it. Hard cap 90%.
- Resistance above the maximum is "overcapped". It does nothing until something lowers your resistance (curses, exposure), then it acts as a buffer.
- **Campaign penalties:** -30% to all four resistances after the first Kitava fight (Act 5), -60% in total after Act 10. Most endgame math assumes -60%.
- **Penetration** applies only to the attacker's hits; it lowers your resistance for that hit only, and does not show on your sheet.
- Negative resistance increases damage taken.

**Elemental damage reduction** is separate from resistance: it is a "less damage taken" style reduction for elemental hits, combined after resistances.

## Endurance charges and fortification

- **Endurance charges** (base maximum 3): each gives 4% physical damage reduction and 4% elemental damage reduction (PoB's character constants). Older guides say "+4% to all elemental resistances"; the current data say elemental damage reduction. When that changed, and whether it holds in 3.30, is not confirmed.
- **Fortification**: each point gives 1% less damage taken from hits. The base maximum is 20. Fortification is gained mostly from melee hits and decays over time. 3.30: Champion's Fortitude gives 20 fortification (was 15).

## Ward

Ward is a pool that takes the damage of a hit before energy shield and life.

- A hit removes ward up to its value; the rest of the hit continues.
- When ward takes damage it breaks and is restored after a short delay (base 2 s, modifiable).
- Ward does not take damage over time.
- Ward comes from specific bases and modifiers; it does not scale with armour or energy shield modifiers.

## Pools: energy shield, Mind over Matter, life

- **Energy shield** takes damage before life. In PoE1, chaos damage does not bypass energy shield by default; some effects make part of a damage type bypass it. PoE2 differs; do not apply this there.
- **Mind over Matter** (keystone): a share of the damage that would go to life is taken from mana instead. Unreserved mana is the pool. Read the share through the tools.
- **Life** is last. Some effects make life loss happen over time instead of at once (for example Petrified Blood style effects); this changes recovery windows, not the hit's size.
- 3.28: Intelligence gives 1% increased maximum energy shield per 10 Intelligence (previously per 5).

## Effective HP and max hit

**Max hit** of a type is the largest single hit of that type you can survive. It reverses steps 3 to 6: take your total pool for that type, then divide by the share of damage you take after mitigation and "damage taken" modifiers.

```
max hit ~ pool / (1 - mitigation) / (damage taken multiplier)
```

Armour makes this non-linear, because its reduction falls as the hit grows. Tools solve it by search.

**Effective HP** spreads that idea over many hits. It counts avoidance (evasion, block, suppression) as expected values. EHP is good for comparing builds; it hides the risk of an unlucky streak (except where entropy smooths evasion).

When quoting either number, say which assumptions the tool used: enemy damage type mix, boss settings, penetration, and which conditional buffs were on.

## Common mistakes

- Treating armour as a flat percentage. It depends on hit size; quote it for a stated hit.
- Using evasion against spells. It does not apply unless a modifier says so.
- Adding suppression to spell block. They are separate steps; suppression does not stop the hit.
- Using the old 50% suppression value. It is 40% since 3.27.
- Applying "taken as" after resistances. It is before mitigation.
- Forgetting the -60% campaign penalty when checking capped resistances.
- Saying overcapped resistance reduces damage. It only protects against resistance reduction.
- Letting armour reduce bleeding or other damage over time.
- Rolling "avoid all damage" and "avoid type damage" separately. Since 3.29 they add.
- Applying PoE2 rules (armour vs elemental, chaos vs energy shield, evasion and deflection).

## Check with the engine

- Exiled Studio's calc result computes armour, evasion, energy shield, the four resistances (with the campaign penalty from the config), attack block, spell block and spell suppression chance. Read those fields and their breakdowns for a sheet-value question.
- Max hit, EHP, and the per-hit damage-taken walk are not computed fields as of v0.9 (not confirmed; check the field list). If missing, say so, compute with the formulas above, and point to PoB's defence breakdown as the reference.
