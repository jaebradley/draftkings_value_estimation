from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.engine.url import URL
from sqlalchemy.sql.expression import delete
from models.nba.config import DRAFTKINGS_NBA
from models.nba.model import Position

def add_data_to_position_table():

    position_list = [
        {
            'name': 'Point Guard',
            'abbreviation': 'PG'
        },
        {
            'name': 'Shooting Guard',
            'abbreviation': 'SG'
        },
        {
            'name': 'Small Forward',
            'abbreviation': 'SF'
        },
        {
            'name': 'Power Forward',
            'abbreviation': 'PF'
        },
        {
            'name': 'Center',
            'abbreviation': 'C'
        }
    ]

    mysql_connection = create_engine(URL(**DRAFTKINGS_NBA))
    metadata = MetaData(mysql_connection)
    position = Table("position", metadata, autoload=True)
    position_insert = position.insert()
    position_insert.execute(position_list)
