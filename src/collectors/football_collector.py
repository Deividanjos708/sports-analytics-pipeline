import requests
import os
from dotenv import load_dotenv
from loguru import logger
from datetime import datetime

load_dotenv()

API_KEY = os.getenv("API_FOOTBALL_KEY")
BASE_URL = os.getenv("API_FOOTBALL_BASE_URL")

HEADERS = {
    "x-apisports-key": API_KEY
}

# IDs das ligas na API
LEAGUES = {
    "premier_league": 39,
    "serie_a": 135,
    "brasileirao": 71
}


def get_league_info(league_id: int) -> dict:
    """Busca informações de uma liga."""
    url = f"{BASE_URL}/leagues"
    params = {"id": league_id}

    logger.info(f"Buscando info da liga {league_id}...")
    response = requests.get(url, headers=HEADERS, params=params)

    if response.status_code == 200:
        data = response.json()
        logger.success(f"Liga encontrada: {data['response'][0]['league']['name']}")
        return data['response'][0]
    else:
        logger.error(f"Erro {response.status_code}: {response.text}")
        return {}


def get_standings(league_id: int, season: int) -> list:
    """Busca classificação de uma liga."""
    url = f"{BASE_URL}/standings"
    params = {"league": league_id, "season": season}

    logger.info(f"Buscando classificação da liga {league_id} temporada {season}...")
    response = requests.get(url, headers=HEADERS, params=params)

    if response.status_code == 200:
        data = response.json()
        standings = data['response'][0]['league']['standings'][0]
        logger.success(f"{len(standings)} times encontrados!")
        return standings
    else:
        logger.error(f"Erro {response.status_code}: {response.text}")
        return []


def get_matches(league_id: int, season: int, last: int = 10) -> list:
    """Busca últimas partidas de uma liga."""
    url = f"{BASE_URL}/fixtures"
    params = {
        "league": league_id,
        "season": season,
        "last": last
    }

    logger.info(f"Buscando últimas {last} partidas...")
    response = requests.get(url, headers=HEADERS, params=params)

    if response.status_code == 200:
        data = response.json()
        matches = data['response']
        logger.success(f"{len(matches)} partidas encontradas!")
        return matches
    else:
        logger.error(f"Erro {response.status_code}: {response.text}")
        return []


def get_match_statistics(fixture_id: int) -> list:
    """Busca estatísticas detalhadas de uma partida."""
    url = f"{BASE_URL}/fixtures/statistics"
    params = {"fixture": fixture_id}

    logger.info(f"Buscando estatísticas da partida {fixture_id}...")
    response = requests.get(url, headers=HEADERS, params=params)

    if response.status_code == 200:
        data = response.json()
        logger.success(f"Estatísticas obtidas!")
        return data['response']
    else:
        logger.error(f"Erro {response.status_code}: {response.text}")
        return []


if __name__ == "__main__":
    # Teste rápido
    print("\n🏴󠁧󠁢󠁥󠁮󠁧󠁿 Testando Premier League...")
    league = get_league_info(LEAGUES["premier_league"])
    print(f"Liga: {league['league']['name']} - {league['country']['name']}")

    print("\n📊 Buscando últimas partidas...")
    matches = get_matches(LEAGUES["premier_league"], 2024, last=3)
    for m in matches:
        home = m['teams']['home']['name']
        away = m['teams']['away']['name']
        score = m['score']['fulltime']
        print(f"  {home} {score['home']} x {score['away']} {away}")