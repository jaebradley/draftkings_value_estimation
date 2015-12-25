from postgres_connector import PostgresConnector

db_connector = PostgresConnector("postgres", "localhost", "5432", "nba", "postgresql://localhost/nba")
db_connection = db_connector.create_database_connection()
db_session = db_connector.create_database_session()