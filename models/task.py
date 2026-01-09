from sqlmodel import SQLModel, Field, Column
from typing import Optional
from datetime import datetime, timezone
from enum import Enum


class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    status: TaskStatus = Field(default=TaskStatus.PENDING)
    priority: TaskPriority = Field(default=TaskPriority.MEDIUM)
    due_date: Optional[datetime] = Field(default=None)


class Task(TaskBase, table=True):
    """Task database model"""
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", nullable=False)  # Associate task with user
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)


class TaskCreate(TaskBase):
    """Model for creating new tasks (excludes id, created_at)"""
    pass


class TaskUpdate(SQLModel):
    """Model for updating tasks (all fields optional)"""
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    status: Optional[TaskStatus] = Field(default=None)
    priority: Optional[TaskPriority] = Field(default=None)
    due_date: Optional[datetime] = Field(default=None)


class TaskResponse(TaskBase):
    """Model for API responses (includes id and timestamps)"""
    id: int
    user_id: int  # Include user_id in response
    created_at: datetime
    updated_at: datetime