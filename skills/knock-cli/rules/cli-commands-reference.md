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
  - variables
  - assets
category: knock-cli
last_updated: 2026-10-21
---

# CLI commands reference

## Core concepts

### Interactive prompts and the `--force` flag

Many Knock CLI commands display interactive confirmation prompts that require user input. This is critical for AI agents and automated scripts, because commands will hang or default to "no" if input is not provided.

**Commands that prompt for confirmation (and support `--force`):**

| Command | Prompt | When |
|---------|--------|------|
| `knock workflow pull <key>` | `Create a new workflow directory? (y/N)` | When the local directory doesn't exist yet |
| `knock layout pull <key>` | `Create a new email layout directory? (y/N)` | When the local directory doesn't exist yet |
| `knock guide pull <key>` | `Create a new guide directory? (y/N)` | When the local directory doesn't exist yet |
| `knock message-type pull <key>` | `Create a new message type directory? (y/N)` | When the local directory doesn't exist yet |
| `knock partial pull <key>` | `Create a new partial directory? (y/N)` | When the local directory doesn't exist yet |
| `knock pull` | Multiple directory creation prompts | When pulling resources that don't exist locally yet |
| `knock commit promote` | Confirmation prompt | When promoting changes between environments |
| `knock commit` | Confirmation prompt | When committing changes |
| `knock workflow activate` | Confirmation prompt | When activating/deactivating a workflow |
| `knock guide activate` | Confirmation prompt | When activating/deactivating a guide |
| `knock variable pull` | Confirmation prompt | When pulling all variables into `variables.json`, or removing an entry that is not in Knock |
| `knock variable push` | Confirmation prompt | When pushing variables (unlike other `push` commands) |
| `knock variable delete <key>` | Confirmation prompt | When deleting a variable or clearing an environment override |
| `knock asset archive <asset-id>` | Confirmation prompt | When archiving an asset. `--force` is required with `--json` |

**Handling prompts:** Pass `--force` to skip all confirmation prompts. Always use `--force` when running commands from agents or automated scripts:

```bash
# Pull without confirmation prompts
knock workflow pull <workflow-key> --force
knock pull --force

# Commit all changes without prompts
knock commit -m "message" --force
# Promote all changes without prompts (promotes ALL unpromoted commits — see scoped approach below)
knock commit promote --to=production --force
```

**Commands that are interactive and cannot use `--force`:**

| Command | Behavior |
|---------|----------|
| `knock init` | Interactive prompt for the resources directory. It takes no directory flag, so have the user run it, or write `knock.json` directly. If a `knock.json` already exists, there is no need to run `knock init`. |
| `knock login` | Opens a browser window for authentication. Must be run manually by the user. |
| `knock workflow new` | Interactive step selection. Use `--key` and `--steps` flags to skip prompts. |
| `knock guide new` | Interactive message type selection. Use `--key` and `--message-type` flags to skip prompts. |
| `knock message-type new` | Interactive setup. Use `--key` and `--name` flags to skip prompts. |
| `knock partial new` | Interactive setup. Use `--key` and `--type` flags to skip prompts. |
| `knock variable new` | Prompts only when it creates `variables.json`. Pass `--force` to skip the prompt. `--key` and `--type` are required. |

**Commands that never prompt (safe for direct execution):**

- All `list` commands (`knock workflow list`, `knock channel list`, etc.)
- All `push` commands (`knock workflow push <key>`, `knock push`, etc.), except `knock variable push`
- All `validate` commands (`knock workflow validate <key>`, etc.)
- `knock whoami`
- `knock workflow run` (trigger)
- Pull commands when the local directory already exists (updates in place without prompting)

### Push required after changes

Local edits to Knock resources (workflows, layouts, partials, etc.) are not synced to Knock until you push. Always run the appropriate push command after modifying files—otherwise Knock continues using the previous version.

### Resource types

The Knock CLI manages several resource types:

| Resource | Description | Command prefix |
|----------|-------------|----------------|
| `workflow` | Notification workflows | `knock workflow` |
| `layout` | Email layout templates | `knock layout` |
| `guide` | In-app guides (lifecycle messaging) | `knock guide` |
| `message-type` | Message type schemas for guides | `knock message-type` |
| `channel` | Notification channels | `knock channel` |
| `translation` | Localization files | `knock translation` |
| `partial` | Reusable template partials | `knock partial` |
| `audience` | Audience definitions | `knock audience` |
| `schema` | Item schemas for users, tenants, and objects | `knock schema` |
| `commit` | Version control for changes | `knock commit` |
| `variable` | Account-wide variables (`vars.<key>`) | `knock variable` |
| `asset` | Account-wide image assets | `knock asset` |

### Global options

These options work with most commands:

| Option | Description |
|--------|-------------|
| `--environment` | Target environment (development, staging, production) |
| `--branch` | Slug of the branch to use |
| `--service-token` | Service token for authentication |
| `--help` | Show help for the command |

Flags are matched by full name, so use `--environment=development` rather than a short alias.

To override the resources directory, use `--knock-dir` on `knock pull` and `knock push`. Resource subcommands take their own directory flag instead, such as `--workflows-dir` on `knock workflow pull` and `--layouts-dir` on `knock layout pull`.

## Pulling resources

**Note:** Pull commands prompt for confirmation when creating new local directories. Use `--force` to skip these prompts (see [Interactive prompts and the `--force` flag](#interactive-prompts-and-the---force-flag)).

### Pull all resources

Sync all resources from Knock to your local project:

```bash
knock pull --force
```

This pulls all resource types into the configured `knockDir`.

### Pull specific resource types

Pull only specific resource types:

```bash
# Pull only workflows
knock workflow pull --all --force

# Pull only email layouts
knock layout pull --all --force

# Pull only translations
knock translation pull --all --force

# Pull only guides
knock guide pull --all --force

# Pull only message types
knock message-type pull --all --force
```

### Pull a specific resource

Pull a single resource by its key:

```bash
# Pull a specific workflow
knock workflow pull <workflow-key> --force

# Pull a specific email layout
knock layout pull <layout-key> --force
```

**Example:**

```bash
knock workflow pull order-confirmation --force
knock layout pull default --force
```

**Note:** If the local directory already exists, pull commands update in place without prompting. The `--force` flag is only needed for the first pull of a given resource, but is safe to always include.

### Pull options

| Option | Description |
|--------|-------------|
| `--all` | Pull all resources of this type |
| `--environment` | Target environment |
| `--hide-uncommitted-changes` | Don't include uncommitted changes |
| `--force` | Skip confirmation prompts (always use in automated/agent contexts) |

## Pushing resources

### Push all resources

Push all local resources to Knock:

```bash
knock push
```

This pushes all resources from the configured `knockDir` to Knock.

### Push specific resource types

Push only specific resource types:

```bash
# Push only workflows
knock workflow push --all

# Push only email layouts
knock layout push --all

# Push only translations
knock translation push --all

# Push only guides
knock guide push --all

# Push only message types
knock message-type push --all
```

### Push a specific resource

Push a single resource by its key (the directory name):

```bash
# Push a specific workflow
knock workflow push <workflow-key>

# Push a specific email layout
knock layout push <layout-key>
```

**Example:**

```bash
knock workflow push order-confirmation
knock layout push default
```

### Push options

| Option | Description |
|--------|-------------|
| `--all` | Push all resources of this type |
| `--environment` | Target environment |
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
knock workflow pull --all --force

# Pull specific workflow
knock workflow pull <workflow-key> --force
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
knock layout list
```

### Pull email layout

```bash
# Pull all layouts
knock layout pull --all --force

# Pull specific layout
knock layout pull <layout-key> --force
```

### Push email layout

```bash
# Push all layouts
knock layout push --all

# Push specific layout
knock layout push <layout-key>
```

## Guide commands

### List guides

```bash
knock guide list
```

### Create a new guide

```bash
knock guide new -k <guide-key> -n "Guide name" -m <message-type-key>
```

### Pull guide

```bash
# Pull all guides
knock guide pull --all --force

# Pull specific guide
knock guide pull <guide-key> --force
```

### Push guide

```bash
# Push all guides
knock guide push --all

# Push specific guide
knock guide push <guide-key>
```

### Validate guide

```bash
knock guide validate <guide-key>
```

### Activate or deactivate guide

```bash
knock guide activate <guide-key> --environment <env> --status true
knock guide activate <guide-key> --environment <env> --status false
```

### Other guide commands

```bash
knock guide get <guide-key>      # Display a single guide
knock guide open <guide-key>     # Open in dashboard
knock guide generate-types --output-file types.ts  # Generate TypeScript types
```

## Message type commands

### List message types

```bash
knock message-type list
```

Lists all message types with their keys. Use these keys when creating guides. Message type keys are project-specific—discover them before creating guides.

### Create a new message type

```bash
knock message-type new -k <message-type-key> -n "Message type name"
```

### Pull message type

```bash
# Pull all message types
knock message-type pull --all --force

# Pull specific message type
knock message-type pull <message-type-key> --force
```

### Push message type

```bash
# Push all message types
knock message-type push --all

# Push specific message type
knock message-type push <message-type-key>
```

Message type push operates only in the development environment.

### Validate message type

```bash
knock message-type validate <message-type-key>
```

### Other message type commands

```bash
knock message-type get <message-type-key>   # Display a single message type
knock message-type open <message-type-key>  # Open in dashboard
```

## Channel commands

### List channels

```bash
knock channel list
```

Lists all channels configured in the project with their keys. Channel keys are project-specific—they vary per project and must be discovered, not assumed. Use the keys from this output for `channel_key` in workflow steps.

## Commit commands

Knock uses a commit model to version and promote changes across environments. By default, accounts have a **development** environment and a **production** environment. Additional intermediate environments (e.g., staging) can be configured between them. Promoting a commit moves it from the environment of origin to the next environment in the account's sequence.

### List commits

View commit history:

```bash
knock commit list
```

Use `--resource-type` and `--resource-id` to scope the list to a specific resource. Use `--environment` to list commits in a non-development environment (useful for finding a commit ID to promote further up the chain):

```bash
# List commits for a specific workflow in development (default)
knock commit list --resource-type=workflow --resource-id=order-confirmation

# List commits for a specific workflow in a higher environment
knock commit list --resource-type=workflow --resource-id=order-confirmation --environment=staging

# List only unpromoted commits in an environment
knock commit list --no-promoted --environment=staging
```

**`knock commit list` flags:**

| Flag | Description |
|------|-------------|
| `--environment` | Target environment (defaults to development) |
| `--resource-type` | Filter by resource type: `workflow`, `email_layout`, `guide`, `message_type`, `partial`, `translation` |
| `--resource-id` | Filter by resource key. Must be used with `--resource-type` |
| `--[no-]promoted` | Show only promoted or unpromoted changes |

### Create commit

Commit staged changes:

```bash
# Commit all uncommitted changes
knock commit -m "Commit message" --force

# Commit only changes for a specific resource (recommended when working on one resource)
knock commit -m "Updated order confirmation" \
  --resource-type=workflow --resource-id=order-confirmation --force
```

Use `--resource-type` and `--resource-id` together to commit only the resource you've been working on, leaving any other uncommitted changes untouched.

**`knock commit` flags:**

| Flag | Description |
|------|-------------|
| `-m, --commit-message` | The commit message |
| `--resource-type` | Commit only changes for this resource type |
| `--resource-id` | Commit only changes for this resource key. Must be used with `--resource-type` |
| `--force` | Skip confirmation prompt |

### Promote commit

> **Warning:** `knock commit promote --to=<env>` promotes **all** unpromoted commits across all resources from the preceding environment. If you are working on a single resource and other resources have commits that aren't ready to promote, use `--only` instead (see below).

Promote all changes to a named environment:

```bash
# Promotes ALL unpromoted commits from the preceding environment — use with caution
knock commit promote --to=production --force
```

Promote a single commit to the next environment in sequence:

```bash
# Promotes only this one commit to the next environment in the account's sequence
knock commit promote --only=<commit-id> --force
```

**Important notes on `--only`:**
- `--to` and `--only` cannot be used together
- `--only` always promotes to the **next** environment in the account's sequence. You cannot specify a named destination environment with `--only`
- When a commit is promoted, it receives a **new ID** in the higher environment. The promote response includes this new commit ID, which you can pass directly to a subsequent `--only` call to continue promoting up the chain (e.g., from an intermediate environment to production)
- Alternatively, use `knock commit list --resource-type=<type> --resource-id=<key> --environment=<env>` to look up the current commit ID for a resource in any environment at any time

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

## Audience commands

### List audiences

```bash
knock audience list
```

### Create a new audience

```bash
knock audience new -k <audience-key> -n "Audience name" -t static
```

| Flag | Description |
|------|-------------|
| `-k`, `--key` | The audience key (directory name) |
| `-n`, `--name` | Display name |
| `-t`, `--type` | `static` or `dynamic` |
| `-d`, `--description` | Optional description |
| `-p`, `--push` | Push to Knock after creation |
| `--force` | Skip the directory confirmation prompt |

### Pull audiences

```bash
# Pull all audiences
knock audience pull --all --force

# Pull a specific audience
knock audience pull <audience-key> --force
```

### Push audiences

```bash
# Push all audiences
knock audience push --all

# Push a specific audience
knock audience push <audience-key>
```

### Validate audiences

```bash
knock audience validate <audience-key>
knock audience validate --all
```

### Other audience commands

```bash
knock audience get <audience-key>    # Display a single audience
knock audience open <audience-key>   # Open in dashboard
```

### Archive an audience

```bash
knock audience archive <audience-key> --environment=<env>
```

> **Warning:** Archiving affects **all** environments and cannot be undone. `--environment` is required on this command, and `--force` skips the confirmation prompt.

## Schema commands

Item schemas describe the properties of users, tenants, and objects. `knock schema` has only `pull` and `push`—there is no `get`, `list`, `new`, `open`, or `validate`.

### Pull schemas

```bash
# Pull all schemas
knock schema pull --all --force

# Pull a single item schema; item type is user, tenant, or object
knock schema pull user

# Object schemas are addressed by collection
knock schema pull object --collection=<collection-key>
```

### Push schemas

```bash
# Push all schemas
knock schema push --all

# Push a single item schema
knock schema push tenant
knock schema push object --collection=<collection-key>
```

| Flag | Description |
|------|-------------|
| `--all` | Operate on every schema in the schemas directory. Cannot be combined with an item type argument or `--collection` |
| `--collection` | Object collection key; valid only with the `object` item type |
| `--schemas-dir` | Override the schemas directory |
| `--force` | Skip the confirmation prompt (`pull` only; `push` has no `--force`) |

Schemas are not covered by the top-level `knock pull` and `knock push`. Use `knock schema pull` and `knock schema push` for them.

## Variable commands

Variables are account-wide values referenced in templates as `vars.<key>`. Each variable has a default value and optional per-environment overrides. They are not scoped to a branch, and they are not included in `knock pull` or `knock push`. Variables are saved when you push or set them, and there is no commit step.

Local variables live in a single `variables.json` file, in the knock directory when `knock.json` is present and otherwise in the current directory. Each property name is a variable key. Keys must start with a letter or underscore and contain only letters, numbers, and underscores.

```json
{
  "base_url": {
    "type": "public",
    "value": "https://example.com",
    "environment_values": { "development": "https://dev.example.com" }
  },
  "api_token": {
    "type": "secret",
    "value_set": true
  }
}
```

**Secret variables.** Knock never returns secret values. Pulled and listed secrets show only whether a value is set (`value_set`, `environment_values_set`). Do not put a secret value in `variables.json` or pass it on the command line. Set secret values with `--value-stdin` or `--value-file`, and secret environment overrides with `--environment-value-file`.

### List and get variables

```bash
knock variable list
knock variable list --environment=production   # Value that applies in one environment
knock variable list --type=secret
knock variable get <key>                        # Default value and every override
```

`--environment` on `list` filters the output. `get` does not accept `--environment`.

### Create a new variable entry

Adds an entry to the local `variables.json`. Does not push unless `--push` is passed.

```bash
knock variable new --key=base_url --type=public --value=https://example.com --force
knock variable new --key=api_token --type=secret --force
```

| Flag | Description |
|------|-------------|
| `--key` | The variable key (required) |
| `--type` | `public` or `secret` (required) |
| `--value` | Default value. Public variables only |
| `--description` | Optional description |
| `--knock-dir` | Directory used to locate `variables.json` |
| `--push` | Push the entry after writing it |
| `--force` | Skip the prompt when creating the file |

### Set a variable

Creates or updates a variable in Knock directly. `--type` is required when creating a variable and must match the existing type otherwise. Pass only one of `--value`, `--value-file`, `--value-stdin`, or `--unset-value`.

```bash
# Public variable with a development override
knock variable set base_url --type=public --value=https://example.com \
  --environment-value=development=https://dev.example.com

# Secret variable (never pass the value as an argument)
printf '%s' "$API_TOKEN" | knock variable set api_token --type=secret --value-stdin

# Clear an override or the description
knock variable set base_url --unset-environment=development
knock variable set base_url --unset-description
```

| Flag | Description |
|------|-------------|
| `--value-file` | Read the default value from a file (bytes are not trimmed) |
| `--value-stdin` | Read the default value from stdin (bytes are not trimmed) |
| `--unset-value` | Clear the default value |
| `--unset-description` | Clear the description |
| `--environment-value` | `<slug>=<value>` override. Repeatable. Public variables only |
| `--environment-value-file` | `<slug>=<path>` override read from a file. Repeatable |
| `--unset-environment` | Clear the override for an environment slug. Repeatable |

### Pull and push variables

```bash
# Pull every variable, replacing variables.json
knock variable pull --force

# Update one entry
knock variable pull <key> --force

# Push every entry, or one entry
knock variable push --force
knock variable push <key> --force
```

- `pull` always fetches the full catalog and does not accept `--environment`. Without a key, entries missing from Knock are removed from the local file.
- `push` does not delete remote variables that are missing from the file. A new variable needs a string `value`, and a variable's type cannot change after creation. A `null` or omitted value is skipped, and an empty string clears it.
- Both accept `--knock-dir` to locate `variables.json`.

### Delete a variable

```bash
# Delete the variable and every override (cannot be undone)
knock variable delete <key> --force

# Clear one environment's override only
knock variable delete <key> --environment=development --force
```

## Asset commands

Assets are account-wide image files hosted by Knock. Asset commands take no environment or branch, and there are only `upload` and `archive` commands.

### Upload an asset

```bash
knock asset upload ./logo.png
knock asset upload ./logo.png --filename="Company logo"
cat ./logo.png | knock asset upload - --filename=logo.png
```

| Flag | Description |
|------|-------------|
| `--filename` | Display name. Defaults to the file name. Required when reading stdin (`-`) |
| `--mime-type` | `image/jpeg`, `image/png`, or `image/gif`. Use it when the type cannot be detected or the extension and file contents disagree |

Files must be JPEG, PNG, or GIF, between 1 byte and 5,000,000 bytes. Pass `--json` to get the asset's `id` and hosted `url` as JSON, then use the URL in templates.

### Archive an asset

```bash
knock asset archive <asset-id> --force
```

> **Warning:** Archiving applies to the whole account. The asset id must be a UUID, which `knock asset upload` prints. `--force` is required with `--json`.

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

# 2. Initialize project (interactive; prompts for the resources directory)
knock init

# 3. Pull existing resources (--force skips confirmation prompts)
knock pull --force
```

### Discover before creating

Before creating workflows that use channels or layouts, discover the project's configuration:

```bash
# List available channel keys (use these for channel_key in workflow steps)
knock channel list

# List available email layout keys (use these for layout_key in template settings)
knock layout list
```

Before creating guides, discover available message types:

```bash
# List available message type keys (use these when creating guides)
knock message-type list

# List existing guides
knock guide list
```

Use the exact keys from this output—don't assume keys from schema examples or other projects.

### Make changes and deploy

When working on a single resource, use the scoped approach to avoid accidentally promoting other resources that may not be ready:

```bash
# 1. Push your changes
knock workflow push <workflow-key>

# 2. Commit only this resource
knock commit -m "Updated workflow" --resource-type=workflow --resource-id=<workflow-key> --force

# 3. Get the commit ID
knock commit list --resource-type=workflow --resource-id=<workflow-key>

# 4. Promote only this commit to the next environment
knock commit promote --only=<commit-id> --force

# 5. To promote further (e.g., to production), use the new commit ID returned in step 4,
#    or look it up in the higher environment:
knock commit list --resource-type=workflow --resource-id=<workflow-key> --environment=<next-env>
knock commit promote --only=<new-commit-id> --force
```

If you are certain you want to promote **all** pending changes across every resource:

```bash
knock commit -m "Updated workflow" --force
knock commit promote --to=production --force
```

### Sync before editing

```bash
# Always pull latest before making changes (--force skips any new directory prompts)
knock pull --force

# Make edits...

# Push and commit (push does not prompt)
knock push --commit -m "Updated templates"
```

## Error handling

### Common errors

**"Resource not found"**
- The specified key doesn't match any resource
- Verify the key matches the directory name exactly

**"Validation failed"**
- The resource has structural errors
- Check the error message for specific field issues
- Run `knock <resource> validate <key>` to see the specific structural errors
- If the error mentions `channel_key` does not exist (e.g., `'knock-in-app' does not exist`), run `knock channel list` to find valid channel keys for this project

**"Uncommitted changes exist"**
- There are pending changes that haven't been committed
- Either commit first or use `--force` if available

**"Environment not found"**
- The specified environment doesn't exist
- Check available environments in the Knock dashboard

### Debugging

Validate a resource locally to surface structural errors before pushing:

```bash
knock workflow validate <key>
```

Pass `--json` for machine-readable output on the commands that support it — all `get` and `list` commands, `knock whoami`, `knock branch list` / `create` / `rebase`, `knock variable set` / `delete`, and `knock asset upload` / `archive`. This makes error details easier to inspect:

```bash
knock workflow get <key> --json
```
