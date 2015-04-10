from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.engine.url import URL
from sqlalchemy.sql.expression import delete
from models.nba.config import DRAFTKINGS_NBA
from models.nba.model import Team, Game
import csv


def add_data_to_game_table():

    mysql_connection = create_engine(URL(**DRAFTKINGS_NBA))
    session = sessionmaker(bind=mysql_connection)
    insert_session = session()
    with open('data_files/nba_schedule.txt') as file:
        reader = csv.reader(file)
        nba_schedule_list = list(reader)[1:]
        insert_nba_schedule_list = list()
        for game in nba_schedule_list:
            home_team = game[2]
            away_team = game[1]
            date = game[0]
            home_team_object = insert_session.query(Team).filter_by(name=home_team).one()
            away_team_object = insert_session.query(Team).filter_by(name=away_team).one()
            game = Game(home_team=home_team_object.id, away_team=away_team_object.id, date=date)
            insert_session.add(game)
            insert_session.commit()


