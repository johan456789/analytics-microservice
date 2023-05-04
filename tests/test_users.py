import json
from fastapi import HTTPException
from fastapi.testclient import TestClient
import uuid
from src.main import app
from utils.utils import delete_user_from_database


client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_get_daily_active_users():
    # TODO: get empty database, add user, and test existence of user
    response = client.get("/users/daily/2021-01-01T00:00:00")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_weekly_active_users():
    # TODO: get empty database, add user, and test existence of user
    response = client.get("/users/weekly/2021-01-01T00:00:00")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_monthly_active_users():
    # TODO: get empty database, add user, and test existence of user
    response = client.get("/users/monthly/2021-01-01T00:00:00")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_add_user_successfully():
    id = uuid.uuid4()
    payload = {"userID":str(id)}
    response = client.post("/users/add",json=payload)
    assert response.status_code == 200
    json_response = json.loads(response.content.decode('utf-8'))
    assert json_response['status code'] == 200
    assert json_response['message'] == "Added user successfully"
    delete_user_from_database(str(id))

def test_add_duplicate_user():
    try:
        id = uuid.uuid4()
        payload = {"userID":str(id)}
        response = client.post("/users/add",json=payload)
        assert response.status_code == 200
        response = client.post("/users/add",json=payload)
        assert response.status_code == 413
        delete_user_from_database(str(id))
    except HTTPException as e:
        print(e)
        assert False

def test_missing_user_id_field():
    payload = {"userID": ""}
    response = client.post("/users/add",json=payload)
    assert response.status_code == 411

def test_add_user_userid_not_uuid():
    not_user_id = "not_uuid"
    payload = {"userID": not_user_id}
    response = client.post("/users/add",json=payload)
    assert response.status_code == 412
