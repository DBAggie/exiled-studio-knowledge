---
game: poe1
patch: 3.30.0
as_of: 2026-11-17
sources:
  - https://www.pathofexile.com/forum/view-thread/4013680
  - https://www.pathofexile.com/forum/view-thread/4015085
  - https://www.pathofexile.com/forum/view-thread/3985332
  - https://www.pathofexile.com/forum/view-thread/3913392
  - https://www.pathofexile.com/forum/view-thread/3869068
  - https://www.pathofexile.com/forum/view-thread/3787013
  - https://www.poewiki.net/wiki/Leech
  - https://www.poewiki.net/wiki/Recoup
  - https://github.com/PathOfBuildingCommunity/PathOfBuilding/blob/v2.67.2/src/Data/Misc.lua
  - https://github.com/PathOfBuildingCommunity/PathOfBuilding/blob/v2.67.2/src/Modules/CalcOffence.lua
  - https://github.com/PathOfBuildingCommunity/PathOfBuilding/blob/v2.67.2/src/Modules/CalcDefence.lua
verification: unverified
---

# Recovery in PoE1

Recovery covers every way life, mana, and energy shield (ES) come back: regeneration, leech, recoup, ES recharge, gain on hit or kill, and flasks (flasks have their own file, `flasks.md`). This file explains the rules. Numbers on specific items, gems, and passives come from the knowledge MCP.

## Two families: instant and over time

- **Instant recovery** applies the full amount at once. Life gained on hit, life gained on kill, and the instant part of leech or flasks are instant.
- **Recovery over time** applies an amount spread across a period. Regeneration, leech, recoup, ES recharge, and non-instant flasks are over time.

The split matters because "recovery rate" modifiers act only on recovery over time (see below).

## Regeneration

- Regeneration restores a fixed amount or a percentage of the maximum every second, all the time.
- Players have no base life regeneration. It comes from modifiers, passives, auras, and so on.
- Players have a base mana regeneration of **1.75% of maximum mana per second** (the game-data character constant PoB 2.67.2 reads is 105% per minute). No 3.26 to 3.30 note changes it.
- ES regeneration also comes only from modifiers. It is separate from ES recharge.
- Flat regeneration ("Regenerate X Life per second") and percentage regeneration ("Regenerate X% of Life per second") add together before rate modifiers.

```
regen per second = (flat regen + percent regen x maximum) x (1 + increased regeneration rate) x (1 + increased recovery rate) x more multipliers
```

- "Increased life regeneration rate" scales only regeneration.
- "Increased life recovery rate" scales all life recovery over time, regeneration included.

## Degeneration and the net change

- Damage over time (burning, poison, bleeding, Righteous Fire, and so on) and regeneration run at the same time.
- The game combines them into one net change per resource each second. If regeneration exceeds degeneration the pool rises; otherwise it falls.
- Damage over time is never a hit. It cannot be evaded, blocked, or dodged. It is reduced by resistances (elemental and chaos) and by "damage taken" modifiers; armour does not reduce physical damage over time.
- Damage over time hits ES before life, except chaos damage, which bypasses ES by default.
- Some keystones change which pool regeneration applies to (for example Zealot's Oath turns life regeneration into ES regeneration). Look up the current keystone text before answering.

## Leech

Leech recovers a resource from damage you deal with hits.

### How an instance is made

- Each hit that leeches creates a **leech instance** for each resource it leeches.
- The instance's total is the leech percentage times the damage the hit actually dealt to the enemy (after the enemy's mitigation). Damage over time does not leech unless a modifier says so.
- An instance recovers its total over time at a fixed rate based on **your** maximum pool, not on the damage.

```
instance total   = leech % x damage dealt by the hit   (capped, see below)
instance rate    = base rate (2% of your maximum per second) x (1 + increased leech rate)
instance duration = instance total / instance rate
```

- **Per-instance cap.** Each instance can recover at most 10% of your maximum of that pool by default (the game-data constants PoB reads give 10% for life, mana and ES alike; poewiki agrees for life). "Increased maximum recovery per life leech" raises it. 3.28 added unique effects that raise or double this cap (example: Bloodseeker, Essentia Sanguis).
- **Total rate cap.** All instances together cannot recover more per second than the maximum leech rate. The defaults are 20% of maximum life per second and 20% of maximum mana per second; ES leech has a lower default cap of **10% of maximum ES per second** (game-data constants in PoB 2.67.2; poewiki gives the same values). "Increased maximum total life recovery per second from leech" raises the cap.
- Because the rate depends on your maximum, a large pool leeches faster in flat terms. Big hits mostly make instances last longer; they do not make them faster.
- **Sources disagree on "increased total recovery per second from leech".** PoB 2.67.2 multiplies each instance's rate by it (the formula above, so instances also end sooner). poewiki says it raises the recovery you get without making an instance end sooner. The total per second is the same in both readings; only instance length differs. Not checked in game.

### When instances end

- An instance ends when it has recovered its total.
- By default every life leech instance is removed when your life is full. "Overleech" effects (for example "life leech effects are not removed when unreserved life is filled") keep the instances running, so they keep you topped up through incoming damage.
- Whether instances keep running after the enemy dies is **not confirmed**: neither the patch notes nor poewiki's leech page state it, and PoB does not model it.

### Instant leech

- "X% of leech is instant" makes that share of each instance apply at once, ignoring the rate. The rest leeches normally.
- 3.26 lowered the leech mastery's instant share (to 5%) and added Gore Dancer (Berserker) with a large instant share. 3.29 gave Deathmarked (Assassin) instant leech per maximum power charge. 3.30 made Atziri's Acuity's crit life leech instant, with a drawback that blocks life regeneration and recoup.

### Other leech rules

- Life, mana, and ES leech are separate instance sets with separate caps.
- 3.26 moved life and mana leech modifiers on equipment and jewels from prefixes to suffixes.
- Keystones and ascendancies can change leech heavily (Vaal Pact, Ghost Reaver, Slayer). Look up their current text.
- Enemies or map modifiers can make a target "cannot be leeched from".

## Recoup

- "X% of damage taken recouped as life" returns that share of the damage you took, spread over 4 seconds by default.
- Some modifiers make recoup happen over a shorter time (for example over 3 seconds). The total stays the same; it arrives faster.
- Recoup is based on damage taken from **hits** only, after mitigation (poewiki's recoup page). Damage over time is not recouped unless a modifier says so. Recoup instances are not removed when the pool is full.
- 3.30.0b Hotfix fixed a bug where "damage taken recouped as life" was not recovering life. The rule did not change.
- Recoup can target life, mana, or ES depending on the modifier. 3.29 raised abyssal jewel mana recoup; 3.30 gave Shavronne's Wrappings ES recoup; 3.27 added Shadowed Blood (Assassin) with physical damage recouped as life.
- "Increased life recovery rate" scales recoup: the same 4-second window recovers more (poewiki; PoB 2.67.2 multiplies the recoup percentage by the recovery rate modifier).

## Energy shield recharge

- ES recharge starts after a delay of **2 seconds** in which you took no damage.
- Once it starts, it restores **33.3% of maximum ES per second** by default (game-data constant: 2000% per minute; PoB uses 0.33) until ES is full or you take damage.
- Taking damage resets the delay and stops a running recharge. Damage over time also interrupts it.

```
recharge delay = 2 s / (1 + faster start of ES recharge)
recharge rate  = base rate x maximum ES x (1 + increased ES recharge rate) x (1 + increased ES recovery rate)
```

- "Faster start of energy shield recharge" shortens the delay. 3.29 added it on the Occultist's Unhallowed Rite; 3.30 moved it on unique and base amulets (example: Seaglass Amulet raised, Shavronne's Wrappings removed).
- Some effects start recharge at once (for example "chance for energy shield recharge to start when you block", or recharge on crit).
- Recharge is separate from ES regeneration and ES leech. All three can run together.

## Gain on hit and on kill

- "Gain X life per enemy hit" is instant and counts each enemy hit. A skill that hits many targets gains for each.
- For spells the stat is worded separately ("for each enemy hit by your spells"); attack and spell versions do not cross over.
- "Gain X life per enemy killed" and "recover X% of life on kill" are instant.
- 3.26 added higher tiers of life on hit, life on kill, and mana on kill modifiers.

## Recovery rate modifiers

- **"Increased life recovery rate"** speeds every life recovery over time: regeneration, leech, recoup and flask recovery. It does not change instant recovery. In PoB 2.67.2 it multiplies leech after the leech rate cap is applied, so it raises the most you can actually leech per second; the cap stat itself is unchanged. Not checked in game.
- **"Increased mana recovery rate"** and **"increased energy shield recovery rate"** do the same for their pools; ES recovery rate also speeds ES recharge.
- **Pool-specific rates** ("increased life regeneration rate", "increased life leech rate", "increased ES recharge rate") scale only their own source.
- 3.30.0 replaced the Pathfinder's Master Surgeon drawback with a life flask recovery rate penalty instead of a penalty to life recovered from flasks. The wording difference is exactly the rate vs amount difference.

## Common mistakes

- Treating leech as proportional to damage in speed. Damage sets the instance size; your maximum pool sets the speed.
- Forgetting the leech rate cap. Adding leech percentage past the cap gives nothing in sustained fights.
- Assuming leech continues at full life. Without overleech it stops.
- Saying recovery rate speeds life gained on hit. It does not; that recovery is instant.
- Mixing "increased regeneration rate" with "increased recovery rate". They are different stats and multiply.
- Expecting ES recharge while standing in a degen. Damage over time interrupts it.
- Saying chaos damage over time hits ES first. It bypasses ES by default.
- Using PoE2 rules. PoE2 differs (leech, recoup, and ES recharge behave differently there); do not apply this there.

## Check with the engine

- Regeneration totals: the calc's life, mana, and ES regeneration breakdown, with each source.
- Leech: the per-instance rate, the per-instance cap, and the total leech rate cap for each pool, and whether a build reaches the cap.
- ES recharge: the recharge delay and recharge per second fields.
- Recoup: the recoup percentages per pool and the recoup duration.
- Where the engine marks a field `not-computed` or `Partial`, say the answer comes from the rules here, not from the calc.

## Verification (2026-11-17)

Checked against the official 3.26.0 to 3.30.x notes (3.30.x read in full), poewiki's leech and recoup pages, and the pinned Path of Building 2.67.2 (game-data constants in `Data/Misc.lua`; leech in `CalcOffence.lua`; recoup in `CalcDefence.lua`). Still `unverified`: whether leech keeps running after the target dies is not confirmed by any source.
