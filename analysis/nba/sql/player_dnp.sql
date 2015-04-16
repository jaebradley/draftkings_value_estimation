SELECT
  player_dnp_stats.team,
  player_dnp_stats.position,
  SUM(player_dnp_stats.draftkings_score) AS draftkings_score,
  SUM(player_dnp_stats.seconds_played) AS seconds_played
FROM (SELECT
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
(SELECT 
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
		(SELECT 
		  pl.first_name,
		  pl.last_name,
		  MAX(last_boxscore) AS last_boxscore
		FROM player AS pl
		GROUP BY
		  pl.first_name,
		  pl.last_name
		  ) AS last_boxscore ON pl.first_name = last_boxscore.first_name AND pl.last_name = last_boxscore.last_name AND last_boxscore.last_boxscore = pl.last_boxscore
    ) AS current_player ON current_player.id = pl.id
WHERE g.date = '2015-04-01'
GROUP BY pl.id)
AND team.id IN (
SELECT
	      g.away_team AS team
	    FROM boxscore AS bs
	    JOIN game AS g ON bs.game = g.id
	WHERE g.date = '2015-04-01'
	GROUP BY
	  g.away_team
UNION ALL
SELECT
	      g.home_team AS team
	    FROM boxscore AS bs
	    JOIN game AS g ON bs.game = g.id
	WHERE g.date = '2015-04-01'
	GROUP BY
	  g.home_team
)
AND g.date >= '2015-03-01' AND g.date < '2015-04-01'
GROUP BY pl.id) AS player_dnp_stats
GROUP BY
  player_dnp_stats.team,
  player_dnp_stats.position
;