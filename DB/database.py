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