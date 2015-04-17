import datetime as dt
import pandas as pd
import statsmodels.formula.api as sm
from analysis.nba.lib.return_player_data_for_regression import return_player_data_for_date_as_df
from data_model.nba.web_scraping.utils.date_utils import daterange


start_date = dt.date(year=2015, month=2, day=1)
end_date = dt.date(year=2015, month=4, day=5)
prediction_date = dt.date(year=2015, month=4, day=10)

combined_df = pd.DataFrame()
for single_date in daterange(start_date,end_date):
    try:
        print "Getting data for {0}".format(single_date)
        player_data_for_date_df = return_player_data_for_date_as_df(date=single_date)
        # print "Sample Data: {0}".format(player_data_for_date_df[:10])
        combined_df = combined_df.append(player_data_for_date_df, ignore_index=True)
    except Exception as error_message:
        print error_message
        pass

print "Getting out of sample data"
raw_out_of_sample_df = return_player_data_for_date_as_df(date=prediction_date)
cleaned_out_of_sample_df = raw_out_of_sample_df.dropna().reset_index(drop=True)
cleaned_df = combined_df.dropna()
print "Starting Regression"
result = sm.ols(formula= "actual_draftkings_score ~ avg_opp_conceded_draftkings_score_for_position + weighted_historical_draftkings_score + missing_draftkings_points + last_game + b2b ", data=cleaned_df).fit()
print result.summary()
predictions = result.predict(cleaned_out_of_sample_df)
predicted_values_df = pd.DataFrame(predictions,columns=["predicted_values"])
cleaned_predictions_df = pd.concat([cleaned_out_of_sample_df,predicted_values_df], axis=1)
cleaned_predictions_df.to_csv(path_or_buf="csv/predictions.csv")
