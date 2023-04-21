from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
from typing import List
from main import *

app = FastAPI()

# Fetch total screen time for a given user
@app.get("/screenTime/{user_id}", response_model=None)
def get_user_screen_time(user_id: str) -> List[Screen]:
    try:
        screens = session.query(Screen).join(SessionTable, Screen.sessionID == SessionTable.sessionID).filter(SessionTable.userID == user_id).all()
        # Calculate total screen time for the session
        total_screen_time = timedelta()
        for screen in screens:
            if screen.startTime and screen.endTime:
                total_screen_time += screen.endTime - screen.startTime + timedelta(seconds=5)

        # Return total screen time in seconds
        return JSONResponse(content={"user_id": user_id, "screen_time": total_screen_time.total_seconds()})
    except Exception as e:
        raise HTTPException(status_code=500, detail='Failed to retrieve screen time.')