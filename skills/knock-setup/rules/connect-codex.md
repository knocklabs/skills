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

Do **not** ask whether they have a Knock account. Plugin sign-in covers signup. Do not send them to settings or a custom MCP URL. Do not paste `https://mcp.knock.app/mcp`. Do not run `codex mcp add`. Do not paste an unverified plugin URL. The verified Knock listing URL may be provided only after searches by both provider name and exact plugin ID fail.

**ChatGPT only:** do not install skills. Do not run `npx skills add` or any other skill installer. The plugin already includes them.

**Codex IDE / app only:** if you have shell access, run `npx skills add knocklabs/skills`. If not, skip this.

If Knock plugin tools are already available, skip to the auth checkpoint.

1. Search the plugin directory for the provider name **Knock**.
2. If that returns no exact match, search once more using the exact plugin ID `plugin_asdk_app_6a8dddd50424819196928510eff4c70f`.
3. If either search returns the exact Knock plugin, surface its inline connection control and wait. Do not substitute a fuzzy or similarly named result.
4. If both searches fail, explain that the recently published listing may not yet be available through directory search, then provide this verified fallback listing:
   `https://chatgpt.com/plugins/plugin_asdk_app_6a8dddd50424819196928510eff4c70f`
   Ask the user to open it, connect Knock, and return to the conversation. This direct-listing fallback is permitted only after both directory searches fail.
5. Once the user returns, perform the required auth checkpoint by calling a Knock tool — prefer `list_environments`, or `execute_mapi_read` with `GET /v1/whoami`.
6. If the authentication call fails because Knock tools are still unavailable, repeat the two directory searches once. If they still fail, provide the verified listing again and stop. Do not use a custom MCP URL, run `codex mcp add`, or exceed two discovery cycles.

The direct listing is only a fallback for opening and connecting the plugin; it does not itself prove that authentication succeeded. Do not continue to discovery, building, or implementation until a Knock tool call succeeds in the current conversation.

Only after the auth checkpoint succeeds: say setup is done (one short line) and continue to `discover-workflows`. Do not summarize or list installed tools/skills.

For users without an account, the plugin's sign-in doubles as signup: they'll create their account, complete onboarding, and be redirected back automatically. If the redirect doesn't complete (e.g. they land on the dashboard instead), have them finish signup there, then repeat the directory searches (and the listing fallback only if both fail), and retry the Knock tool call.

**Hard gate:** steps after Connect Knock tooling (discover, build, implement, wrap-up) are blocked until a Knock tool call has succeeded in this conversation.
