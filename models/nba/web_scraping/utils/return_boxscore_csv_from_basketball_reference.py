import models.nba.web_scraping.lib.basketball_reference_boxscore_returner as boxscore_scraper
import pandas as pd
import datetime as dt

def return_boxscore_csv(date):

    csv_filename = date.strftime("%Y-%m-%d") + ".csv"
    csv_filepath = "../data_files/boxscores/{0}".format(csv_filename)

    column_names = [
        'first_name',
        'last_name',
        'date',
        'team_abbreviation',
        'opponent_abbreviation',
        'minutes_played',
        'made_field_goals',
        'attempted_field_goals',
        'made_three_point_field_goals',
        'attempted_three_point_field_goals',
        'made_free_throws',
        'attempted_free_throws',
        'offensive_rebounds',
        'defensive_rebounds',
        'total_rebounds',
        'assists',
        'steals',
        'blocks',
        'turnovers',
        'fouls_committed',
        'points',
        'draftkings_score'
        ]

    boxscore_df = boxscore_scraper.return_formatted_box_score_as_dataframe(date)
    boxscore_df.to_csv(csv_filepath, index=False, header=column_names)

date = dt.date.today() - dt.timedelta(days=1)
return_boxscore_csv(date)


