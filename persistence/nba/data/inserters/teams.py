import csv

from persistence.nba.data.utils.functions import get_or_create
from persistence.nba.model import Team


class TeamInserter:
    def __init__(self):
        pass

    def insert_teams(self, session, team_name_csv):
        with open(team_name_csv) as file:
            reader = csv.reader(file)
            nba_team_name_list = list(reader)[1:]
            for team in nba_team_name_list:
                get_or_create(session, Team, name=team[2], abbreviation=team[1])