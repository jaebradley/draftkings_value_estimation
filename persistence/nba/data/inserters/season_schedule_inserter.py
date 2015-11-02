# read from file
# create objects
# insert objects into db

from persistence.nba.data.file_readers.schedule import return_schedule_from_json_encoded_schedule
from sqlalchemy.orm import sessionmaker
from persistence.nba.model import Team, Game


def insert_json_encoded_schedule_into_database(json_encoded_schedule, postgres_engine):
    schedule = return_schedule_from_json_encoded_schedule(json_encoded_schedule=json_encoded_schedule)
    session = sessionmaker(bind=postgres_engine)
    insert_session = session()
    for event in schedule.parsed_event_list:
        home_team_object = insert_session.query(Team).filter_by(name=event.home_team_name).one()
        away_team_object = insert_session.query(Team).filter_by(name=event.visiting_team_name).one()
        game = Game(home_team=home_team_object.id, away_team=away_team_object.id, date=event.)
        insert_session.add(game)
        insert_session.commit()
