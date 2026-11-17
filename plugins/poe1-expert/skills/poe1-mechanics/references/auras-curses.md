---
game: poe1
patch: 3.30.0
as_of: 2026-11-17
sources:
  - https://www.pathofexile.com/forum/view-thread/4013680
  - https://www.pathofexile.com/forum/view-thread/3985332
  - https://www.pathofexile.com/forum/view-thread/3377087
  - https://www.pathofexile.com/forum/view-thread/3913392
  - https://www.pathofexile.com/forum/view-thread/3869068
  - https://www.pathofexile.com/forum/view-thread/3787013
  - https://www.pathofexile.com/forum/view-thread/3531661
  - https://www.poewiki.net/wiki/Curse
  - https://www.poewiki.net/wiki/Reservation
  - https://www.poewiki.net/wiki/Divine_Blessing_Support
  - https://github.com/PathOfBuildingCommunity/PathOfBuilding/blob/v2.67.2/src/Modules/CalcPerform.lua
  - https://github.com/PathOfBuildingCommunity/PathOfBuilding/blob/v2.67.2/src/Modules/ConfigOptions.lua
  - repo:DBAggie/exiled-studio/crates/loom-calc/src/poe1/gems.rs
  - repo:DBAggie/exiled-studio/crates/loom-calc/src/poe1/skill_modifiers.rs
  - repo:DBAggie/exiled-studio/crates/loom-calc/src/poe1/exposure.rs
verification: maintainer-approved
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
  reservation, it does not remove it. At -100% or lower the sources differ:
  PoB treats anything below -100% as -100%; poewiki says 100% or more
  *reduced* efficiency makes the reservation infinite, so the skill cannot be
  used.
- Rounding: since 3.14 the game keeps percent reservation to two decimals,
  but the total amount reserved is always a whole number (poewiki). PoB
  2.67.2 rounds each skill's flat reservation to a whole number and its
  percent to two decimals, then takes `flat + ceil(pool x percent / 100)`: the
  percent part is rounded **up** to a whole number. Exiled Studio's engine
  does the same. A 2023 player bug report on the official forum also shows the
  two-decimal percent rounded up in the tooltip (37.037...% shown as 37.04%),
  which cost that player a fourth aura. So plan on rounding up at both steps.
  Older forum threads about rounding describe the pre-3.14 whole-percent
  system and no longer apply. Not tested in game.
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

- Since 3.25.0 the Divine Blessing Support gem no longer exists; the support
  comes only from the unique March of the Legion (official 3.25.0 notes).
- It changes a supported aura into a timed buff. The aura no longer reserves:
  each use costs the aura's base reservation as mana plus a flat cost, and the
  aura lasts a short duration (scaled by skill effect duration).
  Reservation efficiency does nothing to that cost.
- A blessing is still an aura while it runs, so aura effect scales it; the
  support itself grants increased aura effect (poewiki). It cannot support
  non-permanent auras such as mines, banners or stances, and blessed auras
  cannot be triggered.

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
- One mark at a time: you can have a single marked enemy, and a target can
  carry only one mark. A mark **does** take one of the target's curse slots:
  with +1 curse limit you can have two hexes, or a hex and a mark, on one
  enemy, but never two marks (poewiki; PoB models it the same way).
- Hexproof enemies cannot be hexed unless a line says your curses ignore
  hexproof. Marks still apply.

### Doom
- Doom as a general hex mechanic was **removed in 3.20.0** (poewiki). Hexes
  no longer gain doom by default.
- A few older lines still give hexes a maximum doom ("hexes you inflict have
  +X to maximum doom"). PoB still parses those and gives the hex 1% increased
  effect per point of doom, up to that maximum. Treat them as legacy.
- Impending Doom Support still exists: it triggers Doom Blast when a supported
  hex ends. Doom Blast is a spell hit with its own base damage; its damage does
  not depend on doom. 3.25.0 changed its added damage effectiveness from a
  flat value to a range by gem level (220% to 370% at gem levels 1 to 20).
  Read the gem's current numbers through the tools.

### Curses and bosses
- The old general penalty to curse effect on unique monsters and bosses was
  **removed in the 3.20.0 curse rework**, together with doom (poewiki). PoB
  2.67.2's boss settings apply no curse-effect reduction. No 3.26 to 3.30 note
  brings one back. A specific monster can still have its own "reduced effect
  of curses on you" line; check that monster, but do not apply a general boss
  penalty.
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
- Applying the pre-3.20 boss curse penalty or doom to current hexes.
- Assuming an aura with Generosity still buffs the caster.

## Check with the engine

The engine facts below were read from Exiled Studio's source (`crates/loom-calc`, dev branch at `b42e49f`, 2026-11-17; the 0.9 line). The engine follows Path of Building 2.67.2's order of operations and rounding, so a number the engine marks `complete` is PoB's number, apart from registered divergences. It computes 24 fields: `strength`, `dexterity`, `intelligence`, `life`, `mana`, `life-unreserved`, `mana-unreserved`, `energy-shield`, `armour`, `evasion`, `resistance.fire`, `resistance.cold`, `resistance.lightning`, `resistance.chaos`, `block-chance`, `spell-block-chance`, `spell-suppression-chance`, `average-damage`, `speed`, `hit-speed`, `hit-chance`, `crit-chance`, `crit-multiplier` and `hit-dps`. The hit fields exist only when the main skill is a self-cast spell hit or a main-hand attack: not channelled, triggered, a totem, trap, mine, minion or brand skill, not a skill with a cooldown, and not dual wielding. For any other main skill they are `not-computed`.

- **Reservation**: computed as PoB does. Per skill, the flat amount is rounded to a whole number and the percent to two decimals; the pool then loses `flat + ceil(pool x percent / 100)`, so the percent part rounds **up** to a whole number. `life-unreserved` and `mana-unreserved` show the result, with a `ceil` step in the graph.
- **Aura and buff effect**: auras and buffs from the gems the engine knows are scaled by buff effect and non-curse aura effect before they merge, and the breakdown names the aura as the source. A gem the engine does not know shows as an `unmodelled-gem` reason.
- **Exposure**: the strongest exposure per element is applied to the enemy's resistance, with the extras that deepen it.
- **Curses**: a curse from a known gem is applied to the enemy, scaled by curse effect. With a curse limit of one, a second hex is a `curse-limit` reason: PoB's choice of which curse stays is not modelled. Marks are not modelled. Doom is not modelled.
- Divine Blessing and blessings are not modelled.

## Verification (2026-11-17)

Checked against the official 3.25.0 to 3.30.x notes (3.30.x read in full), poewiki's curse, reservation and Divine Blessing pages, the pinned Path of Building 2.67.2 (curse effect and doom in `CalcPerform.lua`; boss settings in `ConfigOptions.lua`; reservation rounding in `CalcPerform.lua`, `doActorLifeManaReservation`), and Exiled Studio's engine source (`gems.rs`, `skill_modifiers.rs`, `exposure.rs`). `engine-checked` since the third pass the same day: the last open point, which way the reserved total rounds, is settled by PoB and the engine (up), which the maintainer accepts as evidence of the game's rule, and a player report agrees. Not tested in game.

Approved by the maintainer on 2026-11-17 (given in chat, recorded by the session). The checks named above are what was done before approval; nothing here was checked in game unless a line says so.
