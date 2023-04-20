from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional

from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Item(BaseModel):
    userID: str
    sessionID: str
    startTime: str
    endTime: Optional[str]=None


class endTimeItem(BaseModel):
    userID: str
    sessionID: str
    endTime: str


class user(Base):
    __tablename__ = 'user'
    userID = Column(VARCHAR, primary_key=true)


class session(Base):
    __tablename__ = 'session'
    sessionID = Column(VARCHAR, primary_key=true)
    userID = Column(VARCHAR, ForeignKey('user.userID'))
    startTime = Column(VARCHAR, nullable=False)
    endTime = Column(VARCHAR, nullable=True)

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
    "endTime_already_exists":{"status code":400,"message":"endTime already exists"},
    "missing_endTime":{"status code":400, "message":"missing required field: endTime"}
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


app = FastAPI()

'''
Why use it:
    To store a session into the database
Parameters in JSON body:
    userID (required): The user's ID that owns the session
    sessionID (required): The session's user ID
    startTime (required): The starting time of the session
'''
@app.post("/api/analysis/record-session-start-time/")
async def record_session_start_time(item:Item):
    # try:
    if item.userID is None or item.userID == "":
        return JSONResponse(status_code=400,content=return_response_400["missing_userID"])
    if item.sessionID is None or item.sessionID == "":
        return JSONResponse(status_code=400,content=return_response_400["missing_sessionID"])
    if item.startTime is None or item.startTime == "":
        return JSONResponse(status_code=400,content=return_response_400["missing_startTime"])
    else:
        print(item.endTime)
        if not getUser(item.userID):
            return JSONResponse(status_code=400,content=return_response_400["user_not_found"])
        if userSessionExists(item.userID, item.sessionID):
            return JSONResponse(status_code=400,content=return_response_400["session_already_exists"])
        else:
            recorded_session = session(sessionID=item.sessionID,userID=item.userID,startTime=item.startTime, endTime=item.endTime)
            db_session=getSession()
            db_session.add(recorded_session)
            db_session.commit()
            return JSONResponse(status_code=200, content=return_response_200["recorded_session_start_time"])
    # except Exception as e:
    #     print("Here")
    #     print(e)
        # raise HTTPException(status_code=500, detail={"status_code":500, "message":str(e)})


'''
Why use this:
    To update the end time of a session into the database
JSON body:
    userID: VARCHAR. The ID of the user that the session belongs to 
    sessionID: VARCHAR. The ID of the updated session row
    endTime: DATETIME. The end time of the session
'''
@app.post("/api/analysis/record-session-end-time/")
async def record_session_end_time(item:endTimeItem):
    if item.userID is None or item.userID == "":
        return JSONResponse(status_code=400,content=return_response_400["missing_userID"])
    if item.sessionID is None or item.sessionID == "":
        return JSONResponse(status_code=400,content=return_response_400["missing_sessionID"])
    if item.endTime is None or item.endTime == "":
        return JSONResponse(status_code=400,content=return_response_400["missing_endTime"])
    else:
        #check user
        if not getUser(item.userID):
            return JSONResponse(status_code=400,content=return_response_400["user_not_found"])
        #check session
        if not userSessionExists(item.userID, item.sessionID):
            return JSONResponse(status_code=400,content=return_response_400["session_not_exists"])
        #check if that row already has endTime
        if endTimeExists(item.userID, item.sessionID):
            return JSONResponse(status_code=400, content=return_response_400["endTime_already_exists"])
        #update endTime from null to the provided one
        updateSessionEndTime(item)
        return JSONResponse(status_code=200, content=return_response_200["recorded_session_end_time"])


def getEngine():
    return create_engine("mysql+pymysql://root:cMgpBzyj3m2KX9OD35s2@containers-us-west-145.railway.app:5515/dev")


def getSession():
    engine = getEngine()
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

def getUser(targetValue):
    db_session = getSession()
    user_exists = db_session.query(user).filter_by(userID=targetValue).first() is not None
    return user_exists

def userSessionExists(targetUserID, targetSessionID):
    db_session = getSession()
    result = db_session.query(session).filter(session.userID==targetUserID, session.sessionID==targetSessionID)
    return len(result.all())==1 

def endTimeExists(targetUserID, targetSessionID):
    db_session = getSession()
    result = db_session.query(session).filter(session.userID==targetUserID, session.sessionID==targetSessionID)
    for row in result:
        return row.endTime is not None


def updateSessionEndTime(item:endTimeItem):
    db_session = getSession()
    row = db_session.query(session).filter_by(sessionID=item.sessionID).first()
    row.endTime = item.endTime
    db_session.commit()

