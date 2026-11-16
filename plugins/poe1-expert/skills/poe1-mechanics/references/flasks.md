---
game: poe1
patch: 3.30.0
as_of: 2026-11-15
sources:
  - https://patchbot.io/games/path-of-exile/articles/2188-content-update-3300-path-of-exile-covens-of-umbra
  - https://poedb.tw/us/Version_3.29.0
  - https://poedb.tw/us/Version_3.27.0
  - https://poedb.tw/us/Version_3.26.0
verification: unverified
---

# Flasks and tinctures in PoE1

A character has five flask slots on the belt. Each flask holds charges, spends a fixed number per use, and refills from kills and other sources. Base values (charges, recovery amounts, durations) are item data; look them up with `get_base` and `get_unique`.

## Flask kinds

- **Life flasks** recover life.
- **Mana flasks** recover mana.
- **Hybrid flasks** recover both, with smaller amounts of each than a dedicated flask of the same level.
- **Utility flasks** grant a timed buff (for example Granite for armour, Quicksilver for movement speed, the elemental resistance flasks, Bismuth, Diamond, Amethyst). They recover nothing.
- **Unique flasks** follow their own text. Treat each as its own rule set and read its current text from the knowledge MCP; never assume it behaves like its base type.

## Life and mana flask recovery

- A recovery flask restores its amount over its duration, not at once, unless a modifier makes some or all of it instant.

```
recovered        = base amount x (1 + increased recovery from flasks) x more multipliers
duration         = base duration / (1 + increased flask recovery rate) x (1 + increased flask effect duration)
recovery per sec = recovered / duration
```

- **"Increased life recovery from flasks"** raises the amount.
- **"Increased flask life recovery rate"** and **"increased life recovery rate"** make the same amount arrive faster.
- **"Increased flask effect duration"** on a recovery flask spreads the same amount over a longer time (slower).
- 3.30 changed the Pathfinder's Master Surgeon drawback from a cut to life recovered from flasks into a cut to life flask recovery rate: same total, slower delivery.
- **Instant recovery.** Some modifiers make a share instant, make all of it instant at reduced value, or make it instant only at low life. The instant part ignores recovery rate.
- **Stacking.** Using a recovery flask again while it is still recovering adds another instance; recovery from separate uses runs at the same time (believed; not confirmed for 3.30).
- **"Flask effect"** (increased effect of flasks) does **not** raise the amount a life or mana flask recovers. It scales buffs a flask grants.

## Utility flasks

- Using a utility flask applies its buff for its duration.
- A utility flask cannot be used again while its own effect is active. It is not refreshed by spamming it.
- **Flask effect** scales the buff: "increased effect" multiplies the flask's granted stats (believed also to scale "during flask effect" modifiers on the flask itself; not confirmed for 3.30).
- **Duration:** "increased flask effect duration" lengthens the buff.
- 3.27 and 3.30 raised the Pathfinder's Master Distiller bonuses tied to Bismuth, Diamond, and Amethyst flasks; 3.30 changed the Diamond bonus to critical strike multiplier. 3.30 raised Nature's Boon (magic utility flask effect).
- 3.30's Doryani's Invitation can roll increased effect for a named resistance or Granite flask.

## Flask charges

- Each flask has a maximum and a charge cost per use. A flask cannot be used with fewer charges than its cost.
- **On kill:** flasks gain charges when you or a nearby ally kills an enemy; rarer monsters give more.
- **Other generation:** charges on crit, on hit, over time, or from passives. 3.30 raised the Pathfinder's passive charge gain (Nature's Adrenaline and the Ascendant's Pathfinder node) to 3 charges every 3 seconds.
- **Modifiers:** "increased charges gained" raises charge income; "reduced charges used" lowers the cost per use; "increased charge recovery" (on the flask) raises its own income.
- Flasks refill fully in town and hideout.
- **3.29:** in The Forbidden Sanctum, flask charges refill when you interact with the Sanctum map between rooms (the Writhing Jar excepted).

## Flask enchantments

- **Instilling Orb** adds a condition that uses the flask automatically (for example when charges are full or after taking a large hit). Only one enchantment per flask.
- **Enkindling Orb** adds an enchantment that changes charge behaviour or flask effect.
- Both predate 3.26. 3.26 fixed instilled flasks not activating in The Trialmaster fight.

## Tinctures

Tinctures (added in 3.23 Affliction) still exist in 3.30: 3.30 changed Living Blade to allow more active tinctures and gave the Warden's Seasoned Hunter a bonus while a tincture is active.

- A tincture sits in a flask slot but does not use flask charges.
- Activating it gives a buff to weapon attacks while it is active.
- While active, it builds **mana burn**: stacks that drain mana over time and grow while it stays on. Turning it off (or running out) starts a cooldown before it can be activated again (details not confirmed for 3.30).
- By default only one tincture can be active at a time; some passives and items raise this.
- Flask effect modifiers do not apply to tinctures; tinctures have their own "tincture effect" modifiers (believed; not confirmed for 3.30).

## Charms

Charms do not exist in PoE1. PoE2 differs (charms, flask rules, and recovery all work differently there); do not apply this there.

## Common mistakes

- Saying "increased flask effect" raises life flask healing. It does not; it scales utility buffs.
- Treating "increased flask effect duration" as more healing on a life flask. It is the same healing, slower.
- Confusing "recovery from flasks" (amount) with "flask recovery rate" (speed).
- Assuming a utility flask can be re-used to refresh its buff while active.
- Quoting a unique flask from the base type's rules.
- Applying PoE2 charms or charm slots to PoE1.

## Check with the engine

- Flask fields (recovery per use, recovery per second, duration, charges per use, utility buff values) are not part of the calc slice yet. Answer from the rules here and say so.
- When a flask buff is active in a build's config, its stats appear in the calc breakdown as their own source, which confirms the buff values the engine applied.
