# Detailed Claude Code Skill Development Guide

## Skill Naming Conventions

- Use lowercase letters only
- Use hyphens for word separation (no underscores or spaces)
- Keep names under 64 characters
- Use descriptive names that clearly indicate the skill's purpose
- Examples: `api-tester`, `code-reviewer`, `database-manager`

## YAML Frontmatter Fields

### Required Fields
- `name`: The skill identifier (lowercase, hyphens only)
- `description`: Explains what the skill does and when to use it

### Optional Fields
- `allowed-tools`: Specifies which tools Claude can use without asking
- `model`: Specific model to use when this skill is active
- `version`: Skill version (if tracking changes)

## Tool Permissions Best Practices

### Common Tool Combinations
```yaml
# Read-only operations
allowed-tools: Read, Grep, Glob

# File modification
allowed-tools: Read, Edit, Write, Grep

# System operations
allowed-tools: Bash, Read, Edit

# Full development workflow
allowed-tools: Read, Grep, Bash, Edit, Write
```

### Security Considerations
- Limit tool access to what's necessary for the skill
- Avoid granting unnecessary permissions
- Consider read-only access for documentation or review skills
- Be cautious with Bash access in shared environments

## Content Structure Best Practices

### Main Sections to Include
1. **Instructions**: Step-by-step guidance
2. **Examples**: Concrete usage examples
3. **Prerequisites**: Any requirements or setup needed
4. **Output Format**: What the skill should produce
5. **Error Handling**: How to handle common issues

### Writing Effective Instructions
- Use numbered lists for sequential steps
- Include conditional logic with "if/then" statements
- Be specific about expected inputs and outputs
- Include quality checks and validation steps

## Supporting Files Strategy

### When to Use Supporting Files
- Detailed reference documentation
- Code templates or snippets
- Configuration examples
- Complex examples that would clutter the main file

### File Organization
- Keep main SKILL.md under 500 lines
- Use descriptive names for supporting files
- Link to supporting files from the main skill
- Maintain clear file relationships

## Examples of Effective Skills

### Simple Skill Example
```yaml
---
name: hello-world
description: Create a simple hello world program. Use when user asks for a basic program example.
allowed-tools: Write
---
# Hello World Creator

## Instructions
1. Create a simple program that prints "Hello, World!"
2. Use the appropriate language based on context
3. Include basic comments explaining the code
```

### Complex Skill Example
```yaml
---
name: api-tester
description: Create comprehensive API tests for REST endpoints. Use when testing API functionality or creating test suites.
allowed-tools: Read, Write, Bash, Grep
---
# API Tester

## Instructions

1. **Analyze API documentation**: Review provided API endpoints and requirements
2. **Plan test coverage**: Identify endpoints, methods, and expected responses
3. **Create test structure**: Set up test directory and configuration
4. **Write test cases**: Implement tests for all endpoints and scenarios
5. **Add error handling**: Include tests for error conditions and edge cases
6. **Document tests**: Add comments explaining test purpose and expectations

## Test Categories to Include

### Positive Tests
- Valid requests with expected responses
- Different parameter combinations
- All supported HTTP methods

### Negative Tests
- Invalid inputs and error responses
- Missing required fields
- Authentication failures

### Edge Cases
- Boundary conditions
- Large inputs
- Special characters
```

## Testing Your Skills

### Before Sharing
- Test the skill with various inputs
- Verify all linked files exist and work
- Check that tool permissions are appropriate
- Ensure instructions are clear and complete

### Common Issues to Check
- Broken file links
- Incorrect tool permissions
- Unclear or incomplete instructions
- Missing required files

## Distribution Options

### Personal Skills
- Location: `~/.claude/skills/`
- Scope: Available across all projects for current user

### Project Skills
- Location: `.claude/skills/` in project root
- Scope: Shared with team via version control

### Enterprise Skills
- Managed through organization settings
- Available to all users in the organization

## Quality Assurance Checklist

- [ ] Skill name follows conventions
- [ ] Description is clear and includes trigger terms
- [ ] Tool permissions are appropriate
- [ ] Main file is under 500 lines
- [ ] Instructions are clear and sequential
- [ ] Examples are concrete and practical
- [ ] All linked files exist
- [ ] Skill addresses a specific, focused purpose