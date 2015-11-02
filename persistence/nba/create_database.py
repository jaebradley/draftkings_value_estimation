def create_database(postgres_engine):
    connection = postgres_engine.connect()
    connection.execute("CREATE DATABASE draftkings_nba")
    connection.close()
