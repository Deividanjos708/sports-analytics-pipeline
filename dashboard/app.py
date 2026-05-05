import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.analytics.match_analysis import (
    get_matches_dataframe,
    calculate_team_performance,
    home_advantage_analysis,
    goals_analysis
)

load_dotenv()

# ── Configuração da página ──────────────────────────────────────
st.set_page_config(
    page_title="Sports Analytics Pipeline",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CSS customizado ─────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #0e1117; }
    .metric-card {
        background: linear-gradient(135deg, #1e2130, #252840);
        border-radius: 12px;
        padding: 20px;
        border-left: 4px solid #00d4ff;
        margin: 8px 0;
    }
    h1 { color: #00d4ff !important; }
    .stMetric { background: #1e2130; border-radius: 8px; padding: 10px; }
</style>
""", unsafe_allow_html=True)

# ── Header ───────────────────────────────────────────────────────
st.title("⚽ Sports Analytics Pipeline")
st.markdown("**Pipeline de análise esportiva de alta performance** — Premier League 2024/25")
st.divider()

# ── Carrega dados ────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = get_matches_dataframe()
    perf = calculate_team_performance(df)
    home = home_advantage_analysis(df)
    goals = goals_analysis(df)
    return df, perf, home, goals

df, perf, home_stats, goals_stats = load_data()

# ── Sidebar ──────────────────────────────────────────────────────
with st.sidebar:
    st.header("🎛️ Filtros")
    selected_teams = st.multiselect(
        "Times",
        options=sorted(df['home_team'].unique()),
        default=[]
    )
    st.divider()
    st.markdown("**Fonte:** API-Football")
    st.markdown("**Período:** Mar 2025")
    st.markdown("**Liga:** Premier League")

# ── KPIs principais ──────────────────────────────────────────────
st.subheader("📊 Visão Geral")
col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Partidas", home_stats['total_matches'])
col2.metric("Média Gols/Jogo", goals_stats['avg_goals_per_match'])
col3.metric("Vitórias Casa", f"{home_stats['home_win_pct']}%")
col4.metric("Vitórias Fora", f"{home_stats['away_win_pct']}%")
col5.metric("+2.5 Gols", f"{goals_stats['pct_over_2_5']}%")

st.divider()

# ── Gráficos ─────────────────────────────────────────────────────
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("🏆 Ranking de Performance")
    fig_ranking = px.bar(
        perf.head(10),
        x='points',
        y='team',
        orientation='h',
        color='win_rate',
        color_continuous_scale='Blues',
        labels={'points': 'Pontos', 'team': 'Time', 'win_rate': 'Taxa Vitória %'},
        title='Top 10 Times por Pontos'
    )
    fig_ranking.update_layout(
        plot_bgcolor='#1e2130',
        paper_bgcolor='#1e2130',
        font_color='white',
        yaxis={'categoryorder': 'total ascending'}
    )
    st.plotly_chart(fig_ranking, use_container_width=True)

with col_right:
    st.subheader("🏠 Distribuição de Resultados")
    fig_pie = px.pie(
        values=[
            home_stats['home_wins'],
            home_stats['away_wins'],
            home_stats['draws']
        ],
        names=['Vitória Casa', 'Vitória Fora', 'Empate'],
        color_discrete_sequence=['#00d4ff', '#ff6b6b', '#ffd93d'],
        hole=0.4
    )
    fig_pie.update_layout(
        plot_bgcolor='#1e2130',
        paper_bgcolor='#1e2130',
        font_color='white'
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# ── Gols por time ────────────────────────────────────────────────
st.subheader("⚽ Gols Marcados vs Sofridos")
fig_goals = go.Figure()
fig_goals.add_trace(go.Bar(
    name='Gols Marcados',
    x=perf['team'],
    y=perf['goals_scored'],
    marker_color='#00d4ff'
))
fig_goals.add_trace(go.Bar(
    name='Gols Sofridos',
    x=perf['team'],
    y=perf['goals_conceded'],
    marker_color='#ff6b6b'
))
fig_goals.update_layout(
    barmode='group',
    plot_bgcolor='#1e2130',
    paper_bgcolor='#1e2130',
    font_color='white',
    xaxis_tickangle=-45
)
st.plotly_chart(fig_goals, use_container_width=True)

# ── Tabela detalhada ─────────────────────────────────────────────
st.subheader("📋 Tabela Completa de Partidas")

display_df = df[['match_date', 'home_team', 'home_score',
                  'away_score', 'away_team', 'venue']].copy()
display_df['match_date'] = display_df['match_date'].dt.strftime('%d/%m/%Y')
display_df.columns = ['Data', 'Casa', 'Gols Casa', 'Gols Fora', 'Fora', 'Estádio']

if selected_teams:
    display_df = display_df[
        display_df['Casa'].isin(selected_teams) |
        display_df['Fora'].isin(selected_teams)
    ]

st.dataframe(display_df, use_container_width=True, hide_index=True)