import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL

from config import DRAFTKINGS_NBA
from data_model.nba.data_manipulation.adding_data_to_base_tables.add_data_to_game_table import add_data_to_game_table
from data_model.nba.model import Base, BasketballReferenceBoxscore
from data_model.nba.data_manipulation.adding_data_to_base_tables.add_data_to_position_table import add_data_to_position_table
from data_model.nba.data_manipulation.adding_data_to_base_tables.add_data_to_team_table import add_data_to_team_table
from data_model.nba.data_manipulation.adding_data_to_base_tables.add_data_to_player_table import add_data_to_player_table
from data_model.nba.data_manipulation.adding_data_to_base_tables.add_data_to_boxscore_table import add_data_to_boxscore_table


mysql_connection = create_engine(URL(**DRAFTKINGS_NBA))
BasketballReferenceBoxscore.__table__.drop(mysql_connection)
BasketballReferenceBoxscore.__table__.create(mysql_connection)
try:
    add_data_to_boxscore_table()
except sqlalchemy.exc.IntegrityError as error_message:
    print "Tried to Insert Duplicate Data"



