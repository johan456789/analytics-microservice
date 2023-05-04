from datetime import datetime
import traceback
from src.models import Screen, User, Session, Event
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

def is_valid_datetime(datetime_str):
    """
    Use it to check if a datetime is valid.
    The definition of valid: the datetime_str is a UTC time in string format. It must meet the date_format defined
    in the function below, and it needs to be earlier than the current UTC time.
    """
    try:
        date_format = '%Y-%m-%d %H:%M:%S'
        datetime_obj = datetime.strptime(datetime_str, date_format)
        return datetime_obj < datetime.utcnow()
    except ValueError:
        return False

def endTime_conflicts_startTime(startTime, endTime):
    """
    Use it to check if the startTime and endTime conflict, i.e. endTime is earlier than startTime
    """
    date_format = '%Y-%m-%d %H:%M:%S'
    if not isinstance(startTime, datetime):
        startTime = datetime.strptime(startTime, date_format)
    if not isinstance(endTime, datetime):
        endTime = datetime.strptime(endTime, date_format)
    return endTime <= startTime

def deleteEvent(target_event_ID):
    try:
        event = session.query(Event).filter_by(eventID=target_event_ID).first()
        session.delete(event)
        session.commit()
        session.close()
    except Exception as e:
        print(e)
        traceback.print_exc()
        session.rollback()

def userSessionExists(targetSessionID):
    """
    Use this function to check if a session that has the targetSessionID exists in the database
    :param targetSessionID:
    :return: True if there is session that has the targetSessionID, False if there is not.
    """
    result = session.query(Session).filter(Session.sessionID==targetSessionID)
    return len(result.all())==1


def delete_screen_from_database(screen_ID):
    """
    Use it to delete this user in the database whose userID matches the parameter user_uuid
    """
    try:
        screen = session.query(Screen).filter_by(screenID=screen_ID).first()
        session.delete(screen)
        session.commit()
        session.close()
    except Exception as e:
        print(e)
        traceback.print_exc()
        session.rollback()
