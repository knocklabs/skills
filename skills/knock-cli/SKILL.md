---
name: knock-cli
description: Guidelines for working with the Knock CLI to manage workflows, templates, and other notification resources in a Knock project.
---

# Knock CLI skill

This skill provides comprehensive guidelines for working with the Knock CLI to manage workflows, templates, and other notification resources.

## Overview

The Knock CLI skill includes detailed rule sets covering:

1. **CLI installation and authentication** - How to install and authenticate with the Knock CLI
2. **Knock directory structure** - Understanding the knock directory layout and configuration
3. **CLI commands reference** - Pull, push, and resource management commands
4. **Workflow templates** - Structures, patterns, and best practices for workflows and templates
5. **Guides and message types** - Working with in-app guides for lifecycle messaging and message types as their schema

## How to use this skill

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
- `rules/cli-commands-reference.md` - CLI commands for resource management
- `rules/workflow-templates.md` - Workflow and template structures and best practices
- `rules/guides-and-message-types.md` - Guides and message types for lifecycle messaging

## Quick reference

### Common commands

```bash
# Initialize a new project
knock init

# Pull all resources from Knock
knock pull --all

# Push all resources to Knock
knock push --all

# Push a specific workflow
knock workflow push <workflow-key>

# Push a specific email layout
knock email-layout push <layout-key>

# List channels (discover valid channel_key values before creating workflows)
knock channel list

# Guide and message type commands
knock message-type list          # Discover message type keys before creating guides
knock guide list                 # List existing guides
knock guide push <guide-key>     # Push a guide after modifying
knock message-type push <key>    # Push a message type after modifying
```

### Key concepts

- **knockDir**: The directory where Knock resources are stored (configured in knock.json)
- **Resource types**: workflows, email-layouts, guides, message-types, translations, partials, commits
- **Guides vs workflows**: Guides are for lifecycle messaging (banners, modals); workflows are for notifications
- **Template modes**: Visual blocks (default for new emails) vs HTML (only when explicitly requested)
- **Variable namespaces**: `data` (trigger payload), `vars` (environment variables), `recipient`, `actor`, `tenant`

### Important patterns

1. **Push after every change** - Local edits stay local until pushed. No push = no update in Knock.
2. **File path references use `@` suffix**: `"content@": "visual_blocks/1.content.md"`
3. **Paths are relative to containing file**: Don't double the step directory
4. **Always use `data.` for trigger payload values**, not `vars.`
5. **Read existing files before modifying** to preserve structure
6. **Discover channel keys before creating workflows** - Run `knock channel list` to get valid `channel_key` values
7. **Discover message type keys before creating guides** - Run `knock message-type list` to get valid message type keys

## Best practices summary

1. **Pull before editing** - Sync latest changes before making modifications
2. **Push after modifying** - Local changes are not persisted to Knock until explicitly pushed
3. **Read before writing** - Understand existing structure to avoid data loss
4. **Use correct namespaces** - `data` for dynamic payload, `vars` for environment constants
5. **Visual blocks by default** - Use visual blocks for new emails; preserve existing mode when editing
6. **Verify paths** - File references are relative to the containing file
7. **Test changes** - Validate workflows after pushing changes
