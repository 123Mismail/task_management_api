from sqlmodel import SQLModel, Field
from sqlalchemy.sql import func
from typing import Optional
from datetime import datetime
import re


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True, nullable=False)
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    hashed_password: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)