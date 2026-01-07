#!/bin/bash

# Script to help create a new Claude Code skill
# Usage: ./create-skill.sh <skill-name>

if [ $# -eq 0 ]; then
    echo "Usage: $0 <skill-name>"
    echo "Example: $0 api-tester"
    exit 1
fi

SKILL_NAME=$1
SKILL_DIR="../../../.claude/skills/$SKILL_NAME"

# Validate skill name format
if [[ ! "$SKILL_NAME" =~ ^[a-z][a-z0-9-]*[a-z0-9]$ ]]; then
    echo "Error: Skill name must be lowercase with hyphens only, starting and ending with alphanumeric characters"
    exit 1
fi

# Create skill directory
mkdir -p "$SKILL_DIR"

# Create basic SKILL.md template
cat > "$SKILL_DIR/SKILL.md" << EOF
---
name: $SKILL_NAME
description: Description of what this skill does. Use when [when to use this skill].
allowed-tools: Read, Grep, Bash, Edit, Write
---
# $SKILL_NAME

## Instructions

1. **Step 1**: [First step in the process]
2. **Step 2**: [Second step in the process]
3. **Step 3**: [Third step in the process]

## Examples

### Example 1: [Common use case]
- [What to do]
- [What to expect]

### Example 2: [Another use case]
- [What to do]
- [What to expect]
EOF

echo "Skill directory created: $SKILL_DIR"
echo "SKILL.md template created with basic structure"
echo "You can now customize the skill content as needed"