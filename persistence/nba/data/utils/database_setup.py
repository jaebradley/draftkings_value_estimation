from persistence.nba.model import Base


def reset_database(postgres_engine):
    connection = postgres_engine.connect()
    connection.execute("DROP DATABASE draftkings_nba")
    connection.execute("CREATE DATABASE draftkings_nba")
    connection.close()


def reset_tables(postgres_engine):
    Base.metadata.drop_all(postgres_engine)
    Base.metadata.create_all(postgres_engine)
