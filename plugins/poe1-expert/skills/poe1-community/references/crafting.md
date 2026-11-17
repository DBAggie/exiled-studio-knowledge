---
game: poe1
patch: 3.30.0
as_of: 2026-11-17
sources:
  - https://www.pathofexile.com/forum/view-thread/4013680
  - https://www.pathofexile.com/forum/view-thread/3985332
  - https://www.pathofexile.com/forum/view-thread/3913392
  - https://www.pathofexile.com/forum/view-thread/3869068
  - https://www.pathofexile.com/forum/view-thread/3787013
  - https://www.pathofexile.com/forum/view-thread/4016174
  - repo:plugins/poe1-expert/skills/poe1-economy/snapshots/covens/2026-11-16.json
  - https://poedb.tw/us/Crafting_Bench
  - https://poedb.tw/us/Horticrafting
  - https://poedb.tw/us/Resonator
  - https://www.craftofexile.com/
verification: engine-checked
---

# Crafting methods

The main ways to make gear, as concepts. No mod weights, tiers or costs here: look
them up with the knowledge tools. Each method notes whether it is confirmed in 3.30
and which patch last changed it. PoE2 has different crafting (no bench, different
essences and orbs); do not apply any of this there.

## The basics every method uses
- An item's **item level** sets which mod tiers can roll.
- A rare has up to three **prefixes** and three **suffixes**.
- Every mod has a **weight**. Rare mods roll rarely; that is why targeted methods exist.
- **Corrupted** items can't be changed by most methods.
- **3.30 item tiers**: rare and magic drops from Act 6 on can have an item tier from 2
  to 5. A higher tier gives better mod tier ratings, quality, sockets and links, and
  tier 5 may add one item level or drop as a fractured magic item. Good crafting bases
  can now be found, not just bought. Not in Ruthless.

## Currency spam
Reroll the whole item with one orb type until you hit what you want.
- **Alteration spam** on magic items: aim for one or two mods, then regal or bench.
- **Chaos spam** on rares: rerolls all mods. Cheap per try, poor odds for exact items.
- 3.29 added bench options that reroll one or three random mods on a rare for chaos.
- 3.30: bench options that cost Orbs of Chance now cost Orbs of Alteration instead.

Confirmed in 3.30. Best for cheap items where many outcomes are fine.

## Essences
An essence makes a rare with one guaranteed mod and random others. Higher essences
give higher tiers; a few special essences add mods that can't roll otherwise.
- 3.27: Vaal Orbs work on monsters trapped by essences (Remnants of Corruption gone).
- 3.28: essences stack to 10.
- 3.30: a new Essence of Trickery; essences have a base chance to spawn in maps.

Confirmed in 3.30. The default league-start crafting tool.

## Fossils and resonators
Fossils in a resonator reroll a rare with weights pushed toward some mod groups and
away from others, or with special effects.
- 3.28: fossils come only from Delve.
- 3.28: fossils are found far more often behind fractured walls and off the main
  paths in Delve.
- 3.29: Fractured Fossils fracture a random mod and cannot be used on fractured or
  influenced items.
- 3.30: Delve's atlas passive clusters were removed, and Sulphite no longer appears
  in maps at random (a few named maps always have it, and its veins give more). Delve
  itself still exists. How much this changes fossil supply is not a rule but a market
  fact: it is snapshot content (`poe1-economy`), and the first Covens snapshot does
  list fossils as traded.

Fossils and resonators both exist in 3.30. The notes do not name resonators, but
poedb's current game data (which already carries the 3.30 bench options) lists the
four Chaotic Resonators, one per socket count.

## Harvest (Horticrafting)
Lifeforce from Harvest buys crafts at the Horticrafting station. The best-known are
**reforges**: reroll a rare with a guaranteed mod of one type (fire, life, defence and
so on), and similar targeted crafts.
- 3.27: reforges that guarantee a mod type respect "cannot roll" meta-crafts.
- 3.29: the white-socket reforge was removed.
- 3.30: Harvest is no longer a separate plot: Sacred Flora spawn in the map and
  release Sacred Fauna when used. Lifeforce drops in bigger stacks (about the same
  total). Crafts that change one resistance mod or one damage-type mod into another
  now cost two lifeforce types; the divination card craft changed cost; the craft that
  swapped Sacrifice or Mortal fragments was removed.

Horticrafting is confirmed in 3.30. The type-guaranteed reforges are still there:
poedb's current Horticrafting list has them (fire, cold, lightning, physical, life,
defence, chaos, attack, caster, speed, critical and more), plus the "more likely" and
"less likely to keep the same mod types" reforges and an influence reforge. It has no
white-socket craft and no Sacrifice or Mortal fragment craft, as the 3.29 and 3.30
notes say. The list and its lifeforce costs are data; look them up, do not quote them
from memory.

## Crafting bench
Unlocked recipes add one crafted mod, change sockets and links, or apply meta-crafts.
- 3.26: veiled-mod recipes moved from unveiling to recipe objects near bosses in
  atlas maps.
- 3.28: options that cost Exalted Orbs now mostly cost a fixed number of exalts.
- 3.29: a bench is in every town from Act 2; socket-colour options changed; two new
  options reroll one or three random mods on a rare.
- 3.30: a white-sockets option; new options that lock one or two prefixes or suffixes,
  paid in Divine Orbs plus other currency by item type. Meta-craft recipes now come
  from Nightmare Maps instead of unique maps.

Confirmed in 3.30.

## Metacrafting
Bench mods that change how other crafting works, then a reroll or a remove step.
The classic moves:
- **Lock prefixes or suffixes**, then reroll or remove the other side.
- **Cannot roll attack / caster mods**, to block groups of mods from a reroll or an
  exalt slam.
- **Multimod**, to add more than one crafted mod.

3.30 changes (official notes):
- Four **new** options lock one or two prefixes, or one or two suffixes.
- The **old** "prefixes cannot be changed" and "suffixes cannot be changed" options
  are still there, next to the new ones. Their cost changed and now depends on the
  item type (weapons, armour and quivers, jewellery). The notes give each cost; look
  it up, do not quote it from memory.
- "Cannot roll attack/caster" no longer stops removal orbs like the Orb of Annulment
  from removing those mods.
- 3.30.0b Hotfix 4: a Veiled Chaos Orb can be used on an item with a veiled mod if
  that mod is not protected by fracturing or a meta-craft.
- **Multimod is still on the bench** ("can have up to 3 crafted modifiers"), next to
  the old and new locks and the two "cannot roll" crafts. The notes do not mention it;
  poedb's current bench list has it. Costs are data; check the bench data before
  planning a craft.

## Recombinators
Combine two items of the same kind into one, keeping some mods from each.
- 3.26: Isla in Kingsmarch offers a method that shows the chance first but can destroy
  items, next to the old random method.
- 3.30: the result uses the item level of the chosen base; mod counts for the random
  method changed; no longer usable on corrupted items.

Confirmed in 3.30.

## Eldritch implicits
Searing Exarch and Eater of Worlds implicits on body, helmet, gloves and boots, added
and upgraded with eldritch currency, rerolled with eldritch chaos and balanced with
the Orb of Conflict.
- Eldritch altars in maps are confirmed in 3.30 (their rarity bonus was lowered, and
  their mods now drop Threads).
- The eldritch currency is confirmed in 3.30: the first Covens snapshot (2026-11-16)
  lists Eldritch Ichors and Embers, the Eldritch Chaos Orb, Eldritch Exalted Orb,
  Eldritch Orb of Annulment and Orb of Conflict as traded in the league. The 3.30.0
  notes also fix a bug with eldritch implicit mods, so the implicits are in the game.

## Other methods worth naming
- **Fracturing Orb**: locks one mod. Part of the core drop pool since 3.28.
- **Foulborn orbs** (3.27): a Foulborn Orb of Augmentation, Regal Orb and Exalted Orb
  that add a mod with higher-level mods more likely. Confirmed in 3.30: all three are
  traded in the first Covens snapshot.
- **Beastcrafting**: Einhar's recipes. 3.30: yellow beasts are no longer captured or
  needed; flask-mod recipes need any red beast; the binding recipe gives Orbs of Regret.
- **Eternal Orb and imprints**: undo a craft step by restoring a saved copy. 3.30:
  imprinting and mirroring no longer count as modifying the item, so they can't be
  used on items with the "can be modified while corrupted" implicit.
- **Influence and awakener crafts**: confirmed in 3.30. The first Covens snapshot
  lists the Shaper, Elder and four Conqueror Exalted Orbs and the Awakener's Orb as
  traded, and the 3.30.0 notes mention Conqueror's Exalted Orbs dropping from
  Conqueror bosses. The notes change none of their rules.
- **Gwennen** (Expedition) no longer gambles items in 3.30; she offers a paid
  coin-flip between two crafting outcomes on one of your rares.
- **Double corruption** (3.30): the Temple's Altar of Corruption and Lapidary Lens now
  corrupt an item or gem a second time ("Twice Corrupted"), with a chance to destroy it.
- **Socket colours** (3.29): sockets are white by default with a small chance of
  colour; any gem fits any socket; matching colour gives extra quality. Chromatic
  orbs force one socket to have colour.

## How to choose a method
1. What mods do you need, and how many are rare? One common mod: currency spam or
   an essence. One specific group: harvest reforge or fossils. Two or more exact mods:
   metacraft or recombine.
2. Is the base worth it? High item level and, in 3.30, a high item tier.
3. What is the cheapest path to a usable item, not a perfect one?
4. Compare with buying. A crafted item that costs more than the trade item is a loss.

## Common mistakes
- Naming scarabs, Orbs of Binding or Remnants of Corruption as current. All three left
  between 3.27 and 3.30.
- Saying fossils drop anywhere in maps. Since 3.28 they come only from Delve.
- Assuming "cannot roll caster/attack" still protects mods from annulment in 3.30.
- Quoting bench costs or mod weights from memory. Look them up.
- Using PoE2 crafting rules (no bench, different essences, omens with other effects).

## Verification (2026-11-17)

Checked against the official 3.26.0 to 3.30.x notes and the first Covens economy snapshot (2026-11-16), which shows which crafting currencies are traded in the league. Confirmed: eldritch currency and implicits, Foulborn orbs, influence and awakener currency, the old locks next to the new ones, the Harvest rework. No bench costs are stated (the notes give exact figures; look them up).

Second pass the same day, at the maintainer's direction, with poedb's game data opened in the maintainer's browser: resonators (the Resonator page), multimod (the Crafting Bench page) and the type-guaranteed Harvest reforges (the Horticrafting page) are confirmed. poedb's data is current for 3.30: its bench list has the 3.30 white-sockets option and the new one- and two-mod locks. Craft of Exile (its data is for 3.29; the maintainer judged general crafting little changed since) agrees: its method list still has currency, fossil, harvest, essence, catalyst, beastcrafting, eldritch and bench crafting, and its metamods are multimod, the two full locks and the two "cannot roll" crafts. It does not yet have the 3.30 one- and two-mod locks; for anything 3.30 added, the official notes and poedb win. `engine-checked` here means checked against the official notes, the economy snapshot and poedb's game data; there is no engine for crafting. Fossil supply is a market question, left to snapshots. Not checked in game.
