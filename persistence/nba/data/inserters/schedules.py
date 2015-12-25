from basketball_reference_web_scraper.readers import return_schedule

from persistence.nba.data.utils.functions import get_or_create
from persistence.nba.model import Team, Game


class ScheduleInserter:
    def __init__(self):
        pass

    def insert_schedules(self, session, first_season_start_year, last_season_start_year):
        for season_start_year in range(first_season_start_year, last_season_start_year + 1):
            season_schedule = return_schedule(season_start_year)
            for event in season_schedule.parsed_event_list:
                home_team = session.query(Team).filter_by(name=event.home_team_name).one()
                away_team = session.query(Team).filter_by(name=event.visiting_team_name).one()
                get_or_create(session, Game, home_team=home_team.id, away_team=away_team.id, start_time=event.start_time)