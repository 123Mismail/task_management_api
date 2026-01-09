from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from sqlmodel import SQLModel
from database import create_db_and_tables
from models import user  # Import user model to register it with SQLModel metadata
import routers.task
import routers.user
import routers.auth
from routers.task import router as task_router
from routers.user import router as user_router
from routers.auth import router as auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create database tables on startup
    create_db_and_tables()
    yield
    # Cleanup on shutdown if needed


app = FastAPI(
    title="Task Management API",
    description="A complete task management system with CRUD operations and authentication",
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
app.include_router(task_router)
app.include_router(user_router)
app.include_router(auth_router)


@app.get("/")
def read_root():
    return {"message": "Task Management API", "status": "running"}


@app.get("/health")
def health_check():
    from datetime import datetime, timezone
    return {"status": "healthy", "timestamp": datetime.now(timezone.utc)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)