from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    print(response ,"/n response is printing ")
    assert response.status_code == 200
    assert response.json()== {"message":"Task Management API","status":"running"}
    
def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    

def test_create_task():
    demo_task={
        "title":"Test task",
        "description":"this is a test task",
        "status":"pending",
        "priority":"medium"
              
    }
    response = client.post("/tasks/",json=demo_task)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == demo_task["title"]
    assert data["description"]==demo_task["description"]
    assert data["status"] == demo_task["status"]
    assert data["priority"] == demo_task["priority"]
    
def test_signup_user():
    demo_user={
        "email":"test1@gmail.com",
        "first_name":"Test",
        "last_name":"User",
        "password":"TestPassword123"
    }  
    response = client.post("/users/signup",json=demo_user)
    assert response.status_code == 201
    data = response.json()
    assert data["email"]== demo_user["email"]
    assert data["first_name"]== demo_user["first_name"]
    assert data["last_name"]== demo_user["last_name"]

