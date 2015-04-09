from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from models.nba.config import DRAFTKINGS_NBA
from models.nba.model import Base

mysql_connection = create_engine(URL(**DRAFTKINGS_NBA))
Base.metadata.drop_all(mysql_connection)
Base.metadata.create_all(mysql_connection)


