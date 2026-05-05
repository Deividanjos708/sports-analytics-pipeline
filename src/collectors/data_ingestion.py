import requests
import os
from dotenv import load_dotenv
from loguru import logger
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models.database import Base, League, Team, Match, MatchStats

load_dotenv()

API_KEY = os.getenv("API_FOOTBALL_KEY")
BASE_URL = os.getenv("API_FOOTBALL_BASE_URL")
DATABASE_URL = os.getenv("DATABASE_URL")

HEADERS = {"x-apisports-key": API_KEY}

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


def get_or_create_league(session, league_data: dict, season: str) -> League:
    """Busca ou cria uma liga no banco."""
    league = session.query(League).filter_by(
        name=league_data['name'],
        season=season
    ).first()

    if not league:
        league = League(
            name=league_data['name'],
            country=league_data['country'],
            sport="football",
            season=season
        )
        session.add(league)
        session.commit()
        logger.success(f"Liga criada: {league.name}")
    else:
        logger.info(f"Liga já existe: {league.name}")

    return league


def get_or_create_team(session, team_data: dict, league: League) -> Team:
    """Busca ou cria um time no banco."""
    team = session.query(Team).filter_by(name=team_data['name']).first()

    if not team:
        team = Team(
            name=team_data['name'],
            country=league.country,
            league_id=league.id
        )
        session.add(team)
        session.commit()
        logger.success(f"Time criado: {team.name}")

    return team


def save_match(session, fixture: dict, league: League) -> Match:
    """Salva uma partida no banco."""
    fixture_id = fixture['fixture']['id']

    # Verifica se a partida já existe
    existing = session.query(Match).filter_by(id=fixture_id).first()
    if existing:
        logger.info(f"Partida já existe: {fixture_id}")
        return existing

    home_team = get_or_create_team(session, fixture['teams']['home'], league)
    away_team = get_or_create_team(session, fixture['teams']['away'], league)

    match_date = datetime.fromisoformat(
        fixture['fixture']['date'].replace('Z', '+00:00')
    )

    match = Match(
        id=fixture_id,
        league_id=league.id,
        home_team_id=home_team.id,
        away_team_id=away_team.id,
        match_date=match_date,
        matchday=fixture['league']['round'],
        home_score=fixture['score']['fulltime']['home'],
        away_score=fixture['score']['fulltime']['away'],
        status=fixture['fixture']['status']['short'],
        venue=fixture['fixture']['venue']['name']
    )

    session.add(match)
    session.commit()
    return match


def ingest_matches(league_id: int, season: int, date_from: str, date_to: str):
    """Pipeline completo de ingestão de partidas."""
    logger.info(f"Iniciando ingestão: liga {league_id}, {date_from} a {date_to}")

    # Busca partidas na API
    r = requests.get(
        f"{BASE_URL}/fixtures",
        headers=HEADERS,
        params={
            'league': league_id,
            'season': season,
            'from': date_from,
            'to': date_to
        }
    )

    data = r.json()
    fixtures = data['response']
    logger.info(f"{len(fixtures)} partidas encontradas na API")

    if not fixtures:
        logger.warning("Nenhuma partida encontrada!")
        return

    session = SessionLocal()

    try:
        # Pega info da liga do primeiro fixture
        league_info = fixtures[0]['league']
        league = get_or_create_league(
            session,
            {
                'name': league_info['name'],
                'country': league_info['country']
            },
            str(season)
        )

        # Salva cada partida
        saved = 0
        for fixture in fixtures:
            match = save_match(session, fixture, league)
            saved += 1

        logger.success(f"✅ {saved} partidas salvas no banco!")

    except Exception as e:
        logger.error(f"Erro durante ingestão: {e}")
        session.rollback()
        raise
    finally:
        session.close()


if __name__ == "__main__":
    # Premier League - março de 2025
    ingest_matches(
        league_id=39,
        season=2024,
        date_from='2025-03-01',
        date_to='2025-03-31'
    )