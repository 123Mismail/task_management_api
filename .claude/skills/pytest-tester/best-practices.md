# Pytest Best Practices and Patterns

## Test Organization

### AAA Pattern (Arrange, Act, Assert)
```python
def test_user_authentication():
    # Arrange
    user = User(email="test@example.com", password="password")
    db = MockDatabase()

    # Act
    result = authenticate_user(user, db)

    # Assert
    assert result is True
```

### Test Isolation
- Each test should be independent of others
- Don't rely on test execution order
- Clean up after each test

## Fixtures

### Function-Scoped Fixtures
```python
@pytest.fixture
def sample_data():
    return {"name": "John", "age": 30}
```

### Session-Scoped Fixtures
```python
@pytest.fixture(scope="session")
def database_connection():
    conn = create_connection()
    yield conn
    conn.close()
```

### Parametrized Fixtures
```python
@pytest.fixture(params=["sqlite", "postgresql"])
def db_type(request):
    return request.param
```

## Advanced Patterns

### Factory Fixtures
```python
@pytest.fixture
def user_factory():
    def _create_user(name, email):
        return User(name=name, email=email)
    return _create_user

def test_user_creation(user_factory):
    user = user_factory("John", "john@example.com")
    assert user.name == "John"
```

### Temporary Directories
```python
import tempfile

@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield tmp_dir
```

## Markers and Parametrization

### Using Markers
```python
@pytest.mark.slow
def test_complex_calculation():
    pass

@pytest.mark.skip(reason="Not implemented yet")
def test_future_feature():
    pass

@pytest.mark.skipif(sys.version_info < (3, 8), reason="Requires Python 3.8+")
def test_new_feature():
    pass
```

### Complex Parametrization
```python
@pytest.mark.parametrize(
    "username,password,expected",
    [
        ("admin", "password123", True),
        ("user", "password", False),
        ("", "", False),
    ],
    ids=["admin_user", "regular_user", "empty_credentials"]
)
def test_login(username, password, expected):
    result = login(username, password)
    assert result == expected
```

## Mocking and Patching

### Mocking External Services
```python
from unittest.mock import patch, MagicMock

@patch('requests.get')
def test_api_call(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {"status": "success"}
    mock_get.return_value = mock_response

    result = external_api_call()

    assert result == {"status": "success"}
    mock_get.assert_called_once()
```

### Context Managers
```python
from unittest.mock import patch

def test_with_context_manager():
    with patch('mymodule.external_function') as mock_func:
        mock_func.return_value = "mocked"
        result = my_function()
        assert result == "mocked"
```

## Testing Asynchronous Code

### Async Tests
```python
import pytest
import asyncio

@pytest.mark.asyncio
async def test_async_function():
    result = await async_function()
    assert result == "expected"
```

## Configuration Files

### pytest.ini
```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py *_test.py
python_classes = Test*
python_functions = test_*
addopts =
    -ra
    --strict-markers
    --strict-config
    --cov=src
    --cov-report=html
    --cov-report=term-missing
    --tb=short
markers =
    slow: marks tests as slow
    integration: marks tests as integration tests
    unit: marks tests as unit tests
```

### pyproject.toml
```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
addopts = [
    "-ra",
    "--strict-markers",
    "--strict-config",
    "--cov=src",
    "--cov-report=html",
    "--cov-report=term-missing"
]
markers = [
    "slow: marks tests as slow",
    "integration: marks tests as integration tests"
]
```

## Common Assertions

### Basic Assertions
```python
def test_basic_assertions():
    assert 1 == 1
    assert [1, 2, 3] == [1, 2, 3]
    assert "hello" in "hello world"
    assert True is True
```

### Exception Testing
```python
def test_exception():
    with pytest.raises(ValueError):
        int("not_a_number")

def test_exception_with_message():
    with pytest.raises(ValueError, match="invalid literal"):
        int("not_a_number")
```

### Approximate Comparisons
```python
def test_floating_point():
    assert 0.1 + 0.2 == pytest.approx(0.3)
    assert 100 == pytest.approx(101, rel=0.05)  # 5% tolerance
```

## Testing with Databases

### Database Fixtures
```python
@pytest.fixture
def database():
    # Setup
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    yield session

    # Teardown
    session.close()
    Base.metadata.drop_all(engine)

def test_database_operation(database):
    user = User(name="Test User")
    database.add(user)
    database.commit()

    retrieved_user = database.query(User).first()
    assert retrieved_user.name == "Test User"
```