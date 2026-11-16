# Maintainer review queue

Decisions the autonomous sessions could not make. **Review one item at a time**, top to bottom. Each item stands on its own: the question, why it matters, what was done meanwhile (the default), and the choices. Answer an item by editing its **Answer** line (or tell a session), then move it to "Answered" at the bottom.

## Open

### Q2. ADR-018 and its five defaults
- **Question:** Accept ADR-018 (knowledge MCP) as proposed in DBAggie/Exiled-Studio PR #123, including its five "Not decided here" defaults?
- **Why:** It blocks plan step 6 (`tools/knowledge-mcp`). The defaults: (1) serve only `Trusted` bundles, not ones accepted in the app; (2) Steam build to patch table in the tool; (3) ship the binary as a release asset beside the app; (4) `get_price` takes item name plus optional variant and links; (5) a preparatory PR moves the bundle scan from `loom-app` into a small host crate.
- **Default taken:** nothing built; the ADR waits for your merge.
- **Choices:** merge as is / merge with changes (say which) / reject.
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

### Q6. poe.ninja User-Agent contact
- **Question:** What contact should the refresh job's User-Agent carry?
- **Why:** poe.ninja asks for a User-Agent that names the app and a contact. Sessions do not put your name, email, or project in requests to outside services without your OK.
- **Default taken:** `exiled-studio-knowledge-refresh/0.1` with no contact. The first snapshot (PR #2) was fetched with it: 16 requests, 2 s apart.
- **Choices:** the repo URL / a contact email / keep it without a contact. Set it with `REFRESH_USER_AGENT` in the scheduled task.
- **Answer:**

### Q7. Register the scheduled refresh
- **Question:** Register the economy refresh as a Windows scheduled task on the main workstation, and at what cadence?
- **Why:** The plan says refreshes run as scheduled tasks on your workstation. Registering a task changes the machine, so the session did not do it.
- **Default taken:** scripts only (PR #2): `tools/refresh/run-economy.ps1` (one refresh as a PR) and `tools/refresh/register-task.ps1` (you run it once: `-League Covens -EveryDays 2` for league-start week, then 7 to 14).
- **Choices:** register now, every 2 days / register after league-start week / run by hand.
- **Answer:**

### Q8. Snapshot size in git
- **Question:** Is about 1.6 MB of JSON per snapshot acceptable in git history?
- **Why:** Every 2 days in league-start week and weekly after, a league adds roughly 15 to 25 MB. Skill gems are most of it (gem variants with fewer than 5 listings are already left out).
- **Default taken:** kept as is, one row per line so diffs stay small.
- **Choices:** keep / drop skill gems / raise the listing floor / Git LFS.
- **Answer:**

### Q9. Mechanics drafts: how to verify
- **Question:** How should the 22 draft references (PRs #4 to #25) reach `maintainer-approved`?
- **Why:** poewiki blocked every automated fetch, and the official 3.30 patch-note thread was not found. Rules were checked against patch-note copies (poedb, patchbot.io), the pinned PoB 2.67.2, and memory. Each PR lists, under "For the maintainer", the exact points nobody could confirm.
- **Default taken:** every file is `unverified`. Nothing merged.
- **Choices:** you review each PR's list and merge / a later session re-checks with the official threads (give the links) and the engine first / merge as drafts, then verify in place.
- **Answer:**

### Q10. Stacked PRs
- **Question:** Merge order for the knowledge repo PRs?
- **Why:** PRs #2 to #25 are stacked on #1 (the skeleton, base `skeleton`). When #1 merges and its branch is deleted, GitHub retargets them to `main`. With a squash merge of #1 the others may show the skeleton's commit as a conflict.
- **Default taken:** none merged.
- **Choices:** merge #1 with a merge commit (no squash), then the rest in any order / squash #1 and let a session rebase the rest.
- **Answer:**

### Q11. Meta and build popularity
- **Question:** Who writes the meta and popularity summary for each snapshot?
- **Why:** The plan says it is written by hand from the poe.ninja builds page (no unsupported endpoints). The first snapshot's summary (PR #2) has prices only.
- **Default taken:** left out, said so in the summary.
- **Choices:** you write it / a session with the builds page open writes it, you review / skip meta for v1.
- **Answer:**

## Answered

### Q1. Repository visibility
- **Question:** Make `DBAggie/exiled-studio-knowledge` public?
- **Why:** The plan sets an MIT license and an install by `/plugin marketplace add`, which suggests a public repo. Making something public is your call, so the session did not.
- **Default taken:** created **private**. Install still works on machines where `gh`/git is signed in as you.
- **Choices:** make it public now / keep private until v1 gate / keep private.
- **Answer (maintainer, 2026-11-16):** keep it a separate private repo. Done: `DBAggie/exiled-studio-knowledge` is private.


### Q3. Which patch is the current bundle?
- **Question:** Is Steam build 26530219 (the bundle in OneDrive, extracted 2026-11-15) patch 3.30.0 (Covens of Umbra) or a 3.29 build?
- **Why:** The pack targets 3.30. ADR-018's patch table and every MCP answer's `patch` field need this row. A 3.29 bundle would answer 3.30 questions with old data.
- **Default taken:** none recorded; references say `patch: 3.30.0`.
- **Choices:** 3.30.0 / 3.29.x (then a new data run for 3.30 is needed) / unknown.
- **Answer (maintainer, 2026-11-16):** 3.30.0. Steam build 26530219 is patch 3.30.0 (Covens of Umbra); the references' `patch: 3.30.0` stands, and ADR-018's patch table gets this row.

