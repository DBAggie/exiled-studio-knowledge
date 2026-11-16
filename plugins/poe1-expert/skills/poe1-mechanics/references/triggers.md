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

# Triggers

A triggered skill is used automatically when a condition is met, instead of
by you pressing a key. The trigger source is a support gem, an item, a passive
or an ascendancy. The rate model below follows Path of Building 2.67's trigger
calculation, the project's pinned oracle.

## No energy-based meta gems in PoE1

PoE1 3.30 has **no** energy-based meta gems. Energy-charging meta gems (gems
that fill "energy" and trigger socketed spells when full) are a PoE2 system.
PoE2 differs; do not apply this there.

The word "energy" does appear in PoE1 in unrelated places (Penance Brand's
stacking resource, energy shield). Those are not triggers.

## The common trigger sources

| Trigger | Condition |
|---|---|
| Cast On Critical Strike | a linked attack lands a critical strike |
| Cast on Melee Kill | a linked melee attack kills an enemy |
| Cast when Damage Taken (CwDT) | you take a total amount of damage since the last trigger |
| Cast when Stunned | you are stunned, with a chance |
| Cast on Death | you die |
| Cast on Ward Break | your ward breaks, with a chance |
| Cast while Channelling (CwC) | at a fixed interval while you channel a linked skill |
| Spellslinger | you **use** a wand projectile attack (on use, not on hit) |
| Item and passive triggers | the condition in the item's text (Poet's Pen, Mjolner, Kitava's Thirst and the like) |

Each has rules on what it can support. Read the gem or item text with the
knowledge tools; level caps (CwDT limits supported gem level) are data.

### Notes per source
- **CwDT** keeps a running total of damage taken. When it passes the
  threshold, the linked spells trigger and the total resets. Lines that lower
  the threshold scale it multiplicatively.
- **CwC** triggers on its own interval while channelling, not on the
  channelled skill's hits. 3.29 set its interval to a range by gem level and
  lowered its less-damage penalty from 30% to 20%.
- **Spellslinger** reserves mana and has its own cooldown. 3.26 set its
  reservation to a flat base at every gem level; 3.27 lowered its less-damage
  penalty to a range of 30% to 20%.
- **Cast on Ward Break**: 3.29 capped the cooldown-recovery bonus from ward.

## Trigger rate

A triggered spell can fire no faster than both of these allow:

1. The **trigger's own cooldown** (the support gem's or item's cooldown).
2. The **triggered skill's own cooldown**, if it has one.

and no faster than the trigger condition happens (crits per second, kills,
damage taken, channel time).

### Cooldown recovery rate

```
effective cooldown = base cooldown / (1 + increased cooldown recovery rate / 100)
```

Cooldown recovery lines that the trigger reads must apply to the trigger (most
trigger gems read your global cooldown recovery). Some sources do not affect
trigger cooldowns; read the line.

### Server tick rounding

The server runs in ticks of 33 ms (about 30 per second). A cooldown that ends
mid-tick ends at the next tick.

```
cooldown on server = ceil(effective cooldown / 0.033) x 0.033
max triggers per second = 1 / cooldown on server
```

This creates **breakpoints**: cooldown recovery helps only when it moves the
rounded cooldown down by a whole tick. A 0.15 s cooldown runs as 5 ticks
(0.165 s); you need enough recovery to reach 4 ticks (0.132 s) before the
rate changes.

### Several spells on one trigger
- PoB models one trigger gem with several spells as a rotation: each trigger
  event fires the next spell in turn that is off cooldown. Each spell then gets
  roughly the trigger rate divided by the number of spells.
- CwDT fires all its linked spells together when the threshold is passed.
  Not confirmed for every trigger source in 3.30; read the gem text.

### Trigger chance
- Triggers with a chance (Cast when Stunned, Cast on Ward Break, some item
  triggers) fire on average at rate x chance. PoB uses an expected-value model
  for this.

## Damage of triggered spells

- A triggered spell uses your spell modifiers as normal.
- Many trigger sources carry a **less damage** multiplier on the triggered
  spell (CwC, Spellslinger, some ascendancy notables such as the Saboteur's
  Perfect Crime, which 3.28 changed). This is a more/less multiplier and
  stacks multiplicatively with everything else.
- **Cast speed does not change a trigger rate.** The triggered spell does not
  use its cast time; cast speed only matters for skills you cast yourself.
  Some cooldown skills add their cast time to their cooldown when triggered;
  3.26 removed this from Hexblast. Treat it as per-skill.
- Triggered skills usually have no mana cost. This depends on the source; not
  confirmed for every trigger in 3.30.
- Supports that need you to cast the skill yourself (Spell Echo, Unleash) do
  not help triggered spells. Check the support's text: many say they cannot
  support triggered skills.

## 3.26 to 3.30 changes touching triggers
- 3.26: Hexblast cooldown rule changed (triggered casts no longer add cast time).
- 3.27: Spellslinger penalty lowered. Snipe's triggered skills got two extra
  arrows by mistake (fixed in 3.29).
- 3.28: Saboteur's Perfect Crime and Like Clockwork changed. Poet's Pen could no
  longer be triggered through Kinetic Flux (bug fix).
- 3.29: CwC interval and penalty changed; Cast on Ward Break cooldown recovery
  capped; General's Cry no longer supports skills with cooldowns.
- 3.30: no trigger rule changes found; only a bug fix for chance to deal double
  damage on full life rolling twice.

## Common mistakes

- Applying PoE2 energy and meta-gem rules to PoE1.
- Scaling a triggered spell's rate with cast speed.
- Ignoring server tick rounding and quoting fractional cooldowns.
- Forgetting that the trigger's cooldown and the spell's own cooldown both cap
  the rate.
- Forgetting the triggered-spell less-damage multiplier of the source.
- Treating Spellslinger as "on hit". It triggers on use of a wand attack.
- Quoting CwC numbers from before 3.29.

## Check with the engine

- The engine computes cooldowns rounded to server ticks where it models a
  skill's rate. Trigger rates for trigger gems may not be computed in 3.30.
  If the main skill shows no trigger rate field, say the rate comes from these
  rules and PoB, and look up the gem's cooldown through the knowledge tools.
