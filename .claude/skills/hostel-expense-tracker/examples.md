# Hostel Expense Tracker - Implementation Examples

## Example 1: Creating the Backend API with FastAPI

### Directory Structure
```
hostel_expense_tracker/
├── main.py
├── models/
│   ├── __init__.py
│   ├── user.py
│   ├── expense.py
│   └── category.py
├── schemas/
│   ├── __init__.py
│   ├── user.py
│   ├── expense.py
│   └── auth.py
├── database/
│   ├── __init__.py
│   └── database.py
├── routers/
│   ├── __init__.py
│   ├── auth.py
│   ├── users.py
│   └── expenses.py
├── utils/
│   ├── __init__.py
│   ├── auth.py
│   └── validators.py
└── requirements.txt
```

### Example Code: main.py
```python
from fastapi import FastAPI, Depends
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
```

### Example Code: models/expense.py
```python
from sqlmodel import SQLModel, Field, Column
from typing import Optional
from datetime import date, datetime
from enum import Enum

class ExpenseCategory(str, Enum):
    FOOD = "food"
    PERSONAL = "personal"
    TRANSPORT = "transport"
    ENTERTAINMENT = "entertainment"
    OTHER = "other"

class ExpenseBase(SQLModel):
    item_name: str = Field(min_length=1, max_length=255)
    price: float = Field(gt=0)
    date: date
    category: ExpenseCategory = Field(default=ExpenseCategory.OTHER)
    notes: Optional[str] = Field(default=None, max_length=1000)
    month_year: str = Field(max_length=7)  # Format: 'YYYY-MM'

class Expense(ExpenseBase, table=True):
    """Expense database model"""
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)

class ExpenseCreate(ExpenseBase):
    """Model for creating new expenses"""
    pass

class ExpenseUpdate(SQLModel):
    """Model for updating expenses (all fields optional)"""
    item_name: Optional[str] = Field(default=None, min_length=1, max_length=255)
    price: Optional[float] = Field(default=None, gt=0)
    date: Optional[date] = Field(default=None)
    category: Optional[ExpenseCategory] = Field(default=None)
    notes: Optional[str] = Field(default=None, max_length=1000)

class ExpenseResponse(ExpenseBase):
    """Model for API responses"""
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
```

### Example Code: routers/expenses.py
```python
from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlmodel import Session, select
from typing import List
from datetime import date, datetime
from database import get_session
from models import Expense, ExpenseCreate, ExpenseUpdate, ExpenseResponse
from utils.auth import get_current_user
from models.user import User

router = APIRouter(prefix="/expenses", tags=["expenses"])

@router.post("/", response_model=ExpenseResponse, status_code=status.HTTP_201_CREATED)
async def create_expense(
    expense: ExpenseCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
) -> ExpenseResponse:
    """Create a new expense entry"""
    # Verify the date is in the current month for residents
    if current_user.role == "resident":
        current_month = datetime.now().strftime("%Y-%m")
        if expense.month_year != current_month:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Residents can only add expenses for the current month"
            )

    db_expense = Expense(
        **expense.model_dump(),
        user_id=current_user.id
    )

    session.add(db_expense)
    session.commit()
    session.refresh(db_expense)

    return ExpenseResponse.model_validate(db_expense)

@router.get("/", response_model=List[ExpenseResponse])
async def get_expenses(
    current_user: User = Depends(get_current_user),
    month_year: str = Query(None, description="Filter by month (YYYY-MM)"),
    category: str = Query(None, description="Filter by category"),
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session)
) -> List[ExpenseResponse]:
    """Get expenses for current user with optional filters"""
    query = select(Expense).where(Expense.user_id == current_user.id)

    if month_year:
        query = query.where(Expense.month_year == month_year)
    if category:
        query = query.where(Expense.category == category)

    query = query.offset(skip).limit(limit).order_by(Expense.date.desc())
    expenses = session.exec(query).all()

    return [ExpenseResponse.model_validate(expense) for expense in expenses]

@router.get("/{expense_id}", response_model=ExpenseResponse)
async def get_expense(
    expense_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
) -> ExpenseResponse:
    """Get a specific expense by ID"""
    expense = session.get(Expense, expense_id)
    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found"
        )

    # Check if user owns the expense (or is manager)
    if expense.user_id != current_user.id and current_user.role != "manager":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this expense"
        )

    return ExpenseResponse.model_validate(expense)

@router.put("/{expense_id}", response_model=ExpenseResponse)
async def update_expense(
    expense_id: int,
    expense_update: ExpenseUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
) -> ExpenseResponse:
    """Update an expense entry"""
    expense = session.get(Expense, expense_id)
    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found"
        )

    # Check if user owns the expense (or is manager)
    if expense.user_id != current_user.id and current_user.role != "manager":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this expense"
        )

    # Update fields that are provided
    update_data = expense_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(expense, field, value)

    expense.updated_at = datetime.now(timezone.utc)
    session.add(expense)
    session.commit()
    session.refresh(expense)

    return ExpenseResponse.model_validate(expense)

@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_expense(
    expense_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Delete an expense entry"""
    expense = session.get(Expense, expense_id)
    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found"
        )

    # Check if user owns the expense (or is manager)
    if expense.user_id != current_user.id and current_user.role != "manager":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this expense"
        )

    session.delete(expense)
    session.commit()
```

## Example 2: Frontend Expense Entry Form

### React Component Example
```jsx
import React, { useState, useEffect } from 'react';

const ExpenseForm = ({ onSubmit, expense = null }) => {
  const [formData, setFormData] = useState({
    item_name: '',
    price: '',
    date: new Date().toISOString().split('T')[0],
    category: 'food',
    notes: ''
  });

  useEffect(() => {
    if (expense) {
      setFormData({
        item_name: expense.item_name,
        price: expense.price,
        date: expense.date,
        category: expense.category,
        notes: expense.notes || ''
      });
    }
  }, [expense]);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const monthYear = formData.date.substring(0, 7); // YYYY-MM format
    onSubmit({ ...formData, month_year: monthYear });
  };

  return (
    <form onSubmit={handleSubmit} className="expense-form">
      <div className="form-group">
        <label htmlFor="item_name">Item Name</label>
        <input
          type="text"
          id="item_name"
          name="item_name"
          value={formData.item_name}
          onChange={handleChange}
          required
        />
      </div>

      <div className="form-group">
        <label htmlFor="price">Price</label>
        <input
          type="number"
          id="price"
          name="price"
          step="0.01"
          value={formData.price}
          onChange={handleChange}
          required
        />
      </div>

      <div className="form-group">
        <label htmlFor="date">Date</label>
        <input
          type="date"
          id="date"
          name="date"
          value={formData.date}
          onChange={handleChange}
          required
        />
      </div>

      <div className="form-group">
        <label htmlFor="category">Category</label>
        <select
          id="category"
          name="category"
          value={formData.category}
          onChange={handleChange}
        >
          <option value="food">Food</option>
          <option value="personal">Personal</option>
          <option value="transport">Transport</option>
          <option value="entertainment">Entertainment</option>
          <option value="other">Other</option>
        </select>
      </div>

      <div className="form-group">
        <label htmlFor="notes">Notes</label>
        <textarea
          id="notes"
          name="notes"
          value={formData.notes}
          onChange={handleChange}
        />
      </div>

      <button type="submit">
        {expense ? 'Update Expense' : 'Add Expense'}
      </button>
    </form>
  );
};

export default ExpenseForm;
```

## Example 3: Monthly Summary Report

### Python function for generating monthly summary
```python
def generate_monthly_summary(user_id: int, month_year: str, session: Session):
    """Generate monthly expense summary for a user"""
    from sqlmodel import func

    # Get all expenses for the user in the specified month
    expenses = session.exec(
        select(Expense)
        .where(Expense.user_id == user_id)
        .where(Expense.month_year == month_year)
    ).all()

    # Calculate totals by category
    category_totals = {}
    total_amount = 0

    for expense in expenses:
        category = expense.category
        if category in category_totals:
            category_totals[category] += expense.price
        else:
            category_totals[category] = expense.price
        total_amount += expense.price

    # Create summary report
    summary = {
        "user_id": user_id,
        "month_year": month_year,
        "total_expenses": len(expenses),
        "total_amount": total_amount,
        "category_breakdown": category_totals,
        "daily_expenses": [
            {
                "date": expense.date,
                "item_name": expense.item_name,
                "price": expense.price,
                "category": expense.category
            }
            for expense in sorted(expenses, key=lambda x: x.date)
        ]
    }

    return summary
```

## Example 4: Data Export Functionality

### CSV Export Example
```python
import csv
from io import StringIO
from fastapi.responses import StreamingResponse

@router.get("/export/{month_year}")
async def export_expenses_csv(
    month_year: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Export expenses for the month as CSV"""
    # Get expenses for the month
    expenses = session.exec(
        select(Expense)
        .where(Expense.user_id == current_user.id)
        .where(Expense.month_year == month_year)
        .order_by(Expense.date.desc())
    ).all()

    # Create CSV content
    output = StringIO()
    writer = csv.writer(output)

    # Write header
    writer.writerow(["Date", "Item Name", "Price", "Category", "Notes", "Created At"])

    # Write data rows
    for expense in expenses:
        writer.writerow([
            expense.date,
            expense.item_name,
            expense.price,
            expense.category,
            expense.notes,
            expense.created_at
        ])

    # Create response
    output.seek(0)
    return StreamingResponse(
        StringIO(output.getvalue()),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=expenses_{month_year}.csv"}
    )
```