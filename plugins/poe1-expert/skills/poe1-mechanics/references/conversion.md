---
game: poe1
patch: 3.30.0
as_of: 2026-11-15
sources:
  - https://poedb.tw/us/Version_3.27.0
  - https://poedb.tw/us/Version_3.28.0
  - https://poedb.tw/us/Version_3.29.0
  - https://patchbot.io/games/path-of-exile/articles/2188-content-update-3300-path-of-exile-covens-of-umbra
verification: unverified
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

1. **Skill conversion**: conversion granted by the active skill itself (for example, an attack that converts half its physical damage to lightning).
2. **Other conversion**: everything else, such as supports, gear, the passive tree, auras and ascendancy nodes.

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

Which group a given support or item stat belongs to is decided by the stat, not by where it sits. Look up the stat when it matters; do not guess from the source.

## "Gained as extra"

"X% of Physical Damage as Extra Fire Damage" adds new damage of the target type. It does **not** remove anything from the source type.

- It is not limited by the 100% cap. Gains can total more than 100%.
- It is based on the full amount of the source type at that step (its base plus what was converted into it), not on the part left after conversion.
- The gained damage becomes part of the target type and moves on along the chain with it, so it can be converted or gained again further on, as Path of Building models it.

## Which modifiers apply to converted damage

Converted and gained damage **remembers every type it was** on the way. It is affected by modifiers to each of those types, plus its current type.

- Physical converted to fire is affected by increased physical, increased fire and increased elemental damage.
- Physical converted straight to cold, skipping lightning, is not affected by lightning modifiers.
- Each modifier still counts once. A mod that names two types the damage passed through is not counted twice.
- Increases from every type it passed through go into the **one** increased pool (they sum). More multipliers for those types each multiply.

This is why conversion builds like "increased physical damage" mods: they keep working after the damage becomes elemental.

What does **not** carry over: effects that care about the final type only. Resistance, penetration, armour and elemental ailments use the type the damage ends as. Physical converted to cold is mitigated by cold resistance, not armour, and it can freeze and chill.

## Monsters (3.27 change)

The 3.27 notes say monster physical-to-elemental conversion scaling was reworked. On high-level monsters that already convert most or all of their physical damage, "physical as extra elemental" on those monsters now has far less effect. This changes enemy damage, not yours.

## Patch notes checked

- No general change to the conversion order, the 100% cap, or "gained as extra" was found in the 3.26 to 3.30 notes (the parts read; some pages were long and not read in full, so this is not confirmed for 3.30). Individual skills and items changed their own conversion values; look those up.
- 3.30 fixed a rounding bug in damage-taken conversion that let a small part of the original type through. That concerns defence, not the damage you deal.

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

The Exiled Studio average damage field breaks hit damage down per damage type, with a provenance graph. For a skill with modelled conversion, expand a type's node to see its converted share, the share the source type keeps, and which type modifiers entered its increased sum. Conversion and gain beyond a vetted skill's own conversion may show as a "not modelled" reason; when it does, the engine cannot confirm the number yet and the answer rests on this file.
