import datetime as dt
import pandas as pd
import patsy
import statsmodels.formula.api as sm
from analysis.nba.regression.experiments.return_player_data_for_single_player import return_player_data_for_date_and_specified_player_as_df
from data_model.nba.web_scraping.utils.date_utils import daterange


start_date = dt.date(year=2015, month=3, day=1)
end_date = dt.date(year=2015, month=3, day=24)
prediction_date = dt.date(year=2015, month=3, day=25)

combined_df = pd.DataFrame()
for single_date in daterange(start_date,end_date):
    try:
        print "Getting data for {0}".format(single_date)
        player_data_for_date_df = return_player_data_for_date_and_specified_player_as_df(date=single_date, player_id=544)
        # print "Sample Data: {0}".format(player_data_for_date_df[:10])
        combined_df = combined_df.append(player_data_for_date_df, ignore_index=True)
    except Exception as error_message:
        print error_message
        pass

formula = "actual_draftkings_score ~ C(teammate) + avg_opp_conceded_draftkings_score_for_position + weighted_historical_draftkings_score + missing_draftkings_points + missing_seconds_played + last_game + b2b "
combined_df[['missing_draftkings_points', 'missing_seconds_played']] = combined_df[['missing_draftkings_points', 'missing_seconds_played']].astype(float)
cleaned_df = combined_df.dropna()
print cleaned_df.dtypes
print "Getting out of sample data"
raw_out_of_sample_df = return_player_data_for_date_and_specified_player_as_df(date=prediction_date, player_id=544)
cleaned_out_of_sample_df = raw_out_of_sample_df.dropna().reset_index(drop=True)
cleaned_out_of_sample_df[['missing_draftkings_points', 'missing_seconds_played']] = cleaned_out_of_sample_df[['missing_draftkings_points', 'missing_seconds_played']].astype(float)
cleaned_out_of_sample_df_y, cleaned_out_of_sample_df_X = patsy.dmatrices(formula, cleaned_out_of_sample_df, return_type='dataframe')
cleaned_out_of_sample_df_X = cleaned_out_of_sample_df_X.drop('C(teammate)[T.DionWaiters]', axis=1)
print "Starting Regression"
y, X = patsy.dmatrices(formula, cleaned_df, return_type='dataframe')
X = X.drop('C(teammate)[T.DionWaiters]', axis=1)
print X
result = sm.OLS(y, X).fit()
print result.summary()
print cleaned_df.to_csv(path_or_buf="../csv/regression.csv")
predictions = result.predict(cleaned_out_of_sample_df_X)
predicted_values_df = pd.DataFrame(predictions,columns=["predicted_values"])
print predicted_values_df
# cleaned_predictions_df = pd.concat([cleaned_out_of_sample_df,predicted_values_df], axis=1)
# cleaned_predictions_df.to_csv(path_or_buf="csv/predictions.csv")

