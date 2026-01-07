#!/usr/bin/env python3
"""
Script to initialize a new Hostel Expense Tracker project
"""

import os
import sys
from pathlib import Path

def create_directory_structure(base_path):
    """Create the project directory structure"""
    directories = [
        "models",
        "schemas",
        "database",
        "routers",
        "utils",
        "tests"
    ]

    for directory in directories:
        dir_path = Path(base_path) / directory
        dir_path.mkdir(exist_ok=True)
        # Create __init__.py files
        (dir_path / "__init__.py").touch(exist_ok=True)

def create_requirements_file(base_path):
    """Create requirements.txt file"""
    requirements_content = """fastapi>=0.104.1
sqlmodel>=0.0.31
uvicorn>=0.24.0
python-jose[cryptography]>=3.3.0
passlib[bcrypt]>=1.7.4
python-multipart>=0.0.6
psycopg2-binary>=2.9.9
pydantic>=2.5.0
pydantic-settings>=2.1.0
pytest>=7.4.0
httpx>=0.25.0
"""

    req_file = Path(base_path) / "requirements.txt"
    req_file.write_text(requirements_content)

def create_main_file(base_path):
    """Create main.py file"""
    main_content = '''from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from database import create_db_and_tables
from routers import auth, users, expenses

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create database tables on startup
    create_db_and_tables()
    yield
    # Cleanup on shutdown if needed

app = FastAPI(
    title="Hostel Expense Tracker",
    description="Expense tracking system for hostel managers",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, change this to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(expenses.router, prefix="/expenses", tags=["expenses"])

@app.get("/")
def read_root():
    return {"message": "Hostel Expense Tracker API", "status": "running"}

@app.get("/health")
def health_check():
    from datetime import datetime, timezone
    return {"status": "healthy", "timestamp": datetime.now(timezone.utc)}
'''

    main_file = Path(base_path) / "main.py"
    main_file.write_text(main_content)

def create_env_file(base_path):
    """Create .env file with environment variables"""
    env_content = """# Database Configuration
DATABASE_URL=postgresql://user:password@localhost/hostel_expenses

# JWT Configuration
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application Configuration
DEBUG=True
"""

    env_file = Path(base_path) / ".env"
    env_file.write_text(env_content)

def main():
    if len(sys.argv) != 2:
        print("Usage: python init_project.py <project_path>")
        sys.exit(1)

    project_path = sys.argv[1]
    project_dir = Path(project_path)

    # Create the main project directory if it doesn't exist
    project_dir.mkdir(parents=True, exist_ok=True)

    print(f"Initializing Hostel Expense Tracker project at: {project_dir}")

    # Create directory structure
    create_directory_structure(project_dir)

    # Create project files
    create_requirements_file(project_dir)
    create_main_file(project_dir)
    create_env_file(project_dir)

    # Create placeholder files for key modules
    models_dir = project_dir / "models"
    (models_dir / "user.py").write_text("# User model will be defined here\n")
    (models_dir / "expense.py").write_text("# Expense model will be defined here\n")

    schemas_dir = project_dir / "schemas"
    (schemas_dir / "user.py").write_text("# User schemas will be defined here\n")
    (schemas_dir / "expense.py").write_text("# Expense schemas will be defined here\n")

    database_dir = project_dir / "database"
    (database_dir / "database.py").write_text("# Database configuration will be defined here\n")

    routers_dir = project_dir / "routers"
    (routers_dir / "auth.py").write_text("# Authentication router will be defined here\n")
    (routers_dir / "users.py").write_text("# Users router will be defined here\n")
    (routers_dir / "expenses.py").write_text("# Expenses router will be defined here\n")

    utils_dir = project_dir / "utils"
    (utils_dir / "auth.py").write_text("# Authentication utilities will be defined here\n")
    (utils_dir / "validators.py").write_text("# Validation utilities will be defined here\n")

    tests_dir = project_dir / "tests"
    (tests_dir / "conftest.py").write_text("# Test configuration will be defined here\n")

    print(f"Project initialized successfully at: {project_dir}")
    print("\nNext steps:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Set up your database and update DATABASE_URL in .env")
    print("3. Start the development server: uvicorn main:app --reload")
    print("4. Begin implementing the models and routes")

if __name__ == "__main__":
    main()