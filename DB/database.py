from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configuration de la base de données MySQL via XAMPP
DATABASE_URL = "mysql+pymysql://root:@localhost:3306/db_fastapi"

# Crée le moteur SQLAlchemy
engine = create_engine(DATABASE_URL)

# Création d'une session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base pour les modèles
Base = declarative_base()
