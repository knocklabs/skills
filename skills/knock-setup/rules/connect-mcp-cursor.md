---
title: Connect MCP in Cursor
description: Add the Knock MCP server and skills in Cursor
tags:
  - setup
  - mcp
  - cursor
category: knock-setup
last_updated: 2026-07-09
---

# Connect MCP in Cursor

1. Add MCP: Cursor Settings → MCP → add server "knock" with URL https://mcp.knock.app/mcp (HTTP transport).
2. Restart Cursor. On first Knock tool use, complete OAuth sign-in.
3. Run: `npx skills add knocklabs/skills`
4. Confirm Knock tools are available.

Verify the Knock tools work, but do not summarize or list the installed tools/skills — say setup is done and move on.
