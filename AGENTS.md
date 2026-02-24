# How to add new skills and rules

This guide explains how to structure and add new skills to this repository.

## Skill structure

Each skill should follow this structure:

```
skills/
└── your-skill-name/
    ├── SKILL.md          # Human-readable guide (required)
    └── rules/            # Rule files directory (required)
        ├── rule-1.md
        ├── rule-2.md
        └── ...
```

## Step-by-step guide

### 1. Create the skill directory

Create a new directory under `skills/` with a descriptive name using kebab-case:

```bash
mkdir -p skills/your-skill-name/rules
```

### 2. Create rule files

Add individual rule files in the `rules/` directory. Each rule file should:

- Use markdown format (`.md`)
- Include frontmatter with metadata:
  ```yaml
  ---
  title: Your rule title
  description: Brief description of the rule
  tags:
    - relevant-tag-1
    - relevant-tag-2
  category: your-skill-name
  last_updated: YYYY-MM-DD
  ---
  ```
- Use sentence case for all titles and headings
- Be focused on a single topic or theme
- Include examples and practical guidance

**Example rule file structure:**
```markdown
---
title: Rule name in sentence case
description: What this rule covers
tags:
  - tag1
  - tag2
category: your-skill-name
last_updated: 2026-01-23
---

# Rule name in sentence case

## Section heading

Content here...

### Subsection

More content...
```

### 3. Create SKILL.md

Create a `SKILL.md` file that serves as a human-readable guide. It should:

- Provide an overview of the skill
- Explain how to use the different rules
- Reference rule files using relative paths (e.g., `rules/rule-1.md`)
- Include quick reference sections
- Use sentence case for all headings

**Example SKILL.md structure:**
```markdown
# Your skill name

Brief description of what this skill provides.

## Overview

List the rule files and what they cover.

## How to use this skill

### For specific use case 1

1. **Start with rule X** (`rules/rule-x.md`)
   - What to look for
   - Key principles

2. **Check rule Y** (`rules/rule-y.md`)
   - Additional considerations

## Rule files reference

- `rules/rule-1.md` - Description
- `rules/rule-2.md` - Description

## Quick reference

Key points and patterns...
```

## Naming conventions

### Directory names
- Use kebab-case: `your-skill-name`
- Be descriptive and concise
- Avoid abbreviations unless widely understood

### Rule file names
- Use kebab-case: `rule-name.md`
- Be descriptive: `email-deliverability-guidelines.md` not `email.md`
- Group related rules logically

### Headings and titles
- **Always use sentence case** (only first word and proper nouns capitalized)
- Examples:
  - ✅ "Email deliverability best practices"
  - ✅ "How to write effective notifications"
  - ❌ "Email Deliverability Best Practices"
  - ❌ "How To Write Effective Notifications"

## Content guidelines

### Rule files should:
- Be focused on a single topic
- Include practical examples
- Use clear, actionable language
- Reference other rules when relevant
- Include code examples when applicable
- Use consistent formatting

### SKILL.md should:
- Include frontmatter with `name` and `description` fields
- Provide a clear overview
- Explain when to use each rule
- Include quick reference sections
- Link to rule files using relative paths
- Be accessible to both humans and AI

## Best practices

1. **Keep rules focused**: Each rule file should cover one topic or theme
2. **Use consistent structure**: Follow the same pattern across rule files
3. **Include examples**: Practical examples help clarify guidelines
4. **Cross-reference**: Link related rules when appropriate
5. **Update dates**: Keep `last_updated` in frontmatter current
6. **Sentence case**: Always use sentence case for titles and headings

## Example: adding a new rule to an existing skill

1. Create the rule file:
   ```bash
   touch skills/your-skill-name/rules/new-rule.md
   ```

2. Add content with frontmatter:
   ```markdown
   ---
   title: New rule name
   description: Description
   tags: [tag1, tag2]
   category: your-skill-name
   last_updated: 2026-01-23
   ---
   
   # New rule name
   
   Content...
   ```

3. Update `SKILL.md` to reference the new rule

## Reference implementation

See `skills/notification-best-practices/` for a complete example:
- Multiple rule files organized by topic
- `SKILL.md` with usage guide and frontmatter
- All using sentence case consistently

## Questions?

When in doubt:
- Follow the structure of existing skills
- Use sentence case for all headings
- Keep rules focused and practical
- Include examples and clear guidance
