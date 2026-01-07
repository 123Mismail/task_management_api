# Task Management API

A complete task management system built with FastAPI and SQLModel, providing full CRUD operations for managing tasks.

## Features

- **Full CRUD Operations**: Create, Read, Update, and Delete tasks
- **RESTful API**: Follows REST conventions for intuitive usage
- **Database Integration**: Uses SQLModel with PostgreSQL for data persistence
- **Input Validation**: Pydantic models for request/response validation
- **Error Handling**: Proper HTTP status codes and error messages
- **Async Support**: Built with async/await for better performance
- **CORS Support**: Configured for web application integration
- **Comprehensive Tests**: Includes unit tests for all endpoints

## Requirements

- Python 3.13+
- PostgreSQL database (or use SQLite for development)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd task-management-api
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
uv pip install -e .
# or
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your database URL
```

## Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/task_management_db
```

## Running the Application

### Development

```bash
# Run directly with Python
python main.py

# Or with uvicorn
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Production

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

The API will be available at `http://0.0.0.0:8000`

## API Endpoints

### Tasks

- `GET /tasks/` - Get all tasks (with pagination)
- `GET /tasks/{task_id}` - Get a specific task
- `POST /tasks/` - Create a new task
- `PUT /tasks/{task_id}` - Update a task completely
- `PATCH /tasks/{task_id}` - Partially update a task
- `DELETE /tasks/{task_id}` - Delete a task

### Other Endpoints

- `GET /` - Root endpoint
- `GET /health` - Health check endpoint

## Task Model

A task has the following properties:

- `id` (int): Unique identifier (auto-generated)
- `title` (str): Task title (required, 1-255 characters)
- `description` (str, optional): Task description (up to 1000 characters)
- `status` (str): Task status (pending, in_progress, completed)
- `priority` (str): Task priority (low, medium, high)
- `created_at` (datetime): Creation timestamp (auto-generated)
- `updated_at` (datetime): Last update timestamp (auto-generated)
- `due_date` (datetime, optional): Task due date

## Example Usage

### Create a Task

```bash
curl -X POST http://localhost:8000/tasks/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Complete project",
    "description": "Finish the task management API project",
    "priority": "high"
  }'
```

### Get All Tasks

```bash
curl http://localhost:8000/tasks/
```

### Get a Specific Task

```bash
curl http://localhost:8000/tasks/1
```

### Update a Task

```bash
curl -X PUT http://localhost:8000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated task title",
    "status": "in_progress",
    "priority": "medium"
  }'
```

### Partially Update a Task

```bash
curl -X PATCH http://localhost:8000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{
    "status": "completed"
  }'
```

### Delete a Task

```bash
curl -X DELETE http://localhost:8000/tasks/1
```

## Running Tests

```bash
# Run all tests
pytest

# Run tests with verbose output
pytest -v

# Run specific test file
pytest tests/test_tasks.py
```

## API Documentation

Interactive API documentation is automatically available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Database Configuration

The application uses SQLModel with the following connection pooling settings optimized for Neon PostgreSQL:

- `pool_size`: 20 connections maintained in the pool
- `max_overflow`: 30 additional overflow connections
- `pool_pre_ping`: True (verifies connections before use)
- `pool_recycle`: 3600 seconds (recycles connections after 1 hour)
- `pool_timeout`: 30 seconds (wait time for connections)

## Error Handling

The API returns appropriate HTTP status codes:

- `200`: Success for GET, PUT, PATCH requests
- `201`: Created for successful POST requests
- `204`: No Content for successful DELETE requests
- `404`: Not Found when a resource doesn't exist
- `422`: Unprocessable Entity for validation errors

## Security Considerations

- Input validation with Pydantic models
- SQL injection prevention through SQLModel/SQLAlchemy
- CORS configured (in production, limit origins to your frontend domain)

## Project Structure

```
task_management_api/
├── main.py              # Main FastAPI application
├── pyproject.toml       # Project configuration
├── .gitignore           # Git ignore file
├── README.md            # Project documentation
├── models/              # Database models
│   ├── __init__.py
│   └── task.py
├── schemas/             # Pydantic schemas
│   ├── __init__.py
│   └── task.py
├── routers/             # API route handlers
│   ├── __init__.py
│   └── task.py
├── database/            # Database configuration
│   ├── __init__.py
│   ├── config.py
│   └── database.py
└── tests/               # Test files
    ├── __init__.py
    └── test_tasks.py
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for your changes
5. Run the tests (`pytest`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request