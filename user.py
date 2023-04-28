from pydantic import BaseModel
import uuid
from main import *
from session import user_exists
from sqlalchemy.orm import declarative_base

Base = declarative_base()
from fastapi.testclient import TestClient

class InsertUserItem(BaseModel):
    userID: str


app = FastAPI()


db_connection = create_db_connection()
Session = sessionmaker(bind=db_connection)
db_session = Session()


return_response_400 = {
    "missing_userID_field":{"status code":400, "message":"Missing field: userID"},
    "userID_is_not_UUID":{"status code":400, "message":"Provided userID is not UUID"},
    "user_exists_already":{"status code":400, "message":"User with the provided userID already exists"}
}


return_response_200 = {
    "added_user":{"status code":200, "message":"Added user successfully"}
}


"""
Why use it:
    To insert a User with userID into the User database
"""
@app.post("/api/analysis/add-user/")
async def record_user(item:InsertUserItem):
    try:
        if item.userID is None or item.userID == "":
            return JSONResponse(status_code=400,content=return_response_400["missing_userID_field"])
        if not is_valid_uuid(item.userID):
            return JSONResponse(status_code=400, content=return_response_400["userID_is_not_UUID"])
        else:
            if user_exists(item.userID):
                return JSONResponse(status_code=400, content=return_response_400["user_exists_already"])
            new_user = UserTable(userID=item.userID)
            db_session.add(new_user)
            db_session.commit()
            return JSONResponse(status_code=200, content=return_response_200["added_user"])
    except Exception as e:
        print(e)
        db_session.rollback()
        raise HTTPException(status_code=500, content={"status_code":500, "message":str(e)})


def is_valid_uuid(uuid_string):
    try:
        uuid_obj = uuid.UUID(uuid_string)
    except ValueError:
        return False
    return str(uuid_obj) == uuid_string


def delete_user_from_database(user_uuid):
    try:
        user = db_session.query(UserTable).filter_by(userID=user_uuid).first()
        db_session.delete(user)
        db_session.commit()
        db_session.close()
    except Exception as e:
        print(e)
        traceback.print_exc()
        db_session.rollback()


