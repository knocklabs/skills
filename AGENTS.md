# How to add new skills and rules

This guide explains how to structure and add new skills to this repository.

## Skill structure

Each skill should follow this structure:

```
skills/
└── your-skill-name/
    ├── SKILL.md          # Human-readable guide (required)
    ├── AGENTS.md         # Complete content for AI agents (optional, can be auto-generated)
    ├── build.sh          # Build script to generate AGENTS.md (optional)
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

### 4. Build AGENTS.md (optional)

The root-level `build.sh` script automatically generates `AGENTS.md` files for all skills. You don't need to create individual build scripts for each skill.

To generate `AGENTS.md` for all skills, run from the repository root:

```bash
./build.sh
```

The build script will:
- Find all skill directories
- Extract the skill title from `SKILL.md` (or use the directory name)
- Concatenate all rule files from `rules/` in alphabetical order
- Generate `AGENTS.md` for each skill

If you need custom build logic for a specific skill, you can still create a `build.sh` in that skill's directory, but the root-level script will handle most cases automatically.

```bash
#!/bin/bash

# Build script to concatenate all rules files into AGENTS.md
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RULES_DIR="$SCRIPT_DIR/rules"
OUTPUT_FILE="$SCRIPT_DIR/AGENTS.md"

# Start with the header
cat > "$OUTPUT_FILE" << 'EOF'
# Your skill name

Brief description.

## How to use this skill

Usage instructions...

---
EOF

# Process each rules file in order
# Remove frontmatter and append content
for file in "$RULES_DIR"/rule-1.md \
            "$RULES_DIR"/rule-2.md \
            "$RULES_DIR"/rule-3.md; do
    if [ -f "$file" ]; then
        echo "" >> "$OUTPUT_FILE"
        echo "" >> "$OUTPUT_FILE"
        # Remove frontmatter (lines between --- markers) and add content
        awk '/^---$/{if(++count==2)next} count<2{next} 1' "$file" >> "$OUTPUT_FILE"
        echo "" >> "$OUTPUT_FILE"
        echo "---" >> "$OUTPUT_FILE"
    fi
done

echo "✅ AGENTS.md built successfully from rules files"
```

### 5. Generate AGENTS.md (optional)

You can either:
- Manually create `AGENTS.md` with all content
- Use `build.sh` to auto-generate it from rules files
- Let AI agents reference individual rule files directly

To generate `AGENTS.md` for all skills, run from the repository root:
```bash
./build.sh
```

This will automatically process all skills and generate their `AGENTS.md` files.

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
- Provide a clear overview
- Explain when to use each rule
- Include quick reference sections
- Link to rule files using relative paths
- Be accessible to both humans and AI

### AGENTS.md should:
- Contain complete, self-contained content
- Include all rules concatenated
- Have clear section separators
- Be optimized for AI agent consumption

## Best practices

1. **Keep rules focused**: Each rule file should cover one topic or theme
2. **Use consistent structure**: Follow the same pattern across rule files
3. **Include examples**: Practical examples help clarify guidelines
4. **Cross-reference**: Link related rules when appropriate
5. **Update dates**: Keep `last_updated` in frontmatter current
6. **Test builds**: If using `build.sh`, test it after adding new rules
7. **Sentence case**: Always use sentence case for titles and headings

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

4. Regenerate `AGENTS.md` using the root-level build script:
   ```bash
   ./build.sh
   ```
   
   The build script automatically finds all rule files in the `rules/` directory, so you don't need to manually update any file lists.

## Reference implementation

See `skills/notification-best-practices/` for a complete example:
- Multiple rule files organized by topic
- `SKILL.md` with usage guide
- `AGENTS.md` with complete content (generated by root-level build script)
- All using sentence case consistently

## Questions?

When in doubt:
- Follow the structure of existing skills
- Use sentence case for all headings
- Keep rules focused and practical
- Include examples and clear guidance
- Test your build script if you create one
