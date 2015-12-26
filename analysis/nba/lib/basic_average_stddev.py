from datetime import timedelta, datetime

import pandas
from pytz import timezone, utc

from persistence.nba.data.database_connector import db_session


def return_average_and_stddev(date):
    twenty_eight_days_ago = date - timedelta(28)
    fourteen_days_ago = date - timedelta(14)
    day_start_est = timezone('US/Eastern').localize(datetime(year=date.year, month=date.month, day=date.day, hour=0, minute=0, second=0, microsecond=0))
    day_end_est = day_start_est + timedelta(hours=24)
    day_start_utc = day_start_est.astimezone(utc)
    day_end_utc = day_end_est.astimezone(utc)
    sql = """
        SELECT
          player.first_name,
          player.last_name,
          SUM(bs.draftkings_points) / COUNT(DISTINCT g.id) AS avg,
          stddev.stddev,
          (SUM(bs.draftkings_points) / COUNT(DISTINCT g.id)) / stddev.stddev AS avg_to_stddev_ratio
        FROM boxscore AS bs
          JOIN game AS g ON bs.game = g.id
          JOIN (
            SELECT
              p.id AS id,
              p.first_name AS first_name,
              p.last_name AS last_name
            FROM player AS p
            JOIN team AS t ON t.id = p.team
            JOIN game AS g ON (g.home_team = t.id OR g.away_team = t.id)
            WHERE g.start_time >= '{DAY_START_UTC}' AND g.start_time <= '{DAY_END_UTC}'
          ) AS player ON bs.player = player.id
          JOIN (
            SELECT
                bs.player AS player,
                STDDEV_POP(bs.draftkings_points) AS stddev
            FROM boxscore AS bs
            JOIN game AS g ON bs.game = g.id
            WHERE g.start_time >= '{TWENTY_EIGHT_DAYS_AGO}'
            GROUP BY bs.player
          ) AS stddev ON bs.player = stddev.player
        WHERE g.start_time >= '{FOURTEEN_DAYS_AGO}'
        GROUP BY
          player.first_name,
          player.last_name,
          stddev.stddev
        HAVING COUNT(DISTINCT g.id) > 5
        ORDER BY
          avg_to_stddev_ratio DESC
    """.format(DAY_START_UTC=day_start_utc, DAY_END_UTC=day_end_utc, TWENTY_EIGHT_DAYS_AGO=twenty_eight_days_ago, FOURTEEN_DAYS_AGO=fourteen_days_ago)

    return pandas.DataFrame(db_session.query("first_name", "last_name", "avg", "stddev").from_statement(sql).all())

print return_average_and_stddev(datetime.now(utc))