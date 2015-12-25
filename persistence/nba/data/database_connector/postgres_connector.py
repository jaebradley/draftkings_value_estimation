from persistence.nba.data.database_connector.database_connector import DatabaseConnector
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker

class PostgresConnector(DatabaseConnector):

    def __init__(self, driver_name, host, port, database, server):
        DatabaseConnector.__init__(self, driver_name, host, port, database, server)

    def create_database_connection(self):
        return create_engine(URL(drivername=self.driver_name, host=self.host, port=self.port, database=self.database))

    def create_database_session(self):
        return sessionmaker(bind=self.create_database_connection())()