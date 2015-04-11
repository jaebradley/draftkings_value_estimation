from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL

from config import SERVER


mysql_connection = create_engine(URL(**SERVER))
mysql_connection.execute("CREATE DATABASE draftkings_nba")
