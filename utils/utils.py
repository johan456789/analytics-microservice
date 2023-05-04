import traceback
from src.models import User, Session
from src.database import session

def delete_user_from_database(user_uuid):
    """
    Use it to delete this user in the database whose userID matches the parameter user_uuid
    """
    try:
        user = session.query(User).filter_by(userID=user_uuid).first()
        session.delete(user)
        session.commit()
        session.close()
    except Exception as e:
        print(e)
        traceback.print_exc()
        session.rollback()

def delete_session_from_database(sessionID):
    """
    Use it to delete a session row in the database whose session id matches the given sessionID
    """
    try:
        target_session = session.query(Session).filter_by(sessionID=sessionID).first()
        session.delete(target_session)
        session.commit()
        session.close()
    except Exception as e:
        print(e)
        traceback.print_exc()
        session.rollback()

def user_exists(targetUserID):
    """
    Use it to check if a user whose userID matches the targetUserID exists in the User table
    """
    user_exists_result = session.query(User).filter_by(userID=targetUserID).first() is not None
    return user_exists_result
