import traceback
from fastapi.testclient import TestClient
import json
from src.main import app
from utils.utils import delete_screen_from_database

"""
File description:
This is the file that contains the tests that test the POST APIs for the endpoints that are related to screen
"""


client = TestClient(app)

"""
If test fails, be sure to check if the "user_id_for_testing" and "session_id_for_testing" exist
in the database
"""

session_id_for_testing = "7255fde8-1941-4382-8f43-d0c6cafac808"


def test_add_screen_to_database_successfully():
    try:
        screen_payload = {
            "sessionID": session_id_for_testing,
            "screenName": "personal page",
            "startTime": "2023-05-02 12:30:45"
        }
        add_event_response = client.post("/api/analysis/setCurrentScreen/", json=screen_payload)
        assert add_event_response.status_code == 200
        add_event_response = json.loads(add_event_response.content.decode('utf-8'))
        assert add_event_response['status code'] == 200
        assert add_event_response['message'] == "Set current screen successfully"
        screenID = add_event_response['screenID']
        assert isinstance(screenID, int)
        delete_screen_from_database(screenID)
    except Exception as err:
        traceback.print_exc()
        assert False

def test_update_screen_close_time_in_database_successfully():
    try:
        screen_payload = {
            "sessionID": session_id_for_testing,
            "screenName": "personal page",
            "startTime": "2023-05-02 12:30:45"
        }
        add_event_response = client.post("/api/analysis/setCurrentScreen/", json=screen_payload)
        assert add_event_response.status_code == 200
        add_event_response = json.loads(add_event_response.content.decode('utf-8'))
        assert add_event_response['message'] == "Set current screen successfully"
        screenID = add_event_response['screenID']
        assert isinstance(screenID, int)

        close_screen_payload = {
            "screenID": screenID,
            "sessionID": session_id_for_testing,
            "screenName": "personal page",
            "endTime": "2023-05-02 13:30:45"
        }
        close_event_response = client.post("/api/analysis/update-current-screen-endTime/", json=close_screen_payload)
        assert close_event_response.status_code == 200
        decoded_close_event_response = json.loads(close_event_response.content.decode('utf-8'))
        assert decoded_close_event_response['message'] == "Set screen endTime successfully"
        delete_screen_from_database(screenID)
    except Exception as err:
        print(err)
        traceback.print_exc()
        assert False

def test_add_screen_with_endTime_to_database_successfully():
    try:
        screen_payload = {
            "sessionID": session_id_for_testing,
            "screenName": "personal page",
            "startTime": "2023-05-02 12:30:45",
            "endTime": "2023-05-02 13:30:45"
        }
        add_event_response = client.post("/api/analysis/setCurrentScreen/", json=screen_payload)
        assert add_event_response.status_code == 200
        add_event_response = json.loads(add_event_response.content.decode('utf-8'))
        assert add_event_response['status code'] == 200
        assert add_event_response['message'] == "Set current screen successfully"
        screenID = add_event_response['screenID']
        assert isinstance(screenID, int)
        delete_screen_from_database(screenID)
    except Exception as err:
        traceback.print_exc()
        assert False




