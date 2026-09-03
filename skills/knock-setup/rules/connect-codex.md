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

If Knock plugin tools are already available, skip to the auth checkpoint for this surface.

1. Search the plugin directory for the provider name **Knock**.
2. If that returns no exact match, search once more using the exact plugin ID `plugin_asdk_app_6a8dddd50424819196928510eff4c70f`.
3. If either search returns the exact Knock plugin, surface its inline connection control and wait. Do not substitute a fuzzy or similarly named result.
4. If both searches fail, explain that the recently published listing may not yet be available through directory search, then provide this verified fallback listing:
   `https://chatgpt.com/plugins/plugin_asdk_app_6a8dddd50424819196928510eff4c70f`
   Ask the user to open it, connect Knock, and return to the conversation. This direct-listing fallback is permitted only after both directory searches fail.

The direct listing is only a fallback for opening and connecting the plugin; it does not itself prove that authentication succeeded.

## Tool loading and authentication checkpoint

A plugin connection and successful authentication are separate states:

- **Connected.** The user completed the plugin's sign-in or connection flow.
- **Authenticated.** A Knock tool call succeeds in the current conversation.

Never describe Knock as authenticated based only on the connection UI or OAuth redirect.

### ChatGPT

After the user connects Knock, attempt the auth checkpoint in the current conversation:

1. Call `list_environments`, or call `execute_mapi_read` with `GET /v1/whoami`.
2. If the call succeeds, say setup is done in one short line and continue to `discover-workflows`.
3. If Knock tools remain unavailable, explain that the conversation has not loaded the newly connected tools and provide the continuation prompt below. End with **Open a new chat, paste the prompt above, and continue there.** Do not repeatedly search the directory.

### Codex IDE / app

Codex loads plugin tools when a task starts. Connecting a plugin during an active task may not add its tools to that task.

- If Knock tools were already available when the task started, perform the auth checkpoint normally.
- If Knock was connected during the current task and its tools are unavailable, do not attempt an inline refresh, repeat directory searches, add a custom MCP server, or claim authentication succeeded. Immediately provide the following continuation prompt, then stop.

```text
Continue Knock setup with the knock-setup skill.

Knock was connected in the previous task, but authentication has not yet been verified in this task. Do not repeat plugin discovery or ask about a Knock account.

First action: call list_environments. If unavailable, call execute_mapi_read with GET /v1/whoami.

After a successful Knock tool call:
Resume from: discover-workflows
Confirmed to build: none confirmed yet
Skipped: none
Deferred: none
Next action: propose workflows
```

End with this as the last line, bolded:

**Open a new Codex task, paste the prompt above, and continue there.**

### New-task verification

In the new task:

1. Call a Knock tool before doing anything else.
2. If the call succeeds, authentication is verified; continue to `discover-workflows`.
3. If the tool is available but requests authorization, surface the authorization control and wait.
4. If no Knock tools are available, search the plugin directory once by provider name **Knock**, then once by exact plugin ID `plugin_asdk_app_6a8dddd50424819196928510eff4c70f`.
5. If both searches fail, provide the verified listing and stop.

For users without an account, the plugin's sign-in doubles as signup: they'll create their account, complete onboarding, and be redirected back automatically. If the redirect doesn't complete (e.g. they land on the dashboard instead), have them finish signup there, then continue from the auth checkpoint for this surface. Do not repeat directory searches in the same Codex task after they return.

**Hard gate:** do not discover, build, implement, or wrap up until a Knock tool call succeeds in the current conversation.
