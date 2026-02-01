---
title: CLI commands reference
description: Reference for Knock CLI commands including pull, push, and resource management
tags:
  - knock
  - cli
  - commands
  - pull
  - push
  - workflow
  - resources
category: knock-cli
last_updated: 2026-02-01
---

# CLI commands reference

## Core concepts

### Resource types

The Knock CLI manages several resource types:

| Resource | Description | Command prefix |
|----------|-------------|----------------|
| `workflow` | Notification workflows | `knock workflow` |
| `email-layout` | Email layout templates | `knock email-layout` |
| `translation` | Localization files | `knock translation` |
| `partial` | Reusable template partials | `knock partial` |
| `commit` | Version control for changes | `knock commit` |

### Global options

These options work with most commands:

| Option | Description |
|--------|-------------|
| `--environment`, `-e` | Target environment (development, staging, production) |
| `--service-token` | Service token for authentication |
| `--knock-dir` | Override the knock directory location |
| `--help` | Show help for the command |

## Pulling resources

### Pull all resources

Sync all resources from Knock to your local project:

```bash
knock pull --all
```

This pulls all resource types into the configured `knockDir`.

### Pull specific resource types

Pull only specific resource types:

```bash
# Pull only workflows
knock workflow pull --all

# Pull only email layouts
knock email-layout pull --all

# Pull only translations
knock translation pull --all
```

### Pull a specific resource

Pull a single resource by its key:

```bash
# Pull a specific workflow
knock workflow pull <workflow-key>

# Pull a specific email layout
knock email-layout pull <layout-key>
```

**Example:**

```bash
knock workflow pull order-confirmation
knock email-layout pull default
```

### Pull options

| Option | Description |
|--------|-------------|
| `--all` | Pull all resources of this type |
| `--environment`, `-e` | Target environment |
| `--hide-uncommitted-changes` | Don't include uncommitted changes |

## Pushing resources

### Push all resources

Push all local resources to Knock:

```bash
knock push --all
```

This pushes all resources from the configured `knockDir` to Knock.

### Push specific resource types

Push only specific resource types:

```bash
# Push only workflows
knock workflow push --all

# Push only email layouts
knock email-layout push --all

# Push only translations
knock translation push --all
```

### Push a specific resource

Push a single resource by its key (the directory name):

```bash
# Push a specific workflow
knock workflow push <workflow-key>

# Push a specific email layout
knock email-layout push <layout-key>
```

**Example:**

```bash
knock workflow push order-confirmation
knock email-layout push default
```

### Push options

| Option | Description |
|--------|-------------|
| `--all` | Push all resources of this type |
| `--environment`, `-e` | Target environment |
| `--commit`, `-m` | Commit changes with a message after pushing |

### Push and commit

To push changes and commit them in one operation:

```bash
knock workflow push order-confirmation --commit -m "Updated order confirmation template"
```

## Workflow commands

### List workflows

```bash
knock workflow list
```

### Pull workflow

```bash
# Pull all workflows
knock workflow pull --all

# Pull specific workflow
knock workflow pull <workflow-key>
```

### Push workflow

```bash
# Push all workflows
knock workflow push --all

# Push specific workflow
knock workflow push <workflow-key>
```

### Validate workflow

Validate workflow structure without pushing:

```bash
knock workflow validate <workflow-key>
```

### Run workflow (trigger)

Trigger a workflow for testing:

```bash
knock workflow run <workflow-key> \
  --recipients='[{"id": "user-123"}]' \
  --data='{"order_id": "12345"}'
```

## Email layout commands

### List email layouts

```bash
knock email-layout list
```

### Pull email layout

```bash
# Pull all layouts
knock email-layout pull --all

# Pull specific layout
knock email-layout pull <layout-key>
```

### Push email layout

```bash
# Push all layouts
knock email-layout push --all

# Push specific layout
knock email-layout push <layout-key>
```

## Commit commands

### List commits

View commit history:

```bash
knock commit list
```

### Create commit

Commit staged changes:

```bash
knock commit create -m "Commit message"
```

### Promote commit

Promote changes between environments:

```bash
knock commit promote --to=production
```

## Translation commands

### Pull translations

```bash
# Pull all translations
knock translation pull --all

# Pull specific locale
knock translation pull <locale>
```

### Push translations

```bash
# Push all translations
knock translation push --all

# Push specific locale
knock translation push <locale>
```

## Initialization and configuration

### Initialize project

Create a new knock.json configuration:

```bash
knock init
```

This interactive command asks for the knock directory location and creates the configuration file.

### Whoami

Check current authentication:

```bash
knock whoami
```

## Common workflows

### Initial setup

```bash
# 1. Authenticate
export KNOCK_SERVICE_TOKEN=<your-token>

# 2. Initialize project
knock init

# 3. Pull existing resources
knock pull --all
```

### Make changes and deploy

```bash
# 1. Make local changes to workflow files

# 2. Push changes
knock workflow push <workflow-key>

# 3. Commit changes
knock commit create -m "Updated workflow"

# 4. Promote to production
knock commit promote --to=production
```

### Sync before editing

```bash
# Always pull latest before making changes
knock pull --all

# Make edits...

# Push and commit
knock push --all --commit -m "Updated templates"
```

## Error handling

### Common errors

**"Resource not found"**
- The specified key doesn't match any resource
- Verify the key matches the directory name exactly

**"Validation failed"**
- The resource has structural errors
- Check the error message for specific field issues
- Reference the JSON schema for correct structure

**"Uncommitted changes exist"**
- There are pending changes that haven't been committed
- Either commit first or use `--force` if available

**"Environment not found"**
- The specified environment doesn't exist
- Check available environments in the Knock dashboard

### Debugging

Use verbose output for troubleshooting:

```bash
knock workflow push <key> --verbose
```
