import csv
import os

from sqlalchemy import create_engine, or_, and_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL

from config import DRAFTKINGS_NBA
from models.nba.model import Team, Player, Game, BasketballReferenceBoxscore


def add_data_to_boxscore_table():

    mysql_connection = create_engine(URL(**DRAFTKINGS_NBA))
    session = sessionmaker(bind=mysql_connection)
    insert_session = session()

    for file in os.listdir("data_files/boxscores/"):
        filepath = "data_files/boxscores/{0}".format(file)
        with open(filepath) as file:
            print "Reading from {0}".format(filepath)
            reader = csv.reader(file)
            boxscore_list = list(reader)[1:]

            for player_boxscore in boxscore_list:

                first_name = player_boxscore[0]
                last_name = player_boxscore[1]
                date = player_boxscore[2]
                team_abbreviation = player_boxscore[3]
                opponent_abbreviation = player_boxscore[4]
                seconds_played = player_boxscore[5]
                made_field_goals = player_boxscore[6]
                attempted_field_goals = player_boxscore[7]
                made_three_point_field_goals = player_boxscore[8]
                attempted_three_point_field_goals = player_boxscore[9]
                made_free_throws = player_boxscore[10]
                attempted_free_throws = player_boxscore[11]
                offensive_rebounds = player_boxscore[12]
                defensive_rebounds = player_boxscore[13]
                total_rebounds = player_boxscore[14]
                assists = player_boxscore[15]
                steals = player_boxscore[16]
                blocks = player_boxscore[17]
                turnovers = player_boxscore[18]
                fouls_committed = player_boxscore[19]
                points = player_boxscore[20]
                draftkings_score = player_boxscore[21]

                try:
                    team_object = insert_session.query(Team).filter(Team.abbreviation==team_abbreviation).one()
                    opponent_object = insert_session.query(Team).filter(Team.abbreviation==opponent_abbreviation).one()
                    player_object = insert_session.query(Player).filter(and_(Player.first_name==first_name, Player.last_name ==last_name, Player.team == team_object.id)).one()
                    game_object = insert_session.query(Game).filter(Game.date==date).filter(and_(or_(Game.home_team == team_object.id, Game.away_team == team_object.id),or_(Game.home_team == opponent_object.id, Game.away_team == opponent_object.id))).one()
                    boxscore_object = BasketballReferenceBoxscore(
                        player=player_object.id,
                        game=game_object.id,
                        date=date,
                        seconds_played=seconds_played,
                        made_field_goals=made_field_goals,
                        attempted_field_goals=attempted_field_goals,
                        made_three_point_field_goals=made_three_point_field_goals,
                        attempted_three_point_field_goals=attempted_three_point_field_goals,
                        made_free_throws=made_free_throws,
                        attempted_free_throws=attempted_free_throws,
                        offensive_rebounds=offensive_rebounds,
                        defensive_rebounds=defensive_rebounds,
                        total_rebounds=total_rebounds,
                        assists=assists,
                        steals=steals,
                        blocks=blocks,
                        turnovers=turnovers,
                        fouls_committed=fouls_committed,
                        points=points,
                        draftkings_score=draftkings_score
                    )
                    insert_session.add(boxscore_object)
                    insert_session.commit()
                except Exception as error_message:
                    print "Error:{0} for {1} {2}".format(error_message, first_name, last_name)
                    continue


