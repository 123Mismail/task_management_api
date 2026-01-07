# FastAPI Best Practices

## Application Structure

A well-structured FastAPI application should follow these patterns:

### Directory Structure
```
my-fastapi-app/
├── main.py              # Main application instance
├── requirements.txt     # Dependencies
├── alembic/             # Database migrations
├── app/
│   ├── __init__.py
│   ├── api/             # API routes
│   │   ├── __init__.py
│   │   └── v1/          # API version
│   │       ├── __init__.py
│   │       └── endpoints/
│   │           ├── __init__.py
│   │           └── users.py
│   ├── models/          # SQLAlchemy models
│   │   ├── __init__.py
│   │   └── user.py
│   ├── schemas/         # Pydantic models
│   │   ├── __init__.py
│   │   └── user.py
│   ├── database/        # Database configuration
│   │   ├── __init__.py
│   │   └── session.py
│   └── utils/           # Utility functions
│       ├── __init__.py
│       └── security.py
```

## FastAPI Specific Best Practices

### 1. Use Type Hints and Pydantic Models
```python
from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    email: str
    name: str
    age: Optional[int] = None

class UserResponse(BaseModel):
    id: int
    email: str
    name: str

    class Config:
        from_attributes = True
```

### 2. Dependency Injection
```python
from fastapi import Depends
from sqlalchemy.orm import Session

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    # Database logic here
    pass
```

### 3. Error Handling
```python
from fastapi import HTTPException

@app.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

### 4. Security
```python
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Token validation logic
    pass
```

## Performance Considerations

- Use async functions for I/O-bound operations
- Implement caching for frequently accessed data
- Use database connection pooling
- Optimize database queries with proper indexing
- Use pagination for large datasets

## Testing Best Practices

- Write unit tests for individual functions
- Write integration tests for API endpoints
- Use pytest with fixtures for database testing
- Test both positive and negative cases
- Mock external services during testing