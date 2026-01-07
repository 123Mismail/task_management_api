# FastAPI CRUD Operations Reference

## Pydantic Model Examples

### Basic Entity Model
```python
from pydantic import BaseModel
from typing import Optional

class ItemBase(BaseModel):
    name: str
    description: Optional[str] = None

class ItemCreate(ItemBase):
    pass

class ItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class ItemResponse(ItemBase):
    id: int
```

## In-Memory Storage Examples

### Using a Dictionary
```python
# Global in-memory storage
items: dict[int, ItemResponse] = {}
next_id = 1
```

### Using a List
```python
# Global in-memory storage
items: list[ItemResponse] = []
```

## Endpoint Examples

### GET All Items
```python
@app.get("/items/", response_model=list[ItemResponse])
async def get_items():
    return list(items.values())
```

### GET Single Item
```python
@app.get("/items/{item_id}", response_model=ItemResponse)
async def get_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_id]
```

### POST New Item
```python
@app.post("/items/", response_model=ItemResponse, status_code=201)
async def create_item(item: ItemCreate):
    global next_id
    new_item = ItemResponse(id=next_id, **item.model_dump())
    items[next_id] = new_item
    next_id += 1
    return new_item
```

### PUT Update Item
```python
@app.put("/items/{item_id}", response_model=ItemResponse)
async def update_item(item_id: int, item: ItemUpdate):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")

    stored_item = items[item_id]
    update_data = item.model_dump(exclude_unset=True)
    updated_item = stored_item.model_copy(update=update_data)
    items[item_id] = updated_item
    return updated_item
```

### DELETE Item
```python
@app.delete("/items/{item_id}", status_code=204)
async def delete_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    del items[item_id]
    return
```

## Error Handling Patterns

### HTTP Exception for Not Found
```python
from fastapi import HTTPException

raise HTTPException(status_code=404, detail="Item not found")
```

### Validation Error Handling
```python
# Pydantic will automatically handle validation errors
# with status code 422 Unprocessable Entity
```

## Complete Example Structure

### main.py
```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI()

# Define models
class ItemBase(BaseModel):
    name: str
    description: Optional[str] = None

class ItemCreate(ItemBase):
    pass

class ItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class ItemResponse(ItemBase):
    id: int

# In-memory storage
items: dict[int, ItemResponse] = {}
next_id = 1

# Endpoints
@app.get("/items/", response_model=List[ItemResponse])
async def get_items():
    return list(items.values())

@app.get("/items/{item_id}", response_model=ItemResponse)
async def get_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_id]

@app.post("/items/", response_model=ItemResponse, status_code=201)
async def create_item(item: ItemCreate):
    global next_id
    new_item = ItemResponse(id=next_id, **item.model_dump())
    items[next_id] = new_item
    next_id += 1
    return new_item

@app.put("/items/{item_id}", response_model=ItemResponse)
async def update_item(item_id: int, item: ItemUpdate):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")

    stored_item = items[item_id]
    update_data = item.model_dump(exclude_unset=True)
    updated_item = stored_item.model_copy(update=update_data)
    items[item_id] = updated_item
    return updated_item

@app.delete("/items/{item_id}", status_code=204)
async def delete_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    del items[item_id]
    return
```

## Status Codes Reference

- `200 OK`: Successful GET, PUT requests
- `201 Created`: Successful POST request
- `204 No Content`: Successful DELETE request
- `404 Not Found`: Resource not found
- `422 Unprocessable Entity`: Validation error
- `500 Internal Server Error`: Server error

## Testing Examples

### Test GET endpoint
```python
def test_get_items():
    response = client.get("/items/")
    assert response.status_code == 200
    assert response.json() == []

def test_get_item():
    # First create an item
    create_response = client.post("/items/", json={"name": "Test Item"})
    item_id = create_response.json()["id"]

    # Then get it
    response = client.get(f"/items/{item_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Test Item"
```

### Test POST endpoint
```python
def test_create_item():
    response = client.post("/items/", json={
        "name": "New Item",
        "description": "A test item"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "New Item"
    assert data["description"] == "A test item"
    assert "id" in data
```

### Test PUT endpoint
```python
def test_update_item():
    # Create an item first
    create_response = client.post("/items/", json={"name": "Original"})
    item_id = create_response.json()["id"]

    # Update the item
    response = client.put(f"/items/{item_id}", json={
        "name": "Updated",
        "description": "Updated description"
    })
    assert response.status_code == 200
    assert response.json()["name"] == "Updated"
```

### Test DELETE endpoint
```python
def test_delete_item():
    # Create an item first
    create_response = client.post("/items/", json={"name": "To Delete"})
    item_id = create_response.json()["id"]

    # Delete the item
    response = client.delete(f"/items/{item_id}")
    assert response.status_code == 204

    # Verify it's gone
    get_response = client.get(f"/items/{item_id}")
    assert get_response.status_code == 404
```