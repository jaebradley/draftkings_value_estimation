import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL

from config import DRAFTKINGS_NBA
from persistence.nba.data.manipulation.adding_data_to_base_tables.add_data_to_position_table import add_data_to_position_table
from persistence.nba.data.manipulation.adding_data_to_base_tables.add_data_to_team_table import add_data_to_team_table
from persistence.nba.model import Base

mysql_connection = create_engine(URL(**DRAFTKINGS_NBA))
Base.metadata.drop_all(mysql_connection)
Base.metadata.create_all(mysql_connection)
try:
    add_data_to_position_table()
    add_data_to_team_table("data/static/teams/nba_team_name_map.csv")
except sqlalchemy.exc.IntegrityError as error_message:
    print "Tried to Insert Duplicate Data"



