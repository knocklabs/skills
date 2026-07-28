---
title: Connect MCP in Claude Code
description: Add the Knock MCP server and skills in Claude Code
tags:
  - setup
  - mcp
  - claude-code
category: knock-setup
last_updated: 2026-07-27
---

# Connect MCP in Claude Code

Prerequisite: step 1 (Confirm Knock account) must already be asked and answered in this conversation. If it hasn't been, stop and ask before continuing — do not add the MCP server or start OAuth.

1. Add MCP: run `claude mcp add --scope user --transport http knock https://mcp.knock.app/mcp`. Use `--scope user` so Knock is available in every project (the CLI default `local` only applies to the current project). If `knock` already exists, leave it (do not remove other servers).
2. Verify config: run `claude mcp list` and confirm `knock` is listed. If it is missing, re-run the add command once, then list again. If it still missing, stop and tell the user the add failed (include the CLI error).
3. Run: `npx skills add knocklabs/skills`
4. **Auth checkpoint (required — do not skip).** Try calling a Knock MCP tool once — prefer `list_environments`, or `execute_mapi` with `GET /v1/whoami`.
   - If the call **succeeds**, say setup is done (one short line) and continue to `discover-workflows`. Do not summarize or list installed tools/skills.
   - If Knock tools are **not available in this session** (tool missing, deferred, "No MCP servers configured", "MCP server \"knock\" not found", reconnection failed, Needs authentication with no usable tool, or any other failure to call a Knock tool): do **not** ask the user to run `/mcp` in this chat. Immediately follow **Claude MCP reload** below. Do **not** discover, propose, or build workflows in this conversation.

`/mcp` is a Claude Code slash command the **user** types in the interactive prompt of a session that already has Knock loaded. Never execute `/mcp`, `/mcp reconnect`, or `/mcp reconnect knock` through Bash or any shell tool — those always fail with `no such file or directory: /mcp`. Do not tell the user to run `/mcp` in the **current** session after a mid-session `claude mcp add` — that session usually still shows "No MCP servers configured". Auth via `/mcp` happens in the **fresh** session after handoff.

For users without an account, OAuth sign-in doubles as signup: they'll create their account, complete onboarding, and be redirected back automatically. If the redirect doesn't complete (e.g. they land on the dashboard instead), have them finish signup there, then retry the Knock tool call (or `/mcp` in the fresh session) to re-trigger OAuth.

**Hard gate:** steps after Connect MCP (discover, build, implement, wrap-up) are blocked until a Knock MCP tool call has succeeded in this conversation (or in the new session after handoff).

## Claude MCP reload

Required whenever Knock tools are not callable in this session after add/list — including right after a successful `claude mcp add`. Claude Code loads MCP servers at session start; mid-session adds and OAuth often do not attach tools here. `/mcp` in this session is the wrong fix.

1. Stop the main skill flow here. Do not ask the user to authenticate in this chat.
2. Explain in one short line: Knock is configured on disk, but this session cannot use it — continue in a fresh session.
3. Output a **copyable continuation prompt** in a fenced code block. Fill in the placeholders from this conversation — omit lines that do not apply.

Use this template (keep the fence; substitute real values):

```text
Continue Knock setup with the knock-setup skill. Knock MCP was added with user scope — do not re-run account ask. First call list_environments (or execute_mapi GET /v1/whoami). If auth is needed, type /mcp in this fresh session's prompt (not Bash) and authenticate Knock, then retry the tool. Do not rediscover until auth proof succeeds.

Resume from: [discover-workflows | build-workflows | recommend-implementation | wrap-up]

Confirmed to build: [workflow names, or "none confirmed yet — run discover-workflows"]
Skipped: [names or none]
Deferred: [names or none]
If present, read detail from knock-plan.md and treat confirmed as authoritative (skip rediscovery).

Next action: [e.g. prove auth then propose workflows / build only “New market brief” / continue implementation]
```

4. End with this as the last line, bolded:

**Start a fresh Claude Code session, paste the prompt above, and continue there.**

Do not continue to discover/build in this chat after emitting the handoff.
