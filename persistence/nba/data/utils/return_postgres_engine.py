from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL

from config import SERVER


def return_postgres_engine():
    return create_engine(URL(**SERVER), isolation_level='AUTOCOMMIT')
