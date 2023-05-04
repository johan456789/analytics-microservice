from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
from typing import List
from models import *
from database import session

app = FastAPI()

@app.get('/')
async def root():
    return {'message': 'The analytics service is running.'}
