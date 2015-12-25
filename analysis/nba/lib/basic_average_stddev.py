from datetime import datetime, timedelta
from persistence.nba.data.database_connector import db_session
import pandas

def return_average_and_stddev(date):
    twenty_eight_days_ago = date - timedelta(28)
    fourteen_days_ago = date - timedelta(14)
    sql = """
        SELECT
          p.first_name,
          p.last_name,
          SUM(bs.points + bs.made_three_point_field_goals * 0.5 + bs.total_rebounds * 1.25 + bs.assists * 1.5 + bs.steals * 2 + bs.blocks * 2 - bs.turnovers * 0.5) / COUNT(DISTINCT g.id) AS avg,
          stddev.stddev
        FROM boxscore AS bs
          JOIN game AS g ON bs.game = g.id
          JOIN player AS p ON bs.player = p.id
          JOIN (
            SELECT
                bs.player AS player,
                STDDEV_POP(bs.points + bs.made_three_point_field_goals * 0.5 + bs.total_rebounds * 1.25 + bs.assists * 1.5 + bs.steals * 2 + bs.blocks * 2 - bs.turnovers * 0.5) AS stddev
            FROM boxscore AS bs
            JOIN game AS g ON bs.game = g.id
            WHERE g.start_time >= '{TWENTY_EIGHT_DAYS_AGO}'
            GROUP BY bs.player
          ) AS stddev ON p.id = stddev.player
        WHERE g.start_time >= '{FOURTEEN_DAYS_AGO}'
        GROUP BY
          p.first_name,
          p.last_name,
          stddev.stddev
        HAVING COUNT(DISTINCT g.id) > 5;
    """.format(TWENTY_EIGHT_DAYS_AGO=twenty_eight_days_ago, FOURTEEN_DAYS_AGO=fourteen_days_ago)

    return pandas.DataFrame(db_session.query("first_name", "last_name", "avg", "stddev").from_statement(sql).all())