from sqlalchemy import (Column,Integer,VARCHAR,Float)

from sqlalchemy.ext.declarative import declarative_base

Base=declarative_base()

class IMDB(Base):
    __tablename__='imdb_info'
    imdb_id=Column(Integer,primary_key=True,autoincrement=True)
    _id=Column(VARCHAR(100))
    popularity=Column(Float)
    director=Column(VARCHAR(100))
    genre=Column(VARCHAR(100))
    imdb_score=Column(Float)
    name=Column(VARCHAR(100))
    awards_won=Column(Integer)
    runtime_minutes=Column(Float)