# Incomplete because Draftkings doesn't do a really good job at passing back the team that a player plays for
import csv
import os
import sqlalchemy

from sqlalchemy import create_engine, or_, and_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL

from config import DRAFTKINGS_NBA
from persistence.nba.model import Game, Player, DraftkingsPlayerSalary

def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance

def add_data_to_draftkings_salary_table():

    mysql_connection = create_engine(URL(**DRAFTKINGS_NBA))
    session = sessionmaker(bind=mysql_connection)
    insert_session = session()

    for file in os.listdir("data_files/draftkings_salary/"):
        filepath = "data_files/draftkings_salary/{0}".format(file)
        with open(filepath) as file:
            reader = csv.reader(file)
            draftkings_salary_list = list(reader)[1:]
            for player_salary in draftkings_salary_list:

                first_name = player_salary[1]
                last_name = player_salary[2]
                salary = player_salary[3]
                date = player_salary[4]

                #should really query with a team object, but not passed back by draftkings so first_name and last_name SHOULD be enough
                #might pick wrong player if more than one player has the same name
                print first_name, last_name
                player_object = insert_session.query(Player).filter(Player.first_name == first_name, Player.last_name == last_name).one()
                game_object = insert_session.query(Game).filter(Game.date == date).filter(or_(Game.home_team == player_object.team, Game.away_team == player_object.team)).one()
                print player_object.first_name, player_object.last_name, game_object.id
                try:
                    get_or_create(insert_session, DraftkingsPlayerSalary, player=player_object.id, game=game_object.id, salary=salary)
                except sqlalchemy.exc.IntegrityError as error_message:
                    print error_message
                    continue
