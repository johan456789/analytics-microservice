import uuid
from fastapi.testclient import TestClient
from utils.utils import delete_user_from_database, deleteEvent
import json
from src.main import app


client = TestClient(app)


"""
File description:
This is the file that contains the tests that test the POST APIs for the endpoints that are related to event
"""


def test_add_event_successfully():
    new_user_id = uuid.uuid4()
    new_session_id = uuid.uuid4()
    try:
        payload = {"userID": str(new_user_id)}
        response = client.post("/users/add", json=payload)
        add_user_response = json.loads(response.content.decode('utf-8'))
        assert add_user_response['status code'] == 200
        assert add_user_response['message'] == "Added user successfully"
        session_payload = {"userID": str(new_session_id),
                           "sessionID": str(new_session_id),
                           "startTime": "2023-04-19 12:30:45"
                           }

        session_response = client.post("/api/analysis/record-session-start-time/", json=session_payload)
        assert session_response.status_code == 200
        add_session_response = json.loads(session_response.content.decode('utf-8'))
        assert add_session_response['status code'] == 200
        assert add_session_response['message'] == "Recorded session start time successfully"

        #add event that is based on this session
        event_payload = {
            "sessionID": str(new_session_id),
            "eventName": "scroll",
            "occurTime": "2023-04-19 12:30:45"
            }
        add_event_response = client.post("/api/analysis/record-event/", json=event_payload)
        assert add_event_response.status_code == 200
        add_event_response = json.loads(add_event_response.content.decode('utf-8'))
        assert add_event_response['status code'] == 200
        assert add_event_response['message'] == "Record event successfully"
        eventID = add_event_response['eventID']
        assert isinstance(eventID, int)
        delete_user_from_database(str(new_user_id))
        deleteEvent(eventID)
    except Exception as e:
        delete_user_from_database(str(new_user_id))


def test_missing_sessionID():
    new_user_id = uuid.uuid4()
    new_session_id = uuid.uuid4()
    try:
        payload = {"userID": str(new_user_id)}
        response = client.post("/users/add", json=payload)
        assert response.status_code == 200
        session_payload = {"userID": str(new_session_id),
                           "sessionID": str(new_session_id),
                           "startTime": "2023-04-19 12:30:45"
                           }
        session_response = client.post("/api/analysis/record-session-start-time/", json=session_payload)
        assert session_response.status_code == 200

        #add event that is based on this session
        event_payload = {
            "sessionID": "",
            "eventName": "scroll",
            "occurTime": "2023-04-19 12:30:45"
            }
        add_event_response = client.post("/api/analysis/record-event/", json=event_payload)
        add_event_response = json.loads(add_event_response.content.decode('utf-8'))
        assert add_event_response['status code'] == 400
        assert add_event_response['message'] == "missing required field: sessionID"
        delete_user_from_database(str(new_user_id))
    except Exception as e:
        delete_user_from_database(str(new_user_id))


def test_missing_eventName():
    new_user_id = uuid.uuid4()
    new_session_id = uuid.uuid4()
    try:
        payload = {"userID": str(new_user_id)}
        response = client.post("/users/add", json=payload)
        assert response.status_code == 200
        session_payload = {"userID": str(new_session_id),
                           "sessionID": str(new_session_id),
                           "startTime": "2023-04-19 12:30:45"
                           }
        session_response = client.post("/api/analysis/record-session-start-time/", json=session_payload)
        assert session_response.status_code == 200

        #add event that is based on this session
        event_payload = {
            "sessionID": str(new_session_id),
            "eventName": "",
            "occurTime": "2023-04-19 12:30:45"
            }
        add_event_response = client.post("/api/analysis/record-event/", json=event_payload)
        add_event_response = json.loads(add_event_response.content.decode('utf-8'))
        assert add_event_response['status code'] == 400
        assert add_event_response['message'] == "missing required field: eventName"
        delete_user_from_database(str(new_user_id))
    except Exception as e:
        delete_user_from_database(str(new_user_id))

def test_missing_occurTime():
    new_user_id = uuid.uuid4()
    new_session_id = uuid.uuid4()
    try:
        payload = {"userID": str(new_user_id)}
        response = client.post("/users/add", json=payload)
        assert response.status_code == 200
        session_payload = {"userID": str(new_session_id),
                           "sessionID": str(new_session_id),
                           "startTime": "2023-04-19 12:30:45"
                           }
        session_response = client.post("/api/analysis/record-session-start-time/", json=session_payload)
        assert session_response.status_code == 200

        #add event that is based on this session
        event_payload = {
            "sessionID": str(new_session_id),
            "eventName": "scroll",
            "occurTime": ""
            }
        add_event_response = client.post("/api/analysis/record-event/", json=event_payload)
        add_event_response = json.loads(add_event_response.content.decode('utf-8'))
        assert add_event_response['status code'] == 400
        assert add_event_response['message'] == "missing required field: occurTime"
        delete_user_from_database(str(new_user_id))
    except Exception as e:
        delete_user_from_database(str(new_user_id))

def test_invalid_sessionID():
    new_user_id = uuid.uuid4()
    try:
        payload = {"userID": str(new_user_id)}
        response = client.post("/users/add", json=payload)
        assert response.status_code == 200

        #add event that is based on this session
        event_payload = {
            "sessionID": "invalid sessionID",
            "eventName": "scroll",
            "occurTime": "2023-04-19 12:30:45"
            }
        add_event_response = client.post("/api/analysis/record-event/", json=event_payload)
        add_event_response = json.loads(add_event_response.content.decode('utf-8'))
        assert add_event_response['status code'] == 400
        assert add_event_response['message'] == "SessionID does not exists"
        delete_user_from_database(str(new_user_id))
    except Exception as e:
        delete_user_from_database(str(new_user_id))


def test_invalid_time():
    new_user_id = uuid.uuid4()
    new_session_id = uuid.uuid4()
    try:
        payload = {"userID": str(new_user_id)}
        response = client.post("/users/add", json=payload)
        assert response.status_code == 200
        session_payload = {"userID": str(new_session_id),
                           "sessionID": str(new_session_id),
                           "startTime": "2023-04-19 12:30:45"
                           }
        session_response = client.post("/api/analysis/record-session-start-time/", json=session_payload)
        assert session_response.status_code == 200

        #add event that is based on this session
        event_payload = {
            "sessionID": str(new_session_id),
            "eventName": "scroll",
            "occurTime": "2023-04-19"
            }
        add_event_response = client.post("/api/analysis/record-event/", json=event_payload)
        add_event_response = json.loads(add_event_response.content.decode('utf-8'))
        assert add_event_response['status code'] == 400
        assert add_event_response['message'] == "provided datetime is either not in mysql datetime format nor an invalid datetime"
        delete_user_from_database(str(new_user_id))
    except Exception as e:
        delete_user_from_database(str(new_user_id))



