from basketball_reference_web_scraper.readers import return_all_player_season_statistics
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound

from persistence.nba.config import DRAFTKINGS_NBA
from persistence.nba.data.utils.functions import get_or_create
from persistence.nba.model import Position, Team, Player


def main(season_start_year):
    connection = create_engine(URL(**DRAFTKINGS_NBA))
    session = sessionmaker(bind=connection)
    insert_session = session()
    player_season_statistics = return_all_player_season_statistics(season_start_year=season_start_year)
    for player_season in player_season_statistics:
        team = insert_session.query(Team).filter(Team.abbreviation == player_season.team).one()
        try:
            position = insert_session.query(Position).filter(Position.abbreviation == player_season.position).one()
            get_or_create(insert_session, Player, first_name=player_season.first_name, last_name=player_season.last_name, team=team.id, position=position.id)
        except NoResultFound:
            print player_season.position

main(2015)