---
game: poe1
patch: 3.30.0
as_of: 2026-11-17
sources:
  - https://www.pathofexile.com/forum/view-thread/4013680
  - https://www.pathofexile.com/forum/view-thread/3985332
  - https://www.pathofexile.com/forum/view-thread/3869068
  - https://www.pathofexile.com/forum/view-thread/3787013
  - https://www.pathofexile.com/forum/view-thread/3531661
  - https://www.poewiki.net/wiki/Flask
  - https://www.poewiki.net/wiki/Tincture
  - https://github.com/PathOfBuildingCommunity/PathOfBuilding/blob/v2.67.2/src/Classes/ItemsTab.lua
  - https://github.com/PathOfBuildingCommunity/PathOfBuilding/blob/v2.67.2/src/Classes/Item.lua
verification: engine-checked
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
recovered (over time) = base amount x (1 + increased recovery from flasks) x more multipliers
                        x (1 + increased flask effect) x (1 + increased flask effect duration)
                        x life recovery rate modifier
duration              = base duration x (1 + increased flask effect duration)
                        / (1 + increased flask recovery rate) / (1 + increased flask life recovery rate)
```

This is PoB 2.67.2's flask tooltip calculation; poewiki describes the same rules.

- **"Increased life recovery from flasks"** raises the amount.
- **"Increased flask effect"** also raises the amount. It multiplies with recovery from flasks and with flask quality.
- **"Increased flask life recovery rate"** (and the flask's own recovery rate) make the same amount arrive faster: the duration is shorter.
- **"Increased life recovery rate"** (the general stat) keeps the duration and recovers more per second, so more in total.
- **"Increased flask effect duration"** on a recovery flask makes it last longer **at the same rate**, so it recovers more in total. It is not "the same amount, slower".
- 3.30.0 changed the Pathfinder's Master Surgeon drawback from "50% less life recovery from flasks" to "50% less life flask recovery rate": same total, slower delivery.
- **Instant recovery.** Some modifiers make a share instant, make all of it instant at reduced value, or make it instant only at low life. The instant part ignores recovery rate.
- **Stacking.** Recovery from several flask uses does **not** run at the same time: active recovery effects queue, and the one with the highest recovery per second applies first (poewiki). A recovery effect ends when the pool is full, unless a line says it is not removed ("effect is not removed when unreserved life is filled").
- **"Flask effect"** (increased effect of flasks) **does** raise the amount a life or mana flask recovers, as well as scaling the buffs a flask grants.

## Utility flasks

- Using a utility flask applies its buff for its duration.
- A utility flask cannot be used again while its own effect is active. It is not refreshed by spamming it.
- **Flask effect** scales the buff: "increased effect" multiplies the flask's granted stats, including the "during effect" modifiers rolled on the flask itself (poewiki: it improves every modifier the flask has, rounded down). Lines elsewhere that say "during any flask effect" are conditions, not flask stats, so flask effect does not scale them.
- Using the same utility flask effect from two sources: each has its own duration and only the strongest applies.
- **Duration:** "increased flask effect duration" lengthens the buff.
- 3.27 and 3.30 raised the Pathfinder's Master Distiller bonuses tied to Bismuth, Diamond, and Amethyst flasks; 3.30 changed the Diamond bonus to critical strike multiplier. 3.30 raised Nature's Boon (magic utility flask effect) **in Ruthless only**.
- 3.30's Doryani's Invitation can roll increased effect for a named resistance or Granite flask.

## Flask charges

- Each flask has a maximum and a charge cost per use. A flask cannot be used with fewer charges than its cost.
- **On kill:** flasks gain charges when you or a nearby ally kills an enemy; rarer monsters give more.
- **Other generation:** charges on crit, on hit, over time, or from passives. 3.30 raised the Pathfinder's passive charge gain (Nature's Adrenaline and the Ascendant's Pathfinder node) to 3 charges every 3 seconds **in Ruthless only** (the lines are under the 3.30.0 Ruthless-specific changes).
- **Modifiers:** "increased charges gained" raises charge income; "reduced charges used" lowers the cost per use; "increased charge recovery" (on the flask) raises its own income.
- Flasks refill fully in town and hideout.
- **3.29:** in The Forbidden Sanctum, flask charges refill when you interact with the Sanctum map between rooms (the Writhing Jar excepted).

## Flask enchantments

- **Instilling Orb** adds a condition that uses the flask automatically (for example when charges are full or after taking a large hit). Only one enchantment per flask.
- **Enkindling Orb** adds an enchantment that changes charge behaviour or flask effect.
- Both predate 3.26. 3.26 fixed instilled flasks not activating in The Trialmaster fight.

## Tinctures

Tinctures (added in 3.23 Affliction, core since 3.25.0) still exist in 3.30: 3.30 changed Living Blade to allow 2 additional active tinctures, gave the Warden's Seasoned Hunter a bonus while a tincture is active, and raised Enduring Suffusion to 50% less mana burn rate.

- A tincture sits in a flask slot but does not use flask charges.
- Activating it gives a buff to attacks made with your weapons while it is active (melee by default; some effects extend it to ranged).
- While active, it builds **mana burn** stacks over time. Each stack drains 1% of maximum mana per second (at least 1 mana). It deactivates when you turn it off or reach 0 mana. Deactivating starts a cooldown on **all** tinctures. The burn rate and the cooldown length depend on the tincture base and its modifiers (official 3.25.0 notes; poewiki).
- By default only one tincture can be active at a time; some passives and items raise this.
- Tinctures are not flasks. Flask effect modifiers do not apply to them; they have their own "tincture effect" modifiers, and tincture quality gives more tincture effect (PoB 2.67.2 keeps a separate tincture effect stat; poewiki agrees).

## Charms

Charms do not exist in PoE1. PoE2 differs (charms, flask rules, and recovery all work differently there); do not apply this there.

## Common mistakes

- Saying "increased flask effect" does not raise life flask healing. It does.
- Treating "increased flask effect duration" as the same healing spread out. It lasts longer at the same rate, so it heals more.
- Expecting two life flasks used together to heal at the same time. Their recovery queues.
- Confusing "recovery from flasks" (amount) with "flask recovery rate" (speed).
- Assuming a utility flask can be re-used to refresh its buff while active.
- Quoting a unique flask from the base type's rules.
- Applying PoE2 charms or charm slots to PoE1.

## Check with the engine

- Flask fields (recovery per use, recovery per second, duration, charges per use, utility buff values) are not part of the calc slice yet. Answer from the rules here and say so.
- When a flask buff is active in a build's config, its stats appear in the calc breakdown as their own source, which confirms the buff values the engine applied.

## Verification (2026-11-17)

`engine-checked` here means: the recovery formula was checked against the pinned Path of Building 2.67.2 flask tooltip (`Classes/ItemsTab.lua`, `Classes/Item.lua`), and the tincture and Pathfinder points against the official 3.25.0 and 3.30.x notes; poewiki's flask and tincture pages agree. Flask fields are still not in the Exiled Studio engine. Not checked in game.
