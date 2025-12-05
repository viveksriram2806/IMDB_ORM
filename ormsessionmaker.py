from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy_utils import (create_database,database_exists)
from dotenv import load_dotenv
import os
from models import Base

load_dotenv()



class SessionMaker:
    def get_engine(self):
        user=os.environ["MYSQL_USER"]
        password=os.environ["MYSQL_PASSWORD"]
        host=os.environ["MYSQL_HOST"]
        port=os.environ["MYSQL_PORT"]
        database=os.environ["MYSQL_DATABASE"]

        conn_str=f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}'
        if not database_exists(conn_str):
            create_database(conn_str)
        _engine=create_engine(conn_str)
        Base.metadata.create_all(_engine)
        return _engine

    def get_session(self):
        _engine=self.get_engine()
        _session=sessionmaker(bind=_engine)

        return _session
        
