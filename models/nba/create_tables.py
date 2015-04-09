from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from models.nba.config import DRAFTKINGS_NBA
from models.nba.model import Base
from models.nba.data_manipulation.add_data_to_position_table import add_data_to_position_table

mysql_connection = create_engine(URL(**DRAFTKINGS_NBA))
Base.metadata.drop_all(mysql_connection)
Base.metadata.create_all(mysql_connection)
add_data_to_position_table()



