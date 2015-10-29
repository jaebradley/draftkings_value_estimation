from persistence.nba.data_writers.write_season_schedule import write_season_schedule_to_json
from persistence.nba.data_writers.write_box_scores_for_season import write_box_scores_for_season_to_json


def main(first_season_start_year, last_season_start_year):
    for season_start_year in range(first_season_start_year, last_season_start_year + 1):
        write_season_schedule_to_json(season_start_year=season_start_year)
        write_box_scores_for_season_to_json(season_start_year=season_start_year)


main(2014, 2015)
