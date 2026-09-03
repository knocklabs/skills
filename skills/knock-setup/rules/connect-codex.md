---
title: Connect Knock in ChatGPT and Codex
description: Route ChatGPT and Codex sessions — the app uses the Knock plugin, Codex CLI uses the Knock CLI
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
- **ChatGPT or Codex IDE / app** — you are the agent inside ChatGPT or the Codex IDE extension / desktop / app UI. → Continue with the plugin path below.
- If you cannot tell, ask the user in one line: are they in ChatGPT, the Codex IDE/app, or the Codex CLI (`codex`)?

## Plugin path (ChatGPT / Codex IDE / app)

ChatGPT and Codex connect to Knock through the **Knock plugin**. You cannot connect it for them. Output the three lines in step 2 and wait. Do not send them to settings or a custom MCP URL. Do not paste `https://mcp.knock.app/mcp`. Do not run `codex mcp add`.

Prerequisite: step 1 (Confirm Knock account) must already be asked and answered in this conversation. If it hasn't been, stop and ask before continuing — do not give plugin instructions or start OAuth.

If Knock plugin tools are already available, skip to the auth checkpoint (step 3).

1. If you have shell access in this session, run `npx skills add knocklabs/skills`. If not, skip this step.
2. Give the user the plugin instructions (this message is an allowed exception to the one-line rule). Output only this, nothing else:

   ```
   1. Add the Knock plugin here: https://chatgpt.com/plugins/plugin_asdk_app_6a8dddd50424819196928510eff4c70f
   2. Click Try in chat and follow the instructions
   3. Return here after complete
   ```
3. **Auth checkpoint (required — do not skip).** Once the user has returned, call a Knock tool once — prefer `list_environments`, or `execute_mapi_read` with `GET /v1/whoami` — and wait for success.
   - If Knock tools are unavailable or the call fails, ask the user (one short line) to open the link again, click Try in chat, then return here, then retry the same tool call. Do not loop more than twice — stop and report what failed. Do not fall back to `codex mcp add` or a custom MCP URL.
4. Only after step 3 succeeds: say setup is done (one short line) and continue to `discover-workflows`. Do not summarize or list installed tools/skills.

For users without an account, the plugin's sign-in doubles as signup: they'll create their account, complete onboarding, and be redirected back automatically. If the redirect doesn't complete (e.g. they land on the dashboard instead), have them finish signup there, then open the link again, click Try in chat, return here, and retry the Knock tool call.

**Hard gate:** steps after Connect Knock tooling (discover, build, implement, wrap-up) are blocked until a Knock tool call has succeeded in this conversation.
