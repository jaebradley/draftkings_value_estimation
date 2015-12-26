from persistence.nba.table_builder import TableBuilder
from persistence.nba.data.inserters.schedules import ScheduleInserter
from persistence.nba.data.inserters.players import PlayerInserter
from persistence.nba.data.inserters.box_scores import BoxScoreInserter
from persistence.nba.data.database_connector import db_session
from datetime import datetime
from pytz import utc


def build_tables():
    table_builder = TableBuilder()
    table_builder.build_table("nba/data/static/teams/nba_team_name_map.csv")

    schedule_inserter = ScheduleInserter()
    schedule_inserter.insert_schedules(db_session, 2015, 2015)

    player_inserter = PlayerInserter()
    player_inserter.insert_players(db_session, 2015)

    box_score_inserter = BoxScoreInserter()
    box_score_inserter.insert_box_scores(db_session, datetime(2015, 10, 1), datetime.now(utc).date())

build_tables()