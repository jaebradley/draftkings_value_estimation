import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL

from config import DRAFTKINGS_NBA
from persistence.nba.model import BoxScore
from persistence.nba.data_manipulation.adding_data_to_base_tables.add_data_to_boxscore_table import add_data_to_boxscore_table


mysql_connection = create_engine(URL(**DRAFTKINGS_NBA))
BoxScore.__table__.drop(mysql_connection)
BoxScore.__table__.create(mysql_connection)
try:
    add_data_to_boxscore_table()
except sqlalchemy.exc.IntegrityError as error_message:
    print "Tried to Insert Duplicate Data"



