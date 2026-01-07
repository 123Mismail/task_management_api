---
name: pytest-tester
description: Write simple, effective pytest tests for Python code. Use when user asks to create tests.
allowed-tools: Read, Grep, Bash, Edit, Write
---

# Pytest Testing

## Instructions

Use this skill to create simple, effective pytest tests for Python functions and classes.

1. **Create test files** with descriptive names (`test_*.py`)
2. **Write simple test functions** that test one thing at a time
3. **Use clear assertions** to verify expected behavior
4. **Test both success and failure cases**
5. **Use fixtures for setup when needed**

## Simple Test Structure

```python
import pytest
from mymodule import function_to_test

def test_function_name():
    # Arrange
    input_value = "test input"

    # Act
    result = function_to_test(input_value)

    # Assert
    assert result == expected_value
```

## Basic Examples

### Testing a Simple Function
```python
def test_add_numbers():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
```

### Testing with Expected Exceptions
```python
def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)
```

### Testing with Multiple Inputs (Parametrize)
```python
@pytest.mark.parametrize("a,b,expected", [
    (2, 3, 5),
    (0, 0, 0),
    (-1, 1, 0),
])
def test_add_numbers_parametrized(a, b, expected):
    assert add(a, b) == expected
```

### Simple Fixture Example
```python
@pytest.fixture
def sample_data():
    return [1, 2, 3, 4, 5]

def test_list_length(sample_data):
    assert len(sample_data) == 5
```