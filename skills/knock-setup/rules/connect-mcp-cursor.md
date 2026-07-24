---
title: Connect MCP in Cursor
description: Add the Knock MCP server and skills in Cursor
tags:
  - setup
  - mcp
  - cursor
category: knock-setup
last_updated: 2026-07-24
---

# Connect MCP in Cursor

Prerequisite: step 1 (Confirm Knock account) must already be asked and answered in this conversation. If it hasn't been, stop and ask before continuing — do not add the MCP server or start OAuth.

1. Add MCP: add a `knock` server with URL https://mcp.knock.app/mcp (HTTP transport) to `~/.cursor/mcp.json`. Merge the entry into the existing `mcpServers` object — do not replace the file or remove other servers. Cursor picks up the change without a restart.
2. Trigger OAuth sign-in once (the first Knock tool use starts it). If no browser window opens within about 10 seconds, do not retry in a loop — direct the user to Cursor Settings → Tools + MCP → knock → "Needs authentication", or have them open the authorization URL from the Output panel (MCP: knock) manually.
3. Run: `npx skills add knocklabs/skills`
4. Confirm Knock tools are available. If they don't appear, first check that the `knock` entry still exists in `~/.cursor/mcp.json` before re-adding the server or debugging further.

For users without an account, OAuth sign-in doubles as signup: they'll create their account, complete onboarding, and be redirected back to the IDE automatically. If the redirect doesn't complete (e.g. they land on the dashboard instead), have them finish signup there, then retry the Knock tool call to re-trigger OAuth. Do not continue until Knock tools are authenticated.

Verify the Knock tools work, but do not summarize or list the installed tools/skills — say setup is done and move on.
