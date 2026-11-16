---
title: CLI installation and authentication
description: How to install the Knock CLI and authenticate with a dashboard login
tags:
  - knock
  - cli
  - installation
  - authentication
  - setup
category: knock-cli
last_updated: 2026-11-16
---

# CLI installation and authentication

## Installation

### Prerequisites

The Knock CLI requires Node.js 18+ or can be installed via Homebrew on macOS.

### Installation methods

**Using npm (recommended):**

```bash
npm install -g @knocklabs/cli
```

**Using Homebrew (macOS):**

```bash
brew install knocklabs/tap/knock
```

**Verify installation:**

```bash
knock --version
```

### Expectation for agents

When working with a project that uses Knock, the CLI should already be installed. If the `knock` command is not available:

1. First attempt to install it using `npm install -g @knocklabs/cli`
2. If npm is not available, try Homebrew on macOS
3. If installation fails, inform the user that the Knock CLI needs to be installed

### Important: Interactive prompts and the `--force` flag

Many Knock CLI commands use interactive prompts (y/N confirmations, multi-step wizards, browser-based auth). These prompts will cause commands to hang or default to "no" if not handled.

**For agents and scripts:** Most commands that prompt support a `--force` flag that skips all confirmation prompts. Always use `--force` when running commands non-interactively:

```bash
knock workflow pull <workflow-key> --force
knock pull --force
knock commit -m "Update workflow" --resource-type=workflow --resource-id=<workflow-key> --force
```

Some commands like `knock init`, `knock login`, and `knock workflow new` are fully interactive and don't support `--force`. Where a command has explicit flags (e.g., `--key`, `--steps` on `knock workflow new`), use them to avoid prompts. `knock init` takes no such flags, so either have the user run it or write `knock.json` directly.

See the CLI commands reference (`rules/cli-commands-reference.md`) for a full table of which commands prompt, which support `--force`, and which are safe to run directly.

## Authentication

Authenticate with an interactive dashboard login. Do not read a token from the environment, a dotenv file, or the chat, and do not pass one on the command line. The CLI stores the session itself after login.

**Interactive login (requires browser — cannot be automated by agents):**

```bash
knock login
```

This opens a browser window for authentication. Once authenticated, the CLI stores the session locally. Because this requires browser interaction, it must be run manually by the user. Agents cannot complete this flow.

**Check authentication status:**

```bash
knock whoami
```

**Logout:**

```bash
knock logout
```

## Environment configuration

### Determine the account's environment model

List environments before choosing a target:

```bash
knock environment list
```

When `--environment` is omitted, Knock CLI v1.3.0 and later use the account's default environment. New accounts have one production environment until environments are enabled.

**Production-only account (one environment):**

```bash
# These target the default production environment and create drafts
knock pull
knock push

# A commit publishes the scoped draft live; run only when the user asks to publish
knock commit -m "Update workflow" \
  --resource-type=workflow --resource-id=<workflow-key> --force
```

Do not use branch or promotion commands on a production-only account. Leave pushed resources as drafts when the user has not approved publication.

**Environments enabled (multiple environments):**

```bash
knock pull --environment=<env-slug>
knock push --environment=<env-slug>
knock commit -m "Update workflow" \
  --resource-type=workflow --resource-id=<workflow-key> \
  --environment=<env-slug> --force
```

Branch commands operate in development. Promotion moves committed changes through the configured environment sequence; scope a single-resource promotion with `knock commit promote --only=<commit-id> --force`.

`push`, `commit`, and `validate` accept any available environment. Avoid `push --commit` in agent workflows because a commit may publish live when the target is production; push first, then use an explicitly scoped commit after user approval.

### Environment variables

| Variable | Description |
|----------|-------------|
| `KNOCK_API_ORIGIN` | Custom API origin (rarely needed) |

## Project initialization

After authentication, initialize your project:

```bash
knock init
```

This creates a `knock.json` configuration file in your project root. See the directory structure documentation for details on this file.

## Troubleshooting

### Common issues

**"Command not found: knock"**
- The CLI is not installed or not in PATH
- Try reinstalling: `npm install -g @knocklabs/cli`

**"Authentication required"**
- Run `knock login` and wait for the user to finish the browser flow

**Authentication failed**
- Run `knock logout`, then `knock login` again
- Confirm the dashboard account can access the target environment

**"Permission denied"**
- The authenticated user/token may lack permissions for the operation
- Verify role assignments in the Knock dashboard

### Verifying setup

Run this command to verify your setup is working:

```bash
knock whoami
```

This displays the authenticated account and user or token. Run `knock environment list` separately to list available environments.
