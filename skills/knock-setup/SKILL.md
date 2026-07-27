---
name: knock-setup
description: Connect Knock to your coding agent, discover and build notification workflows, and recommend how to trigger them from your application.
---

# Setup

End-to-end Knock setup for a coding agent: connect tooling, design and build notification workflows, then wire them into the application. Work through the rules below in order.

While working, keep every response to one short line — no summaries, no menus, no extra questions unless a step fails. The only exceptions are the account ask (step 1), the workflow proposals, a prior-confirmation restatement (2–3 lines max), the implementation confirmation ask, the import-users id ask, the wrap-up test-send asks, and the final wrap-up output, which have their own formats. When you end with a confirmation question (account, workflows, implementation, import-users id, wrap-up test send, or wrap-up guides ask), that question must be the very last line of the message, on its own, and bolded.

## How to use this skill

1. **Confirm Knock account** (required first action — do this before anything else)
   - **Default: always ask.** Your first message in this skill must ask whether they have a Knock account. Do not add MCP, run OAuth, install skills, discover workflows, or call Knock tools until they answer.
   - **Skip only if** the user's message explicitly says they started from the Knock dashboard (e.g. pasted a dashboard setup prompt, or says "from the Knock dashboard"). MCP already configured, a prior chat, or guessing they might have an account does **not** count — still ask.
   - If they say no: do **not** send them to the dashboard to sign up separately. Tell them in one line that they'll create their account during the sign-in step — signup, onboarding, and returning here all happen in that one browser flow — then continue to Connect MCP.
   - End the ask as the last line, bolded, e.g. **Do you already have a Knock account?**

2. **Connect MCP for the current tool**
   - Cursor → `rules/connect-mcp-cursor.md`
   - Codex → `rules/connect-mcp-codex.md`
   - Claude Code → `rules/connect-mcp-claude-code.md`
   - If the tool is unknown, ask which one, then follow the matching rule.

3. **Discover workflows** (`rules/discover-workflows.md`)
   - If this conversation already has an approved build list from `knock-lifecycle-opportunities` or `knock-product-messaging-strategy`, skip rediscovery (see prior-confirmation gate in that rule).
   - Otherwise learn the product, propose high-value workflows, and confirm which to build.

4. **Build workflows** (`rules/build-workflows.md`)
   - Create confirmed workflows in the Knock development environment via MCP.

5. **Recommend an implementation approach** (`rules/recommend-implementation.md`)
   - Pick one trigger path, ask the user to confirm, then create branch `knock-implementation` before file changes.
   - For a Knock Data Source (CDP or custom HTTP), follow `rules/implement-data-source.md`.

6. **Wrap up** (`rules/wrap-up.md`)
   - Ask if they want a test send; if yes, resolve email via `GET /v1/whoami` (`user_email`), falling back to asking for their signup email only if `user_email` is null, then trigger one workflow via Knock MCP with inline identify (not sandbox mode). Then next steps, dashboard link, and close with Knock agent help.
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
- `rules/wrap-up.md` — Optional test send (whoami email + inline identify), next steps, dashboard link, and Knock agent help
- `rules/import-users.md` — Extension: bulk-identify users for production readiness

## Quick reference

- MCP server URL: `https://mcp.knock.app/mcp`
- Install open-source skills: `npx skills add knocklabs/skills`
- Prefer Knock MCP tools for workflow, step, and template creation after tooling is connected
