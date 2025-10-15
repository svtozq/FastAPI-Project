from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL de la base SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///DB/bank.db"

# Le moteur (engine) permet à SQLAlchemy de communiquer avec la BDD
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Pour créer des sessions de connexion
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base pour les modèles (tables)
Base = declarative_base()