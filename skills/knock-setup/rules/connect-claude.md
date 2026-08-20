---
title: Connect Knock in Claude
description: Route Claude sessions — Cowork and Desktop connect via the in-chat community connector button, Claude Code uses the Knock CLI
tags:
  - setup
  - mcp
  - cli
  - claude
category: knock-setup
last_updated: 2026-08-20
---

# Connect Knock in Claude

Use this rule for anything Claude. First determine which surface you are on — do not skip this check:

- **Claude Code** — a terminal agent launched with the `claude` command. If you have a shell tool, run `echo $CLAUDECODE`; if it prints `1`, you are Claude Code. → Stop here and follow `rules/connect-knock-cli.md` (Knock CLI, not MCP). Do not use the connector steps below and do not run `claude mcp add`.
- **Claude Cowork, Claude Desktop, or claude.ai** — you either have no shell tool at all, or the env check above does not print `1`. → Continue with the connector path below.
- If you still cannot tell, ask the user in one line: are they in Claude Cowork / Desktop / claude.ai, or in Claude Code in a terminal?

## Connector path (Claude Cowork, Desktop, and claude.ai)

Claude connects to Knock through the **community connector**. You cannot click Connect for them. Use the connector with the directory link so a **Connect** button appears in this chat. Do not send them to settings or a custom connector URL. Do not paste `https://mcp.knock.app/mcp`.

Prerequisite: step 1 (Confirm Knock account) must already be asked and answered in this conversation. If it hasn't been, stop and ask before continuing — do not give the connector prompt or start OAuth.

1. If you have shell access in this session, run `npx skills add knocklabs/skills`. If not, skip this step.
2. Give the user the connector prompt (this message is an allowed exception to the one-line rule — keep it to these steps):
   - Use the Knock community connector: https://claude.ai/directory/knock
   - A **Connect** button should appear. They click it, sign in with their Knock account, and the flow continues here after.
   - End with this as the last line, bolded: **Click Connect to continue.**
3. **Auth checkpoint (required — do not skip).** Once the user has clicked Connect and returned, call a Knock MCP tool once — prefer `list_environments`, or `execute_mapi_read` with `GET /v1/whoami` — and wait for success.
   - If Knock tools are unavailable or the call fails, ask the user (one short line) to click **Connect** again if the button is still showing, then retry the same tool call. Do not loop more than twice — stop and report what failed.
4. Only after step 3 succeeds: say setup is done (one short line) and continue to `discover-workflows`. Do not summarize or list installed tools/skills.

For users without an account, the connector's **Connect** sign-in doubles as signup: they'll create their account, complete onboarding, and be redirected back automatically. If the redirect doesn't complete (e.g. they land on the dashboard instead), have them finish signup there, then click **Connect** again and retry the Knock tool call.

**Hard gate:** steps after Connect Knock tooling (discover, build, implement, wrap-up) are blocked until a Knock MCP tool call has succeeded in this conversation.
