# ItemCreate: the data required to create an item. 
# Item: the data that is returned when the items are queried.
# ItemBase: the fields that are common to ItemCreate and Item. This is to avoid duplication.
from pydantic import BaseModel
from typing import Optional


class InsertUserItem(BaseModel):
    userID: str

class RecordSessionItem(BaseModel):
    userID: str
    sessionID: str
    startTime: str
    endTime: Optional[str]=None


class EndTimeItem(BaseModel):
    userID: str
    sessionID: str
    endTime: str

class RecordEventItem(BaseModel):
    sessionID: str
    eventName: str
    occurTime: str


class RecordScreenItem(BaseModel):
    sessionID: str
    screenName: str
    startTime: str


class CloseScreenItem(BaseModel):
    screenID: int
    sessionID: str
    screenName: str
    endTime: str