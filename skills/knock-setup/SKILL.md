---
name: knock-setup
description: Connect Knock to your coding agent, discover and build notification workflows, and recommend how to trigger them from your application.
---

# Setup

End-to-end Knock setup for a coding agent: connect tooling, design and build notification workflows, then wire them into the application. Work through the rules below in order.

While working, keep every response to one short line — no summaries, no menus, no extra questions unless a step fails. The only exceptions are the opening encouragement + account ask (step 1), the workflow proposals, a prior-confirmation restatement (2–3 lines max), the implementation confirmation ask, the import-users id ask, the wrap-up signup-email ask (only when whoami has no email), the final wrap-up output, the Codex MCP handoff in `rules/connect-codex.md`, the Claude connector instructions in `rules/connect-claude.md` (directory link + connected ask), and the Grok Bot plugin instructions + surface-area ask in `rules/connect-grok-bot.md`, which have their own formats. When you end with a confirmation question (account, workflows, implementation, import-users id, wrap-up signup email, wrap-up guides ask, or Grok Bot surface area), that question must be the very last line of the message, on its own, and bolded.

## How to use this skill

1. **Open with encouragement, then confirm Knock account** (required first action — do this before anything else)
   - **Opening (first message only).** Before the account ask, say a short word of encouragement (about 2–3 sentences). Keep it warm and plain — not a feature pitch, not a menu of next steps.
     - **Most tools.** They are going to save a lot of time building notifications with Knock, this was a good call, and we will give it our best shot to get them set up as fast as possible.
     - **Grok Bot.** You are a marketing engineer teammate. Say you will use Knock to help with engagement, notifications, and the messy middle between them; you will connect their account, then pick the highest-leverage place to start. Treat Grok Bot, a named teammate, **Agent Computer**, or a `/workspace` cloud computer as this path.
   - **Default: always ask.** That same first message must then ask whether they have a Knock account. Do not add MCP, run OAuth, install skills, discover workflows, or call Knock tools until they answer.
   - **Skip only if** the user's message explicitly says they started from the Knock dashboard (e.g. pasted a dashboard setup prompt, or says "from the Knock dashboard"). MCP already configured, a prior chat, or guessing they might have an account does **not** count — still ask. Still include the opening encouragement in that first message.
   - If they say no: do **not** send them to the dashboard to sign up separately. Tell them in one line that they'll create their account during the sign-in step — signup, onboarding, and returning here all happen in that one browser flow — then continue to Connect Knock tooling.
   - End the ask as the last line, bolded, e.g. **Do you already have a Knock account?**

2. **Connect Knock tooling for the current tool** (hard gate — do not discover, propose, or build workflows until a Knock MCP tool call, or `knock whoami` on the CLI path, has succeeded)
   - Route by tool family, then follow the **surface check at the top of that rule** (app vs CLI) — do not pick a path from this list alone:
     - **Cursor** (editor or Cursor CLI) → `rules/connect-cursor.md` — editor uses MCP; Cursor CLI is routed to `rules/connect-knock-cli.md`
     - **Claude** (app or Claude Code) → `rules/connect-claude.md` — app adds Knock from the connectors directory (give the user the directory link and wait); Claude Code is routed to `rules/connect-knock-cli.md`
     - **Codex** (IDE/app or Codex CLI) → `rules/connect-codex.md` — IDE/app uses MCP + new-task handoff; Codex CLI is routed to `rules/connect-knock-cli.md`
     - **Grok Bot** (desktop or iOS teammate) → `rules/connect-grok-bot.md` — Plugins connector + marketing-engineer surface-area ask. Not Cursor editor; not the Knock CLI path.
     - **Any other terminal/CLI agent** → `rules/connect-knock-cli.md` — install the Knock CLI and auth with `knock login`
   - If the tool is unknown, ask which one, then follow the matching rule.
   - On the Knock CLI path, do **not** set up MCP at any point in this skill — no `claude mcp add`, no `codex mcp add`, no `mcp.json` edits, no connector ask. Use `knock` CLI equivalents wherever later steps mention Knock MCP tools.
   - Auth proof: call `list_environments` or `execute_mapi_read` `GET /v1/whoami` (MCP), or run `knock whoami` (CLI), and wait for success. Checking that MCP or the CLI is installed is not enough.

3. **Discover workflows** (`rules/discover-workflows.md`) — only after step 2 auth proof
   - **Grok Bot:** do not start here. Follow the surface-area ask in `rules/connect-grok-bot.md`, then route from their answer.
   - If this conversation already has an approved build list from `knock-lifecycle-opportunities` or `knock-product-messaging-strategy`, skip rediscovery (see prior-confirmation gate in that rule).
   - Otherwise learn the product, propose high-value workflows, and confirm which to build.

4. **Build workflows** (`rules/build-workflows.md`)
   - Create confirmed workflows in the Knock development environment via MCP.

5. **Recommend an implementation approach** (`rules/recommend-implementation.md`)
   - **Grok Bot:** skip unless they attach a product repo or enable local-computer access.
   - Pick one trigger path, ask the user to confirm, then create branch `knock-implementation` before file changes.
   - For a Knock Data Source (CDP or custom HTTP), follow `rules/implement-data-source.md`.

6. **Wrap up** (`rules/wrap-up.md`)
   - **Grok Bot:** only after workflows were built. Skip for strategy or planning-only turns.
   - Always send a test. Follow the MCP path or Knock CLI path in `rules/wrap-up.md` (do not mix). Shared recipient rules: whoami email + name, or ask for signup email only if missing. Then next steps, dashboard link, and close with Knock agent help.
   - Always mention setting up in-app notifications via `knock-in-app-ui`. If guides were created or mentioned, note that guides need app wiring — then **ask** before starting `knock-in-app-ui` (do not proceed until the user says yes).

## Extension rules (not on the first pass)

Use these when preparing for production or when the user asks — they are optional after the main flow:

- **Import users** (`rules/import-users.md`) — choose a stable Knock user id, research how users are stored, set `KNOCK_API_KEY`, and write a dry-run-first bulk-identify script. Do not run against production unless the user explicitly asks.

## Rule files reference

- `rules/connect-cursor.md` — Cursor: surface check, then editor MCP + skills install (Cursor CLI routes to `connect-knock-cli.md`)
- `rules/connect-claude.md` — Claude: surface check, then app directory connector (Claude Code routes to `connect-knock-cli.md`)
- `rules/connect-codex.md` — Codex: surface check, then IDE/app MCP + new-task handoff (Codex CLI routes to `connect-knock-cli.md`)
- `rules/connect-grok-bot.md` — Grok Bot: Plugins connector, then marketing-engineer surface-area ask
- `rules/connect-knock-cli.md` — shared Knock CLI path: install + `knock login` auth for CLI-based tools
- `rules/discover-workflows.md` — Product discovery and workflow proposals
- `rules/build-workflows.md` — Build confirmed workflows with Knock MCP
- `rules/recommend-implementation.md` — Choose a trigger path, confirm, branch, then implement
- `rules/implement-data-source.md` — Source setup: identify user, mappings, MCP prompts, testing
- `rules/wrap-up.md` — Test send (separate MCP vs Knock CLI paths) + next steps, dashboard link, and Knock agent help
- `rules/import-users.md` — Extension: bulk-identify users for production readiness

## Quick reference

- MCP server URL: `https://mcp.knock.app/mcp`
- Knock CLI: install with `npm install -g @knocklabs/cli`, auth with `knock login` ([docs](https://docs.knock.app/cli/overview))
- Install open-source skills: `npx skills add knocklabs/skills`
- Prefer Knock MCP tools (or Knock CLI commands on the CLI path) for workflow, step, and template creation after tooling is connected
