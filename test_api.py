import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Buscando partidas de março de 2025 da Premier League
r = requests.get(
    'https://v3.football.api-sports.io/fixtures',
    headers={'x-apisports-key': os.getenv('API_FOOTBALL_KEY')},
    params={
        'league': 39,
        'season': 2024,
        'from': '2025-03-01',
        'to': '2025-03-31'
    }
)

data = r.json()
print('Total de partidas:', data['results'])

if data['results'] > 0:
    for m in data['response'][:5]:
        home = m['teams']['home']['name']
        away = m['teams']['away']['name']
        score = m['score']['fulltime']
        date = m['fixture']['date'][:10]
        print(f"{date} | {home} {score['home']} x {score['away']} {away}")