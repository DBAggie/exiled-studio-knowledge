---
game: poe1
patch: 3.30.0
as_of: 2026-11-17
sources:
  - https://www.pathofexile.com/forum/view-thread/4013680
  - https://www.pathofexile.com/forum/view-thread/3985332
  - https://www.pathofexile.com/forum/view-thread/3913392
  - https://www.pathofexile.com/forum/view-thread/3869068
  - https://www.pathofexile.com/forum/view-thread/3531661
  - https://www.poewiki.net/wiki/Evasion
  - https://www.poewiki.net/wiki/Energy_shield
  - https://www.poewiki.net/wiki/Charge
  - https://github.com/PathOfBuildingCommunity/PathOfBuilding/blob/v2.67.2/src/Modules/CalcDefence.lua
  - https://github.com/PathOfBuildingCommunity/PathOfBuilding/blob/v2.67.2/src/Modules/Data.lua
  - https://github.com/PathOfBuildingCommunity/PathOfBuilding/blob/v2.67.2/src/Data/Misc.lua
  - repo:DBAggie/exiled-studio/crates/loom-calc/src/poe1/phases.rs
  - repo:DBAggie/exiled-studio/crates/loom-calc/src/poe1/charges.rs
verification: maintainer-approved
---

# Defences (PoE1 3.30)

This file explains how each defence works and the order in which the game applies them to a hit. Constants were checked against the pinned Path of Building 2.67.2 and the official 3.25.0 to 3.30.x notes (see Verification at the end). They are not checked in game.

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

Since **3.29.0**, chance to "avoid all damage from hits" and chance to avoid damage of a specific type from hits are **additive** with each other (official 3.29.0 notes, Player Changes). Earlier they rolled separately.

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

Evasion against critical strikes: a crit from an enemy attack must pass the accuracy check a second time; if it fails, you take a normal hit instead. So evasion lowers how often you take attack crits. This second check is a plain random roll, outside the entropy counter. Spell crits ignore evasion. (poewiki's evasion page; PoB 2.67.2 multiplies the enemy's crit chance by your chance to evade it the same way. No 3.26 to 3.30 note changes it.)

## Block

Block stops all damage from a hit. Blocked hits do not apply on-hit effects such as ailments.

- **Attack block** and **spell block** are separate chances.
- Both have a default maximum of 75%. Modifiers can raise the maximum, to a hard cap of 90%.
- Block chance comes mostly from shields, dual wielding (a small inherent amount), staves and passives.
- Some keystones change block (for example Glancing Blows, where blocked hits deal part of their damage). Read their text through the tools.

3.30.0 lowered the Ascendant's Gladiator node (block chance taken from the shield) **in Ruthless only**; outside Ruthless nothing changed for block.

## Spell suppression

Suppression works only against spell hits (and the ailments those hits apply).

```
suppressed spell hit: damage x (1 - P)
P = 40% by default, raised by "prevent +X% of suppressed spell damage"
suppression chance is capped at 100%
```

Changed in **3.27.0**: the base prevented share is now **40%** (previously 50%; official 3.27.0 notes, and PoB 2.67.2 uses 40). Ailments inflicted by a suppressed hit are reduced by the same share. 3.30.0 raised the Trickster's Spellbreaker to +20% prevented while on full energy shield (was +15%).

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

- **Endurance charges** (base maximum 3): each gives 4% additional physical damage reduction and 4% additional elemental damage reduction. The elemental part changed in **3.25.0** from +4% to all elemental resistances to elemental damage reduction (official 3.25.0 notes, Player Balance); guides from before 3.25 are out of date. No later note changes it; PoB 2.67.2's game data and poewiki agree. `charges.md` says the same.
- **Fortification**: each point gives 1% less damage taken from hits. The base maximum is 20 (game-data constants in PoB 2.67.2). Fortification is gained mostly from melee hits and decays over time. 3.30.0 raised Champion's Fortitude to 20 fortification (was 15) **in Ruthless only**.

## Ward

Ward is a pool that takes the damage of a hit before energy shield and life.

- A hit removes ward up to its value; the rest of the hit continues.
- When ward takes damage it breaks and is restored after a short delay (base 2 s, modifiable).
- Ward does not take damage over time.
- Ward comes from specific bases and modifiers; it does not scale with armour or energy shield modifiers.

## Pools: energy shield, Mind over Matter, life

- **Energy shield** takes damage before life. In PoE1, **chaos damage bypasses energy shield by default** and goes to life (poewiki); some effects stop that in part or in full (for example an energy shield mastery, Grasping Mail, or Esh's breach modifier). `recovery.md` says the same. PoE2 differs; do not apply this there.
- **Mind over Matter** (keystone): a share of the damage that would go to life is taken from mana instead. Unreserved mana is the pool. Read the share through the tools.
- **Life** is last. Some effects make life loss happen over time instead of at once (for example Petrified Blood style effects); this changes recovery windows, not the hit's size.
- 3.28.0: Intelligence gives 1% increased maximum energy shield per 10 Intelligence (previously per 5; official 3.28.0 notes, Player Changes).

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

The engine facts below were read from Exiled Studio's source (`crates/loom-calc`, dev branch at `b42e49f`, 2026-11-17; the 0.9 line). The engine follows Path of Building 2.67.2's order of operations and rounding, so a number the engine marks `complete` is PoB's number, apart from registered divergences. It computes 24 fields: `strength`, `dexterity`, `intelligence`, `life`, `mana`, `life-unreserved`, `mana-unreserved`, `energy-shield`, `armour`, `evasion`, `resistance.fire`, `resistance.cold`, `resistance.lightning`, `resistance.chaos`, `block-chance`, `spell-block-chance`, `spell-suppression-chance`, `average-damage`, `speed`, `hit-speed`, `hit-chance`, `crit-chance`, `crit-multiplier` and `hit-dps`. The hit fields exist only when the main skill is a self-cast spell hit or a main-hand attack: not channelled, triggered, a totem, trap, mine, minion or brand skill, not a skill with a cooldown, and not dual wielding. For any other main skill they are `not-computed`.

- Computed, each with a breakdown: `armour`, `evasion`, `energy-shield`, `resistance.fire`, `resistance.cold`, `resistance.lightning`, `resistance.chaos` (with the campaign penalty from the config, and the capped value), `block-chance`, `spell-block-chance` and `spell-suppression-chance`. Armour, evasion and energy shield show a row per equipment slot.
- **Not computed, and no field exists**: max hit, effective HP, physical damage reduction against a hit, damage taken, endurance charge and fortification effects, ward, and anything about recovery. Never read their absence as zero.
- For those, compute with the formulas above or use PoB's defence breakdown, and say which.

## Verification (2026-11-17)

`engine-checked` here means: the armour and hit chance formulas (`CalcDefence.lua`), the caps (90% physical damage reduction, 95% evade, 75% default and 90% hard block and resistance caps, -200% resistance floor, 40% suppression; `Modules/Data.lua`), the -30%/-60% campaign penalty, fortification and endurance charges (game-data constants in `Data/Misc.lua`) were checked against the pinned Path of Building 2.67.2 and the official 3.25.0 to 3.30.x notes. poewiki was used for the crit second check and for chaos damage and energy shield. Not checked in game.

Approved by the maintainer on 2026-11-17 (given in chat, recorded by the session). The checks named above are what was done before approval; nothing here was checked in game unless a line says so.
