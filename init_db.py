from src.models.database import Base
from sqlalchemy import create_engine

engine = create_engine("sqlite:///./sports_analytics.db", echo=True)
Base.metadata.create_all(bind=engine)
print("✅ Tabelas criadas com sucesso!")