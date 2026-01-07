# Hostel Expense Tracker - Technical Reference

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'resident', -- 'resident' or 'manager'
    room_number VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Expenses Table
```sql
CREATE TABLE expenses (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    item_name VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    date DATE NOT NULL,
    category VARCHAR(100),
    month_year VARCHAR(7) NOT NULL, -- Format: 'YYYY-MM'
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Categories Table
```sql
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE, -- NULL for system categories
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Monthly Summaries Table
```sql
CREATE TABLE monthly_summaries (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    month_year VARCHAR(7) NOT NULL, -- Format: 'YYYY-MM'
    total_amount DECIMAL(10, 2) NOT NULL,
    expense_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - User login
- `POST /auth/logout` - User logout
- `GET /auth/me` - Get current user info

### Users
- `GET /users` - Get all users (manager only)
- `GET /users/{id}` - Get specific user
- `PUT /users/{id}` - Update user info
- `DELETE /users/{id}` - Delete user (manager only)

### Expenses
- `GET /expenses` - Get current user's expenses (with filters)
- `GET /expenses/{id}` - Get specific expense
- `POST /expenses` - Create new expense
- `PUT /expenses/{id}` - Update expense
- `DELETE /expenses/{id}` - Delete expense

### Monthly Operations
- `GET /expenses/monthly/{month_year}` - Get expenses for specific month
- `GET /expenses/monthly/{month_year}/summary` - Get monthly summary
- `GET /expenses/users/{user_id}/monthly/{month_year}` - Get specific user's expenses for month

### Reports
- `GET /reports/monthly/{month_year}` - Get all users' expenses for month
- `GET /reports/user/{user_id}/monthly/{month_year}` - Get specific user's report
- `GET /reports/summary/{month_year}` - Get summary report for month

## Frontend Components

### Authentication Components
- Login Form
- Registration Form
- Password Reset
- User Profile Page

### Expense Components
- Expense Entry Form
- Expense List View
- Expense Detail View
- Expense Edit Form
- Monthly Notebook View

### Reporting Components
- Monthly Summary Dashboard
- Individual Expense Reports
- Expense Trends Chart
- Export Options

## Data Models

### User Model
```python
class User:
    id: int
    name: str
    email: str
    role: str  # 'resident' or 'manager'
    room_number: str
    created_at: datetime
    updated_at: datetime
```

### Expense Model
```python
class Expense:
    id: int
    user_id: int
    item_name: str
    price: float
    date: date
    category: str
    month_year: str  # 'YYYY-MM'
    notes: str
    created_at: datetime
    updated_at: datetime
```

### MonthlySummary Model
```python
class MonthlySummary:
    id: int
    user_id: int
    month_year: str  # 'YYYY-MM'
    total_amount: float
    expense_count: int
    created_at: datetime
```

## Business Logic

### Monthly Notebook Management
1. System automatically creates new notebook at the beginning of each month
2. Previous month's data remains accessible but is not editable
3. Users can only add expenses to the current month
4. At month-end, system calculates totals and generates summary

### Expense Validation
1. Price must be a positive number
2. Date must be within the current month
3. Item name cannot be empty
4. Category must be from predefined list or user-created

### Role-Based Access
- Residents can only view and edit their own expenses
- Managers can view all expenses and user information
- Managers can generate reports for all residents
- Managers can export data

## Error Handling

### Common Error Responses
- 400 Bad Request: Invalid input data
- 401 Unauthorized: Authentication required
- 403 Forbidden: Insufficient permissions
- 404 Not Found: Resource not found
- 422 Unprocessable Entity: Validation errors
- 500 Internal Server Error: Server errors

### Validation Rules
- Expense price must be positive
- Date must be within current month for residents
- Required fields cannot be empty
- Email format must be valid
- Password must meet security requirements

## Security Measures

### Authentication
- JWT token-based authentication
- Secure password hashing (bcrypt)
- Session management
- Rate limiting for auth endpoints

### Authorization
- Role-based access control
- Permission checks for each endpoint
- Input validation and sanitization
- SQL injection prevention

### Data Protection
- HTTPS encryption
- Data backup procedures
- Audit logging
- Secure file upload (for receipts)