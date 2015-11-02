from persistence.nba.data.inserters.season_schedule_inserter import insert_json_encoded_schedule_into_database
from persistence.nba.data.utils.return_postgres_engine import return_postgres_engine
from persistence.nba.data.utils.database_setup import reset_database, reset_tables
import os
import json


def main(season_first_start_year, season_last_start_year):
    postgres_engine = return_postgres_engine()
    reset_database(postgres_engine)
    reset_tables(postgres_engine)
    dir = os.path.dirname(__file__)
    for season_start_year in range(season_first_start_year, season_last_start_year + 1):
        season_schedule_output_file = os.path.join(dir, '../static/schedules/{0}.json'.format(season_start_year))
        season_schedule_json = open(season_schedule_output_file).read()
        insert_json_encoded_schedule_into_database(season_schedule_json, postgres_engine)

main(2014, 2014)