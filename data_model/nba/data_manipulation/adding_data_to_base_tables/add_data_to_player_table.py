import csv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL

from config import DRAFTKINGS_NBA
from data_model.nba.model import Team, Player, Position


def add_data_to_player_table():

    mysql_connection = create_engine(URL(**DRAFTKINGS_NBA))
    session = sessionmaker(bind=mysql_connection)
    insert_session = session()

    with open('data_files/player_position.csv') as file:
        reader = csv.reader(file)
        nba_player_list = list(reader)[1:]
        for player in nba_player_list:

            first_name = player[0]
            last_name = player[1]
            position = player[2]
            team_abbreviation = player[3]

            team_object = insert_session.query(Team).filter_by(abbreviation=team_abbreviation).one()
            position_object = insert_session.query(Position).filter_by(abbreviation=position).one()

            player = Player(first_name=first_name, last_name=last_name, team=team_object.id, position=position_object.id)
            insert_session.add(player)
            insert_session.commit()


