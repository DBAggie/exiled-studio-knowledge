# Maintainer review queue

Decisions the autonomous sessions could not make. **Review one item at a time**, top to bottom. Each item stands on its own: the question, why it matters, what was done meanwhile (the default), and the choices. Answer an item by editing its **Answer** line (or tell a session), then move it to "Answered" at the bottom.

## Open

### Q1. Repository visibility
- **Question:** Make `DBAggie/exiled-studio-knowledge` public?
- **Why:** The plan sets an MIT license and an install by `/plugin marketplace add`, which suggests a public repo. Making something public is your call, so the session did not.
- **Default taken:** created **private**. Install still works on machines where `gh`/git is signed in as you.
- **Choices:** make it public now / keep private until v1 gate / keep private.
- **Answer:**

### Q2. ADR-018 and its five defaults
- **Question:** Accept ADR-018 (knowledge MCP) as proposed in DBAggie/Exiled-Studio PR #123, including its five "Not decided here" defaults?
- **Why:** It blocks plan step 6 (`tools/knowledge-mcp`). The defaults: (1) serve only `Trusted` bundles, not ones accepted in the app; (2) Steam build to patch table in the tool; (3) ship the binary as a release asset beside the app; (4) `get_price` takes item name plus optional variant and links; (5) a preparatory PR moves the bundle scan from `loom-app` into a small host crate.
- **Default taken:** nothing built; the ADR waits for your merge.
- **Choices:** merge as is / merge with changes (say which) / reject.
- **Answer:**

### Q3. Which patch is the current bundle?
- **Question:** Is Steam build 26530219 (the bundle in OneDrive, extracted 2026-11-15) patch 3.30.0 (Covens of Umbra) or a 3.29 build?
- **Why:** The pack targets 3.30. ADR-018's patch table and every MCP answer's `patch` field need this row. A 3.29 bundle would answer 3.30 questions with old data.
- **Default taken:** none recorded; references say `patch: 3.30.0`.
- **Choices:** 3.30.0 / 3.29.x (then a new data run for 3.30 is needed) / unknown.
- **Answer:**

### Q4. Knowledge MCP missing at install
- **Question:** Keep `.mcp.json` in `poe1-expert` now, while `exiled-studio-knowledge-mcp` does not exist yet?
- **Why:** Until the binary exists, every session with the plugin shows one failed MCP server. Removing it loses nothing today.
- **Default taken:** kept (the plan's layout), with `EXILED_STUDIO_KNOWLEDGE_MCP` to point at a dev build; the skills say what to do without it.
- **Choices:** keep / remove until step 6 lands.
- **Answer:**

### Q5. How CI runs evals
- **Question:** How should CI call Claude for the fast eval subset (plan D8), and with whose key?
- **Why:** The runner needs a model call per case, twice (with and without the plugin). That needs an Anthropic API key as a GitHub secret, which costs money per PR.
- **Default taken:** CI only checks case format; the runner is not built.
- **Choices:** API key secret, fast subset on PRs, full suite manually / run evals only on the workstation / decide later.
- **Answer:**
