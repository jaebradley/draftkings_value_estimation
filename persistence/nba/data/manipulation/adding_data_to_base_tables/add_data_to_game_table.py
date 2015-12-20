import csv

from sqlalchemy.orm import sessionmaker
from persistence.nba.model import Team, Game


def add_data_to_game_table(postgres_engine, nba_schedule_file_name):
    session = sessionmaker(bind=postgres_engine)
    insert_session = session()
    with open(nba_schedule_file_name) as file:
        reader = csv.reader(file)
        nba_schedule_list = list(reader)[1:]
        for game in nba_schedule_list:
            home_team = game[2]
            away_team = game[1]
            date = game[0]
            home_team_object = insert_session.query(Team).filter_by(name=home_team).one()
            away_team_object = insert_session.query(Team).filter_by(name=away_team).one()
            game = Game(home_team=home_team_object.id, away_team=away_team_object.id, date=date.start_time)
            insert_session.add(game)
            insert_session.commit()


