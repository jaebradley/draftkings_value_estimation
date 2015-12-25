from datetime import datetime
from pytz import utc

from persistence.nba.data.inserters.players import PlayerInserter
from persistence.nba.data.inserters.box_scores import BoxScoreInserter
from persistence.nba.data.database_connector import db_session


def insert_data():
    player_inserter = PlayerInserter()
    player_inserter.insert_players(db_session, 2015)
    box_score_inserter = BoxScoreInserter()
    box_score_inserter.insert_box_scores(db_session, datetime(2015, 10, 10), datetime.now(utc))