---
game: poe1
patch: 3.30.0
as_of: 2026-11-15
sources:
  - https://poedb.tw/us/Version_3.30.0
  - https://poedb.tw/us/Version_3.29.0
  - https://poedb.tw/us/Version_3.28.0
  - https://poedb.tw/us/Version_3.27.0
  - https://patchbot.io/games/path-of-exile/articles/2188-content-update-3300-path-of-exile-covens-of-umbra
verification: unverified
---

# Totems, traps, mines, brands

Four ways to use a skill without casting or attacking with it directly. The
key question for each is **who uses the skill**, because that decides which
modifiers apply and which "on hit" or "on kill" effects fire.

| Delivery | Who uses the skill | Your damage mods | Delivery-specific mods |
|---|---|---|---|
| Totem | the totem | yes | "Totem Damage", totem life, totem placement |
| Trap | you, via the trap | yes | "Trap Damage", trap throwing speed, trap duration |
| Mine | you, via the mine | yes | "Mine Damage", mine throwing speed, detonation |
| Brand | you | yes | brand activation frequency, brand attachment range |

The limits and rounding below follow Path of Building 2.67 where noted.

PoE2 has totems and traps with different rules; do not apply this there.

## Totems

### What a totem is
- A totem is a stationary allied object. It has its own life and resistances.
  It is **not a minion**: minion lines never reach it.
- A totem uses the skill linked with a totem support (Spell Totem, Ballista
  Totem) or a skill that is a totem by itself.
- The skill on the totem uses **your** offensive modifiers: your increased
  damage, added damage, crit and the like. "Totem Damage" lines add to that.
- Supports that make a skill a totem usually carry a less-damage multiplier.
  Several of these changed in 3.29; look up the current value.

### Totem limit
- Base limit is one totem active at a time. Lines raise it, sometimes only for
  one totem kind (for example "+1 to maximum number of Summoned Ballista
  Totems", or 3.30's Artillery Quiver line that raises the limit for attack
  totems only).
- Placing past the limit removes the oldest totem.

### Totem life and defences
- Totems have their own life, scaled by "Totem Life" lines and the totem's level.
- Totem resistances are their own, raised by lines that name totems. Your
  resistances do not apply. Totem maximum resistance follows the 75% default
  rule unless a totem line raises it.
- Some lines let totems take damage for you ("damage taken from totems before
  you"); that is a defence, not an offence.

### Placement
- Totem placement speed scales how fast you place a totem.
- 3.28: placement speed now also scales how fast a totem emerges after being
  placed, and ranged attack totems got a fixed base placement time.

### What a totem's kill or hit triggers
- The totem deals the damage, so your "on hit" and "on kill" lines that say
  "you" do not fire from it. Lines that say "your totems" or "you or your
  totems" do.
- Leech from totem damage does not go to you.
- Keystones such as Ancestral Bond stop you dealing damage yourself; only
  totems then deal your skill damage. Check the exact current keystone text.

## Traps

- A trap is thrown to a spot. After a short arm time it waits until an enemy
  comes within its trigger radius, then the skill fires from it.
- Trap damage is your damage. "Trap Damage" lines and trap supports add to it.
- **Throwing speed** scales how fast you throw. PoB caps throwing at one throw
  per server tick.
- Many trap skills have a **cooldown** with several uses. Cooldown recovery
  rate scales it; the result is rounded up to whole server ticks (33 ms).
- Traps have a duration and a maximum active count. The base count is a game
  constant; lines raise it. The exact arm time in 3.30 is not confirmed.
- Supports like Multiple Traps and Cluster Traps throw more traps per use.
  3.29 raised the extra throw time per projectile from Barrage.

## Mines

- A mine is thrown and then **detonated**. Detonation is a separate action
  (Detonate Mines) or comes from supports and passives that detonate
  automatically.
- Mine damage is your damage. "Mine Damage" lines and mine supports add to it.
- Mines detonate in sequence, not all at once.
- Mines can carry aura-like effects while armed. Supports and passives give
  armed mines effects on nearby enemies (for example hinder or increased damage
  taken); these are mine effects, not your auras, and aura effect does not
  scale them unless the line says so. 3.27 changed Pyroclast Mine's armed effect
  to a fire exposure aura that does not grow with more mines; 3.30's
  Demolitions Specialist makes landing mines hinder nearby enemies.
- **Throwing speed** scales how fast you lay mines; PoB caps it at one per
  server tick.
- A mine skill that reserves mana reserves it for each armed mine (PoB
  multiplies the reservation by the active mine count). Which mines reserve in
  3.30 is a per-gem fact; check the gem.
- Mine limit: a base count from game data, raised by lines.

## Brands

- A brand is a spell that you cast onto the ground or an enemy. It attaches to
  an enemy and **activates** on a timer, using its effect each activation.
- Cast speed changes how fast you place brands. **Activation frequency**
  changes how often an attached brand activates. They are different stats.
- Brands have a duration and attach within a range. When their target dies they
  detach and look for a new target within range.
- Brand damage is your spell damage.
- Penance Brand calls its stacking resource "Energy". That is a brand-only
  mechanic and has nothing to do with PoE2 meta-gem energy.

## Which mods apply where (summary)

- Your generic damage, spell or attack mods: totems, traps, mines, brands all.
- "Totem Damage", "Trap Damage", "Mine Damage": only that delivery.
- "Trap and Mine Damage": both traps and mines.
- Minion lines: none of the four.
- Your on-hit and on-kill effects: traps, mines and brands yes (you deal the
  damage); totems no, unless the line names totems.

## Common mistakes

- Treating totems as minions, or minions as totems.
- Expecting your leech or "on kill" effects from totem damage.
- Expecting cast speed to raise a brand's activation rate.
- Counting several mines' fire exposure as stronger exposure.
- Ignoring server-tick rounding on trap cooldowns.
- Quoting pre-3.28 totem placement behaviour.

## Check with the engine

- Totem damage: the skill breakdown shows totem-only lines as named sources
  when the main skill is used by a totem. Totem life and resistance fields may
  not exist in the engine; say so if absent.
- Trap and mine throw rate, cooldown and mine reservation: if the engine shows
  no rate field for the skill, use these rules and PoB.
