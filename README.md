# Knock skills repository

This repository contains structured skills and best practices for AI agents. Each skill is a self-contained module with rules, guidelines, and examples.

```
                       ┌─────────────────────────┐
                       │   Notification System   │
                       └────────────┬────────────┘
                                    │
          ┌──────────┬──────────────┴──────────────┬──────────┐
          │          │              │              │          │
      ┌───┴───┐  ┌───┴───┐     ┌────┴────┐    ┌────┴────┐  ┌──┴───┐
      │ Email │  │  SMS  │     │  Push   │    │ In-app  │  │ Chat │
      └───────┘  └───────┘     └─────────┘    └─────────┘  └──────┘
```

## Structure

```
skills/
├── build.sh               # Root-level script to build all AGENTS.md files
└── notification-best-practices/
    ├── SKILL.md          # Human-readable guide for using the skill
    ├── AGENTS.md         # Complete content for AI agents (auto-generated)
    └── rules/            # Individual rule files
        ├── *.md          # Rule files in markdown format
```

## Skills

### notification-best-practices

Comprehensive guidelines for designing, writing, and implementing effective notification systems across all channels (email, push, SMS, in-app, chat).

**Includes:**
- Channel-specific guidelines and constraints
- Copy writing best practices
- System implementation rules
- Template examples
- Transactional email best practices
- Welcome email patterns

## Adding new skills

See `AGENTS.md` for detailed instructions on how to add new skills and rules to this repository.

## Usage

### For AI agents

Reference skills using their path:
- `skills/notification-best-practices/AGENTS.md` - Complete skill content
- `skills/notification-best-practices/SKILL.md` - Skill overview and usage guide

### For humans

Each skill includes:
- `SKILL.md` - Overview and how to use the skill
- `rules/*.md` - Individual rule files organized by topic
- `AGENTS.md` - Complete concatenated content (auto-generated)

## Building skills

Run the root-level build script to generate `AGENTS.md` files for all skills:

```bash
./build.sh
```

This script:
- Finds all skill directories in `skills/`
- Concatenates all rule files from each skill's `rules/` directory
- Generates `AGENTS.md` for each skill
- Extracts skill titles and descriptions from `SKILL.md` files

The build script automatically processes all skills, so you only need to run it once to update all `AGENTS.md` files.

## Contributing

When adding new skills:
1. Create a new directory under `skills/`
2. Add rule files in a `rules/` subdirectory
3. Create `SKILL.md` with usage instructions
4. Optionally create `build.sh` to generate `AGENTS.md`
5. Follow the sentence case convention for all titles and headings

See `AGENTS.md` for complete guidelines.
