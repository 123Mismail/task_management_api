---
name: fastapi-crud
description: Create FastAPI CRUD operations with in-memory storage. Use when user asks to create CRUD functionality, REST API endpoints, or basic API operations.
allowed-tools: Read, Grep, Bash, Edit, Write
---
# FastAPI CRUD Operations

## Instructions

Use this skill to create complete FastAPI CRUD (Create, Read, Update, Delete) operations with in-memory storage.

1. **Analyze requirements**: Understand the entity/resource for CRUD operations
2. **Create data model**: Define Pydantic models for the entity
3. **Set up in-memory storage**: Create data structures to store items
4. **Create API endpoints**: Implement GET, POST, PUT, PATCH, DELETE endpoints
5. **Implement CRUD logic**: Add functions for each CRUD operation
6. **Include proper error handling**: Handle not found and validation errors
7. **Add dependency injection**: Use Depends() for configuration, database connections, etc.
8. **Add documentation**: Include proper API documentation and examples

## Implementation Steps

### 1. Define Pydantic Models
- Create `EntityCreate` model for POST requests (without ID)
- Create `EntityUpdate` model for PUT/PATCH requests (optional fields)
- Create `EntityResponse` model for responses (with ID and all fields)

### 2. Set Up In-Memory Storage
- Create a dictionary or list for storage
- Initialize with sample data if needed
- Implement thread-safe operations if needed

### 3. Create API Endpoints
- `GET /entities/` - List all entities
- `GET /entities/{id}` - Get specific entity by ID
- `POST /entities/` - Create new entity
- `PUT /entities/{id}` - Full update of existing entity
- `PATCH /entities/{id}` - Partial update of existing entity
- `DELETE /entities/{id}` - Delete entity by ID

### 4. Implement CRUD Functions
- Create functions for each CRUD operation
- Include proper validation and error handling
- Return appropriate data structures

### 5. Include Error Handling
- Handle `404 Not Found` for missing resources
- Handle validation errors with 422 status
- Return appropriate error responses

### 6. Add Dependency Injection Patterns
- Use `Depends()` for configuration, database connections, authentication
- Chain dependencies when needed (e.g., logger depends on config)
- Use `yield` for cleanup operations in dependencies
- Implement caching with `@lru_cache` for expensive operations

## Dependency Injection Patterns

### Basic Dependency
```python
def get_config():
    return {"app_name": "MyApp", "debug": True}

@app.get("/info")
def app_info(config: dict = Depends(get_config)):
    return config
```

### Chained Dependencies
```python
def get_config():
    return {"app_name": "MyApp", "log_level": "INFO"}

def get_logger(config: dict = Depends(get_config)):
    logger = logging.getLogger(config["app_name"])
    logger.setLevel(config["log_level"])
    return logger

@app.get("/log-test")
def log_test_endpoint(logger: logging.Logger = Depends(get_logger)):
    logger.info("Test log message")
    return {"message": "Logged successfully"}
```

### Dependency with Cleanup (using yield)
```python
def get_db_connection():
    db = create_connection()
    try:
        yield db
    finally:
        db.close()

@app.get("/data")
def get_data(db: Connection = Depends(get_db_connection)):
    return db.query("SELECT * FROM table")
```

### Caching Dependencies
```python
from functools import lru_cache

@lru_cache
def get_cached_config():
    # Expensive operation that loads config from file
    return load_config_from_file()

@app.get("/settings")
def get_settings(config: dict = Depends(get_cached_config)):
    return config
```

## Best Practices to Follow

- Use async functions for endpoints
- Use Pydantic for request/response validation
- Follow REST API conventions
- Include proper status codes (200, 201, 204, 404, 422, etc.)
- Add proper documentation with FastAPI's automatic docs
- Use descriptive endpoint names
- Include proper type hints
- Implement dependency injection for configuration and services
- Use `@lru_cache` for expensive operations that don't change frequently
- Use `yield` in dependencies for proper resource cleanup
- Chain dependencies when one depends on another (e.g., logger needs config)

## Output Format

- Create complete CRUD functionality for the specified entity
- Include Pydantic models for validation
- Implement all 6 CRUD endpoints (GET, POST, PUT, PATCH, DELETE)
- Include dependency injection patterns where appropriate
- Include proper error handling and status codes
- Add comprehensive documentation
- Include sample usage examples with dependency patterns