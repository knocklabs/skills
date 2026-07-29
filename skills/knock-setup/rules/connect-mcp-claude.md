---
title: Connect MCP in Claude
description: Add the Knock MCP server to Claude as a custom connector
tags:
  - setup
  - mcp
  - claude
category: knock-setup
last_updated: 2026-07-29
---

# Connect MCP in Claude

Use this rule for the Claude app (web or desktop). Claude connects to remote MCP servers through **connectors**, which the user adds in Claude settings — you cannot add one for them, so give the instructions below and wait. If the user is in the Claude Code terminal instead, that is a CLI-based tool — use `rules/connect-cli.md`.

Prerequisite: step 1 (Confirm Knock account) must already be asked and answered in this conversation. If it hasn't been, stop and ask before continuing — do not give connector instructions or start OAuth.

1. If you have shell access in this session, run `npx skills add knocklabs/skills`. If not, skip this step.
2. Give the user the connector instructions (this message is an allowed exception to the one-line rule — keep it to these steps):
   - Go to **Settings → Connectors** (browser: profile icon → Settings; desktop: app menu → Settings).
   - Click **Add custom connector**.
   - Name it `Knock` and set the URL to `https://mcp.knock.app/mcp`. Leave the advanced settings empty.
   - Click **Add**, then click **Connect** on the Knock connector and sign in with their Knock account.
   - On Team or Enterprise plans, an Owner may need to add the connector under **Admin settings → Connectors** first; members then connect it from **Settings → Connectors**.
   - End with this as the last line, bolded: **Tell me when the Knock connector is connected.**
3. **Auth checkpoint (required — do not skip).** Once the user says it's connected, call a Knock MCP tool once — prefer `list_environments`, or `execute_mapi` with `GET /v1/whoami` — and wait for success.
   - If Knock tools are unavailable or the call fails, ask the user (one short line) to confirm the connector shows as connected in **Settings → Connectors** and is enabled for this chat, then retry the same tool call. Do not loop more than twice — stop and report what failed.
4. Only after step 3 succeeds: say setup is done (one short line) and continue to `discover-workflows`. Do not summarize or list installed tools/skills.

For users without an account, the connector's **Connect** sign-in doubles as signup: they'll create their account, complete onboarding, and be redirected back automatically. If the redirect doesn't complete (e.g. they land on the dashboard instead), have them finish signup there, then reconnect the connector and retry the Knock tool call.

**Hard gate:** steps after Connect Knock tooling (discover, build, implement, wrap-up) are blocked until a Knock MCP tool call has succeeded in this conversation.
