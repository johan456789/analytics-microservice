from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
from main import *

app = FastAPI()

# Calculate the average engagement time for a given user for the selected time period
@app.get("/average-engagement/{user_id}", response_model=None)
def get_average_engagement(user_id: str, time_period: str) -> JSONResponse:
    try:
        # Get the sessions for the user
        sessions = session.query(SessionTable).filter_by(userID=user_id).all()

        # Calculate the total engagement time for the user for the selected time period
        total_engagement_time = timedelta()
        selected_sessions = []
        for s in sessions:
            if s.startTime >= datetime.now() - timedelta(days=7):
                selected_sessions.append(s)
                if s.startTime and s.endTime:
                    total_engagement_time += s.endTime - s.startTime

        # Calculate the average engagement time
        if len(selected_sessions) > 0:
            average_engagement_time = total_engagement_time / len(selected_sessions)
            return JSONResponse(content={"user_id": user_id, "average_engagement_time": average_engagement_time.total_seconds()})
        else:
            return JSONResponse(content={"user_id": user_id, "average_engagement_time": 0})
    except Exception as e:
        raise HTTPException(status_code=500, detail='Failed to retrieve average engagement time.')
