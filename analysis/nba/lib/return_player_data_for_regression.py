import sqlalchemy
import csv
import os
import datetime as dt
import pandas as pd

from sqlalchemy import create_engine, or_, and_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL

from config import DRAFTKINGS_NBA
from models.nba.model import Team, Player, Position, Game, BasketballReferenceBoxscore


def return_data(date):

    date_format = "%Y-%m-%d"
    date_string = date.strftime(date_format)
    p28_date_string = (date - dt.timedelta(28)).strftime(date_format)
    p14_date_string = (date - dt.timedelta(14)).strftime(date_format)
    p7_date_string = (date - dt.timedelta(7)).strftime(date_format)

    raw_sql = """
    SELECT
      bs.player AS player,
      opp_team.name AS opp_team,
      player_team.name AS player_team,
      last_game.date AS last_game,
      CASE
        WHEN DATEDIFF('{DATE}',last_game.date) = 1 THEN 1
        ELSE 0
      END AS b2b,
      opp_conceded.draftkings_score AS avg_opp_conceded_draftkings_score_for_position,
      p28_days.avg_draftkings_score AS p28_day_avg_draftkings_score,
      p14_days.avg_draftkings_score AS p14_day_avg_draftkings_score,
      p7_days.avg_draftkings_score AS p7_day_avg_draftkings_score,
      bs.draftkings_score AS actual_draftkings_score
    FROM boxscore AS bs
    JOIN player AS pl ON bs.player = pl.id
    JOIN game AS g ON bs.game = g.id
    JOIN position AS po ON pl.position = po.id
    JOIN team AS opp_team ON g.home_team = opp_team.id OR g.away_team = opp_team.id
    JOIN team AS player_team ON player_team.id = pl.team
    LEFT JOIN (
      SELECT
      bs1.player AS player,
      MAX(g1.date) AS date
    FROM boxscore AS bs1
      JOIN player AS pl1
        ON bs1.player = pl1.id
      JOIN game AS g1
        ON bs1.game = g1.id
    WHERE g1.date < '{DATE}'
    GROUP BY bs1.player
    ) AS last_game ON last_game.player = bs.player
    LEFT JOIN (
    SELECT
      bs2.player,
      AVG(bs2.draftkings_score) AS avg_draftkings_score
    FROM boxscore AS bs2
      JOIN game AS g2
        ON bs2.game = g2.id
      JOIN player AS pl2
        ON bs2.player = pl2.id
    WHERE g2.date >= '{PREVIOUS7DAYS}'
      AND g2.date < '{DATE}'
    GROUP BY bs2.player
    ) AS p7_days ON p7_days.player = bs.player
    LEFT JOIN (
    SELECT
      bs2.player,
      AVG(bs2.draftkings_score) AS avg_draftkings_score
    FROM boxscore AS bs2
      JOIN game AS g2
        ON bs2.game = g2.id
      JOIN player AS pl2
        ON bs2.player = pl2.id
    WHERE g2.date >= '{PREVIOUS14DAYS}'
      AND g2.date < '{DATE}'
    GROUP BY bs2.player
    ) AS p14_days ON p14_days.player = bs.player
    LEFT JOIN (
    SELECT
      bs2.player,
      AVG(bs2.draftkings_score) AS avg_draftkings_score
    FROM boxscore AS bs2
      JOIN game AS g2
        ON bs2.game = g2.id
      JOIN player AS pl2
        ON bs2.player = pl2.id
    WHERE g2.date >= '{PREVIOUS28DAYS}'
      AND g2.date < '{DATE}'
    GROUP BY bs2.player
    ) AS p28_days ON p28_days.player = bs.player
    LEFT JOIN (
    SELECT
      opp_stats_by_game.position,
      opp_stats_by_game.opp,
      AVG(opp_stats_by_game.points) AS points,
      AVG(opp_stats_by_game.rebounds) AS rebounds,
      AVG(opp_stats_by_game.assists) AS assists,
      AVG(opp_stats_by_game.blocks) AS blocks,
      AVG(opp_stats_by_game.turnovers) AS turnovers,
      AVG(opp_stats_by_game.draftkings_score) AS draftkings_score
    FROM (
        SELECT
          p.position,
          t.id AS opp,
          t1.id AS team,
          SUM(bs.points) AS points,
          SUM(bs.total_rebounds) AS rebounds,
          SUM(bs.assists) AS assists,
          SUM(bs.steals) AS steals,
          SUM(bs.blocks) AS blocks,
          SUM(bs.turnovers) AS turnovers,
          AVG(bs.draftkings_score) AS draftkings_score
        FROM team AS t
          JOIN game AS g
            ON g.away_team = t.id OR g.home_team = t.id
          JOIN boxscore AS bs
            ON bs.game = g.id
          JOIN player AS p
            ON p.id = bs.player
          JOIN team AS t1
            ON p.team = t1.id
        WHERE
          t.id != t1.id
          AND g.date >= '{PREVIOUS28DAYS}'
          AND g.date <= '{DATE}'
        GROUP BY
          p.position,
          t.id,
          t1.id
        ) AS opp_stats_by_game
    GROUP BY
      opp_stats_by_game.position,
      opp_stats_by_game.opp
    ) AS opp_conceded ON opp_conceded.position = po.id AND opp_conceded.opp = opp_team.id
    WHERE g.date = '{DATE}'
      AND opp_team.id != player_team.id
    GROUP BY
      bs.player
    """

    magic_string_dict = {
        'DATE': date_string,
        'PREVIOUS28DAYS': p28_date_string,
        'PREVIOUS14DAYS': p14_date_string,
        'PREVIOUS7DAYS': p7_date_string
    }

    formatted_sql = raw_sql.format(**magic_string_dict)

    mysql_connection = create_engine(URL(**DRAFTKINGS_NBA))
    mysql_connection.echo = True
    session = sessionmaker(bind=mysql_connection)
    insert_session = session()

    try:
        # boxscores for the given date
        player_data_for_date = insert_session.query("player", "opp_team", "player_team", "last_game", "b2b", "avg_opp_conceded_draftkings_score_for_position", "p28_day_avg_draftkings_score", "p14_day_avg_draftkings_score", "p7_day_avg_draftkings_score", "actual_draftkings_score").from_statement(formatted_sql).all()
        column_names = ["player", "opp_team", "player_team", "last_game", "b2b", "avg_opp_conceded_draftkings_score_for_position", "p28_day_avg_draftkings_score", "p14_day_avg_draftkings_score", "p7_day_avg_draftkings_score", "actual_draftkings_score"]
        print player_data_for_date[:10]
        player_data_for_date_df = pd.DataFrame(player_data_for_date, columns=column_names)
        print player_data_for_date_df

    except Exception as error_message:
        print "Error:{0}".format(error_message)

date = dt.date.today() - dt.timedelta(days=5)

return_data(date)


