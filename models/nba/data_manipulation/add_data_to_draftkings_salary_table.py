from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.engine.url import URL
from models.nba.config import DRAFTKINGS_NBA
from models.nba.model import Position, Team, Player, Game, DraftkingsPlayerSalary
import csv
import os

def add_data_to_draftkings_salary_table():

    mysql_connection = create_engine(URL(**DRAFTKINGS_NBA))
    session = sessionmaker(bind=mysql_connection)
    insert_session = session()

    for file in os.listdir("../data_files/draftkings_salary/"):
        filepath = "../data_files/draftkings_salary/{0}".format(file)
        with open(filepath) as file:
            reader = csv.reader(file)
            draftkings_salary_list = list(reader)[1:]
            for player_salary in draftkings_salary_list:

                position = player_salary[0]
                first_name = player_salary[1]
                last_name = player_salary[2]
                salary = player_salary[3]
                date = player_salary[4]

                position_object = insert_session.query(Position).filter_by(abbreviation=position).one()
                #should really query with a team object, but not passed back by draftkings so first_name and last_name SHOULD be enough
                #might pick wrong player if more than one player has the same name
                player_object = insert_session.query(Player).filter_by(first_name=first_name, last_name=last_name)
                #home + away = team + opponent
                #concat(home,away) = concat(team,opponent) or concat(opponent,team)
                game_object = insert_session.query(Game).filter_by(date=date).one()
                draftkings_salary_object = DraftkingsPlayerSalary(
                    player=player_object.id,
                    game=game_object.id,
                    salary=salary
                )
                insert_session.add(draftkings_salary_object)
                insert_session.commit()

add_data_to_draftkings_salary_table()
