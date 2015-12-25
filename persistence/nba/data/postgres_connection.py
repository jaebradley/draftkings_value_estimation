from persistence.nba.data.database_connection import DatabaseConnection
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL

class PostgresConnection(DatabaseConnection):

    def __init__(self, driver_name, host, port, database, server):
        DatabaseConnection.__init__(self, driver_name, host, port, database, server)

    def create_database_connection(self):
        return create_engine(URL(drivername=self.driver_name, host=self.host, port=self.port, database=self.database))
