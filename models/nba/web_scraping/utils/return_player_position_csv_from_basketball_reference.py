import models.nba.web_scraping.lib.basketball_reference_player_position_returner as player_scraper
import pandas as pd

def return_player_position_csv():

    column_names = ['first_name', 'last_name', 'position', 'team_abbreviation']
    player_positions = player_scraper.return_player_position_list()
    df = pd.DataFrame(player_positions)
    df.to_csv("../data_files/player_position.csv", index=False, header=column_names)

