---
title: Connect MCP in Claude Code
description: Add the Knock MCP server and skills in Claude Code
tags:
  - setup
  - mcp
  - claude-code
category: knock-setup
last_updated: 2026-07-24
---

# Connect MCP in Claude Code

Prerequisite: step 1 (Confirm Knock account) must already be asked and answered in this conversation. If it hasn't been, stop and ask before continuing — do not add the MCP server or start OAuth.

1. Run: `claude mcp add --transport http knock https://mcp.knock.app/mcp`
2. Run `/mcp` and authenticate with Knock OAuth.
3. Run: `npx skills add knocklabs/skills`
4. Confirm Knock tools are available.

For users without an account, OAuth sign-in doubles as signup: they'll create their account, complete onboarding, and be redirected back automatically. If the redirect doesn't complete (e.g. they land on the dashboard instead), have them finish signup there, then retry `/mcp` authentication. Do not continue until Knock tools are authenticated.

Verify the Knock tools work, but do not summarize or list the installed tools/skills — say setup is done and move on.
