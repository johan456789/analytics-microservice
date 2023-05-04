import uuid
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
from typing import List
from ..models import *
from ..schemas import *
from ..database import session
from ..session import user_exists

router = APIRouter()

return_response_200 = {
    "added_user":{"status code":200, "message":"Added user successfully"}
}

# Note: for the 200, it is used for display in the OpenAPI document, the actual 200 return is the return_response_200 above
user_response = {
    200: {"description": "Added user successfully",
          "content": {"application/json": {"example": {"status code": 200, "message":"Added user successfully"}}}},
    411: {"status_code":411,"description": "missing userID"},
    412: {"status_code":412,"description": "userID is not an UUID"},
    413: {"status_code":413,"description": "User with the provided userID already exists"}
}

@router.get("/daily_active_users/{date}")
def get_daily_active_users(date: datetime) -> List[str]:
    '''
    get users who have sessions with start time on the given date
    '''
    try:
        result = session.query(Session.userID).filter(Session.startTime == date).distinct().all()
        return [row.userID for row in result]
    except Exception as e:
        raise HTTPException(status_code=500, detail='Failed to retrieve daily active users.')

@router.get("/weekly_new_users/{date}")
def get_weekly_new_users(date: datetime) -> List[str]:
    '''
    get user who have sessions with start time within the last 14 days
    '''
    try:
        result = session.query(Session.userID).filter(Session.startTime >= date - timedelta(days=14)).distinct().all()
        return [row.userID for row in result]
    except Exception as e:
        raise HTTPException(status_code=500, detail='Failed to retrieve weekly new users.')

@router.get("/monthly_active_users/{date}")
def get_monthly_active_users(date: datetime) -> List[str]:
    '''
    get users who have sessions with start time within the last 30 days
    '''
    try:
        result = session.query(Session.userID).filter(Session.startTime >= date - timedelta(days=60)).distinct().all()
        return [row.userID for row in result]
    except Exception as e:
        raise HTTPException(status_code=500, detail='Failed to retrieve monthly active users.')

@router.post("/api/analysis/add-user/", responses=user_response)
async def record_user(item:InsertUserItem):
    """
    Use it to insert a user with userID into the User database
    """
    try:
        if item.userID is None or item.userID == "":
            raise HTTPException(411, detail=user_response[411])
        if not is_valid_uuid(item.userID):
            raise HTTPException(412, detail=user_response[412])
        else:
            if user_exists(item.userID):
                print("user exists already")
                raise HTTPException(413, detail=user_response[413])
            else:
                new_user = User(userID=item.userID)
                session.add(new_user)
                session.commit()
                return JSONResponse(status_code=200, content=return_response_200["added_user"])
    except Exception as e:
        session.rollback()
        raise e


def is_valid_uuid(uuid_string):
    """
    Use it to check if an id is a valid UUID
    """
    try:
        uuid_obj = uuid.UUID(uuid_string)
    except ValueError:
        return False
    return str(uuid_obj) == uuid_string


