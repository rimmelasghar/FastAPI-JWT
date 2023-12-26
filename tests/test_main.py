from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
STUDENT_ID=1
INNCORRECT_STUDENT_ID=101
ADDED_STUDENT_ID=0
headers = {
        "api-key": "UmltbWVsQXNnaGFy"
}

def test_base():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"message": "The API is LIVE!!"}

def test_api_key():
    response = client.get("/student", headers=headers)
    assert response.status_code == 200

def test_api_invalid_key():
    headers = {
        "api-key": "Not_a_valid_Key"
    }
    response = client.get("/student", headers=headers)
    assert response.status_code == 401
    assert response.json() == {
    "detail": "Invalid or missing API Key"
    }
    
def test_get_a_student_by_id():
    response = client.get(f"/student/{STUDENT_ID}/",headers=headers)
    assert response.status_code == 200
    assert response.json() ==  {
            "name": "John Smith",
            "gpa": 3.8,
            "attendance": 93,
            "class_name": "Mathematics"
        }

def test_get_a_student_by_incorrect_id():
        response = client.get(f"/student/{INNCORRECT_STUDENT_ID}/",headers=headers)
        assert response.status_code == 404
        assert response.json() == {
            "detail": "Student not found"
        }

def test_add_a_student():
    payload = {
        "name": "rimmel Asghar",
        "gpa": 3.8,
        "attendance": 77,
        "class_name": "Mathematics"
    }
    response = client.post("/student/", json=payload,headers=headers)
    assert response.status_code == 201



# run command
# pytest tests/test_main.py -v -s