from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy import VARCHAR, INTEGER, DATE, TEXT, FLOAT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Position(Base):

    __tablename__ = "position"

    id = Column(INTEGER, primary_key=True)
    name = Column("name", VARCHAR(length=50))
    abbreviation = Column("abbreviation", VARCHAR(length=10))

class Team(Base):

    __tablename__ = "team"

    id = Column(INTEGER, primary_key=True)
    name = Column("name", VARCHAR(length=50))
    abbreviation = Column("abbreviation", VARCHAR(length=20))

class Game(Base):

    __tablename__ = "game"

    id = Column(INTEGER, primary_key=True)
    home_team = Column("home_team", ForeignKey(Team.id))
    away_team = Column("away_team", ForeignKey(Team.id))
    date = Column("date", DATE)

class Player(Base):

    __tablename__ = "player"

    id = Column(INTEGER, primary_key=True)
    first_name = Column("first_name", TEXT)
    last_name = Column("last_name", TEXT)
    team = Column("team", ForeignKey(Team.id))
    position = Column("position", ForeignKey(Position.id))
    number = Column("number", INTEGER, nullable=True)

class DraftkingsPlayerSalary(Base):

    __tablename__ = "draftkings_player_salary"

    id = Column(INTEGER, primary_key=True)
    player = Column("player", ForeignKey(Player.id))
    salary = Column("salary", FLOAT(precision=2))
    date = Column("date", DATE)

class BasketballReferenceBoxscore(Base):

    __tablename__ = "boxscore"

    id = Column(INTEGER, primary_key=True)
    player_id = Column("player", ForeignKey(Player.id))
    game = Column("game", ForeignKey(Game.id))
    date = Column("date", DATE)




