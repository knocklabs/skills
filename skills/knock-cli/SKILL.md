---
name: knock-cli
description: Guidelines for working with the Knock CLI to manage workflows, templates, and other notification resources, and to run a prompt with the Knock agent.
---

# Knock CLI skill

This skill provides comprehensive guidelines for working with the Knock CLI to manage workflows, templates, and other notification resources.

## Overview

The Knock CLI skill includes detailed rule sets covering:

1. **CLI installation and authentication** - How to install and authenticate with the Knock CLI
2. **Knock directory structure** - Understanding the knock directory layout and configuration
3. **CLI commands reference** - Pull, push, resource management, variable, asset, and Knock agent commands
4. **Workflow templates** - Structures, patterns, and best practices for workflows and templates
5. **Guides and message types** - Working with in-app guides for lifecycle messaging and message types as their schema
6. **Partials** - Reusable template building blocks for email design systems

## How to use this skill

### Before managing resources

Run `knock environment list` before choosing an environment:

- If the account has one environment, environments are not enabled. Commands without `--environment` target the account's default environment (production on new accounts), `knock push` creates drafts there, and `knock commit` publishes those drafts live. Do not use promotion or branch commands.
- If the account has multiple environments, environments are enabled. Commands without `--environment` still target the account's default environment (development when environments are enabled); pass an explicit environment when needed. Branch commands apply to development, and commits can be promoted through the environment sequence.
- In either model, scope commits to the resource being changed with `--resource-type` and `--resource-id`. Leave drafts uncommitted unless the user asked to publish them.

### For initial setup

When setting up a new project with Knock:

1. **Start with installation and authentication** (`rules/cli-installation-authentication.md`)
   - Verify the CLI is installed
   - Authenticate with a service token or dashboard account
   - Initialize the project with `knock init`

2. **Understand the directory structure** (`rules/knock-directory-structure.md`)
   - Learn the knock.json configuration
   - Understand resource organization

### For managing resources

When working with Knock resources:

1. **Use the CLI commands reference** (`rules/cli-commands-reference.md`)
   - Pull resources from Knock to your local project
   - Push changes back to Knock
   - Work with specific resource types

2. **Follow workflow and template guidelines** (`rules/workflow-templates.md`)
   - Understand template modes and structures
   - Avoid common mistakes with file paths and variables
   - Follow best practices for workflow modifications

### For managing guides and message types

When working with in-app guides (banners, modals, announcements):

1. **Start with guides and message types** (`rules/guides-and-message-types.md`)
   - Understand that guides are separate from workflows (lifecycle messaging vs notifications)
   - Message types define the schema; guides reference them via `schema_key` and `schema_variant_key`
   - Use built-in types (banner, modal, card) when possible; create custom message types when needed

2. **Discover before creating**
   - Run `knock message-type list` to see available message type keys
   - Run `knock guide list` to see existing guides
   - Use exact keys from output when creating new guides

### For working with partials

When building reusable email components (callouts, quote blocks, comment cards):

1. **Start with partials** (`rules/partials.md`)
   - Understand partial file structure and `partial.json` schema
   - Define `input_schema` for block editor fields (same format as message type variant fields)
   - Use `visual_block_enabled: true` for partials that appear in the email visual block editor

2. **Create and push**
   - Run `knock partial new -k <key> -n "Name" -t html --force` to scaffold
   - Add `input_schema` and edit content; validate and push with `knock partial push <key>`

### For managing variables and assets

When working with `vars.<key>` values or hosted images:

1. **Use the variable and asset command sections** (`rules/cli-commands-reference.md`)
   - Run `knock variable list` to see existing keys before referencing `vars.<key>` in templates
   - Set secret values with `--value-stdin` or `--value-file`, never as a command-line argument
   - Run `knock asset upload <file>` and use the returned URL in templates

### For running the Knock agent

When the user wants the hosted Knock agent to answer a question or change resources in the account:

1. **Read the agent command section** (`rules/cli-commands-reference.md`)
   - Pass a prompt. With no prompt, `knock agent` opens an interactive chat and waits for a terminal.
   - Pass `--json`, and keep `session_id` for a follow-up with `--session`.
   - The agent writes to Knock. Pull afterward when the user needs those changes in local files.
   - Committing and promoting stay separate commands.

### For modifying workflows and templates

When making changes to workflows or templates:

1. **Always read before writing** - Understand existing structure before modifying
2. **Use visual blocks for new emails** - Always default to visual blocks mode; only use HTML mode if explicitly requested
3. **Use correct variable namespaces** - `data` for trigger payload, `vars` for environment variables
4. **Verify file path references** - Paths are relative to the file containing the reference
5. **Push after modifying** - Local file changes are not synced to Knock until you push. Run `knock workflow push <key>` (or the equivalent for other resource types) for changes to take effect.

## Rule files reference

- `rules/cli-installation-authentication.md` - Installation and authentication setup
- `rules/knock-directory-structure.md` - Directory structure and configuration
- `rules/cli-commands-reference.md` - CLI commands for resource management, variables, assets, and the Knock agent
- `rules/workflow-templates.md` - Workflow and template structures and best practices
- `rules/guides-and-message-types.md` - Guides and message types for lifecycle messaging
- `rules/partials.md` - Partials and reusable template building blocks

## Quick reference

### Common commands

```bash
# Initialize a new project (interactive; prompts for the resources directory)
knock init

# Pull all resources from Knock (--force skips confirmation prompts)
knock pull --force

# Pull a specific workflow
knock workflow pull <workflow-key> --force

# Push all resources to Knock (push never prompts)
knock push

# Push a specific workflow
knock workflow push <workflow-key>

# Push a specific email layout
knock layout push <layout-key>

# List channels (discover valid channel_key values before creating workflows)
knock channel list

# Guide and message type commands
knock message-type list          # Discover message type keys before creating guides
knock guide list                 # List existing guides
knock guide push <guide-key>     # Push a guide after modifying
knock message-type push <key>    # Push a message type after modifying

# Partial commands (email design system building blocks)
knock partial list               # List existing partials
knock partial new -k <key> -n "Name" -t html --force   # Create a new partial
knock partial pull <key> --force # Pull a partial from Knock
knock partial push <key>         # Push a partial after modifying
knock partial validate <key>     # Validate a partial locally

# Variable commands (account-wide `vars.<key>` values; not included in knock pull/push)
knock variable list              # List variables and overrides (secret values are never shown)
knock variable set <key> --type=public --value=<value>   # Create or update a variable
knock variable pull --force      # Pull variables into variables.json
knock variable push --force      # Push variables from variables.json

# Asset commands (account-wide image hosting)
knock asset upload ./logo.png    # Upload a JPEG, PNG, or GIF and get a hosted URL
knock asset archive <asset-id> --force

# Knock agent (writes to the account; local files stay unchanged until you pull)
knock agent "Add an email step to the welcome workflow" --json
knock agent --session <session-id> "Now shorten the subject line" --json

# Commit a specific resource only (publishes it live when the target is production)
knock commit -m "message" --resource-type=workflow --resource-id=<key> --force

# With environments enabled, get the commit ID and promote only that commit
knock commit list --resource-type=workflow --resource-id=<key>
knock commit promote --only=<commit-id> --force
```

### Key concepts

- **knockDir**: The directory where Knock resources are stored (configured in knock.json)
- **Resource types**: workflows, layouts, guides, message-types, translations, partials, audiences, schemas
- **Variables and assets**: Account-wide, with no branch or commit. `knock variable` commands use a single `variables.json` file, and `knock pull`/`knock push` skip both. Secret variable values are never returned or written locally
- **Knock agent**: `knock agent` runs a prompt in a hosted agent session. It can create or update resources in the account. Local files stay unchanged until you pull, and committing or promoting is a separate command
- **Guides vs workflows**: Guides are for lifecycle messaging (banners, modals); workflows are for notifications
- **Template modes**: Visual blocks (default for new emails) vs HTML (only when explicitly requested)
- **Variable namespaces**: `data` (trigger payload), `vars` (environment variables), `recipient`, `actor`, `tenant`

### Important patterns

1. **Use `--force` on commands with prompts** - Many CLI commands (pull, commit, promote, activate) display interactive confirmation prompts. Always pass `--force` to skip them in automated/agent contexts.
2. **Push after every change** - Local edits stay local until pushed. No push = no update in Knock.
3. **File path references use `@` suffix**: `"content@": "visual_blocks/1.content.md"`
4. **Paths are relative to containing file**: Don't double the step directory
5. **Always use `data.` for trigger payload values**, not `vars.`
6. **Read existing files before modifying** to preserve structure
7. **Discover channel keys before creating workflows** - Run `knock channel list` to get valid `channel_key` values
8. **Discover message type keys before creating guides** - Run `knock message-type list` to get valid message type keys
9. **Scope every commit when working on a single resource** - Use `--resource-type` and `--resource-id`; on a production-only account, that commit publishes the resource live. When environments are enabled, use `knock commit promote --only=<commit-id>` to promote only that commit. Never run promotion commands on a production-only account.
10. **Pass a prompt to `knock agent`** - With no prompt, the command opens an interactive chat and waits. From an agent, pass the prompt and `--json`. Pull afterward when the user needs the agent's changes in the repo.

## Best practices summary

1. **Pull before editing** - Sync latest changes before making modifications
2. **Push after modifying** - Local changes are not persisted to Knock until explicitly pushed
3. **Read before writing** - Understand existing structure to avoid data loss
4. **Use correct namespaces** - `data` for dynamic payload, `vars` for environment constants
5. **Visual blocks by default** - Use visual blocks for new emails; preserve existing mode when editing
6. **Verify paths** - File references are relative to the containing file
7. **Test changes** - Validate workflows after pushing changes
8. **Respect the account's environment model** - On a production-only account, leave pushed changes as drafts unless the user asks to publish; a scoped commit publishes live. Only use branches and promotion when `knock environment list` shows that environments are enabled.
