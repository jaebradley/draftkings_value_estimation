SELECT
  pl.id,
  pl.first_name,
  pl.last_name,
  t.name
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
 WHERE t.id = 21
 GROUP BY pl.id;