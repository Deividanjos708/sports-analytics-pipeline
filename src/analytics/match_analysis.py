from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import pandas as pd
import os
from dotenv import load_dotenv
from loguru import logger

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)


def get_matches_dataframe() -> pd.DataFrame:
    """Carrega todas as partidas em um DataFrame."""
    query = """
        SELECT 
            m.id,
            m.match_date,
            m.matchday,
            m.home_score,
            m.away_score,
            m.status,
            m.venue,
            t1.name AS home_team,
            t2.name AS away_team,
            l.name AS league,
            l.season
        FROM matches m
        JOIN teams t1 ON m.home_team_id = t1.id
        JOIN teams t2 ON m.away_team_id = t2.id
        JOIN leagues l ON m.league_id = l.id
    """
    df = pd.read_sql(query, engine)
    df['match_date'] = pd.to_datetime(df['match_date'])
    return df


def calculate_team_performance(df: pd.DataFrame) -> pd.DataFrame:
    """Calcula performance de cada time — vitórias, derrotas, gols."""
    teams = {}

    for _, row in df.iterrows():
        home = row['home_team']
        away = row['away_team']
        hs = row['home_score']
        as_ = row['away_score']

        if pd.isna(hs) or pd.isna(as_):
            continue

        # Inicializa times
        for t in [home, away]:
            if t not in teams:
                teams[t] = {
                    'team': t,
                    'games': 0,
                    'wins': 0,
                    'draws': 0,
                    'losses': 0,
                    'goals_scored': 0,
                    'goals_conceded': 0,
                    'points': 0
                }

        teams[home]['games'] += 1
        teams[away]['games'] += 1
        teams[home]['goals_scored'] += hs
        teams[home]['goals_conceded'] += as_
        teams[away]['goals_scored'] += as_
        teams[away]['goals_conceded'] += hs

        if hs > as_:  # Vitória do mandante
            teams[home]['wins'] += 1
            teams[home]['points'] += 3
            teams[away]['losses'] += 1
        elif hs < as_:  # Vitória do visitante
            teams[away]['wins'] += 1
            teams[away]['points'] += 3
            teams[home]['losses'] += 1
        else:  # Empate
            teams[home]['draws'] += 1
            teams[away]['draws'] += 1
            teams[home]['points'] += 1
            teams[away]['points'] += 1

    performance = pd.DataFrame(list(teams.values()))
    performance['goal_diff'] = (
        performance['goals_scored'] - performance['goals_conceded']
    )
    performance['win_rate'] = (
        performance['wins'] / performance['games'] * 100
    ).round(1)

    return performance.sort_values('points', ascending=False)


def home_advantage_analysis(df: pd.DataFrame) -> dict:
    """Analisa a vantagem de jogar em casa."""
    finished = df[df['status'] == 'FT'].copy()

    home_wins = len(finished[finished['home_score'] > finished['away_score']])
    away_wins = len(finished[finished['home_score'] < finished['away_score']])
    draws = len(finished[finished['home_score'] == finished['away_score']])
    total = len(finished)

    return {
        'total_matches': total,
        'home_wins': home_wins,
        'away_wins': away_wins,
        'draws': draws,
        'home_win_pct': round(home_wins / total * 100, 1),
        'away_win_pct': round(away_wins / total * 100, 1),
        'draw_pct': round(draws / total * 100, 1),
        'avg_goals_home': round(finished['home_score'].mean(), 2),
        'avg_goals_away': round(finished['away_score'].mean(), 2),
    }


def goals_analysis(df: pd.DataFrame) -> dict:
    """Análise de gols."""
    finished = df[df['status'] == 'FT'].copy()
    finished['total_goals'] = finished['home_score'] + finished['away_score']

    return {
        'avg_goals_per_match': round(finished['total_goals'].mean(), 2),
        'max_goals_match': int(finished['total_goals'].max()),
        'matches_over_2_5': len(finished[finished['total_goals'] > 2]),
        'matches_btts': len(
            finished[
                (finished['home_score'] > 0) & (finished['away_score'] > 0)
            ]
        ),
        'pct_over_2_5': round(
            len(finished[finished['total_goals'] > 2]) / len(finished) * 100, 1
        ),
    }


if __name__ == "__main__":
    print("\n📊 SPORTS ANALYTICS PIPELINE — RELATÓRIO\n")
    print("=" * 50)

    df = get_matches_dataframe()
    print(f"\n✅ {len(df)} partidas carregadas do banco\n")

    # Performance dos times
    print("🏆 RANKING DE PERFORMANCE — MARÇO 2025")
    print("-" * 50)
    perf = calculate_team_performance(df)
    print(perf[['team', 'games', 'wins', 'draws', 'losses',
                 'goals_scored', 'goal_diff', 'points',
                 'win_rate']].to_string(index=False))

    # Vantagem em casa
    print("\n🏠 ANÁLISE DE VANTAGEM EM CASA")
    print("-" * 50)
    home = home_advantage_analysis(df)
    print(f"  Vitórias em casa:    {home['home_wins']} ({home['home_win_pct']}%)")
    print(f"  Vitórias fora:       {home['away_wins']} ({home['away_win_pct']}%)")
    print(f"  Empates:             {home['draws']} ({home['draw_pct']}%)")
    print(f"  Média gols (casa):   {home['avg_goals_home']}")
    print(f"  Média gols (fora):   {home['avg_goals_away']}")

    # Análise de gols
    print("\n⚽ ANÁLISE DE GOLS")
    print("-" * 50)
    goals = goals_analysis(df)
    print(f"  Média de gols/jogo:  {goals['avg_goals_per_match']}")
    print(f"  Máximo em um jogo:   {goals['max_goals_match']}")
    print(f"  Partidas +2.5 gols:  {goals['matches_over_2_5']} ({goals['pct_over_2_5']}%)")
    print(f"  Ambos marcaram:      {goals['matches_btts']}")