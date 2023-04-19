import sys
from fastapi.testclient import TestClient

sys.path.append('..')
from src.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200

def test_get_monthuser():
    # TODO: get empty database, add user, and test existence of user
    response = client.get("/getMonthActiveUser/2021-01")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_dayuser():
    # TODO: get empty database, add user, and test existence of user
    response = client.get("/getDayActiveUser/2022-02-01")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
