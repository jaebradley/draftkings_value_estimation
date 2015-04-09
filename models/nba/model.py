from sqlalchemy import Column, Integer, String, ForeignKey, Date, PrimaryKeyConstraint, UniqueConstraint
from sqlalchemy import VARCHAR, INTEGER, DATE, TEXT, FLOAT, TIME
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Position(Base):

    __tablename__ = "position"

    id = Column(INTEGER, primary_key=True)
    name = Column("name", VARCHAR(length=50))
    abbreviation = Column("abbreviation", VARCHAR(length=10))

    __table_args__ = ((UniqueConstraint("name", "abbreviation", name="name_abbreviation")),)

class Team(Base):

    __tablename__ = "team"

    id = Column(INTEGER, primary_key=True)
    name = Column("name", VARCHAR(length=50))
    abbreviation = Column("abbreviation", VARCHAR(length=20))

    __table_args__ = ((UniqueConstraint("name", "abbreviation", name="name_abbreviation")),)

class Game(Base):

    __tablename__ = "game"

    id = Column(INTEGER, primary_key=True)
    home_team = Column("home_team", ForeignKey(Team.id))
    away_team = Column("away_team", ForeignKey(Team.id))
    date = Column("date", DATE)

    __table_args__ = (UniqueConstraint("home_team", "away_team", "date", name="custom_uc_home_away_date"),)

class Player(Base):

    __tablename__ = "player"

    id = Column(INTEGER, primary_key=True)
    first_name = Column("first_name", VARCHAR(length=250))
    last_name = Column("last_name", VARCHAR(length=250))
    team = Column("team", ForeignKey(Team.id))
    position = Column("position", ForeignKey(Position.id))
    number = Column("number", INTEGER, nullable=True)

    __table_args__ = (UniqueConstraint("first_name", "last_name", "team", "position", "number", name="custom_uc_first_name_last_name_team_position_number"),)

class DraftkingsPlayerSalary(Base):

    __tablename__ = "draftkings_player_salary"

    id = Column(INTEGER, primary_key=True)
    player = Column("player", ForeignKey(Player.id))
    salary = Column("salary", FLOAT(precision=2))
    date = Column("date", DATE)

    __table_args__ = (UniqueConstraint("player", "salary", "date", name="custom_uc_player_salary_date"),)

class BasketballReferenceBoxscore(Base):

    __tablename__ = "boxscore"

    id = Column(INTEGER, primary_key=True)
    player = Column("player", ForeignKey(Player.id))
    game = Column("game", ForeignKey(Game.id))
    date = Column("date", DATE)
    minutes_played = Column("minutes_played", TIME)
    made_field_goals = Column("made_field_goals", INTEGER)
    attempted_field_goals = Column("attempted_field_goals", INTEGER)
    made_three_point_field_goals = Column("made_three_point_field_goals", INTEGER)
    attempted_three_point_field_goals = Column("attempted_three_point_field_goals", INTEGER)
    made_free_throws = Column("made_free_throws", INTEGER)
    attempted_free_throws = Column("attempted_free_throws", INTEGER)
    offensive_rebounds = Column("offensive_rebounds", INTEGER)
    defensive_rebounds = Column("defensive_rebounds", INTEGER)
    total_rebounds = Column("total_rebounds", INTEGER)
    assists = Column("assists", INTEGER)
    steals = Column("steals", INTEGER)
    blocks = Column("blocks", INTEGER)
    turnovers = Column("turnovers", INTEGER)
    fouls_committed = Column("fouls_committed", INTEGER)
    points = Column("points", INTEGER)
    draftkings_score = Column("draftkings_score", FLOAT(precision=2))

    __table_args__ = (UniqueConstraint("player", "game", name="custom_uc_player_game"),)
