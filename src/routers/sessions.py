from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from ..models import Session
from ..schemas import EndTimeItem, RecordSessionItem
from ..database import session
from utils.utils import endTime_conflicts_startTime, is_valid_datetime, user_exists
import traceback

"""
File description:
This is the file that contains the POST endpoints related to session
"""

"""
What it is:
    A collection of 400 response messages
Why use it:
    In our API response, it will use the key of the return_response_400 to get the corresponding message
"""
return_response_400 = {
    "missing_userID": {"status code":400, "message":"missing required field: userID"},
    "missing_sessionID": {"status code":400, "message":"missing required field: sessionID"},
    "missing_startTime": {"status code":400, "message":"missing required field: startTime"},
    "user_not_found":{"status code":400, "message":"UserID does not exist. User not found"},
    "session_already_exists":{"status code":400, "message":"SessionID already exists"},
    "session_not_exists":{"status code":400, "message":"SessionID does not exists"},
    "user_not_match_session":{"status code":400, "message":"The provided userID does not match the userID that holds the session"},
    "endTime_already_exists":{"status code":400,"message":"endTime already exists"},
    "missing_endTime":{"status code":400, "message":"missing required field: endTime"},
    "invalid_datetime": {"status code": 400, "message": "provided datetime is either not in mysql datetime format nor an invalid datetime"},
    "endTime_conflict_startTime":{"status code":400, "message":"endTime conflicts with startTime"}
}

"""
What it is:
    A collection of 200 response messages
Why use it:
    In our API response, it will use the key of the return_response_400 to get the corresponding message
"""
return_response_200 = {
    "recorded_session_start_time":{"status code":200, "message":"Recorded session start time successfully"},
    "recorded_session_end_time":{"status code":200, "message":"Recorded session end time successfully"}
}




router = APIRouter()


@router.post("/api/analysis/record-session-start-time/")
async def record_session_start_time(item:RecordSessionItem):
    '''
    Use this endpoint to store a session into the database
    '''
    try:
        if item.userID is None or item.userID == "":
            return JSONResponse(status_code=400,content=return_response_400["missing_userID"])
        if item.sessionID is None or item.sessionID == "":
            return JSONResponse(status_code=400,content=return_response_400["missing_sessionID"])
        if item.startTime is None or item.startTime == "":
            return JSONResponse(status_code=400,content=return_response_400["missing_startTime"])
        if not is_valid_datetime(item.startTime):
            return JSONResponse(status_code=400,content=return_response_400["invalid_datetime"])
        else:
            if item.endTime == "":
                item.endTime = None
            if not user_exists(item.userID):
                return JSONResponse(status_code=400,content=return_response_400["user_not_found"])
            if user_session_match(item.userID, item.sessionID):
                return JSONResponse(status_code=400,content=return_response_400["session_already_exists"])
            else:
                recorded_session = Session(sessionID=item.sessionID, userID=item.userID, startTime=item.startTime, endTime=item.endTime)
                session.add(recorded_session)
                session.commit()
                return JSONResponse(status_code=200, content=return_response_200["recorded_session_start_time"])
    except Exception as e:
        traceback.print_exc()
        session.rollback()
        raise HTTPException(status_code=500, detail={"status_code":500, "message":str(e)})



@router.post("/api/analysis/update-session-end-time/")
async def update_session_end_time(item:EndTimeItem):
    '''
    Use this endpoint to update the end time of a session into the database
    '''
    try:
        if item.userID is None or item.userID == "":
            return JSONResponse(status_code=400,content=return_response_400["missing_userID"])
        if item.sessionID is None or item.sessionID == "":
            return JSONResponse(status_code=400,content=return_response_400["missing_sessionID"])
        if item.endTime is None or item.endTime == "":
            return JSONResponse(status_code=400,content=return_response_400["missing_endTime"])
        if not is_valid_datetime(item.endTime):
            return JSONResponse(status_code=400, content=return_response_400["invalid_datetime"])
        else:
            #check user
            session_row = get_session_row_in_session_table(item.sessionID)
            if session_row is None:
                return JSONResponse(status_code=400, content=return_response_400["session_not_exists"])
            #check session
            if session_row.userID != item.userID:
                return JSONResponse(status_code=400,content=return_response_400["user_not_match_session"])
            #check if that row already has endTime
            if session_row.endTime is not None:
                return JSONResponse(status_code=400, content=return_response_400["endTime_already_exists"])
            if endTime_conflicts_startTime(session_row.startTime, item.endTime):
                return JSONResponse(status_code=400, content=return_response_400["endTime_conflict_startTime"])
            #update endTime from null to the provided one
            updateSessionEndTime(item)
            return JSONResponse(status_code=200, content=return_response_200["recorded_session_end_time"])
    except Exception as e:
        traceback.print_exc()
        session.rollback()
        raise HTTPException(status_code=500, detail={"status_code": 500, "message": str(e)})






def get_session_row_in_session_table(target_sessionID):
    """
    Use it to get a session from the database whose sessionID matches the parameter target_sessionID
    """
    result = session.query(Session).filter_by(sessionID=target_sessionID).first()
    return result


def user_session_match(targetUserID, targetSessionID):
    """
    Use it to check if there exists a session whose userID and sessionID match the targetUserID and targetSessionID
    """
    result = session.query(Session).filter(Session.userID == targetUserID, Session.sessionID == targetSessionID)
    return len(result.all())==1 


def endTimeExists(targetUserID, targetSessionID):
    """
    Use it to check if the session row that has the targetSessionID has endTime column filled already.
    """
    result = session.query(Session).filter(Session.userID == targetUserID, Session.sessionID == targetSessionID)
    for row in result:
        return row.endTime is not None


def updateSessionEndTime(item:EndTimeItem):
    """
    Use it to update a session row's endTime in the database
    """
    row = session.query(Session).filter_by(sessionID=item.sessionID).first()
    row.endTime = item.endTime
    session.commit()
