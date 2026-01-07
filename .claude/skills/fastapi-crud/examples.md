# FastAPI CRUD Examples

## Example 1: Creating a User Management System

### User Request
"Create a CRUD API for managing users with name, email, and age"

### Generated Implementation

#### models/user.py
```python
from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    name: str
    email: str
    age: Optional[int] = None

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    age: Optional[int] = None

class UserResponse(UserBase):
    id: int
    is_active: bool = True
```

#### routers/users.py
```python
from fastapi import APIRouter, HTTPException
from typing import List
from models.user import UserCreate, UserUpdate, UserResponse

router = APIRouter()

# In-memory storage
users: dict[int, UserResponse] = {}
next_id = 1

@router.get("/", response_model=List[UserResponse])
async def get_users():
    return list(users.values())

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    return users[user_id]

@router.post("/", response_model=UserResponse, status_code=201)
async def create_user(user: UserCreate):
    global next_id
    new_user = UserResponse(id=next_id, **user.model_dump(), is_active=True)
    users[next_id] = new_user
    next_id += 1
    return new_user

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user: UserUpdate):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")

    stored_user = users[user_id]
    update_data = user.model_dump(exclude_unset=True)
    updated_user = stored_user.model_copy(update=update_data)
    users[user_id] = updated_user
    return updated_user

@router.delete("/{user_id}", status_code=204)
async def delete_user(user_id: int):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    del users[user_id]
    return
```

## Example 2: Creating a Product Catalog

### User Request
"Create a CRUD API for products with name, price, and category"

### Generated Implementation

#### models/product.py
```python
from pydantic import BaseModel
from typing import Optional

class ProductBase(BaseModel):
    name: str
    price: float
    category: str

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None

class ProductResponse(ProductBase):
    id: int
    in_stock: bool = True
```

#### routers/products.py
```python
from fastapi import APIRouter, HTTPException
from typing import List
from models.product import ProductCreate, ProductUpdate, ProductResponse

router = APIRouter()

# In-memory storage
products: dict[int, ProductResponse] = {}
next_id = 1

@router.get("/", response_model=List[ProductResponse])
async def get_products():
    return list(products.values())

@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int):
    if product_id not in products:
        raise HTTPException(status_code=404, detail="Product not found")
    return products[product_id]

@router.post("/", response_model=ProductResponse, status_code=201)
async def create_product(product: ProductCreate):
    global next_id
    new_product = ProductResponse(id=next_id, **product.model_dump(), in_stock=True)
    products[next_id] = new_product
    next_id += 1
    return new_product

@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(product_id: int, product: ProductUpdate):
    if product_id not in products:
        raise HTTPException(status_code=404, detail="Product not found")

    stored_product = products[product_id]
    update_data = product.model_dump(exclude_unset=True)
    updated_product = stored_product.model_copy(update=update_data)
    products[product_id] = updated_product
    return updated_product

@router.delete("/{product_id}", status_code=204)
async def delete_product(product_id: int):
    if product_id not in products:
        raise HTTPException(status_code=404, detail="Product not found")
    del products[product_id]
    return
```

## Example 3: Complete Application Structure

### main.py
```python
from fastapi import FastAPI
from routers import users, products

app = FastAPI(
    title="CRUD API",
    description="A simple CRUD API built with FastAPI",
    version="1.0.0"
)

# Include routers
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(products.router, prefix="/products", tags=["products"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the CRUD API"}
```

## API Usage Examples

### Create a User
```
POST /users/
{
    "name": "John Doe",
    "email": "john@example.com",
    "age": 30
}
```

### Get All Users
```
GET /users/
Response: [{"id": 1, "name": "John Doe", "email": "john@example.com", "age": 30, "is_active": true}]
```

### Get Specific User
```
GET /users/1
Response: {"id": 1, "name": "John Doe", "email": "john@example.com", "age": 30, "is_active": true}
```

### Update User
```
PUT /users/1
{
    "name": "Jane Doe",
    "age": 28
}
```

### Delete User
```
DELETE /users/1
Status: 204 No Content
```

## Testing Examples

### Test User Creation
```python
def test_create_user():
    response = client.post("/users/", json={
        "name": "Test User",
        "email": "test@example.com",
        "age": 25
    })
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test User"
    assert data["email"] == "test@example.com"
    assert data["age"] == 25
    assert "id" in data
```

### Test User Retrieval
```python
def test_get_user():
    # Create a user first
    create_response = client.post("/users/", json={
        "name": "Test User",
        "email": "test@example.com"
    })
    user_id = create_response.json()["id"]

    # Retrieve the user
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test User"
    assert data["email"] == "test@example.com"
```

### Test User Update
```python
def test_update_user():
    # Create a user first
    create_response = client.post("/users/", json={
        "name": "Original User",
        "email": "original@example.com"
    })
    user_id = create_response.json()["id"]

    # Update the user
    response = client.put(f"/users/{user_id}", json={
        "name": "Updated User",
        "age": 30
    })
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated User"
    assert data["age"] == 30
```

### Test User Deletion
```python
def test_delete_user():
    # Create a user first
    create_response = client.post("/users/", json={
        "name": "User to Delete",
        "email": "delete@example.com"
    })
    user_id = create_response.json()["id"]

    # Delete the user
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 204

    # Verify deletion
    get_response = client.get(f"/users/{user_id}")
    assert get_response.status_code == 404
```