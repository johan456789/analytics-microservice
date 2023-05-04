from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from ..models import Screen, Session
from ..database import session

router = APIRouter()


def get_screen_name(screen_id: int):
    """
    Get the screen name for a given screen ID
    """
    screen = session.query(Screen).filter_by(screenID=screen_id).first()
    if screen:
        return screen.screenName
    else:
        return JSONResponse(content={"message": "Screen not found."})


def get_total_screen_time(screen_id: int):
    """
    Calculate the total screen time for a given screen ID
    """
    screens = session.query(Screen).filter_by(screenID=screen_id).all()
    total_screen_time = 0
    for scr in screens:
        if scr.startTime and scr.endTime:
            total_screen_time += (scr.endTime - scr.startTime).total_seconds()
    return total_screen_time


def get_average_screen_time_per_session(screen_id: int):
    """
    Get the average screen time per session for a given screen ID
    """
    screens = session.query(Screen).filter_by(screenID=screen_id).all()
    total_session_count = len(screens)
    total_screen_time = get_total_screen_time(screen_id)
    if total_session_count > 0:
        average_screen_time_per_session = total_screen_time / total_session_count
        return average_screen_time_per_session
    else:
        return 0

@router.get("/screen_time/{screen_id}", response_model=None)
def get_screen_time_statistics(screen_id: int) -> JSONResponse:
    """
    Get screen statistics for a given screen ID
    """
    try:
        screen_name = get_screen_name(screen_id)
        total_screen_time = get_total_screen_time(screen_id)
        average_screen_time_per_session = get_average_screen_time_per_session(screen_id)
        return JSONResponse(content={
            "screen_id": screen_id,
            "screen_name": screen_name,
            "total_screen_time(sec)": total_screen_time,
            "average_screen_time_per_session(sec)": average_screen_time_per_session
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail='Failed to retrieve screen time statistics.')

@router.get("/screen_time/{user_id}/{screen_id}", response_model=None)
def get_user_screen_time(user_id: str, screen_id: int) -> JSONResponse:
    """
    Get the total screen time for a given user and screen ID
    """
    try:
        # Get all sessions for the given user
        sessions = session.query(Session).filter(Session.userID == user_id).all()
        if not sessions:
            return JSONResponse(status_code=404, content={"message": "User not Found."})
        total_screen_time = 0
        for s in sessions:
            # Get all sessions with the given screen ID
            screens = session.query(Screen).filter(Screen.screenID == screen_id).all()
            for scr in screens:
                # Calculate total screen time
                if scr.startTime and scr.endTime:
                    total_screen_time += (scr.endTime - scr.startTime).total_seconds()

        # Return total screen time in seconds
        return JSONResponse(content={"user_id": user_id, "screen_id": screen_id, "screen_time(sec)": total_screen_time})
    except Exception as e:
        raise HTTPException(status_code=500, detail='Failed to retrieve screen time.')
