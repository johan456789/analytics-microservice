from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
from main import *

app = FastAPI()

# Fetch total screen time for a given screen for a given user
@app.get("/screenTime/{user_id}/{screen_id}", response_model=None)
def get_user_screen_time(user_id: str, screen_id: int) -> JSONResponse:
    try:
        screen = session.query(Screen).join(SessionTable, Screen.sessionID == SessionTable.sessionID).filter(SessionTable.userID == user_id, Screen.screenID == screen_id).first()

        if screen:
            # Calculate total screen time for the screen
            if screen.startTime and screen.endTime:
                total_screen_time = screen.endTime - screen.startTime + timedelta(minutes=10)

                # Return total screen time in seconds
                return JSONResponse(content={"user_id": user_id, "screen_id": screen_id, "screen_time": total_screen_time.total_seconds()})
            else:
                return JSONResponse(content={"user_id": user_id, "screen_id": screen_id, "screen_time": 0})
        else:
            return JSONResponse(content={"user_id": user_id, "screen_id": screen_id, "screen_time": 0})
    except Exception as e:
        raise HTTPException(status_code=500, detail='Failed to retrieve screen time.')
