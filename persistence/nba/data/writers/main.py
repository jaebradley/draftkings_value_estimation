from persistence.nba.data.writers.write_season_schedule import write_season_schedule_to_json
from persistence.nba.data.writers.write_box_scores_for_season import write_box_scores_for_season_to_json
import os


def main(first_season_start_year, last_season_start_year):
    dir = os.path.dirname(__file__)
    for season_start_year in range(first_season_start_year, last_season_start_year + 1):
        season_schedule_output_file = os.path.join(dir, '../static/schedules/{0}.json'.format(season_start_year))
        write_season_schedule_to_json(season_start_year=season_start_year, output_file_path=season_schedule_output_file)
        write_box_scores_for_season_to_json(season_start_year=season_start_year)


main(2014, 2015)
