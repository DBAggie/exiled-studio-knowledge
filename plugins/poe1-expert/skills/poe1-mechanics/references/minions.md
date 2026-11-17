---
game: poe1
patch: 3.30.0
as_of: 2026-11-17
sources:
  - https://www.pathofexile.com/forum/view-thread/4013680
  - https://www.pathofexile.com/forum/view-thread/3985332
  - https://www.poewiki.net/wiki/Summon_Skeletons
  - https://www.pathofexile.com/forum/view-thread/3913392
  - https://www.pathofexile.com/forum/view-thread/3869068
  - https://www.pathofexile.com/forum/view-thread/3787013
  - https://www.poewiki.net/wiki/Minion
  - https://github.com/PathOfBuildingCommunity/PathOfBuilding/blob/v2.67.2/src/Data/Minions.lua
  - https://github.com/PathOfBuildingCommunity/PathOfBuilding/blob/v2.67.2/src/Modules/CalcSetup.lua
  - https://github.com/PathOfBuildingCommunity/PathOfBuilding/blob/v2.67.2/src/Modules/CalcPerform.lua
  - repo:DBAggie/exiled-studio/crates/loom-calc/src/poe1/minions.rs
  - repo:DBAggie/exiled-studio/crates/loom-calc/src/poe1/hit.rs
verification: engine-checked
---

# Minions

A minion is a separate allied entity that a skill creates. It has its own life,
its own defences and its own skills. Your character sheet does not describe it.
Most mistakes come from assuming your own modifiers reach your minions.

PoE2 differs; do not apply this there.

## Which of your modifiers apply to minions

Only these reach a minion:

1. **Lines that name minions.** "Minions deal X% increased Damage", "Minions have
   X% increased maximum Life", "+X% to Minion resistances". The source can be
   gear, the tree, jewels, or a support gem linked to the minion skill.
2. **Lines that name both.** "You and your Minions ...", "you and nearby Allies
   ...". Minions are allies.
3. **Auras and other ally buffs.** An aura buffs every ally in its radius,
   minions included. The aura's effect on them follows the aura's own scaling
   (see `auras-curses.md`).
4. **Support gems linked to the minion skill.** A linked support modifies the
   skills the minion uses, unless the support says it cannot modify minion
   skills. Since 3.27 Windburst and Living Lightning cannot; 3.28 made Hallow
   and Excommunicate the same; 3.29 replaced Minion Pact with Communion, which
   also cannot.
5. **Specific exceptions** that say so in their text, for example a keystone
   that moves your shield's modifiers onto your minions instead of you.

What does **not** reach a minion:

- Plain "increased Damage", "increased Attack Speed", "added Physical Damage",
  "increased Critical Strike Chance" and every other line that does not name
  minions. These are yours only.
- Your flat added damage, your weapon, your crit, your conversion.
- Your life, resistances, armour, evasion, block and suppression.

Things that act on the enemy help minions indirectly: your curses, exposure and
other debuffs lower the enemy's defences for every source of damage, the
minion's too.

The reverse also exists: some lines give **you** your minion modifiers (for
example "increases and reductions to Minion Damage also affect you"). Those make
minion lines count for you; they never make your lines count for minions.

## Minion level, life and defences

- A minion's base stats come from its level, which comes from the gem level (or
  the item that grants the skill). A higher gem level is the largest base
  scaling a minion gets.
- Minion life and energy shield scale with "Minions have X% increased maximum
  Life / Energy Shield" and the minion gem's own stats.
- Minion resistances are their own. They start from the minion type's base
  values and rise with "Minions have +X% to ... Resistances". Your resistances
  do not apply. The default maximum resistance is 75%, the same rule as yours,
  raised only by lines that name minions.
- Minion base resistances are **not** all 0%. In the game data PoB 2.67.2
  reads, most player minion types start at 40% elemental and 20% chaos
  resistance, some start at 0%, and a few higher. Look the minion up.
- Minions do not take the campaign (act) resistance penalty: PoB 2.67.2 applies
  the -30%/-60% penalty to the player only and gives minions just their base
  values. No 3.26 to 3.30 note changes this. Not checked in game.
- Do not confuse minions with **Mercenaries**: 3.30.0 gave hired Mercenaries
  their own area-level resistance penalty (-30% in level 46 to 67 areas, -60%
  in level 68+ areas and hideouts). That line names Mercenaries only.
- Minion armour, evasion, block and other defences also need minion lines.
- 3.29: Spectre life was lowered across the board. Companionship no longer gives
  more life to a sole minion; it gives it less damage taken.
- 3.30: Transfusion Support now gives a nearby minion a power, frenzy or
  endurance charge per 400 life spent on upfront costs (it used to give souls).

## Minion damage scaling

Minion damage follows the same increased/more rules as yours (see `damage.md`),
applied to the minion's own skill:

```
minion hit = minion skill base damage
           x (1 + sum of increased/reduced that applies to the minion)
           x product of all more/less on the minion
```

- "Minions deal X% increased Damage" is an increased modifier on the minion.
- Minion support gems (Minion Damage and the like) give more multipliers.
- Your "increased Damage" does not add to that sum.
- Minions that copy your gear are the main exception. Animated weapons and
  guardians use the item given to them. Holy Strike's Holy Armaments (3.28) copy
  your main-hand weapon's stats. Even then, only minion lines and the copied item
  apply, not your passive tree.
- Minion crit uses the minion's own crit. 3.28 added Exemplar Support, which
  gives minions crit based on your recent crits.

### Minion hits since 3.27
- 3.27: minion attacks always hit. Every source of minion accuracy was removed,
  and old items keep a line that does nothing. Do not scale minion accuracy.
- 3.29: non-Spectre minions no longer pause while attacking. This raised the
  real damage of melee minions such as zombies and golems; old DPS comparisons
  from before 3.29 are off.

## Minion count limits

- Each minion skill has its own maximum count, given by the gem and raised only
  by lines that name that minion type (for example "+1 to maximum number of
  Raised Zombies") or minions in general where the line says so.
- Limits are per skill type, not shared. Zombies, spectres and skeletons each
  have their own cap.
- When you summon past the cap, the **oldest** minion of that type is replaced
  (confirmed by the maintainer, 2026-11-17; poewiki states the same for Summon
  Skeletons, and for traps, mines and totems).
- Some minions have a duration (skeletons, clones, temporary minions) and die
  when it ends. Permanent minions persist between areas unless they die.
- 3.27: a Spectre that dies turns into an untargetable orb that cannot act, and
  comes back when you enter an area. 3.28 made the Guardian's Sentinel of
  Radiance a permanent minion.

## Minion behaviour (rules only)

- Minions follow you and fight enemies near you. If you move too far, they
  return to you instead of fighting.
- Convocation (a white gem since 3.27) and similar effects pull minions to you.
- Some minions use "command" skills that you activate; most choose their own
  targets.
- Minion actions count as minion actions, not yours: "on kill" and "on hit"
  lines on you do not fire from a minion's kill unless the line says "you or
  your minions".

## Common mistakes

- Adding the player's "increased Damage" or flat added damage to a minion.
- Expecting the player's resistances, life or armour to protect minions.
- Scaling minion accuracy in 3.27 or later. It no longer exists.
- Linking a support that says it cannot modify minion skills, such as Communion
  (3.29) or Windburst (3.27), and expecting it to buff the minion.
- Treating totems as minions. Totems are a separate entity type with their own
  modifiers (`totems-traps-mines.md`); minion lines do not reach them.
- Quoting pre-3.29 numbers for melee minions or Spectres.
- Assuming the minion limit is shared across all minion skills.

## Check with the engine

The engine facts below were read from Exiled Studio's source (`crates/loom-calc`, dev branch at `b42e49f`, 2026-11-17; the 0.9 line). The engine follows Path of Building 2.67.2's order of operations and rounding, so a number the engine marks `complete` is PoB's number, apart from registered divergences. It computes 24 fields: `strength`, `dexterity`, `intelligence`, `life`, `mana`, `life-unreserved`, `mana-unreserved`, `energy-shield`, `armour`, `evasion`, `resistance.fire`, `resistance.cold`, `resistance.lightning`, `resistance.chaos`, `block-chance`, `spell-block-chance`, `spell-suppression-chance`, `average-damage`, `speed`, `hit-speed`, `hit-chance`, `crit-chance`, `crit-multiplier` and `hit-dps`. The hit fields exist only when the main skill is a self-cast spell hit or a main-hand attack: not channelled, triggered, a totem, trap, mine, minion or brand skill, not a skill with a cooldown, and not dual wielding. For any other main skill they are `not-computed`.

- The engine does not compute minions. When the main skill is a minion skill the hit fields are `not-computed`, and there are no minion life, resistance or DPS fields.
- What it does model (`loom_calc::poe1::minions`): minion modifiers that also affect **you** (Spiritual Aid, Spiritual Command and the like). They show in your own damage and speed breakdowns with the source named.
- A summoned golem's buff to you is modelled for the golems the engine knows; other minion effects on you show as reasons.
- For minion numbers, use PoB (it has a minion stats view) and the knowledge tools for the minion gem's base values, and say the engine does not compute them.

## Verification (2026-11-17)

Checked against the official 3.26.0 to 3.30.x notes (3.30.x read in full), poewiki's minion page, and the pinned Path of Building 2.67.2 (minion base resistances in `Data/Minions.lua`; the player-only campaign penalty in `CalcSetup.lua` and `CalcPerform.lua`). Still `unverified`: replacing the oldest minion when summoning past the cap is confirmed only for Summon Skeletons (poewiki, second pass the same day); the other minion skills wait for an in-game test.

Fourth pass, 2026-11-17: the maintainer confirmed that summoning past the limit replaces the oldest minion, which closes the last open point. `engine-checked`: the numeric rules were checked against Path of Building 2.67.2 and the official notes. Exiled Studio's engine does not compute minions.
