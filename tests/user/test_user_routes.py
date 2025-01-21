from fastapi.testclient import TestClient
from faker import Faker
from app import app

fake = Faker()
client = TestClient(app)


def test_signup():
    data = {
        "username": fake.user_name(),
        "email": fake.email(),
        "password": "password1",
    }
    response = client.post("/user/signup", json=data)
    assert response.status_code == 200
    assert response.json() == {"message": "User created Successfully"}


def get_user_data():
    data = {
        "username": fake.user_name(),
        "email": fake.email(),
        "password": "password1",
    }
    response = client.post("/user/signup", json=data)

    return data


def test_login():
    data = get_user_data()
    response = client.post("/user/login", json=data)
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"
