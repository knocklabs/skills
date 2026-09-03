---
title: Connect Knock in ChatGPT and Codex
description: Route ChatGPT and Codex sessions — ChatGPT surfaces the Knock plugin inline, Codex CLI uses the Knock CLI
tags:
  - setup
  - plugin
  - cli
  - chatgpt
  - codex
category: knock-setup
last_updated: 2026-09-03
---

# Connect Knock in ChatGPT and Codex

Use this rule for ChatGPT or Codex. First determine which surface you are on — do not skip this check:

- **Codex CLI** — this session was launched by running `codex` in a terminal; there is no IDE UI. → Stop here and follow `rules/connect-knock-cli.md` (Knock CLI, not the plugin). Do not use the plugin path below and do not run `codex mcp add`.
- **ChatGPT** — the ChatGPT web or app chat (not Codex). → Continue with the plugin path below. Do not ask about a Knock account. Do not install skills.
- **Codex IDE / app** — you are the agent inside the Codex IDE extension or desktop/app UI. → Continue with the plugin path below. Do not ask about a Knock account.
- If you cannot tell, ask the user in one line: are they in ChatGPT, the Codex IDE/app, or the Codex CLI (`codex`)?

## Plugin path (ChatGPT / Codex IDE / app)

Do **not** ask whether they have a Knock account. Plugin sign-in covers signup. Do not send them to settings or a custom MCP URL. Do not paste `https://mcp.knock.app/mcp` or a plugin URL. Do not run `codex mcp add`. A plugin URL alone does not surface the connect control.

**ChatGPT only:** do not install skills. Do not run `npx skills add` or any other skill installer. The plugin already includes them.

**Codex IDE / app only:** if you have shell access, run `npx skills add knocklabs/skills`. If not, skip this.

If Knock plugin tools are already available, skip to the auth checkpoint.

1. Search the plugin directory for **Knock**. If there is a supported, unconnected plugin, surface the inline connection control for it. Name the provider Knock — do not search by a generic capability like "notifications". This message is an allowed exception to the one-line rule: search and surface the control, then wait. Do not output a URL or a numbered install list.
2. **Auth checkpoint (required — do not skip).** Once the user has connected, call a Knock tool once — prefer `list_environments`, or `execute_mapi_read` with `GET /v1/whoami` — and wait for success.
   - If Knock tools are unavailable or the call fails, search the plugin directory for Knock again and surface the inline connection control. Do not loop more than twice — stop and report what failed. Do not fall back to a plugin URL, `codex mcp add`, or a custom MCP URL.
3. Only after step 2 succeeds: say setup is done (one short line) and continue to `discover-workflows`. Do not summarize or list installed tools/skills.

For users without an account, the plugin's sign-in doubles as signup: they'll create their account, complete onboarding, and be redirected back automatically. If the redirect doesn't complete (e.g. they land on the dashboard instead), have them finish signup there, then search and surface the Knock plugin again, and retry the Knock tool call.

**Hard gate:** steps after Connect Knock tooling (discover, build, implement, wrap-up) are blocked until a Knock tool call has succeeded in this conversation.
