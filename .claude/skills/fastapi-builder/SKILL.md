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
- Use secure password hashing with pwdlib/Argon2
- Validate password strength (min 8 chars, 1 upper, 1 lower, 1 number)
- Use EmailStr validator for email fields to ensure proper format
- Implement secure password reset flow with time-limited tokens
- Prevent user enumeration in authentication and password reset flows

## Best Practices to Follow

- Use async/await for I/O-bound operations
- Implement proper error handling with custom exceptions
- Follow REST API conventions
- Use environment variables for configuration
- Include health check endpoints
- Add logging for debugging and monitoring
- Document all endpoints with FastAPI's automatic docs
- For user management:
  - Use separate models for request (with password) and response (without password exposure)
  - Implement password validation in Pydantic models using @field_validator
  - Use EmailStr for email validation, with additional checks if needed for disposable domains
  - Store hashed_password in the database, never plain text passwords
  - Include signup endpoint with duplicate email prevention (return 409 Conflict for duplicates)
  - Implement secure password reset flow with time-limited tokens

## User Management Implementation

### Password Validation Approaches
- **Pydantic Model Validation**: Use `@field_validator` for early validation at API boundary
  - Pros: Early validation, automatic error handling, type safety
  - Cons: Mixing validation with data models, less reusability

- **Security Module Validation**: Separate validation functions for better separation of concerns
  - Pros: Separation of concerns, reusability, centralized policy management
  - Cons: Later validation in process, manual error handling required

### Email Validation with Pydantic EmailStr
- Use `EmailStr` from Pydantic for RFC-compliant email validation
- Automatically rejects invalid formats like "not-an-email", "@", "test@"
- Validates proper email structure (local-part@domain)
- Sufficient for most user registration scenarios
- For advanced validation, add custom `@field_validator` for domain restrictions

### Password Reset Flow
1. **Forgot Password Endpoint**: `POST /users/forgot-password` - Accept email, generate secure token, send notification
2. **Reset Password Endpoint**: `POST /users/reset-password` - Validate token, verify new password, update securely
3. **Token Generation**: Use cryptographically secure random tokens (secrets module), typically 1-hour validity
4. **Token Cleanup**: Invalidate tokens immediately after use, implement automatic cleanup for expired tokens

### User Model Examples
```python
from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import datetime
import re

class UserBase(BaseModel):
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

    @field_validator('password')
    def validate_password_strength(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')

        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')

        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')

        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one number')

        return v

    @field_validator('email')
    def validate_email_format(cls, v):
        # EmailStr already validates basic format
        # Additional custom email validation can go here if needed
        return v

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None

class UserResponse(UserBase):
    id: int
    created_at: datetime
    # Note: Never include password fields in response models for security

class UserInDB(UserBase):
    id: int
    hashed_password: str
    created_at: datetime
```

### Password Reset Implementation
```python
from typing import Dict
import secrets
import string
from datetime import datetime, timedelta
from pwdlib import PasswordHasher
from fastapi import HTTPException, Depends

# Models for password reset
class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str

    @field_validator('new_password')
    def validate_new_password(cls, v):
        # Reuse the same password validation from signup
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')

        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')

        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')

        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one number')

        return v

# Password hasher dependency
def get_password_hasher():
    # Configure pwdlib with Argon2 algorithm for secure password hashing
    return PasswordHasher(
        time_cost=3,
        memory_cost=65536,
        parallelism=1,
        hash_len=32,
        salt_len=16,
        type="argon2"
    )

def hash_password(plain_password: str, ph: PasswordHasher = Depends(get_password_hasher)):
    return ph.hash(plain_password)

# In-memory storage for reset tokens (use database in production)
reset_tokens: Dict[str, Dict] = {}

def generate_reset_token(length: int = 32) -> tuple[str, datetime]:
    """Generate a cryptographically secure random token."""
    alphabet = string.ascii_letters + string.digits
    token = ''.join(secrets.choice(alphabet) for _ in range(length))
    expires_at = datetime.utcnow() + timedelta(hours=1)  # 1 hour validity
    return token, expires_at

def is_token_valid(expires_at: datetime) -> bool:
    """Check if reset token is still valid."""
    return datetime.utcnow() < expires_at

@app.post("/users/forgot-password")
async def forgot_password(request: ForgotPasswordRequest):
    # Check if user exists (but don't reveal in response)
    user_id = None
    for uid, user in users_db.items():
        if user.email == request.email:
            user_id = uid
            break

    # Generate and store reset token
    if user_id is not None:  # Only create token if user exists
        token, expires_at = generate_reset_token()
        reset_tokens[token] = {
            'user_id': user_id,
            'expires_at': expires_at,
            'created_at': datetime.utcnow()
        }

    # Always return the same response to prevent user enumeration
    return {"message": "If your email exists in our system, you will receive a password reset link"}

@app.post("/users/reset-password")
async def reset_password(
    request: ResetPasswordRequest,
    ph: PasswordHasher = Depends(get_password_hasher)
):
    # Verify token exists and is valid
    reset_record = reset_tokens.get(request.token)
    if not reset_record:
        raise HTTPException(status_code=400, detail="Invalid token")

    if not is_token_valid(reset_record['expires_at']):
        # Clean up expired token
        del reset_tokens[request.token]
        raise HTTPException(status_code=400, detail="Token has expired")

    # Hash the new password
    hashed_password = hash_password(request.new_password, ph)

    # Update user's password
    user = users_db[reset_record['user_id']]
    user.hashed_password = hashed_password  # Direct update in our in-memory store

    # Immediately invalidate the used token
    del reset_tokens[request.token]

    # Optional: Clear user sessions here for security

    return {"message": "Password has been reset successfully"}
```

## Output Format

- Provide a complete, runnable FastAPI application
- Include all necessary configuration files
- Add comprehensive README with setup instructions
- Ensure the application follows FastAPI best practices
- Include sample data and test endpoints