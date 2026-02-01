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
4. **Workflow and template gotchas** - Important patterns and common mistakes when working with workflows and templates

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

2. **Follow workflow and template guidelines** (`rules/workflow-template-gotchas.md`)
   - Understand template modes and structures
   - Avoid common mistakes with file paths and variables
   - Follow best practices for workflow modifications

### For modifying workflows and templates

When making changes to workflows or templates:

1. **Always read before writing** - Understand existing structure before modifying
2. **Check template mode** - Preserve visual blocks or HTML mode as appropriate
3. **Use correct variable namespaces** - `data` for trigger payload, `vars` for environment variables
4. **Verify file path references** - Paths are relative to the file containing the reference

## Rule files reference

- `rules/cli-installation-authentication.md` - Installation and authentication setup
- `rules/knock-directory-structure.md` - Directory structure and configuration
- `rules/cli-commands-reference.md` - CLI commands for resource management
- `rules/workflow-template-gotchas.md` - Workflow and template best practices and gotchas

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
```

### Key concepts

- **knockDir**: The directory where Knock resources are stored (configured in knock.json)
- **Resource types**: workflows, email-layouts, translations, partials, commits
- **Template modes**: Visual blocks (structured) vs HTML (raw)
- **Variable namespaces**: `data` (trigger payload), `vars` (environment variables), `recipient`, `actor`, `tenant`

### Important patterns

1. **File path references use `@` suffix**: `"content@": "visual_blocks/1.content.md"`
2. **Paths are relative to containing file**: Don't double the step directory
3. **Always use `data.` for trigger payload values**, not `vars.`
4. **Read existing files before modifying** to preserve structure

## Best practices summary

1. **Pull before editing** - Sync latest changes before making modifications
2. **Read before writing** - Understand existing structure to avoid data loss
3. **Use correct namespaces** - `data` for dynamic payload, `vars` for environment constants
4. **Preserve template modes** - Keep visual blocks or HTML as originally set
5. **Verify paths** - File references are relative to the containing file
6. **Test changes** - Validate workflows after pushing changes
