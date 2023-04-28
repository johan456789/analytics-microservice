import uuid

from fastapi.testclient import TestClient
import session
import user
import json
from session import app
from user import app as user_app


non_existing_userID = uuid.uuid4()

client = TestClient(app)
user_client = TestClient(user_app)

def test_add_session_with_non_existing_userID():
    payload = { "userID": str(non_existing_userID),
                "sessionID": "94b0af25-ca4f-4d4b-b539-6058ffb64ba3",
                "startTime":"2023-04-19 12:30:45"
                }
    response = client.post("/api/analysis/record-session-start-time/", json=payload)
    assert response.status_code == 400
    json_response = json.loads(response.content.decode('utf-8'))
    assert json_response['status code'] == 400
    assert json_response['message'] == "UserID does not exist. User not found"


def test_add_session_successfully():
    new_user_id = uuid.uuid4()
    new_session_id = uuid.uuid4()
    try:
        payload = {"userID":str(new_user_id)}
        response = user_client.post("/api/analysis/add-user/",json=payload)
        add_user_response = json.loads(response.content.decode('utf-8'))
        print(response)
        assert add_user_response['status code'] == 200
        assert add_user_response['message'] == "Added user successfully"
        payload = { "userID": str(new_session_id),
                    "sessionID": "94b0af25-ca4f-4d4b-b539-6058ffb64ba3",
                    "startTime":"2023-04-19 12:30:45"
                    }
        response = client.post("/api/analysis/record-session-start-time/", json=payload)
        assert response.status_code == 400
        add_session_response = json.loads(response.content.decode('utf-8'))
        assert add_session_response['status code'] == 400
        assert add_session_response['message'] == "UserID does not exist. User not found"
        user.delete_user_from_database(str(new_user_id))
        session.delete_session_from_database(str(new_session_id))
    except Exception as e:
        user.delete_user_from_database(str(new_user_id))
        session.delete_session_from_database(str(new_session_id))




