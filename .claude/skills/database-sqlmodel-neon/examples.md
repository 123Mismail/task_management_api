# SQLModel and Neon Database Integration Examples

## Example 1: Complete Project Setup

### User Request
"Set up complete database integration with SQLModel and Neon for my FastAPI project"

### Generated Files Structure
```
project/
├── config.py          # Configuration with environment variables
├── database.py        # Database engine and session management
├── models.py          # Database and API models
├── main.py            # FastAPI app with CRUD endpoints
└── pyproject.toml     # Dependencies
```

### Generated config.py
```python
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application configuration from environment variables."""

    POSTGRES_DATABASE_URL: str

    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    """Getting settings with caching to avoid multiple reads."""
    return Settings()
```

### Generated database.py
```python
from sqlmodel import SQLModel, create_engine, Session
from config import get_settings
import os

settings = get_settings()

# Enhanced engine configuration with connection pooling for Neon
engine = create_engine(
    settings.POSTGRES_DATABASE_URL,
    pool_size=20,
    max_overflow=30,
    pool_pre_ping=True,
    pool_recycle=3600,
    pool_timeout=30,
    echo=os.getenv("DATABASE_ECHO", "False").lower() == "true",
    connect_args={
        "application_name": "task-api",
        "sslmode": "require",  # Required for Neon
    }
)

def create_db_and_tables():
    """Create all tables in the database."""
    SQLModel.metadata.create_all(engine)

def get_session():
    """Dependency that provides database sessions."""
    with Session(engine) as session:
        yield session
```

### Generated models.py
```python
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class Task(SQLModel, table=True):
    """Task stored in database."""
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = None
    status: str = Field(default="pending")
    created_at: datetime = Field(default_factory=datetime.utcnow)


# API models for separation of concerns
class TaskBase(BaseModel):
    """Base task model for API operations."""
    title: str
    description: Optional[str] = None
    status: str = "pending"


class TaskCreate(TaskBase):
    """Model for creating new tasks (no id, no created_at)."""
    title: str
    description: Optional[str] = None
    status: str = "pending"


class TaskUpdate(BaseModel):
    """Model for updating tasks (all fields optional)."""
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None


class TaskResponse(TaskBase):
    """Model for task responses (includes id and created_at)."""
    id: int
    created_at: datetime
```

### Generated main.py with CRUD
```python
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select
from models import Task, TaskCreate, TaskUpdate, TaskResponse
from database import create_db_and_tables, get_session
from typing import List
from datetime import datetime, timedelta

app = FastAPI(title="Task API")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.post("/tasks", status_code=201, response_model=TaskResponse)
def create_task(task_create: TaskCreate, session: Session = Depends(get_session)):
    task = Task.model_validate(task_create)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

@app.get("/tasks", response_model=List[TaskResponse])
def list_tasks(session: Session = Depends(get_session)):
    tasks = session.exec(select(Task)).all()
    return tasks

@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    session: Session = Depends(get_session)
):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Update only the fields that are provided
    update_data = task_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if value is not None:
            setattr(task, field, value)

    session.add(task)
    session.commit()
    session.refresh(task)
    return task

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    session.delete(task)
    session.commit()

# Filtered endpoints
@app.get("/tasks/status/{status}", response_model=List[TaskResponse])
def get_tasks_by_status(status: str, session: Session = Depends(get_session)):
    statement = select(Task).where(Task.status == status)
    tasks = session.exec(statement).all()
    return tasks

@app.get("/tasks/recent", response_model=List[TaskResponse])
def get_recent_tasks(days: int = 7, session: Session = Depends(get_session)):
    date_limit = datetime.utcnow() - timedelta(days=days)
    statement = select(Task).where(Task.created_at >= date_limit)
    tasks = session.exec(statement).all()
    return tasks
```

## Example 2: Adding New Model

### User Request
"Add a User model with authentication fields to my SQLModel setup"

### Generated User Model
```python
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from pydantic import BaseModel
import bcrypt


class User(SQLModel, table=True):
    """User stored in database."""
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, min_length=3, max_length=50)
    email: str = Field(unique=True, max_length=100)
    hashed_password: str
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class UserBase(BaseModel):
    """Base user model for API operations."""
    username: str
    email: str


class UserCreate(UserBase):
    """Model for creating new users."""
    username: str
    email: str
    password: str  # Plain text password, will be hashed


class UserUpdate(BaseModel):
    """Model for updating users."""
    username: Optional[str] = None
    email: Optional[str] = None
    is_active: Optional[bool] = None


class UserResponse(UserBase):
    """Model for user responses."""
    id: int
    is_active: bool
    created_at: datetime
```

## Example 3: Connection Pooling Configuration

### User Request
"Optimize database connection pooling for high-concurrency applications"

### Generated Configuration
```python
# database.py - High concurrency configuration
from sqlmodel import SQLModel, create_engine, Session
from config import get_settings
import os

settings = get_settings()

# High-concurrency engine configuration for Neon
engine = create_engine(
    settings.POSTGRES_DATABASE_URL,
    pool_size=int(os.getenv("DB_POOL_SIZE", 50)),      # 50 connections in pool
    max_overflow=int(os.getenv("DB_MAX_OVERFLOW", 100)), # 100 overflow connections
    pool_pre_ping=True,                                 # Verify connections before use
    pool_recycle=3600,                                  # Recycle connections after 1 hour
    pool_timeout=30,                                    # Wait up to 30 seconds for connection
    echo=os.getenv("DATABASE_ECHO", "False").lower() == "true",  # Log SQL in development
    connect_args={
        "application_name": "high-traffic-app",         # Identify application in logs
        "options": "-c statement_timeout=30000",        # 30 second query timeout
    }
)
```

## Example 4: Advanced Filtering

### User Request
"Add complex filtering capabilities to my task API"

### Generated Filtering Endpoints
```python
# Additional endpoints in main.py
from typing import Optional

@app.get("/tasks/filter", response_model=List[TaskResponse])
def filter_tasks(
    status: Optional[str] = None,
    days: Optional[int] = None,
    title_contains: Optional[str] = None,
    session: Session = Depends(get_session)
):
    statement = select(Task)

    if status:
        statement = statement.where(Task.status == status)

    if days:
        date_limit = datetime.utcnow() - timedelta(days=days)
        statement = statement.where(Task.created_at >= date_limit)

    if title_contains:
        statement = statement.where(Task.title.contains(title_contains))

    filtered_tasks = session.exec(statement).all()
    return filtered_tasks

@app.get("/tasks/stats")
def get_task_stats(session: Session = Depends(get_session)):
    """Get task statistics."""
    total = session.exec(select(Task)).all()
    pending = session.exec(select(Task).where(Task.status == "pending")).all()
    completed = session.exec(select(Task).where(Task.status == "completed")).all()

    return {
        "total": len(total),
        "pending": len(pending),
        "completed": len(completed)
    }
```