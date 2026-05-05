from sqlalchemy import (
    create_engine, Column, Integer, String, 
    Float, DateTime, ForeignKey, Boolean, Text
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime

Base = declarative_base()


class League(Base):
    __tablename__ = "leagues"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)       # "Premier League"
    country = Column(String(100), nullable=False)    # "England"
    sport = Column(String(50), nullable=False)       # "football" ou "basketball"
    season = Column(String(20), nullable=False)      # "2023/2024"
    created_at = Column(DateTime, default=datetime.utcnow)

    teams = relationship("Team", back_populates="league")
    matches = relationship("Match", back_populates="league")


class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    short_name = Column(String(10))                  # "MCI", "ARS"
    country = Column(String(100))
    league_id = Column(Integer, ForeignKey("leagues.id"))
    founded_year = Column(Integer)
    stadium = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)

    league = relationship("League", back_populates="teams")
    home_matches = relationship("Match", foreign_keys="Match.home_team_id")
    away_matches = relationship("Match", foreign_keys="Match.away_team_id")
    players = relationship("Player", back_populates="team")


class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True)
    league_id = Column(Integer, ForeignKey("leagues.id"))
    home_team_id = Column(Integer, ForeignKey("teams.id"))
    away_team_id = Column(Integer, ForeignKey("teams.id"))
    match_date = Column(DateTime, nullable=False)
    matchday = Column(Integer)                       # rodada
    home_score = Column(Integer)
    away_score = Column(Integer)
    status = Column(String(20), default="scheduled") # scheduled, live, finished
    venue = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)

    league = relationship("League", back_populates="matches")
    home_team = relationship("Team", foreign_keys=[home_team_id])
    away_team = relationship("Team", foreign_keys=[away_team_id])
    stats = relationship("MatchStats", back_populates="match")
    odds = relationship("Odds", back_populates="match")


class MatchStats(Base):
    __tablename__ = "match_stats"

    id = Column(Integer, primary_key=True)
    match_id = Column(Integer, ForeignKey("matches.id"))
    team_id = Column(Integer, ForeignKey("teams.id"))
    possession = Column(Float)                       # % de posse de bola
    shots = Column(Integer)
    shots_on_target = Column(Integer)
    corners = Column(Integer)
    fouls = Column(Integer)
    yellow_cards = Column(Integer)
    red_cards = Column(Integer)
    passes = Column(Integer)
    pass_accuracy = Column(Float)                    # %
    xg = Column(Float)                              # expected goals
    created_at = Column(DateTime, default=datetime.utcnow)

    match = relationship("Match", back_populates="stats")
    team = relationship("Team")


class Odds(Base):
    __tablename__ = "odds"

    id = Column(Integer, primary_key=True)
    match_id = Column(Integer, ForeignKey("matches.id"))
    bookmaker = Column(String(100))                  # "Bet365", "Betfair"
    home_win = Column(Float)                         # odd para vitória em casa
    draw = Column(Float)                             # odd para empate
    away_win = Column(Float)                         # odd para vitória fora
    recorded_at = Column(DateTime, default=datetime.utcnow)  # momento da coleta
    is_opening = Column(Boolean, default=False)      # odd de abertura?
    is_closing = Column(Boolean, default=False)      # odd de fechamento?

    match = relationship("Match", back_populates="odds")


class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    team_id = Column(Integer, ForeignKey("teams.id"))
    position = Column(String(50))                    # "Forward", "Midfielder"
    nationality = Column(String(100))
    age = Column(Integer)
    market_value = Column(Float)                     # em milhões €
    created_at = Column(DateTime, default=datetime.utcnow)

    team = relationship("Team", back_populates="players")