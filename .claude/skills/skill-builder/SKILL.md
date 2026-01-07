---
name: skill-builder
description: Create new Claude Code skills following best practices. Use when user wants to create a new skill for Claude Code.
allowed-tools: Read, Grep, Bash, Edit, Write
---

# Skill Builder

## Instructions

Use this skill to create new Claude Code skills following established best practices.

1. **Determine skill purpose**: Understand what the new skill should accomplish
2. **Plan skill structure**: Create appropriate directory and file structure
3. **Write main skill file**: Create SKILL.md with proper YAML frontmatter
4. **Add supporting documentation**: Include additional files if needed
5. **Follow best practices**: Ensure proper naming, permissions, and content

## Skill Structure

Create the following directory structure for each new skill:
```
.claude/skills/skill-name/
├── SKILL.md              # Main skill file (required)
├── reference.md          # Detailed reference (optional)
├── examples.md           # Usage examples (optional)
└── scripts/              # Utility scripts (optional)
    └── helper-script.py
```

## SKILL.md Template

Each skill must have a SKILL.md file with this structure:

```yaml
---
name: skill-name
description: Brief description of what this Skill does and when to use it. Include trigger terms users would naturally say.
allowed-tools: Read, Grep, Bash, Edit, Write  # Adjust as needed
model: claude-sonnet-4-20250514  # Optional
---
# Skill Name

## Instructions
Provide clear, step-by-step guidance for Claude.

## Examples
Show concrete examples of using this Skill.

## Additional Resources
- [reference.md](reference.md) - Additional documentation
- [examples.md](examples.md) - Usage examples
```

## Best Practices to Follow

### 1. Clear Descriptions
- Include specific trigger terms users would naturally say
- Answer: "What does this Skill do?" and "When should Claude use it?"
- Example: "Extract text from PDF files. Use when working with PDFs or document extraction."

### 2. Progressive Disclosure
- Keep SKILL.md under 500 lines for optimal performance
- Put essential information in SKILL.md
- Place detailed reference material in separate files
- Use links to reference supporting files

### 3. Focused Purpose
- Keep each skill focused on a specific task or domain
- Use multiple specialized skills rather than one general-purpose skill
- Avoid overly broad skills that try to do everything

### 4. Tool Permissions
- Use `allowed-tools` to restrict which tools Claude can use
- Be mindful of security for sensitive operations
- Example: `allowed-tools: Read, Grep, Glob` for read-only skills

### 5. Step-by-Step Instructions
- Break down complex tasks into clear, sequential steps
- Use numbered lists for ordered processes
- Include conditional logic where appropriate
- Provide context for each step

## Implementation Steps

1. **Create the skill directory**: `.claude/skills/[skill-name]/`
2. **Write the main SKILL.md file**: With proper YAML frontmatter and content
3. **Add supporting files**: As needed for detailed documentation
4. **Include examples**: Concrete examples of the skill in action
5. **Test the skill**: Verify it works as expected

## Output Format

- Create proper directory structure
- Include main SKILL.md file with YAML frontmatter
- Add supporting documentation files if needed
- Ensure proper naming conventions (lowercase, hyphens)
- Include appropriate tool permissions
- Provide clear instructions and examples