---
name: hostel-expense-tracker
description: Create a comprehensive expense tracking system for hostel managers to track daily expenses of residents. Each resident can maintain their personal expense notebook with item name, price, and date. The system supports monthly notebook management, individual and collective expense views, and reporting. Use when building expense tracking applications for hostels or shared living spaces.
allowed-tools: Read, Grep, Bash, Edit, Write
model: claude-sonnet-4-20250514
---
# Hostel Expense Tracker

## Instructions

Use this skill to create a comprehensive expense tracking system for hostel managers. The system should allow residents to maintain personal expense notebooks with daily entries, support monthly notebook management, and provide both individual and collective expense views.

### 1. **System Architecture**
- Design a full-stack application with backend API and frontend interface
- Implement user authentication and authorization
- Create database schema for users, expenses, and monthly notebooks
- Design RESTful API endpoints for all operations

### 2. **User Management**
- Create user registration and login system
- Implement role-based access (Residents vs. Manager)
- Design user profile management features
- Include account verification and password recovery

### 3. **Expense Tracking Features**
- Create personal expense notebook for each resident
- Implement daily expense entry with item name, price, date, and category
- Design monthly notebook management with automatic rollovers
- Add search, filter, and bulk entry capabilities

### 4. **Database Design**
- Design Users table with user information and roles
- Create Expenses table with item, amount, date, user_id, month
- Implement Monthly summaries table
- Design Categories table for expense categorization

### 5. **Backend API Development**
- Create expense entry endpoints (POST, GET, PUT, DELETE)
- Implement monthly notebook management
- Design reporting endpoints
- Add authentication and authorization middleware

### 6. **Frontend Development**
- Create user-friendly interface for expense entry
- Design dashboard for viewing expenses
- Implement monthly notebook navigation
- Add report generation and viewing features

### 7. **Reporting & Analytics**
- Generate individual monthly expense summaries
- Create collective expense reports
- Implement expense trend analysis
- Add cost comparison features

### 8. **Administrative Features**
- Design manager dashboard
- Create view for all residents' expenses
- Implement bulk operations
- Add data export functionality

## Implementation Steps

### 1. **Project Setup**
- Create project directory structure
- Initialize package.json/requirements.txt
- Set up database configuration
- Configure environment variables

### 2. **Database Schema Creation**
- Define Users model (id, name, email, password, role, created_at)
- Define Expenses model (id, user_id, item_name, price, date, category, month, created_at)
- Define Categories model (id, name, user_id, created_at)
- Define MonthlySummaries model (id, user_id, month, total_amount, created_at)

### 3. **Backend Development**
- Create authentication middleware
- Implement user registration/login endpoints
- Build expense CRUD operations
- Add monthly notebook management
- Create reporting endpoints

### 4. **Frontend Development**
- Design expense entry form
- Create monthly notebook views
- Implement dashboard interface
- Add reporting features

### 5. **Testing & Documentation**
- Write unit tests for backend functions
- Create API documentation
- Add user guides and help documentation

## Key Features to Implement

1. **Daily Expense Entry**: Simple form with item name, price, date, and category
2. **Monthly Organization**: Automatic notebook creation and navigation
3. **Individual Tracking**: Personal expense notebooks for each resident
4. **Manager View**: Access to all residents' expenses
5. **Reporting**: Monthly summaries and detailed reports
6. **Data Export**: CSV/PDF export functionality
7. **Mobile Responsive**: Works on smartphones and tablets

## Example Usage Scenarios

### Scenario 1: Resident Adding Daily Expenses
```
As a resident, I want to add my daily expenses so that I can track my spending.
1. Login to the application
2. Navigate to the current month's notebook
3. Enter expense details: item name, price, date, category
4. Save the entry
5. View all entries for the current month
```

### Scenario 2: Manager Viewing All Expenses
```
As a hostel manager, I want to see all residents' expenses for budget planning.
1. Login as manager
2. Access the management dashboard
3. View all residents' expenses for the current month
4. Generate reports for all residents
5. Export data for accounting purposes
```

### Scenario 3: Monthly Summary Generation
```
At the end of each month, the system should automatically generate summaries.
1. Calculate total expenses per resident for the month
2. Generate comparison reports
3. Prepare data for the next month's notebook
4. Send notifications to residents about their monthly totals
```

## Security Considerations
- Implement proper authentication and authorization
- Use secure password hashing
- Validate and sanitize all user inputs
- Implement rate limiting for API endpoints
- Use HTTPS for all communications
- Implement proper session management

## Technology Stack Recommendations
- Backend: FastAPI (Python) or Express.js (Node.js)
- Database: PostgreSQL or MySQL
- Frontend: React/Vue.js or mobile-first design
- Authentication: JWT tokens or session-based
- File Storage: For receipt photos (optional)

## Output Format
- Complete backend API with all necessary endpoints
- Database schema with proper relationships
- Frontend interface with responsive design
- Authentication system with role-based access
- Reporting and analytics features
- Comprehensive documentation
- Sample data and test cases