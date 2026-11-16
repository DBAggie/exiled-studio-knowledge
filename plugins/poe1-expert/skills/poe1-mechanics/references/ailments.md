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
  - https://poedb.tw/us/Scorch
  - https://poedb.tw/us/Ignite
  - https://poedb.tw/us/Bleeding
verification: unverified
---

# Ailments (PoE1 3.30)

Ailments are debuffs that a hit can apply. There are two families:

- **Damaging ailments:** ignite (fire), bleeding (physical), poison (physical and chaos). They deal damage over time.
- **Non-damaging ailments:** chill, freeze, shock (the classic three), and scorch, brittle, sap (the "alternative" three). They change how the target behaves or how much damage it takes.

Ignite, chill, freeze, shock, scorch, brittle and sap are the **elemental ailments**. Bleeding and poison are not elemental.

The constants below match Path of Building's data (pinned PoB v2.67.2, which tracks 3.29). No patch from 3.26 to 3.30 changed them in the notes we read. They are not confirmed in game for 3.30.

PoE2 differs; do not apply this there.

## Damaging ailments: base damage

A damaging ailment takes the damage of the hit that applied it, of the matching types only, and turns a share of it into damage per second.

```
ignite DPS   = 90% of the hit's fire damage per second         base duration 4 s
bleeding DPS = 70% of the hit's physical damage per second     base duration 5 s
poison DPS   = 30% of the hit's physical + chaos damage per s  base duration 2 s
```

"The hit's damage" here is the hit's damage of those types after conversion, scaled only by modifiers that apply to the ailment (next section). It is not the damage the hit dealt after the enemy's resistances or armour. The ailment then meets the enemy's resistances itself, as damage over time.

Conversion matters: fire that came from converted physical counts as fire for ignite, not as physical for bleeding. Some modifiers let other types apply an ailment (for example "your cold damage can ignite"); then that type's damage is added to the ailment's base.

## Damaging ailments: what scales them

A modifier applies to an ailment only if it can apply to damage over time from that source. In practice:

Applies:
- Generic "increased damage" and "more damage" (unless the text says "with hits").
- The damage type: fire damage for ignite, physical for bleeding, physical or chaos for poison. Elemental damage for ignite.
- "Damage over time", the matching "X damage over time", and the matching "damage over time multiplier".
- The ailment by name: "increased ignite damage", "burning damage" (ignite is burning), "bleeding damage", "poison damage".
- Keyword modifiers carried from the skill: "damage with attack skills", "damage with spell skills".
- Weapon-type modifiers on an attack, such as "increased damage with swords" (but not ones that say "with hits").
- "Damage with ailments".

Does not apply:
- "Damage with hits", "attack damage", "spell damage", "melee damage", "projectile damage", "area damage". These carry a hit or delivery flag that a damage-over-time effect does not have.
- Critical strike multiplier (see below).
- Penetration. It applies to hits only. Lowering the enemy's resistance (curses, exposure, scorch) does work.

This list is how PoB's modifier flags work (an ailment's flags are damage-over-time, ailment, the weapon types, and the skill's keywords). Check a doubtful line by its exact wording.

## Critical strikes and ailments

A damaging ailment from a crit does **not** use your critical strike multiplier. It gets a flat +50% to damage-over-time multiplier instead (a character constant). Perfect Agony changes this rule; read its text through the tools.

Crits always apply ignite, chill, freeze and shock when the hit has the needed damage. They do not guarantee bleeding, poison, scorch, brittle or sap.

## Stacking

- **Poison:** every poison is its own instance. All of them deal damage at once. No cap by default.
- **Ignite:** only the strongest ignite on a target deals damage. Some effects let ignites stack (check the item or passive text).
- **Bleeding:** only the strongest bleed deals damage. Crimson Dance and some unique effects let bleeding stack up to a set number; those stacks follow their own rules (read the text through the tools).
- **Moving targets** take extra bleeding damage. **Aggravated** bleeding deals that extra damage even when the target stands still. The exact multipliers come from data, not from this file.

## Duration and "faster"

Three kinds of modifier change an ailment's timing. They are easy to mix up.

```
increased duration      -> lasts longer, same DPS, more total damage
deals damage X% faster  -> DPS x (1 + X/100), duration / (1 + X/100),
                           same total damage, delivered sooner
debuff expires slower   -> lasts longer, same DPS (like duration)
```

"Faster" matters most against enemies that die or cleanse before the ailment ends, and for ignite and bleed, where only the strongest one counts at any moment.

## Chance to apply

- **Chill:** any hit that deals cold damage chills, if the effect is high enough (see thresholds).
- **Ignite, freeze, shock:** need a chance on the skill or gear, or a crit. Some sources make hits always apply one (3.30: Elementalist's Shaper of Flames and Shaper of Storms now give "always ignite" and "always shock").
- **Bleeding, poison:** need a chance. A crit does not guarantee them.
- **Scorch, brittle, sap:** need their own chance modifiers.

Chance to apply is rolled per hit. A chance above 100% does nothing more.

## Ailment threshold

Non-damaging ailments scale with how big the hit is compared to the target's **ailment threshold**.

- For most monsters the threshold equals their maximum life.
- Many bosses have a threshold lower than their life, so ailments land better on them than their life suggests. Some also have reduced ailment effect on them. Look this up per boss.
- For players, the threshold is maximum life unless a modifier says otherwise (whether energy shield counts is not confirmed here).

In the formulas, `D` is the hit's damage of the ailment's type and `T` is the target's threshold.

## Non-damaging ailment formulas

```
chill   effect = 50%  x (D/T)^0.4   min 5%, max 30%   base 2 s   slows action speed
shock   effect = 50%  x (D/T)^0.4   min 5%, max 50%   base 2 s   increased damage taken
scorch  effect = 50%  x (D/T)^0.4             max 30% base 4 s   lower elemental resistances
brittle effect = 10%  x (D/T)^0.4             max 6%  base 4 s   + crit chance against it
sap     effect = 33.3% x (D/T)^0.4            max 20% base 4 s   less damage dealt
```

Then multiply by your "increased/more effect of X" and the target's "reduced effect of X on you". Then cap at the maximum. Below the minimum (chill, shock) the ailment is not applied.

Freeze uses duration, not effect:

```
freeze duration = 0.06 s per 1% of threshold dealt as cold   (so 5% -> 0.3 s)
minimum 0.3 s (below this, no freeze), maximum 3 s
```

Freeze duration modifiers multiply the result. A frozen target cannot act.

Notes:
- Only the strongest instance of each non-damaging ailment applies (shock does not stack by default).
- The 30% chill and 50% shock caps can be raised by specific modifiers; check the text.
- Some sources apply a fixed value instead of the formula (for example "chill for 10%", some ground effects, fixed scorch on certain items). Those ignore the threshold.
- The coefficients for scorch, brittle and sap above come from PoB's calc code; the in-game numbers for 3.30 are not confirmed.

## Avoidance and immunity

Your own defences against ailments, from strongest to weakest:

1. **Immunity / "cannot be X"**: the ailment never lands. Flasks with an "immune" suffix, Pantheon powers, and some keystones and uniques give this.
2. **Avoid chance** ("X% chance to avoid being frozen"): rolled per application. 100% is full avoidance.
3. **Reduced effect on you**: scales the non-damaging effect down.
4. **Reduced duration on you** or "expires faster": shortens it. For damaging ailments this lowers their total damage, not their DPS.
5. **Resistances** reduce ignite and poison damage taken (as damage over time). Armour does nothing against any ailment damage.
6. **Spell suppression**: a suppressed spell hit also has the damaging ailments it applies reduced by the same prevented share. Since **3.27** the base share is 40% (it was 50%).

Removing an ailment: flasks with a matching suffix, and some passives, remove ailments on use. 3.30: Pathfinder's Master Alchemist now removes all ailments, not only elemental ones.

## Common mistakes

- Adding crit multiplier to ignite, bleed or poison. They get +50% DoT multiplier from a crit, not the crit multiplier (except with Perfect Agony).
- Counting "spell damage", "attack damage", "melee damage", "area damage" or "damage with hits" towards ailments. They do not apply.
- Using penetration to scale ailments. Penetration is hits only.
- Thinking more duration raises DPS. It raises total damage only.
- Stacking ignite or bleed like poison. Only the strongest one deals damage, unless a named effect says otherwise.
- Computing chill or shock from the hit's total damage. Only the cold (chill, freeze, brittle), lightning (shock, sap) or fire (scorch) part counts.
- Treating a boss's threshold as its life. Many bosses have a lower threshold and reduced ailment effect.
- Using the old 50% suppression value. It is 40% since 3.27.
- Mixing in PoE2 rules (different ailment math, chaos vs energy shield, and so on).

## Check with the engine

- Exiled Studio's calc result (v0.9) computes hit damage, the enemy's damage taken with shock, and chill's effect on the enemy's damage. Read the enemy damage-taken part of the breakdown for a shock or chill question.
- Damaging ailment DPS (ignite, bleed, poison) is not a computed field in the engine as of v0.9 (not confirmed; check which fields the calc result lists). If it is missing, say so, use the formulas above, and point to PoB's ailment breakdown as the reference.
- Ailment threshold values come from game data (monster level tables); use the tools, not memory.
