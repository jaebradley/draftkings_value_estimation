from basketball_reference_web_scraper.readers import return_json_encoded_schedule
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL

from persistence.nba.config import DRAFTKINGS_NBA
from persistence.nba.data.inserters.season_schedule_inserter import insert_json_encoded_schedule_into_database


def main(season_first_start_year, season_last_start_year):
    mysql_connection = create_engine(URL(**DRAFTKINGS_NBA))
    for season_start_year in range(season_first_start_year, season_last_start_year + 1):
        season_schedule_json = return_json_encoded_schedule(season_start_year)
        insert_json_encoded_schedule_into_database(season_schedule_json, mysql_connection)

main(2014, 2015)