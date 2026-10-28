---
title: Build workflows
description: Create confirmed workflows in Knock using MCP tools
tags:
  - setup
  - workflows
  - mcp
category: knock-setup
last_updated: 2026-10-28
---

# Build workflows

1. Build each confirmed **workflow** as a draft in the account's default environment using the Knock MCP tools (workflow, steps, and message templates). On new production-only accounts, the default environment is production. On the Knock CLI path, use `knock` CLI commands instead (see the `knock-cli` skill) — do not set up MCP to build.
2. If a confirmed item is a **guide** (or knock shape `guide` / `both`), create the guide resource when MCP/CLI allows, but do **not** treat app UI as done and do **not** start `knock-in-app-ui` here — wrap-up will ask the user before that next step.
3. Leave every created resource as a draft. Do not commit, publish, activate, promote, or create a branch; publishing is the user's decision.
4. After building, list each created workflow/guide in one line with a link to it in the Knock dashboard.
