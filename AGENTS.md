# AGENTS.md - working in exiled-studio-knowledge

Rules for anyone contributing, human or AI agent. The plan is `KNOWLEDGE-PACK-PLAN.md` (agreed 2026-11-15); its decisions D1 to D9 are authoritative here. Code for the knowledge MCP and the dev skill lives in `DBAggie/Exiled-Studio`, under its own `AGENTS.md` and ADRs (ADR-018).

## Hard rules
1. **Games are kept strictly apart.** Every knowledge file says `game` and `patch`. PoE1 files live only under `plugins/poe1-expert`, PoE2 only under `plugins/poe2-expert`. The validator fails a file whose `game` does not match its plugin.
2. **Every knowledge file has the header** (`schema/knowledge-header.schema.json`): `game`, `patch`, optional `league`, `as_of`, `sources`, `verification`, optional `status`.
3. **All prose is ours.** Verify against the game, the Exiled Studio engine, patch notes and the wikis, and cite sources by link. **Never copy text from poewiki or poedb** (CC BY-NC-SA 3.0, which conflicts with this repo's MIT license), nor from guides, Reddit or forums. Take ideas, credit them in `sources`, write your own words.
4. **Game data is never written into references.** Gem, mod, unique, base and passive numbers come from the knowledge MCP at answer time. A reference may name an example and explain a rule, not list data tables.
5. **Economy data** comes only from poe.ninja's supported economy-overview endpoints, through the refresh job (`tools/refresh/`). Meta and popularity are summarized by hand. Sessions never call poe.ninja.
6. **Verification is honest.** A new file starts `unverified`. Only the maintainer sets `maintainer-approved`; `engine-checked` and `in-game-checked` need the check named in the file.
7. **Answer keys are the maintainer's.** Sessions may draft eval questions, never keys (`evals/README.md`).
8. Nothing may suggest the pack is made or endorsed by Grinding Gear Games.
9. Never commit GGG art, audio or other assets, or raw game files.
10. `main` is protected: branch, open a PR, and commit or push only when the maintainer asks.

## Layout
```
.claude-plugin/marketplace.json     marketplace: poe1-expert, poe2-expert (stub)
plugins/poe1-expert/                plugin: skills/, .mcp.json (knowledge MCP over stdio)
  skills/poe1-mechanics/            layer 2: references/<topic>.md
  skills/poe1-build-advisor/        layer 4: references/<playbook>.md
  skills/poe1-community/            layer 3: references/<topic>.md
  skills/poe1-economy/              snapshots/<league-slug>/<date>.{json,md}
plugins/poe2-expert/                stub until after PoE2 1.0 (2026-12-11)
schema/knowledge-header.schema.json the header every knowledge file carries
evals/                              suites/<suite>.jsonl, check_cases.py, run.py (local runner)
tools/validate/                     validate.py and its tests
tools/refresh/                      economy refresh, patch-note triage
REVIEW-QUEUE.md                     decisions waiting on the maintainer, one at a time
VERIFICATION-HANDOFF.md             work list for verifying the draft references (Q9)
```

## Commands
```sh
python -m unittest discover -s tools/validate -v
python tools/validate/validate.py
python evals/check_cases.py
python -m unittest discover -s evals            # eval runner tests (fake model)
python -m unittest discover -s tools/refresh    # triage and refresh tool tests
python evals/run.py --dry-run                   # the runner itself is run by hand, never in CI
```

## Versioning
`poe1-expert` is `<patch>-kb.<n>` (for example `3.30.0-kb.4`); bump `n` on each merged content PR, and set it in both `plugins/poe1-expert/.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` (the validator checks they match).

## Pull requests
One topic per PR, one PR per session. Each PR says what it verified and how, lists its sources, and updates `REVIEW-QUEUE.md` with any decision it needs.
