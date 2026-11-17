---
game: poe1
patch: 3.30.0
as_of: 2026-11-17
sources:
  - https://www.pathofexile.com/forum/view-thread/3985332
  - https://www.pathofexile.com/forum/view-thread/4013680
  - https://www.pathofexile.com/forum/view-thread/3913392
  - https://www.pathofexile.com/forum/view-thread/3869068
verification: maintainer-approved
---

# Build archetypes and league starters

This file explains archetypes in general terms. It does not say which skill or
ascendancy is strong this league. That is meta, and meta is snapshot content: use
`poe1-economy` and state its league and `as_of`. Balance changes each patch, so an
archetype that was strong last league may not be now.

## Two axes: how you deal damage, how you survive
Every build is one choice on each axis. Name both when you describe a build.

## Damage delivery

### Self-cast spells
You press the button and the spell goes off. Scales with cast speed, spell damage,
gem levels and crit or elemental damage. Easy to level with and easy to gear early.
3.29.0 retuned most spells (official notes): higher base damage with more growth per
gem level, faster but costlier lightning spells, cheaper fire spells with more added
damage effectiveness, and Unleash made stronger. Pre-3.29 spell numbers are out of date.

### Attacks
Melee or ranged skills that use weapon damage. The weapon is the biggest damage
source, so the build lives and dies by one item. Needs accuracy (unless the build
never misses). Bows are ranged attacks with their own scaling.

### Damage over time (DoT)
Ignite, poison, bleed and degen spells. Degen spells never hit, so evasion and
block don't stop them; ailments from hits still need the hit to land. Scales with DoT multipliers rather than crit multi. Often
cheap to start, because many DoT layers come from the tree and gems, not gear.

### Minions
Your summons deal the damage. Since 3.27 minion attacks always hit, and since 3.29
non-Spectre minions no longer pause while attacking. Gear and tree scale the minions, not you, so your own
gear can go to defence. Good for players who want safety. Weak points: minion AI,
minions dying in hard content, and fewer ways to scale on cheap gear late.

### Totems, traps, mines
The skill is placed and hits on its own. You stay out of danger. Totem, trap and
mine supports change the skill's damage and speed. 3.29.0 raised the
less-damage penalty on Spell Totem, Ballista Totem, Blastchain Mine and High-Impact
Mine and raised the two mine supports' cost multiplier (official notes); check current
gem data before recommending one.

### Triggers
A support casts spells for you when something happens: on crit (CoC), while
channelling (CwC), when hit (CwDT), or through a unique item. Damage is capped by the
trigger's cooldown and rate, so cast-speed scaling stops working. Often strong but
gear-heavy and fiddly; rarely a league starter.

## Defence layers

### Life-based
Life plus armour, evasion, block or suppression. The default. Forgiving, cheap, and
the best choice for a starter. Most uniques and rares are made for it.

### ES-based
Energy shield as the main pool. Chaos damage bypasses ES unless the build is CI. High pools on endgame gear, but ES needs a recovery
plan (regen, leech, recharge). Bad at league start because ES gear is costly.

### CI (Chaos Inoculation)
Life set to 1, chaos immunity. Pure ES. Removes chaos damage as a threat. Needs
good ES gear before it is safer than life. A mid-league switch, not a starter.

### Low-life (LL)
Life reserved down to low life on purpose, to turn on low-life bonuses, with ES as the
real pool. Needs reservation set-up and specific items. Expensive; never a starter.

### Hybrid
Life and ES both high. Two pools but neither is maxed. Works on gear with both stats
and with ascendancies that help both.

### MoM and mana-heavy defence
Part of the damage goes through mana. Works with big mana pools. Combine with any of
the above.

## What makes a good league starter
A league starter must get through the campaign and early maps with self-found gear
and almost no currency. The tests:

1. **Damage from gems and tree, not gear.** If one unique or a high-tier weapon is
   needed, it fails on day one.
2. **Levels as itself or close to it.** Swapping skills mid-campaign is fine, but the
   end skill should be online by the late acts.
3. **Life-based defence that works with any rare.** Resists and life from drops.
4. **Clear speed in early maps.** Starters farm currency, so killing packs fast
   matters more than bossing at first.
5. **A plan for pinnacle bosses later.** Not on day one, but there must be an upgrade
   path that adds single target.
6. **Cheap upgrades with clear steps.** See `budget-tiers.md`.
7. **Survives patch changes.** A build that relied on a mechanic changed this patch
   is a risk. Read the patch notes for the skill and its supports.
8. **Not hit by the league mechanic.** Some league mechanics punish slow, fragile or
   melee builds. Check what the current league asks of the player.

## How to judge a build someone shows you
- Ask what content it is for: mapping, bossing, or both.
- Check the defence layers first. A build with no answer to big hits fails in red maps.
- Check resists at cap, a stun answer, a flask set-up, and a way to remove ailments.
- Check its damage config: what buffs, charges and enemy debuffs it assumed.
- Check what it costs to work. A "budget" build that needs a rare chase unique is not.
- Check the patch: were its skill, supports or key uniques changed in 3.26 to 3.30?
- For HC or SSF, weigh safety and self-found gear far more than DPS.

## Mode notes
- **HC**: defence first. A build that dies once is worth nothing.
- **SSF**: no trade, so the build must work with what drops and what you can craft.
  Builds that need one specific unique are poor SSF picks.
- **Ruthless**: much lower loot and different balance. Normal-league advice does not
  carry over. Note: 3.30 rare item tiers do not apply in Ruthless.

## Common mistakes
- Naming this league's strongest skills from memory. That is snapshot content.
- Calling a trigger, CI or low-life build a league starter.
- Comparing builds by DPS alone, without defences or the config behind the number.
- Recommending a build from an older patch without checking 3.26 to 3.30 changes to
  its skill, supports, ascendancy and key uniques.
- Treating "minion build" as automatically safe. Minions die, and the player can too.
- Giving PoE2 archetype advice. PoE2 has different skills, supports and defences.

## Verification (2026-11-17)

`engine-checked` here means: the two 3.29 claims that came from third-party summaries (self-cast changes, totem and mine support nerfs) are now confirmed from the official 3.29.0 notes; the minion and energy shield lines agree with the mechanics references; "meta gem" (a PoE2 term) was removed from the triggers section. The archetype descriptions and the league-starter tests are community advice, not game rules.

Approved by the maintainer on 2026-11-17 (given in chat, recorded by the session). The checks named above are what was done before approval; nothing here was checked in game unless a line says so.
