import datetime as dt
import pandas as pd
import statsmodels.formula.api as sm
from analysis.nba.lib.return_player_data_for_regression import return_player_data_for_date_as_df
from data_model.nba.web_scraping.utils.date_utils import daterange


start_date = dt.date(year=2015, month=3, day=1)
end_date = dt.date(year=2015, month=4, day=5)

#column_names = ["player", "opp_team", "player_team", "last_game", "b2b", "avg_opp_conceded_draftkings_score_for_position", "p28_day_avg_draftkings_score", "p14_day_avg_draftkings_score", "p7_day_avg_draftkings_score", "actual_draftkings_score"]
combined_df = pd.DataFrame()
for single_date in daterange(start_date,end_date):
    print single_date
    try:
        print "Getting data for {0}".format(single_date)
        player_data_for_date_df = return_player_data_for_date_as_df(date=single_date)
        print "Sample Data: {0}".format(player_data_for_date_df[:10])
        combined_df = combined_df.append(player_data_for_date_df, ignore_index=True)
    except Exception as error_message:
        print error_message
        pass

print combined_df
result = sm.ols(formula= "actual_draftkings_score ~ avg_opp_conceded_draftkings_score_for_position + p28_day_avg_draftkings_score + p14_day_avg_draftkings_score + p7_day_avg_draftkings_score + b2b", data=combined_df).fit()
print result.summary()




