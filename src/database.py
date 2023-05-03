from fastapi import HTTPException
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()
DB_CONNECTION_STRING = os.getenv('DB_CONNECTION_STRING', '')
Base = declarative_base()


def create_db_connection():
    '''
    establish a connection to the MySQL database
    '''
    try:
        engine = create_engine(DB_CONNECTION_STRING)
        return engine
    except Exception as e:
        print(f'Error: {e}')
        raise HTTPException(status_code=500, detail='Failed to connect to MySQL database.')

def create_db_session():
    '''
    create a instance of session to the MySQL database
    '''
    engine = create_db_connection()
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)

    return Session()

session = create_db_session()
