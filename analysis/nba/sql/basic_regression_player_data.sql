SELECT
  bs.player AS player,
  pl.first_name,
  pl.last_name,
  opp_team.name AS opp_team,
  player_team.name AS player_team,
  CONCAT(teammates.first_name, teammates.last_name) AS teammate,
  last_game.draftkings_score AS last_game,
  CASE
    WHEN DATEDIFF('{DATE}',last_game.date) = 1 THEN 1
    ELSE 0
  END AS b2b,
  opp_conceded.draftkings_score AS avg_opp_conceded_draftkings_score_for_position,
  0.6 * week_1.avg_draftkings_score + 0.3 * week_2.avg_draftkings_score + 0.1 * week_4.avg_draftkings_score AS weighted_historical_draftkings_score,
  bs.draftkings_score AS actual_draftkings_score,
  CASE
    WHEN dnp.draftkings_score IS NULL THEN 0
    ELSE dnp.draftkings_score
  END AS missing_draftkings_points,
  CASE
    WHEN dnp.seconds_played IS NULL THEN 0
    ELSE dnp.seconds_played
  END AS missing_seconds_played
FROM boxscore AS bs
JOIN player AS pl ON bs.player = pl.id
JOIN game AS g ON bs.game = g.id
JOIN position AS po ON pl.position = po.id
JOIN team AS opp_team ON g.home_team = opp_team.id OR g.away_team = opp_team.id
JOIN team AS player_team ON player_team.id = pl.team
LEFT JOIN (
  SELECT
      last_game1.player,
      last_game1.date,
      g.id,
      bs.draftkings_score
    FROM (
    SELECT
          bs1.player AS player,
          pl1.team AS team,
          MAX(g1.date) AS date
        FROM boxscore AS bs1
          JOIN player AS pl1
            ON bs1.player = pl1.id
          JOIN game AS g1
            ON bs1.game = g1.id
        WHERE g1.date < '{DATE}'
        GROUP BY bs1.player
    ) AS last_game1
    JOIN game AS g
      ON g.date = last_game1.date AND (g.away_team = last_game1.team OR g.home_team = last_game1.team)
    JOIN boxscore AS bs
      ON bs.game = g.id AND last_game1.player = bs.player
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
) AS week_1 ON week_1.player = bs.player
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
  AND g2.date < '{PREVIOUS7DAYS}'
GROUP BY bs2.player
) AS week_2 ON week_2.player = bs.player
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
  AND g2.date < '{PREVIOUS14DAYS}'
GROUP BY bs2.player
) AS week_4 ON week_4.player = bs.player
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
LEFT JOIN (
SELECT
  player_dnp_stats.team,
  player_dnp_stats.position,
  SUM(player_dnp_stats.draftkings_score) AS draftkings_score,
  SUM(player_dnp_stats.seconds_played) AS seconds_played
FROM (
    SELECT
      pl.id AS player,
      team.id AS team,
      pl.position AS position,
      AVG(bs.draftkings_score) AS draftkings_score,
      AVG(bs.seconds_played) AS seconds_played
    FROM player AS pl
    JOIN team ON pl.team = team.id
    JOIN boxscore AS bs ON bs.player = pl.id
    JOIN game AS g ON bs.game = g.id
    JOIN
        (
        SELECT
          pl.first_name,
          pl.last_name,
          MAX(last_boxscore) AS last_boxscore
        FROM player AS pl
        GROUP BY
          pl.first_name,
          pl.last_name
        ) AS last_boxscore ON pl.first_name = last_boxscore.first_name AND pl.last_name = last_boxscore.last_name AND last_boxscore.last_boxscore = pl.last_boxscore
    WHERE pl.id NOT IN (
        SELECT
          pl.id
        FROM boxscore AS bs
        JOIN player AS pl ON bs.player = pl.id
        JOIN game AS g ON bs.game = g.id
        JOIN position AS po ON pl.position = po.id
        JOIN team AS opp_team ON g.home_team = opp_team.id OR g.away_team = opp_team.id
        JOIN team AS player_team ON player_team.id = pl.team
        JOIN (
            SELECT
              pl.id
            FROM player AS pl
            JOIN
            (
                SELECT
                  pl.first_name,
                  pl.last_name,
                  MAX(last_boxscore) AS last_boxscore
                FROM player AS pl
                GROUP BY
                  pl.first_name,
                  pl.last_name
             ) AS last_boxscore ON pl.first_name = last_boxscore.first_name AND pl.last_name = last_boxscore.last_name AND last_boxscore.last_boxscore = pl.last_boxscore
        ) AS current_player ON current_player.id = pl.id
        WHERE g.date = '{DATE}'
        GROUP BY pl.id
    )
    AND team.id IN (
    SELECT
      g.away_team AS team
    FROM boxscore AS bs
    JOIN game AS g ON bs.game = g.id
    WHERE g.date = '{DATE}'
    GROUP BY
      g.away_team
    UNION ALL
    SELECT
      g.home_team AS team
    FROM boxscore AS bs
    JOIN game AS g ON bs.game = g.id
    WHERE g.date = '{DATE}'
    GROUP BY
      g.home_team
    )
    AND g.date >= '{PREVIOUS14DAYS}' AND g.date < '{DATE}'
    GROUP BY pl.id) AS player_dnp_stats
GROUP BY
  player_dnp_stats.team,
  player_dnp_stats.position
) AS dnp ON dnp.team = player_team.id AND dnp.position = pl.position
LEFT JOIN (
  SELECT
    pl.id AS player,
    pl.first_name,
    pl.last_name,
    t.id AS team
  FROM player AS pl
  JOIN team AS t ON pl.team = t.id
  JOIN
  (
      SELECT
        pl.first_name,
        pl.last_name,
        MAX(last_boxscore) AS last_boxscore
      FROM player AS pl
      GROUP BY
        pl.first_name,
        pl.last_name
   ) AS last_boxscore ON pl.first_name = last_boxscore.first_name AND pl.last_name = last_boxscore.last_name AND last_boxscore.last_boxscore = pl.last_boxscore
   GROUP BY pl.id
) AS teammates ON teammates.team = player_team.id
WHERE g.date = '{DATE}'
  AND opp_team.id != player_team.id
  AND teammates.player != pl.id
  AND pl.id = {PLAYER}
GROUP BY
  bs.player,
  teammates.player