# ⚽ Sports Analytics Pipeline

> Pipeline de análise esportiva de alta performance para coleta, processamento e visualização de dados de ligas internacionais.

![Python](https://img.shields.io/badge/Python-3.14-blue?style=flat-square&logo=python)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-red?style=flat-square)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-ff4b4b?style=flat-square&logo=streamlit)
![Plotly](https://img.shields.io/badge/Plotly-Interactive-3D4DB7?style=flat-square&logo=plotly)
![Status](https://img.shields.io/badge/Status-Active-success?style=flat-square)

---

## 🎯 Sobre o Projeto

Sistema end-to-end de engenharia e análise de dados esportivos, desenvolvido com foco em arquitetura profissional e boas práticas de mercado.

O pipeline coleta dados reais via API, persiste em banco de dados relacional, processa métricas avançadas de performance e exibe tudo em um dashboard interativo.

**Ligas suportadas:**
- 🏴󠁧󠁢󠁥󠁮󠁧󠁿 Premier League (Inglaterra)
- 🇮🇹 Serie A (Itália)  
- 🇧🇷 Brasileirão Série A

---

## 🏗️ Arquitetura

[API-Football] → [Collectors] → [SQLite/PostgreSQL] → [Analytics] → [Dashboard]
↑               ↑                  ↑                  ↑              ↑
Dados reais      Python            SQLAlchemy          Pandas        Streamlit
requests            ORM               NumPy          Plotly


---

## 📊 Funcionalidades

- **Coleta automatizada** de partidas, times e ligas via API REST
- **Banco de dados relacional** com 6 entidades modeladas (League, Team, Match, MatchStats, Odds, Player)
- **Pipeline de ingestão** com tratamento de duplicatas e logging estruturado
- **Análise de performance** com ranking, taxa de vitória e saldo de gols
- **Análise de vantagem em casa** com métricas estatísticas reais
- **Dashboard interativo** com filtros dinâmicos, gráficos e KPIs
- **Arquitetura modular** separada em camadas (collectors, models, processors, analytics)

---

## 🛠️ Stack Tecnológica

| Camada | Tecnologia | Função |
|--------|-----------|--------|
| Coleta | `requests` + API-Football | Ingestão de dados reais |
| Banco | `SQLAlchemy` + SQLite | Persistência e modelagem |
| Análise | `Pandas` + `NumPy` | Processamento e métricas |
| Dashboard | `Streamlit` + `Plotly` | Visualização interativa |
| Logs | `Loguru` | Monitoramento do pipeline |
| Config | `python-dotenv` | Gestão de variáveis de ambiente |

---

## 🚀 Como Executar

### Pré-requisitos
- Python 3.10+
- Conta gratuita em [api-football.com](https://www.api-football.com)

### Instalação

```bash
# Clone o repositório
git clone https://github.com/Deividanjos708/sports-analytics-pipeline.git
cd sports-analytics-pipeline

# Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instale as dependências
pip install -r requirements.txt
```

### Configuração

```bash
# Crie o arquivo .env
cp .env.example .env

# Preencha com sua chave de API
API_FOOTBALL_KEY=sua_chave_aqui
DATABASE_URL=sqlite:///./sports_analytics.db
API_FOOTBALL_BASE_URL=https://v3.football.api-sports.io
```

### Execução

```bash
# 1. Cria as tabelas no banco
python init_db.py

# 2. Ingere dados reais da Premier League
python -m src.collectors.data_ingestion

# 3. Visualiza análises no terminal
python -m src.analytics.match_analysis

# 4. Abre o dashboard interativo
streamlit run dashboard/app.py
```

---

## 📁 Estrutura do Projeto

sports-analytics-pipeline/
│
├── src/
│   ├── collectors/          # Coleta de dados via API
│   │   ├── football_collector.py
│   │   └── data_ingestion.py
│   ├── models/              # Modelos do banco de dados
│   │   ├── database.py      # Entidades ORM
│   │   └── base.py          # Configuração do engine
│   ├── processors/          # Transformação de dados
│   └── analytics/           # Análises e métricas
│       └── match_analysis.py
│
├── dashboard/
│   └── app.py               # Dashboard Streamlit
│
├── data/
│   ├── raw/                 # Dados brutos
│   └── processed/           # Dados processados
│
├── tests/                   # Testes automatizados
├── init_db.py               # Script de inicialização
├── requirements.txt
└── .env.example

---

## 📈 Exemplos de Análises

🏆 RANKING — MARÇO 2025 (Premier League)
──────────────────────────────────────────
Nottingham Forest   6 pts  |  100% aproveitamento
Manchester United   4 pts  |  50% aproveitamento
Brighton            4 pts  |  50% aproveitamento
🏠 VANTAGEM EM CASA
Vitórias casa:  38.9%
Vitórias fora:  33.3%
Empates:        27.8%
⚽ GOLS
Média por jogo:  2.44
Partidas +2.5:   44.4%

---

## 🔮 Próximos Passos

- [ ] Integração com odds de mercado em tempo real
- [ ] Análise preditiva com Machine Learning
- [ ] Suporte à NBA e Serie A italiana
- [ ] Deploy na nuvem (Railway / Render)
- [ ] Agendamento automático do pipeline (Airflow)
- [ ] Testes automatizados com pytest

---

## 👨‍💻 Autor

Desenvolvido por **Deivid Anjos**  
Estudante de Análise e Desenvolvimento de Sistemas

[![GitHub](https://img.shields.io/badge/GitHub-Deividanjos708-black?style=flat-square&logo=github)](https://github.com/Deividanjos708)

---

*Projeto desenvolvido para portfólio profissional — dados reais, arquitetura real, código de produção.*

