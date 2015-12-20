import csv

from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.engine.url import URL

from config import DRAFTKINGS_NBA


def add_data_to_team_table(team_name_map_filename):

    with open(team_name_map_filename) as file:
        reader = csv.reader(file)
        nba_team_name_list = list(reader)[1:]
        insert_nba_team_name_list = list()
        for team in nba_team_name_list:
            temp_dict = {
                'name': team[2],
                'abbreviation': team[1]
            }
            insert_nba_team_name_list.append(temp_dict)

    mysql_connection = create_engine(URL(**DRAFTKINGS_NBA))
    metadata = MetaData(mysql_connection)
    team = Table("team", metadata, autoload=True)
    team_insert = team.insert()
    team_insert.execute(insert_nba_team_name_list)
