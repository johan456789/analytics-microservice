from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

# Create SQLAlchemy models
Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    userID = Column(String(40))


class Event(Base):
    __tablename__ = 'event'
    eventID = Column(Integer, primary_key=True)
    eventName = Column(String(45))
    occurTime = Column(DateTime)
    sessionID = Column(String(40))

class SessionTable(Base):
    __tablename__ = 'session'
    sessionID = Column(String(40), primary_key=True)
    userID = Column(String(40))
    startTime = Column(DateTime)
    endTime = Column(DateTime)

class Screen(Base):
    __tablename__ = 'screen'
    screenID = Column(Integer, primary_key=True)
    endTime = Column(DateTime)
    startTime = Column(DateTime)
    screenName = Column(String(50))
    sessionID = Column(String(40))

# Function to establish a connection to the MySQL database
def create_db_connection():
    try:
        engine = create_engine('mysql://root:cMgpBzyj3m2KX9OD35s2@containers-us-west-145.railway.app:5515/dev')
        return engine
    except Exception as e:
        raise HTTPException(status_code=500, detail='Failed to connect to MySQL database.')

engine = create_db_connection()

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Insert test data into the database
# def insert_test_data():
#     # Add a test user
#     test_user = User(userID='U8765432')
#     session.add(test_user)
#     session.commit()

#     # Add a test session for the user
#     test_session = SessionTable(sessionID='S2345678', userID='U8765432', startTime=datetime.now(), endTime=datetime.now())
#     session.add(test_session)
#     session.commit()

#     # Add a test screen for the session
#     test_screen = Screen(screenName='SCR00221', startTime=datetime.now(), endTime=datetime.now(), sessionID='S2345678')
#     session.add(test_screen)
#     session.commit()

#     print("Test data inserted successfully.")

# insert_test_data()