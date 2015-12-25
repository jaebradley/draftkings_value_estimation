from basketball_reference_web_scraper.readers import return_all_player_season_statistics
from sqlalchemy.orm.exc import NoResultFound

from persistence.nba.data.utils.functions import get_or_create
from persistence.nba.model import Position, Team, Player


class PlayerInserter:
    def __init__(self):
        pass

    def insert_players(self, session, season_start_year):
        player_season_statistics = return_all_player_season_statistics(season_start_year=season_start_year)
        for player_season in player_season_statistics:
            team = session.query(Team).filter(Team.abbreviation == player_season.team).one()
            try:
                position = session.query(Position).filter(Position.abbreviation == player_season.position).one()
                get_or_create(session, Player, first_name=player_season.first_name, last_name=player_season.last_name, team=team.id, position=position.id)
            except NoResultFound:
                print player_season.position