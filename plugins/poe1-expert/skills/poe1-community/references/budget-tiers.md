---
game: poe1
patch: 3.30.0
as_of: 2026-11-17
sources:
  - https://www.pathofexile.com/forum/view-thread/4013680
  - https://www.pathofexile.com/forum/view-thread/3913392
  - repo:plugins/poe1-expert/skills/poe1-economy/snapshots/covens/2026-11-16.json
verification: maintainer-approved
---

# Budget tiers

How players talk about budgets, what each tier usually buys, and how to plan upgrades.
No prices here. What a divine buys, and what an item costs, changes daily and by
league: that is snapshot content in `poe1-economy`. Always state the snapshot's
league and `as_of` when you put a price on a tier.

## The units
- **Chaos**: the small unit. Rares, gems and cheap uniques are priced in chaos.
- **Divine**: the main unit for anything valuable. Budgets are almost always said
  in divines.
- **Mirror**: the top. "Mirror tier" means near-perfect gear, priced in mirrors or
  hundreds of divines.
- Exalted Orbs are a low-value orb in PoE1 now, not the budget unit (the first Covens
  snapshot has one well under a chaos).

## The tiers players use

### League start / zero budget
Self-found gear, vendor recipes, and crafts from the bench and essences. The build
must work with whatever drops. The goal is resist cap, life, a 4L or 5L for the main
skill, and a movement skill. Sell good drops for the first currency.

### A few divines (early to mid maps)
Buys the basics on trade: a 6L body armour of the needed base (often a cheap rare or
a common unique), key build-enabling uniques that are not chase items, capped resists
with decent life or ES, and a solid weapon if the build needs one. Enough for yellow
and early red maps.

### Tens of divines (red maps, early pinnacle bosses)
Good rares in every slot, cluster or other key jewels, high-level or Exceptional gems
for the main links (most Awakened supports can no longer be obtained since 3.28), better flasks with good mods, and the first real defence layers
(suppression, block, max res, a strong defensive aura set-up). Enough for T16 and
the easier pinnacle bosses with a well-made build.

### Hundreds of divines (uber bosses, juiced maps)
Chase uniques, crafted high-tier rares, corrupted implicits, top jewels, and the last
few percent of each layer. Enough for T17 / Nightmare Maps and uber bosses for most
strong builds.

### Mirror tier
Near-perfect items, often mirrored copies. The build is at its ceiling. Each upgrade
costs a lot and adds little.

## What gives the most per divine
Rough order for most builds. Always check the specific build.

1. **Resist cap and enough life or ES.** Free power. Nothing else matters if you die.
2. **The main skill's links.** Going 4L to 5L to 6L is a big damage step each time.
3. **The build-enabling item.** If the build needs one unique to work, buy it first.
4. **Weapon (for attacks) or gem levels (for spells).** The biggest damage scalers.
5. **Flasks.** Cheap, and good flask mods are a large defence and speed gain.
6. **Movement and quality of life.** Faster maps mean more currency.
7. **Defence layers.** Suppression, block, armour or evasion, max res, ailment answers.
8. **Jewels and the last affixes.** Expensive per percent; leave for late.

## How to plan upgrades by tier
- Write down what the build needs at the next tier: the content (red maps, a boss),
  the defence target, and the damage target.
- Find the one or two weakest slots. A slot with no life and no resists is the first
  fix, before any damage slot.
- Prefer upgrades that carry to the next tier. A good weapon base you keep beats a
  cheap one you replace.
- Avoid half-steps on expensive items. Buying a poor version of a chase unique often
  means buying it twice.
- Craft where crafting is cheaper than buying. Essences and the bench make good
  league-start rares. See `crafting.md`.
- Re-check after each upgrade with the build's calc (the Exiled Studio engine or
  PoB). Do not assume the gain.

## Things that change budgets in 3.30
- **Rare item tiers.** From Act 6 on, rare and magic drops can have an item tier (2 to
  5). Higher tiers roll better mods and more sockets and links. Good self-found rares
  may be easier to find at league start. Not in Ruthless.
- **Orbs of Chance** are much rarer and no longer sold by vendors. Chance-based
  unique hunting costs more.
- **Orbs of Binding** no longer drop. Plan links with jewellers, fusings and the bench.
- **Vendor recipes**: two rares with the same name give a Chaos Orb; three give an
  Exalted Orb. A full rare set with an item below level 60 now gives Orbs of Alchemy.
  This helps a zero-budget start.
- **Scarabs are gone.** Map investment is Threads now; budgets that counted scarab
  costs or scarab income need redoing (`atlas.md`).
- **Sacrifice and Mortal fragments** are gone as an income source (Atziri moved into
  the Temple of Atzoatl).
- **Bench locks** (keeping prefixes or suffixes) now cost several Divine Orbs plus a
  second currency that depends on the item type; the new one- and two-mod locks cost
  one or two divines. That makes metacrafting a mid-budget step, not a league-start
  one. See `crafting.md`.

## Mode notes
- **SSF**: there is no budget, only what you find and craft. Plan by what drops and
  what the bench, essences and recipes can make.
- **HC**: spend on defence first at every tier.

## Common mistakes
- Quoting prices or "this costs N divines" from memory. Prices are snapshot content.
- Spending on damage before resists, life and links are done.
- Calling a build "budget" when it needs one chase unique.
- Buying for the next tier before the current tier's content is on farm.
- Giving PoE2 budget advice; PoE2's top trade unit is the exalted orb, not the divine.

## Verification (2026-11-17)

`engine-checked` here means: the items and rules 3.30 removed or changed were checked against the official 3.30.0 notes (item tiers, Orbs of Chance and Binding, vendor recipes, bench lock costs, scarabs, Atziri's fragments) and 3.28.0 notes (Awakened supports), and cross-checked with the first Covens economy snapshot (2026-11-16: no scarab overview, Threads in its place, only Awakened Empower/Enlighten/Enhance listed, the exalt well under a chaos). No prices are stated here. What each tier buys is a community rule of thumb.

Approved by the maintainer on 2026-11-17 (given in chat, recorded by the session). The checks named above are what was done before approval; nothing here was checked in game unless a line says so.
