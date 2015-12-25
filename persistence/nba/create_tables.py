import sqlalchemy

from persistence.nba.data.database_connector import db_connection, db_session
from persistence.nba.data.inserters.positions import PositionInserter
from persistence.nba.data.inserters.teams import insert_teams
from persistence.nba.model import Base


Base.metadata.drop_all(db_connection)
Base.metadata.create_all(db_connection)
position_inserter = PositionInserter()
try:
    position_inserter.insert_positions(db_session)
    insert_teams("data/static/teams/nba_team_name_map.csv")
except sqlalchemy.exc.IntegrityError as error_message:
    print "Tried to Insert Duplicate Data"



