import json
from fastapi import HTTPException
from src.main import *
from fastapi.testclient import TestClient
import uuid
import traceback
from src.main import app


client = TestClient(app)

from src.database import session
def delete_user_from_database(user_uuid):
    """
    Use it to delete this user in the database whose userID matches the parameter user_uuid
    """
    try:
        user = session.query(User).filter_by(userID=user_uuid).first()
        session.delete(user)
        session.commit()
        session.close()
    except Exception as e:
        print(e)
        traceback.print_exc()
        session.rollback()


def test_add_user_successfully():
    id = uuid.uuid4()
    payload = {"userID":str(id)}
    response = client.post("/api/analysis/add-user/",json=payload)
    assert response.status_code == 200
    json_response = json.loads(response.content.decode('utf-8'))
    assert json_response['status code'] == 200
    assert json_response['message'] == "Added user successfully"
    delete_user_from_database(str(id))


def test_add_duplicate_user():
    try:
        id = uuid.uuid4()
        payload = {"userID":str(id)}
        response = client.post("/api/analysis/add-user/",json=payload)
        assert response.status_code == 200
        response = client.post("/api/analysis/add-user/",json=payload)
        assert response.status_code == 413
        delete_user_from_database(str(id))
    except HTTPException as e:
        print(e)
        assert False


def test_missing_user_id_field():
    payload = {"userID": ""}
    response = client.post("/api/analysis/add-user/",json=payload)
    assert response.status_code == 411


def test_add_user_userid_not_uuid():
    not_user_id = "not_uuid"
    payload = {"userID": not_user_id}
    response = client.post("/api/analysis/add-user/",json=payload)
    assert response.status_code == 412
