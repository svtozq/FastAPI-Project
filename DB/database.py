"""
Configuration de la base de données SQLite.

Ce module initialise la connexion SQLAlchemy,
définit la session et fournit une dépendance FastAPI
pour accéder à la base de données.
"""




from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite URL
SQLALCHEMY_DATABASE_URL = "sqlite:///DB/bank.db"

# SQLAlchemy and DB linked to communicate
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base for models tabless
Base = declarative_base()

def get_db():
    """
        Fournit une session de base de données SQLAlchemy.

        Utilisée comme dépendance FastAPI.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()