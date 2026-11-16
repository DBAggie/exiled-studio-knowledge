---
name: poe1-economy
description: Path of Exile 1 economy and meta snapshots - item and currency prices, craft costs, build popularity, and league-specific strategy, as dated snapshots of a league. Use when a PoE1 player asks what something costs, what is popular, or what is worth farming. Not for PoE2.
---

# PoE1 economy snapshots

## Rules
1. **Every answer from a snapshot states its `as_of` date and its league**, for example "As of 2026-11-15 in Covens of Umbra (softcore trade), a Divine Orb was about N Chaos Orbs."
2. **Warn when the snapshot is stale.** Refresh cadence: league-start week, every 1 to 2 days; after that, weekly to every two weeks. If the newest snapshot is older than that for the current point in the league, say prices may have moved.
3. **Never fetch prices yourself.** Prices come from the snapshots here (or the knowledge MCP's `get_price`, which reads the same files). Do not call poe.ninja or the trade site. Tell the user to check the official trade site for live prices.
4. Use the snapshot for the user's league only. Never use one league's prices for another (Standard, Hardcore, SSF and the challenge league differ).
5. Meta and popularity notes are hand-written summaries, dated like prices.
6. Snapshots from ended leagues are kept and marked `historical`; never present them as current.

## Files
- `snapshots/<league-slug>/<date>.json`: prices from poe.ninja's economy overviews (written by the refresh job, `tools/refresh/`).
- `snapshots/<league-slug>/<date>.md`: the hand-written summary for that date (meta, popularity, notable prices).
- The newest file per league is the current one.
