# get all distinct game dates
# for each game date, get the box scores
# insert the box scores

from datetime import timedelta

from basketball_reference_web_scraper.readers import return_box_scores_for_date
from pytz import timezone
from sqlalchemy import desc
from sqlalchemy import distinct
from sqlalchemy import func
from sqlalchemy import or_, and_
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from persistence.nba.data.utils.functions import get_or_create
from persistence.nba.model import Game, BoxScore, Team, Player


class BoxScoreInserter:
    def __init__(self):
        pass

    def insert_box_score(self, box_score, session):
        team_object = session.query(Team).filter(Team.abbreviation == box_score.team).one()
        opponent = session.query(Team).filter(Team.abbreviation == box_score.opponent).one()
        try:
            player_object = session.query(Player).filter(and_(Player.first_name == box_score.first_name, Player.last_name == box_score.last_name, Player.team == team_object.id)).one()
            game = session.query(Game).filter(or_(func.date(Game.start_time) == box_score.date, func.date(Game.start_time) == box_score.date + timedelta(days=1))).filter(and_(or_(Game.home_team == team_object.id, Game.away_team == team_object.id),or_(Game.home_team == opponent.id, Game.away_team == opponent.id))).one()
            get_or_create(
                session,
                BoxScore,
                player=player_object.id,
                game=game.id,
                seconds_played=box_score.seconds_played,
                made_field_goals=box_score.field_goals,
                attempted_field_goals=box_score.field_goal_attempts,
                made_three_point_field_goals=box_score.three_point_field_goals,
                attempted_three_point_field_goals=box_score.three_point_field_goal_attempts,
                made_free_throws=box_score.free_throws,
                attempted_free_throws=box_score.free_throw_attempts,
                offensive_rebounds=box_score.offensive_rebounds,
                defensive_rebounds=box_score.defensive_rebounds,
                total_rebounds=box_score.total_rebounds,
                assists=box_score.assists,
                steals=box_score.steals,
                blocks=box_score.blocks,
                turnovers=box_score.turnovers,
                fouls_committed=box_score.personal_fouls,
                points=box_score.points
            )
        except (NoResultFound, MultipleResultsFound):
            print box_score.date, box_score.team, box_score.opponent


    def insert_box_scores(self, session, minimum_date, maximum_date):
        start_times = session.query(distinct(Game.start_time)).outerjoin(BoxScore, Game.id == BoxScore.game).filter(Game.start_time > minimum_date).filter(Game.start_time <= maximum_date).filter(BoxScore.game == None).order_by(desc(Game.start_time))
        distinct_start_days = set()
        for start_time in start_times:
            distinct_start_days.add(timezone('US/Eastern').localize(start_time[0]).astimezone(timezone('US/Eastern')).date())
        for start_day in distinct_start_days:
            box_scores = return_box_scores_for_date(start_day)
            for box_score in box_scores:
                self.insert_box_score(box_score, session)