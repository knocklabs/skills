---
title: Connect MCP in Codex
description: Add the Knock MCP server and skills in Codex
tags:
  - setup
  - mcp
  - codex
category: knock-setup
last_updated: 2026-07-24
---

# Connect MCP in Codex

Prerequisite: step 1 (Confirm Knock account) must already be asked and answered in this conversation. If it hasn't been, stop and ask before continuing — do not connect MCP or run `knock login`.

1. If needed: `npm install -g @knocklabs/cli` — then `knock login`
2. Connect Knock MCP at https://mcp.knock.app/mcp
3. Run: `npx skills add knocklabs/skills`
4. Confirm Knock tools are available.

For users without an account, the browser sign-in doubles as signup: they'll create their account, complete onboarding, and be redirected back automatically. If the redirect doesn't complete (e.g. they land on the dashboard instead), have them finish signup there, then retry authentication. Do not continue until Knock tools are authenticated.

Verify the Knock tools work, but do not summarize or list the installed tools/skills — say setup is done and move on.
