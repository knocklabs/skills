---
name: knock-setup
description: Connect Knock to your coding agent, discover and build notification workflows, and recommend how to trigger them from your application.
---

# Setup

End-to-end Knock setup for a coding agent: connect tooling, design and build notification workflows, then wire them into the application. Work through the rules below in order.

While working, keep every response to one short line — no summaries, no menus, no extra questions unless a step fails. The only exceptions are the workflow proposals, a prior-confirmation restatement (2–3 lines max), the implementation confirmation ask, the import-users id ask, and the final wrap-up output, which have their own formats. When you end with a confirmation question (workflows, implementation, import-users id, or wrap-up guides ask), that question must be the very last line of the message, on its own, and bolded.

Assume the user already has a Knock account when this skill is invoked from the Knock dashboard. Otherwise, ask once whether they have an account; if not, point them to https://dashboard.knock.app/ to sign up, then continue.

## How to use this skill

1. **Connect MCP for the current tool**
   - Cursor → `rules/connect-mcp-cursor.md`
   - Codex → `rules/connect-mcp-codex.md`
   - Claude Code → `rules/connect-mcp-claude-code.md`
   - If the tool is unknown, ask which one, then follow the matching rule.

2. **Discover workflows** (`rules/discover-workflows.md`)
   - If this conversation already has an approved build list from `knock-lifecycle-opportunities` or `knock-product-messaging-strategy`, skip rediscovery (see prior-confirmation gate in that rule).
   - Otherwise learn the product, propose high-value workflows, and confirm which to build.

3. **Build workflows** (`rules/build-workflows.md`)
   - Create confirmed workflows in the Knock development environment via MCP.

4. **Recommend an implementation approach** (`rules/recommend-implementation.md`)
   - Pick one trigger path, ask the user to confirm, then create branch `knock-implementation` before file changes.
   - For a Knock Data Source (CDP or custom HTTP), follow `rules/implement-data-source.md`.

5. **Wrap up** (`rules/wrap-up.md`)
   - Test one workflow via Knock MCP (not sandbox mode; recipient is current user), then next steps, dashboard link, and close with Knock agent help.
   - Always mention setting up in-app notifications via `knock-in-app-ui`. If guides were created or mentioned, note that guides need app wiring — then **ask** before starting `knock-in-app-ui` (do not proceed until the user says yes).

## Extension rules (not on the first pass)

Use these when preparing for production or when the user asks — they are optional after the main flow:

- **Import users** (`rules/import-users.md`) — choose a stable Knock user id, research how users are stored, set `KNOCK_API_KEY`, and write a dry-run-first bulk-identify script. Do not run against production unless the user explicitly asks.

## Rule files reference

- `rules/connect-mcp-cursor.md` — Cursor MCP + skills install
- `rules/connect-mcp-codex.md` — Codex MCP + skills install
- `rules/connect-mcp-claude-code.md` — Claude Code MCP + skills install
- `rules/discover-workflows.md` — Product discovery and workflow proposals
- `rules/build-workflows.md` — Build confirmed workflows with Knock MCP
- `rules/recommend-implementation.md` — Choose a trigger path, confirm, branch, then implement
- `rules/implement-data-source.md` — Source setup: identify user, mappings, MCP prompts, testing
- `rules/wrap-up.md` — MCP workflow test, next steps, dashboard link, and Knock agent help
- `rules/import-users.md` — Extension: bulk-identify users for production readiness

## Quick reference

- MCP server URL: `https://mcp.knock.app/mcp`
- Install open-source skills: `npx skills add knocklabs/skills`
- Prefer Knock MCP tools for workflow, step, and template creation after tooling is connected
