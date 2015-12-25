from sqlalchemy.exc import IntegrityError

from persistence.nba.data.database_connector import db_connection, db_session
from persistence.nba.data.inserters.positions import PositionInserter
from persistence.nba.data.inserters.teams import TeamInserter
from persistence.nba.model import Base


class TableBuilder:
    def __init__(self):
        pass

    def build_table(self, team_name_csv):
        Base.metadata.drop_all(db_connection)
        Base.metadata.create_all(db_connection)
        position_inserter = PositionInserter()
        team_inserter = TeamInserter()
        try:
            position_inserter.insert_positions(db_session)
            team_inserter.insert_teams(db_session, team_name_csv)
        except IntegrityError:
            print "Tried to Insert Duplicate Data"