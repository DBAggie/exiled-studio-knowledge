# Exiled Studio knowledge

Path of Exile knowledge for Claude sessions, as a Claude Code plugin marketplace: game mechanics, community knowledge, build advice, and dated economy snapshots. It serves sessions working on [Exiled Studio](https://github.com/DBAggie/Exiled-Studio) and sessions helping a player plan, fix or theorycraft a character.

- **`poe1-expert`**: Path of Exile 1, patch 3.30 (Covens of Umbra). Skills `poe1-mechanics`, `poe1-build-advisor`, `poe1-community`, `poe1-economy`, and the Exiled Studio knowledge MCP for game-data lookups.
- **`poe2-expert`**: a placeholder until after Path of Exile 2 1.0 (2026-12-11).

Status: skeleton. The references, playbooks and snapshots arrive in reviewed PRs, and every file says how far it has been verified. The plan is [KNOWLEDGE-PACK-PLAN.md](KNOWLEDGE-PACK-PLAN.md).

## Install
```
/plugin marketplace add DBAggie/exiled-studio-knowledge
/plugin install poe1-expert@exiled-studio-knowledge
```
The knowledge MCP (`exiled-studio-knowledge-mcp`, built in the Exiled Studio repository, ADR-018) starts with the plugin over stdio; set `EXILED_STUDIO_KNOWLEDGE_MCP` to its path if it is not on `PATH`. Until it exists, the skills fall back to labelled estimates. For the app MCP, start it in Exiled Studio and add its URL and token to your client once.

## License and notices
MIT ([LICENSE](LICENSE)). All text is our own; sources are cited by link.

This is a fan-made project. It is not made, endorsed or authorised by Grinding Gear Games. Path of Exile is a trademark of Grinding Gear Games.
