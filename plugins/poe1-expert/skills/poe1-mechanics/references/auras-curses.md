---
game: poe1
patch: 3.30.0
as_of: 2026-11-15
sources:
  - https://poedb.tw/us/Version_3.30.0
  - https://poedb.tw/us/Version_3.29.0
  - https://poedb.tw/us/Version_3.28.0
  - https://poedb.tw/us/Version_3.27.0
  - https://poedb.tw/us/Version_3.26.0
  - https://patchbot.io/games/path-of-exile/articles/2188-content-update-3300-path-of-exile-covens-of-umbra
verification: unverified
---

# Auras, heralds, blessings, curses, reservation

The formulas for reservation and doom below follow Path of Building 2.67's
calculation (the project's pinned oracle). It agrees with the game as far as we
know. No 3.26 to 3.30 patch changed these rules; 3.30 changed only items and
ascendancy numbers here.

PoE2 has spirit instead of mana reservation and different curse rules; do not
apply this there.

## Auras

- An aura is a buff in an area around its source. It affects you and allies in
  range (minions too). Some auras are debuffs on enemies instead.
- **Aura effect** scales every value the aura grants:

```
aura value = gem's base value x (1 + sum of increased aura effect / 100)
                              x product of more/less aura effect
```

- Lines can be narrow: "increased effect of Non-Curse Auras from your Skills"
  reaches only your own non-curse auras. "Increased Aura Effect" on a single
  named aura reaches only that aura. Generic "buff effect" lines reach some
  auras, depending on the wording.
- Some supports give more aura effect but stop the aura affecting you
  (Generosity is the classic case). The aura then helps allies and minions only.
- Auras from the same skill do not stack. Two copies of the same aura from two
  sources: only the strongest applies to you.

## Reservation

Most aura and herald skills reserve part of your mana (or life) while active.

```
reserved = base reservation
         x product of linked supports' cost & reservation multipliers
         x (1 + increased reservation / 100) x more/less reservation
         / (1 + reservation efficiency / 100)
         / more reservation efficiency
```

- **Base** is either a percent of the pool or a flat amount, from the gem.
- **Support multipliers** (shown on the support as "Cost & Reservation
  Multiplier") multiply together. 3.26 to 3.29 changed several of these; read
  the current values through the knowledge tools.
- **Reservation efficiency** divides. 100% increased efficiency halves the
  reservation, it does not remove it. Efficiency below -100% is treated as
  -100%.
- PoB rounds flat reservation to a whole number and percent reservation to
  two decimals at the end. The game's exact rounding is not confirmed.
- **Cost efficiency** is a different stat: it changes skill costs, not
  reservation. 3.29 converted the tree's "reduced cost" lines into cost
  efficiency; they never touched reservation.
- Unreserved mana is what pays skill costs. A build can reserve itself into
  having no mana for its main skill.
- Life reservation works the same way but reserves life. A source that makes
  skills reserve life instead of mana moves the whole amount.

## Heralds

- A herald is a buff skill that reserves mana and adds an on-kill or on-hit
  effect. Heralds are **not auras**: aura effect does not scale them.
- Herald buffs scale with "buff effect" lines and with herald-specific lines.
- Some heralds summon minions (Herald of Purity, Herald of Agony). Those minions
  follow minion rules (`minions.md`).
- 3.26 replaced the Elementalist's Elemancer notable with Bringer of Ruin, which
  gives herald reservation efficiency and herald buff effect.

## Blessings

- Divine Blessing Support changes a supported aura into a timed buff. The aura
  no longer reserves; it costs mana each use and lasts a short duration.
- A blessing is still an aura while it runs, so aura effect still scales it.
  Not confirmed for every aura in 3.30.

## Curses

A curse is a debuff placed on enemies. **Hexes** are the usual curses (Elemental
Weakness, Vulnerability, Enfeeble and so on). **Marks** are single-target curses
(Assassin's Mark, Sniper's Mark and so on).

### Curse effect

```
curse value = gem's base value x (1 + sum of increased curse effect / 100)
                               x product of more/less curse effect
                               x enemy's modifiers to curse effect on itself
```

- Increased curse effect from you and the enemy's own "reduced effect of curses
  on you" add together before multiplying; the enemy's more/less multiplies.
- Mark effect lines scale marks only. Hex lines scale hexes only.

### Curse limit

- The default curse limit is one. Lines give "+1 to maximum number of Curses"
  or similar.
- When a new curse would go over the limit, it replaces an older one. The game
  ranks curses by when they were applied; PoB ranks them by a priority list, so
  its choice of which curses stay may differ from the game's.
- Some curses ignore the limit (skills that say they ignore the hex limit, and
  some item effects). These sit on top of the limit.
- One mark at a time: you can have a single marked enemy. In PoB's model the
  mark still takes one of your curse slots. Not confirmed in game for 3.30.
- Hexproof enemies cannot be hexed unless a line says your curses ignore
  hexproof. Marks still apply.

### Doom
- Some hexes can gain **Doom** while on an enemy. A hex gains doom only if a
  source gives it a maximum doom (some skills and items do).
- Each point of doom gives the hex 1% increased effect, up to its maximum.
  A rare line doubles that per point.
- Impending Doom Support triggers Doom Blast when a supported hex ends. How its
  damage relates to doom in 3.30 is not confirmed; read the gem's current text.

### Curses and bosses
- Many bosses have reduced curse effect on themselves. The size depends on the
  boss and is part of the monster's data. Exact values in 3.30 are not
  confirmed; do not quote a fixed percentage.
- Curse effect on players (monster curses) uses the player's "reduced effect
  of curses on you".

### Exposure
- Exposure is a debuff that lowers one element's resistance. It is **not a
  curse**, does not use a curse slot and is not scaled by curse effect.
- Only one exposure per element applies to an enemy: the strongest. Several
  sources of fire exposure do not add.
- Exposure and a resistance-lowering curse (Elemental Weakness, Flammability)
  both apply. They stack with each other and with penetration.
- Exposure effect lines scale exposure. 3.27 changed Pyroclast Mine to apply
  fire exposure, and more mines do not make it stronger.

## Common mistakes

- Scaling heralds with aura effect.
- Treating 100% reservation efficiency as "free" (it halves the reservation).
- Confusing cost efficiency (skill costs) with reservation efficiency.
- Adding two exposures of the same element.
- Counting exposure against the curse limit, or scaling it with curse effect.
- Expecting marks on hexproof enemies to fail, or hexes on hexproof to work.
- Quoting a fixed boss curse-effect reduction without checking the boss.
- Assuming an aura with Generosity still buffs the caster.

## Check with the engine

- Reservation: the engine computes reservation with the supports' cost
  multipliers and efficiency, and shows the reserved amount per skill.
- Aura effect: the engine scales non-curse auras from your skills before they
  merge, and the breakdown names the aura as the source.
- Exposure: the engine applies the strongest exposure per element to the enemy
  resistance; the enemy resistance breakdown shows it.
- Curse effect, the curse limit and doom may not all be modelled. If no field
  exists, say the answer comes from these rules and PoB.
