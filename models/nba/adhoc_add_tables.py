import sqlalchemy
from sqlalchemy import Table, MetaData
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from models.nba.config import DRAFTKINGS_NBA
from models.nba.model import Base, Position
from models.nba.data_manipulation.add_data_to_position_table import add_data_to_position_table
from models.nba.data_manipulation.add_data_to_game_table import add_data_to_game_table
from models.nba.data_manipulation.add_data_to_team_table import add_data_to_team_table
from models.nba.data_manipulation.add_data_to_player_table import add_data_to_player_table
from models.nba.model import Player

mysql_engine = create_engine(URL(**DRAFTKINGS_NBA))
metadata = MetaData()
player_table = Table("player", metadata)
player_table.drop(mysql_engine)

try:
    add_data_to_player_table()
except sqlalchemy.exc.IntegrityError as error_message:
    print "Tried to Insert Duplicate Data"




