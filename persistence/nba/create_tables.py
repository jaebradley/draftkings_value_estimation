import sqlalchemy
from persistence.nba.data.inserters.positions import positions
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL

from config import DRAFTKINGS_NBA
from persistence.nba.data.inserters.teams import teams
from persistence.nba.model import Base

mysql_connection = create_engine(URL(**DRAFTKINGS_NBA))
Base.metadata.drop_all(mysql_connection)
Base.metadata.create_all(mysql_connection)
try:
    positions()
    teams("data/static/teams/nba_team_name_map.csv")
except sqlalchemy.exc.IntegrityError as error_message:
    print "Tried to Insert Duplicate Data"



