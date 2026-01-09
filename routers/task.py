from fastapi import APIRouter, HTTPException, Depends, status
from sqlmodel import Session, select
from typing import List
from datetime import datetime, timezone
from database import get_session
from models import Task, TaskCreate, TaskUpdate, TaskResponse
from auth.dependencies import get_current_user
from schemas.user import UserResponse

router = APIRouter(prefix="/tasks", tags=["tasks"])

class TaskStatus:
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class TaskPriority:
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    
@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task: TaskCreate,
    current_user: UserResponse = Depends(get_current_user),
    session: Session = Depends(get_session)
) -> TaskResponse:
    """Create a new task"""
    # Create task instance manually to avoid conflicts with default_factory fields
    utc_now = datetime.now(timezone.utc)
    db_task = Task(
        title=task.title,
        description=task.description,
        status=task.status if task.status else TaskStatus.PENDING,
        priority=task.priority if task.priority else TaskPriority.MEDIUM,
        due_date=task.due_date,
        user_id=current_user.id,  # Associate task with the authenticated user
        created_at=utc_now,
        updated_at=utc_now
    )

    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    return TaskResponse.model_validate(db_task)


@router.get("/", response_model=List[TaskResponse])
async def get_tasks(
    current_user: UserResponse = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session)
) -> List[TaskResponse]:
    """Get a list of tasks for the authenticated user with pagination"""
    statement = select(Task).where(Task.user_id == current_user.id).offset(skip).limit(limit)
    tasks = session.exec(statement).all()

    return [TaskResponse.model_validate(task) for task in tasks]


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    current_user: UserResponse = Depends(get_current_user),
    session: Session = Depends(get_session)
) -> TaskResponse:
    """Get a specific task by ID"""
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )

    # Check if the task belongs to the current user
    if task.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this task"
        )

    return TaskResponse.model_validate(task)


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_update: TaskUpdate,
    current_user: UserResponse = Depends(get_current_user),
    session: Session = Depends(get_session)
) -> TaskResponse:
    """Update a task completely"""
    db_task = session.get(Task, task_id)
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )

    # Check if the task belongs to the current user
    if db_task.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this task"
        )

    # Update fields that are provided
    update_data = task_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_task, field, value)

    db_task.updated_at = datetime.now(timezone.utc)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    return TaskResponse.model_validate(db_task)


@router.patch("/{task_id}", response_model=TaskResponse)
async def partial_update_task(
    task_id: int,
    task_update: TaskUpdate,
    current_user: UserResponse = Depends(get_current_user),
    session: Session = Depends(get_session)
) -> TaskResponse:
    """Partially update a task"""
    db_task = session.get(Task, task_id)
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )

    # Check if the task belongs to the current user
    if db_task.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this task"
        )

    # Update only the fields that are provided
    update_data = task_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_task, field, value)

    db_task.updated_at = datetime.now(timezone.utc)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    return TaskResponse.model_validate(db_task)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    current_user: UserResponse = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Delete a task by ID"""
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )

    # Check if the task belongs to the current user
    if task.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this task"
        )

    session.delete(task)
    session.commit()

    return {"message": "Task deleted successfully"}