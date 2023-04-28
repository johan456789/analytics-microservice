import json

from fastapi.testclient import TestClient
import uuid
import user
from user import app


client = TestClient(app)
def test_add_user_successfully():
    id = uuid.uuid4()
    payload = {"userID":str(id)}
    response = client.post("/api/analysis/add-user/",json=payload)
    assert response.status_code == 200
    json_response = json.loads(response.content.decode('utf-8'))
    assert json_response['status code'] == 200
    assert json_response['message'] == "Added user successfully"
    user.delete_user_from_database(str(id))


def test_add_duplicate_user():
    existing_user_id = "9701a9cb-9448-40a2-81bb-02a0f9ffce2d"
    payload = {"userID": existing_user_id}
    response = client.post("/api/analysis/add-user/",json=payload)
    assert response.status_code == 400
    json_response = json.loads(response.content.decode('utf-8'))
    assert json_response['status code'] == 400
    assert json_response['message'] == "User with the provided userID already exists"


def test_missing_user_id_field():
    payload = {"userID": ""}
    response = client.post("/api/analysis/add-user/",json=payload)
    assert response.status_code == 400
    json_response = json.loads(response.content.decode('utf-8'))
    assert json_response['status code'] == 400
    assert json_response['message'] == "Missing field: userID"

def test_add_user_userid_not_uuid():
    not_user_id = "not_uuid"
    payload = {"userID": not_user_id}
    response = client.post("/api/analysis/add-user/",json=payload)
    assert response.status_code == 400
    json_response = json.loads(response.content.decode('utf-8'))
    assert json_response['status code'] == 400
    assert json_response['message'] == "Provided userID is not UUID"