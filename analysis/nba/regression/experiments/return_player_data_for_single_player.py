import datetime as dt
import pandas as pd

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL

from config import DRAFTKINGS_NBA


def return_player_data_for_date_and_specified_player_as_df(date, player_id):

    date_format = "%Y-%m-%d"
    date_string = date.strftime(date_format)
    p28_date_string = (date - dt.timedelta(28)).strftime(date_format)
    p14_date_string = (date - dt.timedelta(14)).strftime(date_format)
    p7_date_string = (date - dt.timedelta(7)).strftime(date_format)

    #add players who didn't play on today but have played in the past 28 days and their average points and average seconds played

    raw_sql = open("../../sql/basic_regression_player_data.sql").read()

    magic_string_dict = {
        'DATE': date_string,
        'PREVIOUS28DAYS': p28_date_string,
        'PREVIOUS14DAYS': p14_date_string,
        'PREVIOUS7DAYS': p7_date_string,
        'PLAYER': player_id
    }

    formatted_sql = raw_sql.format(**magic_string_dict)

    mysql_connection = create_engine(URL(**DRAFTKINGS_NBA))
    # mysql_connection.echo = True
    session = sessionmaker(bind=mysql_connection)
    insert_session = session()

    try:
        # boxscores for the given date
        player_data_for_date = insert_session.query("player", "opp_team", "player_team", "teammate", "last_game", "b2b", "avg_opp_conceded_draftkings_score_for_position", "weighted_historical_draftkings_score", "actual_draftkings_score", "missing_draftkings_points", "missing_seconds_played").from_statement(formatted_sql).all()
        column_names = ["player", "opp_team", "player_team", "teammate", "last_game", "b2b", "avg_opp_conceded_draftkings_score_for_position", "weighted_historical_draftkings_score", "actual_draftkings_score", "missing_draftkings_points", "missing_seconds_played"]
        player_data_for_date_df = pd.DataFrame(player_data_for_date, columns=column_names)
        return player_data_for_date_df

    except Exception as error_message:
        print "Error:{0}".format(error_message)




