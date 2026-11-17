# Refresh jobs

Run on the maintainer's workstation as scheduled tasks (plan D7). Each run opens a PR to this repository; nothing is committed directly, and every refresh goes through the maintainer's review.

- **Economy** (`economy.py`, plan step 8): fetches poe.ninja's supported economy-overview endpoints for one league, low volume and cached, with a plain User-Agent, and writes `plugins/poe1-expert/skills/poe1-economy/snapshots/<league-slug>/<date>.json`. Claude sessions never call poe.ninja.
- **Patch-note triage** (later): matches patch-note lines to mechanics references by keyword and stat ID and opens issues. It never rewrites a reference.

Cadence: league-start week every 1 to 2 days; then weekly to every two weeks; stop at league end and mark that league's snapshots `historical`.
