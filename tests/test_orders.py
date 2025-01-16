from fastapi.testclient import TestClient
from app.main import create_app

clint = TestClient(create_app())


def test_create_user():
    pass
