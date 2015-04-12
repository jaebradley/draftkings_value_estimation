import sqlalchemy
from sqlalchemy import Table, MetaData
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL

from config import DRAFTKINGS_NBA
from data_model.nba.data_manipulation.adding_data_to_base_tables import add_data_to_player_table


mysql_engine = create_engine(URL(**DRAFTKINGS_NBA))
metadata = MetaData()
player_table = Table("player", metadata)
player_table.drop(mysql_engine)

try:
    add_data_to_player_table()
except sqlalchemy.exc.IntegrityError as error_message:
    print "Tried to Insert Duplicate Data"




