# Skill Builder Examples

## Example 1: Creating a Database Migration Skill

### User Request
"Create a skill for database migrations using Alembic"

### Generated Skill Structure
```
.claude/skills/db-migrator/
├── SKILL.md
├── alembic-templates.md
└── migration-checklist.md
```

### Generated SKILL.md
```yaml
---
name: db-migrator
description: Create and manage database migrations using Alembic. Use when working with database schema changes, migrations, or versioning.
allowed-tools: Read, Bash, Edit, Write
---
# Database Migrator

## Instructions

1. **Analyze schema changes**: Review the requested database changes
2. **Generate migration files**: Create Alembic migration files with proper up/downgrades
3. **Validate migrations**: Check for potential conflicts or issues
4. **Test migrations**: Verify migration works in safe environment
5. **Document changes**: Add notes about the migration purpose

## Examples

### New Table Migration
- Generate migration to create new table
- Include proper indexes and constraints
- Add downgrades to reverse the change

### Column Modification
- Handle data type changes carefully
- Consider data migration needs
- Plan for application compatibility

## Additional Resources
- [alembic-templates.md](alembic-templates.md) - Migration file templates
- [migration-checklist.md](migration-checklist.md) - Pre-deployment checklist
```

## Example 2: Creating a Security Review Skill

### User Request
"Create a skill for security code review"

### Generated Skill Structure
```
.claude/skills/security-review/
├── SKILL.md
├── security-checklist.md
└── vulnerability-templates.md
```

### Generated SKILL.md
```yaml
---
name: security-review
description: Perform security review of code changes. Use when reviewing code for vulnerabilities, security issues, or when user asks for security analysis.
allowed-tools: Read, Grep, Bash
---
# Security Code Review

## Instructions

1. **Input validation review**: Check for proper validation and sanitization
2. **Authentication/authorization**: Verify proper access controls
3. **Data protection**: Check for encryption and secure handling
4. **Dependency security**: Scan for vulnerable packages
5. **Logging and monitoring**: Ensure proper security logging
6. **Report findings**: Provide structured security assessment

## Security Focus Areas
- SQL injection prevention
- Cross-site scripting (XSS) protection
- Cross-site request forgery (CSRF) protection
- Secure authentication flows
- Proper error handling

## Output Format
- List critical vulnerabilities first
- Provide specific code locations
- Suggest remediation steps
- Rate severity levels (Critical/High/Medium/Low)

## Additional Resources
- [security-checklist.md](security-checklist.md) - Comprehensive security checklist
- [vulnerability-templates.md](vulnerability-templates.md) - Standard vulnerability descriptions
```

## Example 3: Creating a CI/CD Configuration Skill

### User Request
"Create a skill for generating CI/CD pipelines"

### Generated Skill Structure
```
.claude/skills/ci-cd-generator/
├── SKILL.md
├── pipeline-templates.md
└── best-practices.md
```

### Generated SKILL.md
```yaml
---
name: ci-cd-generator
description: Generate CI/CD pipeline configurations for various platforms. Use when setting up CI/CD, deployment pipelines, or when user asks for pipeline configuration.
allowed-tools: Write, Read, Edit
---
# CI/CD Pipeline Generator

## Instructions

1. **Identify platform**: Determine target CI/CD platform (GitHub Actions, GitLab CI, Jenkins, etc.)
2. **Analyze requirements**: Understand build, test, and deployment needs
3. **Generate configuration**: Create appropriate pipeline file
4. **Add security**: Include secure credential handling
5. **Set up testing**: Include automated testing stages
6. **Configure deployment**: Add deployment steps and checks

## Pipeline Components to Include

### Build Stage
- Dependency installation
- Code compilation or packaging
- Build artifact creation

### Test Stage
- Unit tests
- Integration tests
- Security scans
- Code quality checks

### Deploy Stage
- Environment-specific configurations
- Deployment validation
- Rollback procedures

## Additional Resources
- [pipeline-templates.md](pipeline-templates.md) - Ready-made pipeline templates
- [best-practices.md](best-practices.md) - CI/CD best practices and patterns
```

## Usage Pattern

When creating a new skill, follow this pattern:

1. **Understand the domain**: What specific task or domain should the skill address?
2. **Plan the scope**: What will the skill do and what will it not do?
3. **Choose the name**: Use appropriate naming conventions
4. **Select tool permissions**: Grant only necessary access
5. **Design the structure**: Plan main file and supporting documentation
6. **Write the content**: Follow best practices for clarity and completeness
7. **Test the skill**: Verify it works as expected

The skill-builder ensures each new skill follows consistent patterns and best practices.