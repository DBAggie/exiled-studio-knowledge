---
game: poe1
patch: 3.30.0
as_of: 2026-11-17
sources:
  - https://www.pathofexile.com/forum/view-thread/3787013
  - https://www.pathofexile.com/forum/view-thread/3869068
  - https://www.pathofexile.com/forum/view-thread/3913392
  - https://www.pathofexile.com/forum/view-thread/3985332
  - https://www.pathofexile.com/forum/view-thread/4013680
  - https://www.poewiki.net/wiki/Damage_conversion
  - https://github.com/PathOfBuildingCommunity/PathOfBuilding/blob/v2.67.2/src/Modules/CalcOffence.lua
  - repo:DBAggie/exiled-studio/crates/loom-calc/src/poe1/hit.rs
verification: engine-checked
---

# Damage conversion and "gained as extra" (PoE1)

This covers damage you deal. "Damage taken as" (your defences) is a different mechanic and is not covered here.

PoE2 has conversion too, with different rules. Do not apply this file there.

## The chain

Damage types sit in a fixed order:

```
physical -> lightning -> cold -> fire -> chaos
```

- Damage can only move **forward** (to the right) along this chain. Cold can become fire or chaos; fire can never become cold.
- A step may skip types: physical can convert straight to fire or chaos.
- Chaos is the end of the chain. Nothing converts chaos damage you deal into another type.
- A type is processed once, in chain order. Everything that reached it (its own base, plus what was converted or gained into it) is then converted or gained onward together.

## When conversion happens

Conversion and gain happen **after** flat added damage joins the base and **before** any increased or more modifier.

So added physical damage on gear converts with the rest of your physical damage. A spell's base fire damage and your added fire damage both move if you have fire-to-chaos conversion.

## Skill conversion first, then everything else

Conversion comes in two groups:

1. **Skill conversion**: conversion from the active skill gem itself, from support gems linked to it, and from lines that name a specific skill (for example "X% of Manabond and Stormbind Lightning Damage Converted to Cold Damage").
2. **Other conversion**: everything else, such as gear, the passive tree, auras, buffs and ascendancy nodes.

For each source type:

```
skill = sum of skill conversion from this type
if skill > 100%: scale each skill conversion so they total 100%
remaining = 100% - skill
other = sum of other conversion from this type
if other > remaining: scale each other conversion so they total remaining
kept = 100% - skill - other   (the part that stays this type)
```

- If the skill already converts 100% of a type, conversion from gear or tree does nothing for that type.
- When a group is over its limit, each source in it is scaled down by the same factor, so the split keeps its ratios.

Which group a line belongs to is decided by its stat. In PoB the skill group is the `Skill...ConvertTo...` stats, which the gem's own conversion and skill-named lines use. The wiki also puts support gem conversion in the skill group. If a case matters, look up the stat; do not guess from the source.

## "Gained as extra"

"X% of Physical Damage as Extra Fire Damage" adds new damage of the target type. It does **not** remove anything from the source type.

- It is not limited by the 100% cap. Gains can total more than 100%.
- It is based on the full amount of the source type at that step (its base plus what was converted into it), not on the part left after conversion. Within each source type, the gain is worked out before that type's conversion takes anything away.
- The gained damage becomes part of the target type and moves on along the chain with it, so it can be converted or gained again further on. PoB models it this way, and the wiki describes the same order (so a "non-chaos as extra chaos" line can apply once per type the damage passes through). Not checked in game.

## Which modifiers apply to converted damage

Converted and gained damage **remembers every type it was** on the way. It is affected by modifiers to each of those types, plus its current type.

- Physical converted to fire is affected by increased physical, increased fire and increased elemental damage.
- Physical converted straight to cold, skipping lightning, is not affected by lightning modifiers.
- Each modifier still counts once. A mod that names two types the damage passed through is not counted twice.
- Increases from every type it passed through go into the **one** increased pool (they sum). More multipliers for those types each multiply.

This is why conversion builds like "increased physical damage" mods: they keep working after the damage becomes elemental.

What does **not** carry over: effects that care about the final type only. Resistance, penetration, armour and elemental ailments use the type the damage ends as. Physical converted to cold is mitigated by cold resistance, not armour, and it can freeze and chill.

## Monsters (3.27 change)

The official 3.27.0 notes (Monster Changes) say the way monsters that convert physical to elemental damage scale with monster and map modifiers that grant "physical as extra element" was reworked. On high-level monsters that already convert most or all of their physical damage, those modifiers now have far less effect. This changes enemy damage, not yours. A 3.27.0c fix also stopped your own effects that convert a monster's physical damage to an element from raising that element's damage.

## Patch notes checked

- No general change to the conversion order, the 100% cap, or "gained as extra" is in the official 3.26.0 to 3.30.0 notes. The 3.30.x posts (3.30.0 and every hotfix to 3.30.0b Hotfix 4) were read in full; the 3.26.0 to 3.29.0 posts were searched for every line about conversion or "as extra". Individual skills, items and monsters changed their own values (3.29 Void Sphere and Voltaxic Burst, 3.28 Spectres losing a hidden elemental bonus); look those up.
- 3.30.0 fixed a rounding bug in damage-taken conversion that let a small part of the original type through. That concerns defence, not the damage you deal.

## Worked example

An attack, numbers chosen for the example only:

- 100 physical damage after flat added damage
- the skill converts 50% physical to lightning (skill conversion)
- gear converts 60% physical to cold (other conversion)
- 20% of physical damage gained as extra fire
- 50% increased physical, 30% increased lightning, 20% increased cold, 40% increased elemental

Conversion from physical:

```
skill:  50% to lightning              (under 100%, no scaling)
other:  60% to cold, but only 50% remains -> scaled to 50%
kept:   0% stays physical
gain:   20% of the full 100 physical -> 20 extra fire
```

Damage after the step: 0 physical, 50 lightning, 50 cold, 20 fire.

Increased pools:

```
lightning (was physical): 1 + 0.50 + 0.30 + 0.40 = 2.20 -> 50 x 2.20 = 110
cold (was physical):      1 + 0.50 + 0.20 + 0.40 = 2.10 -> 50 x 2.10 = 105
fire (gained from phys):  1 + 0.50 + 0.40        = 1.90 -> 20 x 1.90 = 38
total                                                                 = 253
```

The cold part does not get the lightning increase, because it never was lightning.

## Common mistakes

- Converting backward along the chain (fire to cold, or anything to physical).
- Adding skill and gear conversion together and scaling both. Skill conversion takes its share first; only the other group is scaled down.
- Thinking "gained as extra" reduces the source type or counts toward the 100% cap.
- Computing a gain from the leftover after conversion instead of the full source amount.
- Applying increases before conversion, or forgetting that converted damage still uses the source type's increases.
- Applying armour to physical damage that was converted away, or cold resistance to cold that was converted on to fire.
- Using PoE2 conversion rules. PoE2 differs; do not apply this there.

## Check with the engine

The engine facts below were read from Exiled Studio's source (`crates/loom-calc`, dev branch at `b42e49f`, 2026-11-17; the 0.9 line). The engine follows Path of Building 2.67.2's order of operations and rounding, so a number the engine marks `complete` is PoB's number, apart from registered divergences. It computes 24 fields: `strength`, `dexterity`, `intelligence`, `life`, `mana`, `life-unreserved`, `mana-unreserved`, `energy-shield`, `armour`, `evasion`, `resistance.fire`, `resistance.cold`, `resistance.lightning`, `resistance.chaos`, `block-chance`, `spell-block-chance`, `spell-suppression-chance`, `average-damage`, `speed`, `hit-speed`, `hit-chance`, `crit-chance`, `crit-multiplier` and `hit-dps`. The hit fields exist only when the main skill is a self-cast spell hit or a main-hand attack: not channelled, triggered, a totem, trap, mine, minion or brand skill, not a skill with a cooldown, and not dual wielding. For any other main skill they are `not-computed`.

- `average-damage` breaks hit damage down per damage type. The engine builds PoB's conversion table: the skill's own conversion first (scaled to 100% if above), then other conversion of one type to a later one, scaled into what is left.
- Not mapped: "elemental damage converted to" and "non-chaos damage converted to" style lines, and "gained as extra". A build with those gets `partial` hit fields with a reason; the engine cannot confirm that number and the answer rests on this file and PoB.
- Converted damage is computed with both types' modifiers, as described above; expand a type's node to see its converted share and the share the source keeps.

## Verification (2026-11-17)

`engine-checked` here means: the order, the 100% scaling with skill conversion first, and "gained as extra" were checked against the pinned Path of Building 2.67.2 (`CalcOffence.lua`, the conversion table and `calcDamage`) and against the official 3.26.0 to 3.30.x notes; poewiki's conversion page agrees with PoB on every point. The worked example was recomputed. Not checked in game.
