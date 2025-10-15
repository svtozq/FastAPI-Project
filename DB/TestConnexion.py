from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from DB.database import DATABASE_URL

# Crée le moteur SQLAlchemy
engine = create_engine(DATABASE_URL)

# Crée une session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

try:
    db = SessionLocal()
    # Essaye une simple requête SQL
    result = db.execute(text("SELECT DATABASE();")).fetchone()
    print("Connexion réussie ! Base actuelle :", result[0])
except Exception as e:
    print("Erreur de connexion :", e)
finally:
    db.close()
