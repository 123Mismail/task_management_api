from fastapi import APIRouter, HTTPException, Depends, status
from sqlmodel import Session, select
from typing import List
from datetime import datetime, timezone
from database import get_session
from models import Task, TaskCreate, TaskUpdate, TaskResponse

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(task: TaskCreate, session: Session = Depends(get_session)) -> TaskResponse:
    """Create a new task"""
    # Create task instance manually to avoid conflicts with default_factory fields
    utc_now = datetime.now(timezone.utc)
    db_task = Task(
        title=task.title,
        description=task.description,
        status=task.status if task.status else TaskStatus.PENDING,
        priority=task.priority if task.priority else TaskPriority.MEDIUM,
        due_date=task.due_date,
        created_at=utc_now,
        updated_at=utc_now
    )

    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    return TaskResponse.model_validate(db_task)


@router.get("/", response_model=List[TaskResponse])
async def get_tasks(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session)
) -> List[TaskResponse]:
    """Get a list of tasks with pagination"""
    statement = select(Task).offset(skip).limit(limit)
    tasks = session.exec(statement).all()

    return [TaskResponse.model_validate(task) for task in tasks]


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task_id: int, session: Session = Depends(get_session)) -> TaskResponse:
    """Get a specific task by ID"""
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )

    return TaskResponse.model_validate(task)


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_update: TaskUpdate,
    session: Session = Depends(get_session)
) -> TaskResponse:
    """Update a task completely"""
    db_task = session.get(Task, task_id)
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
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
    session: Session = Depends(get_session)
) -> TaskResponse:
    """Partially update a task"""
    db_task = session.get(Task, task_id)
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
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
async def delete_task(task_id: int, session: Session = Depends(get_session)):
    """Delete a task by ID"""
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )

    session.delete(task)
    session.commit()

    return {"message": "Task deleted successfully"}