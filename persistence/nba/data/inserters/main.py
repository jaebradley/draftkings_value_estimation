from basketball_reference_web_scraper.readers import return_schedule
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker

from persistence.nba.config import DRAFTKINGS_NBA
from persistence.nba.data.utils.functions import get_or_create
from persistence.nba.model import Team, Game


def main(season_first_start_year, season_last_start_year):
    postgres_engine = create_engine(URL(**DRAFTKINGS_NBA))
    session = sessionmaker(bind=postgres_engine)
    insert_session = session()
    for season_start_year in range(season_first_start_year, season_last_start_year + 1):
        season_schedule = return_schedule(season_start_year)
        for event in season_schedule.parsed_event_list:
            home_team = insert_session.query(Team).filter_by(name=event.home_team_name).one()
            away_team = insert_session.query(Team).filter_by(name=event.visiting_team_name).one()
            get_or_create(insert_session, Game, home_team=home_team.id, away_team=away_team.id, start_time=event.start_time)


main(2014, 2015)