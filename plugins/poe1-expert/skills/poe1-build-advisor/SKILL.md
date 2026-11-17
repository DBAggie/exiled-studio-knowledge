---
name: poe1-build-advisor
description: Path of Exile 1 (patch 3.30) build advice - diagnosing a character, defensive thresholds, gearing progression, reading calculation breakdowns, trade-offs, and planning or theorycrafting a build. Use when a player asks for help with a PoE1 build, character, or upgrade, or with Exiled Studio's build data. Not for PoE2.
---

# PoE1 build advisor (patch 3.30)

## Hard rules for numbers
1. **When the Exiled Studio app MCP is reachable** (tools such as `get_build`, `get_breakdown`, `preview_item_edit`), every numeric claim about the user's build (DPS, EHP, max hit, resistances, the effect of a change) is checked with `get_breakdown` or `preview_item_edit` (or `preview_tree_change`) **before** you state it. Quote the tool's number, not your own arithmetic.
2. **When it is not reachable**, label every number an **estimate**, and say how to check it (Exiled Studio or Path of Building).
3. **A field whose state is `unsupported`, `indeterminate`, or `not-computed` is never read as zero.** Say the app does not compute it yet.
4. Read `list_warnings` before giving a verdict: unresolved lines and partial results change what the numbers mean.
5. Game data (gems, mods, uniques, bases, passives) comes from the knowledge MCP, never from memory.

## Before answering
- Confirm the game is PoE1 and the league or patch (`poe2-scope` skill for PoE2).
- Ask for what you need: the build (Exiled Studio open, PoB code, or the character), the budget, the content the player wants to do, and their league (Challenge or Standard, softcore or hardcore, SSF or trade).
- Mechanics questions: use `poe1-mechanics`. Prices or meta: use `poe1-economy`, and state its `as_of` and league.

## Playbooks (load only what the question needs)
| Playbook | File |
|---|---|
| Diagnosis checklist: "why do I die", "why is my damage low" | `references/diagnosis.md` |
| Defensive thresholds by content tier | `references/defensive-thresholds.md` |
| Gearing progression and upgrade order | `references/gearing.md` |
| Reading Exiled Studio and PoB breakdowns | `references/reading-breakdowns.md` |
| Common trade-offs | `references/trade-offs.md` |

A playbook with no file yet: give general advice, mark it as not from a reviewed playbook.
