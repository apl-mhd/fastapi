from http import server
from sqlite3 import Timestamp
from time import time
from .database_con import Base
from sqlalchemy import Column, Integer, Boolean, String,TIMESTAMP


class Post(Base):
    __tablename__ = 'posts'
    
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, default=True)
    #created_at = Column(TIMESTAMP(timezone=True), nullable=True, server_default=func.now())
    