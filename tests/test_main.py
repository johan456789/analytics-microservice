import sys
from fastapi.testclient import TestClient

sys.path.append('..')
from src.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_get_daily_active_users():
    # TODO: get empty database, add user, and test existence of user
    response = client.get("/daily_active_users/2021-01-01T00:00:00")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_weekly_new_users():
    # TODO: get empty database, add user, and test existence of user
    response = client.get("/weekly_new_users/2021-01-01T00:00:00")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_monthly_active_users():
    # TODO: get empty database, add user, and test existence of user
    response = client.get("/monthly_active_users/2021-01-01T00:00:00")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
