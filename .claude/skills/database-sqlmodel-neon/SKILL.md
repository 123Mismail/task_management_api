---
name: database-sqlmodel-neon
description: Set up database integration with SQLModel and Neon PostgreSQL. Use when setting up database models, engine configuration, session management, and CRUD operations with SQLModel and Neon.
allowed-tools: Read, Edit, Write, Bash
---

# SQLModel and Neon Database Integration

## Instructions

1. **Analyze project structure**: Review existing project files and identify where database integration is needed
2. **Create configuration**: Set up database configuration with proper environment variable handling
3. **Configure SQLModel engine**: Create engine with connection pooling optimized for Neon
4. **Design models**: Create database models with proper validation and API separation
5. **Implement session management**: Set up dependency injection for database sessions
6. **Create CRUD operations**: Implement comprehensive Create, Read, Update, Delete operations
7. **Add filtering capabilities**: Include examples of common filtering operations
8. **Configure connection pooling**: Optimize for high-concurrency applications

## Configuration Setup

### 1. Create config.py for environment management
- Use Pydantic Settings with caching
- Define POSTGRES_DATABASE_URL environment variable
- Include proper error handling

### 2. Create database.py for connection management
- Configure engine with appropriate connection pooling settings
- Set up session dependency for FastAPI
- Include table creation function

### 3. Create models.py with proper separation
- Define database model with table=True
- Create separate API models for request/response
- Include proper validation constraints

### 4. Update main.py with CRUD endpoints
- Implement POST endpoint for creating records
- Create GET endpoints for reading records
- Add PUT endpoint for updating records
- Include DELETE endpoint for removing records
- Add filtered endpoints for common queries

## Connection Pooling Configuration

Use these optimal settings for Neon PostgreSQL:
- pool_size: 20 (connections maintained in pool)
- max_overflow: 30 (additional overflow connections)
- pool_pre_ping: True (verify connections before use)
- pool_recycle: 3600 (recycle connections after 1 hour)
- pool_timeout: 30 (wait time for connections)

## API Model Separation

Create separate models for different purposes:
- TaskCreate: For creating new records (excludes id, created_at)
- TaskUpdate: For updating records (all fields optional)
- TaskResponse: For API responses (includes all fields)
- Task (database model): For database operations

## Common Filtering Examples

Include these filtering patterns:
- Status-based filtering: `WHERE status = 'value'`
- Date range filtering: `WHERE created_at >= date`
- Combined filters: Multiple WHERE conditions
- IN clause filtering: `WHERE status IN ['value1', 'value2']`

## Security Considerations

- Never expose sensitive database fields in API responses
- Use proper validation on input models
- Implement proper error handling
- Use environment variables for database credentials
- Enable SSL connections for Neon

## Output Format

The skill should produce:
1. Complete database configuration files
2. Properly structured models with API separation
3. Working CRUD endpoints
4. Connection pooling optimized for production
5. Comprehensive filtering examples
6. Environment configuration recommendations

## Additional Resources
- [examples.md](examples.md) - Complete implementation examples
- [best-practices.md](best-practices.md) - Database integration best practices