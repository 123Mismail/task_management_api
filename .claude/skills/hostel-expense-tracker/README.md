# Hostel Expense Tracker Skill

A comprehensive skill for creating expense tracking applications for hostel managers. This skill provides all the necessary components to build a complete expense tracking system where residents can maintain personal expense notebooks and managers can view collective expenses.

## Features

- User authentication and role-based access (Residents vs. Managers)
- Personal expense notebooks for each resident
- Daily expense entry with item name, price, date, and category
- Monthly notebook management with automatic rollovers
- Individual and collective expense views
- Reporting and analytics capabilities
- Data export functionality (CSV/PDF)
- Mobile-responsive interface

## Usage

This skill is designed to help you build a complete expense tracking application for hostel management. Use it when you need to:

- Track daily expenses of residents
- Create personal expense notebooks
- Generate monthly expense reports
- Manage shared living space expenses
- Maintain financial records for multiple residents

## Components

- **SKILL.md**: Main skill definition with instructions and usage guidelines
- **reference.md**: Technical reference with database schema and API specifications
- **examples.md**: Implementation examples with code snippets
- **scripts/init_project.py**: Project initialization script

## Getting Started

1. Use the initialization script to create a new project:
   ```
   python scripts/init_project.py /path/to/new/project
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up your database and configure environment variables in `.env`

4. Start implementing the models and routes as outlined in the examples

## Architecture

The skill provides guidance for building a full-stack application with:
- Backend API using FastAPI
- SQLModel for database operations
- JWT-based authentication
- Role-based access control
- RESTful API design
- Frontend components for user interaction

## Security

- Secure authentication with JWT tokens
- Role-based access control
- Input validation and sanitization
- Password hashing with bcrypt
- SQL injection prevention

## Customization

The skill is designed to be flexible and can be customized to meet specific requirements:
- Add additional expense categories
- Modify user roles and permissions
- Customize the reporting features
- Integrate with existing accounting systems
- Add receipt photo upload functionality