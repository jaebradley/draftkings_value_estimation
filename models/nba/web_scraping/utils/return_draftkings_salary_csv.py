from models.nba.web_scraping.lib.draftkings_player_salary_returner import return_draftkings_daily_nba_player_salary_as_dataframe
import datetime as dt

def draftkings_salary_to_csv():
    today = dt.date.today()
    csv_filename = today.strftime("%Y-%m-%d") + ".csv"
    csv_filepath = "../data_files/draftkings_salary/{0}".format(csv_filename)
    draftkings_salary_df = return_draftkings_daily_nba_player_salary_as_dataframe(date=today)
    draftkings_salary_df.to_csv(csv_filepath, index=False)
