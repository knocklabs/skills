#!/bin/bash

# Build script to generate AGENTS.md files for all skills
# This script finds all skill directories and concatenates their rules files
# into AGENTS.md files for use by AI agents

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_DIR="$SCRIPT_DIR/skills"

# Function to extract title from SKILL.md or use directory name
get_skill_title() {
    local skill_dir="$1"
    local skill_file="$skill_dir/SKILL.md"
    
    if [ -f "$skill_file" ]; then
        # Extract the first H1 heading from SKILL.md
        local title=$(grep -m 1 '^# ' "$skill_file" | sed 's/^# //')
        if [ -n "$title" ]; then
            echo "$title"
            return
        fi
    fi
    
    # Fallback to directory name converted to title case
    basename "$skill_dir" | sed 's/-/ /g' | awk '{for(i=1;i<=NF;i++)sub(/./,toupper(substr($i,1,1)),$i)}1'
}

# Function to extract description from SKILL.md
get_skill_description() {
    local skill_dir="$1"
    local skill_file="$skill_dir/SKILL.md"
    
    if [ -f "$skill_file" ]; then
        # Get the first paragraph after the title (skip H1 and empty lines)
        awk '/^# /{getline; while(getline && /^$/); if (!/^#/) print; exit}' "$skill_file" | head -1
    fi
}

# Function to build AGENTS.md for a single skill
build_skill_agent() {
    local skill_dir="$1"
    local skill_name=$(basename "$skill_dir")
    local rules_dir="$skill_dir/rules"
    local output_file="$skill_dir/AGENTS.md"
    
    if [ ! -d "$rules_dir" ]; then
        echo "⚠️  Skipping $skill_name: no rules/ directory found"
        return
    fi
    
    # Get all rule files, sorted alphabetically
    local rule_files=$(find "$rules_dir" -name "*.md" -type f | sort)
    
    if [ -z "$rule_files" ]; then
        echo "⚠️  Skipping $skill_name: no rule files found in rules/"
        return
    fi
    
    # Get skill title and description
    local skill_title=$(get_skill_title "$skill_dir")
    # Remove " skill" suffix if present for cleaner title
    skill_title=$(echo "$skill_title" | sed 's/ skill$//')
    local skill_description=$(get_skill_description "$skill_dir")
    
    # Start with the header
    {
        echo "# $skill_title"
        echo ""
        if [ -n "$skill_description" ]; then
            echo "$skill_description"
            echo ""
        fi
        echo "## How to use this skill"
        echo ""
        echo "When working with this skill, follow these guidelines:"
        echo ""
        echo "1. Review the relevant rule files for your specific use case"
        echo "2. Follow the guidelines and best practices outlined in each rule"
        echo "3. Reference the examples and templates provided"
        echo "4. Ensure compliance with any requirements mentioned"
        echo ""
        echo "---"
        echo ""
    } > "$output_file"
    
    # Process each rules file
    local file_count=0
    while IFS= read -r file; do
        if [ -f "$file" ]; then
            file_count=$((file_count + 1))
            echo "" >> "$output_file"
            echo "" >> "$output_file"
            # Remove frontmatter (lines between --- markers) and add content
            awk '/^---$/{if(++count==2)next} count<2{next} 1' "$file" >> "$output_file"
            echo "" >> "$output_file"
            echo "---" >> "$output_file"
        fi
    done <<< "$rule_files"
    
    if [ $file_count -gt 0 ]; then
        echo "✅ Built AGENTS.md for $skill_name ($file_count rule files)"
    else
        echo "⚠️  No rule files processed for $skill_name"
        rm -f "$output_file"
    fi
}

# Main execution
echo "Building AGENTS.md files for all skills..."
echo ""

# Find all skill directories
skill_dirs=$(find "$SKILLS_DIR" -mindepth 1 -maxdepth 1 -type d | sort)

if [ -z "$skill_dirs" ]; then
    echo "No skill directories found in $SKILLS_DIR"
    exit 1
fi

# Build AGENTS.md for each skill
skill_count=0
while IFS= read -r skill_dir; do
    build_skill_agent "$skill_dir"
    skill_count=$((skill_count + 1))
done <<< "$skill_dirs"

echo ""
echo "✅ Build complete! Processed $skill_count skill(s)"
