---
title: Connect Knock in Codex
description: Route Codex sessions — IDE/app uses the Knock MCP server, Codex CLI uses the Knock CLI
tags:
  - setup
  - mcp
  - cli
  - codex
category: knock-setup
last_updated: 2026-07-30
---

# Connect Knock in Codex

Use this rule for anything Codex. First determine which surface you are on — do not skip this check:

- **Codex CLI** — this session was launched by running `codex` in a terminal; there is no IDE UI. → Stop here and follow `rules/connect-knock-cli.md` (Knock CLI, not MCP). Do not use the MCP path below and do not run `codex mcp add`.
- **Codex IDE / app** — you are the agent inside the Codex IDE extension or desktop/app UI. → Continue with the MCP path below.
- If you cannot tell, ask the user in one line: are they in the Codex IDE/app or the Codex CLI (`codex`)?

## MCP path (Codex IDE / app)

Prerequisite: step 1 (Confirm Knock account) must already be asked and answered in this conversation. If it hasn't been, stop and ask before continuing — do not add the MCP server or start OAuth.

1. Add MCP: run `codex mcp add knock --url https://mcp.knock.app/mcp`. If `knock` already exists, leave it (do not remove other servers).
2. Run: `npx skills add knocklabs/skills`
3. **Auth checkpoint (required — do not skip).** Call a Knock MCP tool once to trigger OAuth — prefer `list_environments`, or `execute_mapi` with `GET /v1/whoami`. If no browser opens within about 10 seconds, run `codex mcp login knock`, or have the user open the authorization URL Codex printed. Codex may show a local "Authentication complete. You may close this window." page — that is expected; close it and return here.
4. Do **not** discover, propose, or build workflows in this task. Auth that completes mid-task does not attach Knock tools here — continue with the handoff below (do not re-add the server in a loop).

For users without an account, OAuth sign-in doubles as signup: they'll create their account, complete onboarding, and be redirected back automatically. If the redirect doesn't complete (e.g. they land on the dashboard instead), have them finish signup there, then retry the Knock tool call (or `codex mcp login knock`) to re-trigger OAuth.

## Codex tool reload (required)

Codex loads MCP tools when a task starts. Auth that completes mid-task does **not** attach Knock tools to this chat — you must hand off to a new task. Do not keep calling Knock tools here, and do not pretend setup can continue in this conversation.

After auth succeeds (or as soon as you see that Knock tools are missing in this task):

1. Stop the main skill flow here.
2. Explain in one short line: Codex only picks up newly authenticated MCP tools in a **new** task.
3. Output a **copyable continuation prompt** in a fenced code block so the user can paste it into a new Codex chat. Fill in the placeholders from this conversation — omit lines that do not apply.

Use this template (keep the fence; substitute real values):

```text
Continue Knock setup with the knock-setup skill. Knock MCP is already connected and authenticated — do not re-run account ask or MCP OAuth.

Resume from: [discover-workflows | build-workflows | recommend-implementation | wrap-up]

Confirmed to build: [workflow names, or "none confirmed yet — run discover-workflows"]
Skipped: [names or none]
Deferred: [names or none]
If present, read detail from knock-plan.md and treat confirmed as authoritative (skip rediscovery).

Next action: [e.g. propose workflows / build only “New market brief” / continue implementation]
```

4. End with this as the last line, bolded:

**Open a new Codex task, paste the prompt above, and continue there.**

Do not summarize installed tools/skills. Do not continue to discover/build in this chat after emitting the handoff.
