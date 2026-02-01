---
title: CLI installation and authentication
description: How to install the Knock CLI and authenticate using service tokens or dashboard accounts
tags:
  - knock
  - cli
  - installation
  - authentication
  - service-token
  - setup
category: knock-cli
last_updated: 2026-02-01
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

## Authentication

The Knock CLI supports two authentication methods: service tokens (recommended for CI/CD and automation) and interactive dashboard login (for local development).

### Method 1: Service token authentication (recommended)

Service tokens are the preferred method for automated workflows and CI/CD pipelines.

**Setting up a service token:**

1. Generate a service token from the Knock dashboard under Developer settings
2. Set the environment variable:

```bash
export KNOCK_SERVICE_TOKEN=<your-service-token>
```

**Using in commands:**

```bash
# The CLI automatically uses KNOCK_SERVICE_TOKEN if set
knock pull --all

# Or pass explicitly
knock pull --all --service-token=<your-service-token>
```

**Best practices for service tokens:**

- Store tokens securely in environment variables or secrets management
- Use different tokens for different environments (development, staging, production)
- Rotate tokens periodically
- Never commit tokens to version control

### Method 2: Dashboard account authentication

For local development, you can authenticate using your Knock dashboard account.

**Interactive login:**

```bash
knock auth login
```

This opens a browser window for authentication. Once authenticated, credentials are stored locally.

**Check authentication status:**

```bash
knock auth whoami
```

**Logout:**

```bash
knock auth logout
```

## Environment configuration

### Working with multiple environments

Knock supports multiple environments (development, staging, production). Specify the environment when running commands:

```bash
# Pull from development environment
knock pull --all --environment=development

# Push to production
knock push --all --environment=production
```

### Environment variables

| Variable | Description |
|----------|-------------|
| `KNOCK_SERVICE_TOKEN` | Service token for authentication |
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
- Set the `KNOCK_SERVICE_TOKEN` environment variable
- Or run `knock auth login` for interactive authentication

**"Invalid service token"**
- Verify the token is correct and hasn't been revoked
- Check if the token has access to the target environment

**"Permission denied"**
- The authenticated user/token may lack permissions for the operation
- Verify role assignments in the Knock dashboard

### Verifying setup

Run this command to verify your setup is working:

```bash
knock whoami
```

This displays the authenticated account and available environments.
