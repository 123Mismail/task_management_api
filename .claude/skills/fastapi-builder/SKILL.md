---
name: fastapi-builder
description: Build FastAPI backend applications with proper structure, models, and documentation. Use when user asks to create a FastAPI application or backend API.
allowed-tools: Read, Grep, Bash, Edit, Write
---

# FastAPI Builder

## Instructions

Use this skill to create a complete FastAPI backend application with proper structure, models, schemas, routers, and documentation.

1. **Analyze requirements**: Understand what kind of API the user wants to build
2. **Create project structure**: Generate the standard FastAPI project layout
3. **Implement core components**: Create models, schemas, routers, and database connections
4. **Add documentation**: Include proper README and API documentation
5. **Configure dependencies**: Set up requirements.txt and pyproject.toml

## Project Structure

Create the following directory structure:
```
project-name/
├── main.py              # Main FastAPI application
├── requirements.txt     # Python dependencies
├── pyproject.toml      # Project configuration
├── .gitignore          # Git ignore file
├── README.md           # Project documentation
├── models/             # Database models
│   ├── __init__.py
│   └── user.py
├── schemas/            # Pydantic schemas
│   ├── __init__.py
│   └── user.py
├── routers/            # API route handlers
│   ├── __init__.py
│   └── users.py
├── database/           # Database configuration
│   ├── __init__.py
│   └── database.py
└── tests/              # Test files
    ├── __init__.py
    └── test_users.py
```

## Implementation Steps

1. **Create main.py** with FastAPI app, middleware, and basic endpoints
2. **Set up database models** using SQLAlchemy
3. **Define Pydantic schemas** for request/response validation
4. **Create API routers** for different resource types
5. **Add dependency injection** for database sessions
6. **Include security components** (authentication, authorization)
7. **Write comprehensive tests** using pytest
8. **Document the API** with examples

## Security Considerations

- Use proper authentication (OAuth2, JWT tokens)
- Validate all input with Pydantic models
- Implement rate limiting for public endpoints
- Use HTTPS in production
- Sanitize user inputs to prevent injection attacks

## Best Practices to Follow

- Use async/await for I/O-bound operations
- Implement proper error handling with custom exceptions
- Follow REST API conventions
- Use environment variables for configuration
- Include health check endpoints
- Add logging for debugging and monitoring
- Document all endpoints with FastAPI's automatic docs

## Output Format

- Provide a complete, runnable FastAPI application
- Include all necessary configuration files
- Add comprehensive README with setup instructions
- Ensure the application follows FastAPI best practices
- Include sample data and test endpoints