from fastapi import FastAPI
from pydantic import BaseModel
from sqlmodel import Session, create_engine
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    last_name: str = Field(index=True)
    first_name: str = Field(index=True)
    email: str = Field(index=True)


app = FastAPI()


class bankUser(BaseModel):
    iban: int
    balance: float
    clotured: bool


def get_session():
    with Session(create_engine) as session:
        yield session


@app.post("/accounts/create")
def create_account():
    with Session(create_engine) as session:
        account = bankUser(iban=12122122222, balance=0, clotured=False)
        session.add(account)
        session.commit()
        return {
            "message": "Compte créé avec succès",
            "account_number": account.iban,
            "solde : ": account.balance
        }


# -------------------- SQLALCHEMY CONFIGURATION --------------------
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
