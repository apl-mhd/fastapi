from math import fabs
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import time

import psycopg2
from psycopg2.extras import RealDictCursor

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:admin@localhost/fastapi'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()



while True:
    try:
        conn =  psycopg2.connect(host='localhost', database='fastapi', user='postgres',
                                password='admin', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('database successfully connected')
        break

    except Exception as error:
        print("Connecting to database failed")
        print("error", error)
        time.sleep(2)
        

def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()