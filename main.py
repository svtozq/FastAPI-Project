import datetime
import random
from pydantic import BaseModel
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from DB.database import SessionLocal, engine, get_db
from DB import models
#Pour importer depuis ma methode transaction
from Transactions.transactionDB import router as transactions_router




# Création automatique des tables dans la base SQLite
models.Base.metadata.create_all(bind=engine)
app = FastAPI()
# Ouali lie mon code au main via router
app.include_router(transactions_router)


class UserAccount(BaseModel):
    id: int
    last_name: str
    first_name: str
    email: str
    password: str
    date: datetime.datetime

class BankAccount(BaseModel):
    id: int
    user_id: int
    iban: str
    balance: float
    clotured: bool

    class Config:
        orm_mode = True

# ✅ Exemple 1 : créer un utilisateur
@app.post("/users/")
def create_user(last_name: str, first_name: str, email: str, password: str, db: Session = Depends(get_db)):
    now = datetime.datetime.now()

    user = models.UserAccount(
        last_name=last_name,
        first_name=first_name,
        email=email,
        password=password,
        date=now
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# ✅ Exemple 2 : afficher tous les utilisateurs
@app.get("/users/")
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.UserAccount).all()
    return users





"Partie de Lenny pour les comptes bancaires"
# ✅ POST - Créer un compte bancaire
@app.post("/accounts/")
def create_account(user_id: int, db: Session = Depends(get_db)):
    # Vérifie si l'utilisateur existe
    user = db.query(models.UserAccount).filter(models.UserAccount.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")

    # Vérifie s’il a déjà un compte actif
    existing = (
        db.query(models.BankAccount)
        .filter(models.BankAccount.user_id == user_id, models.BankAccount.clotured == False)
        .first()
    )
    if existing:
        raise HTTPException(status_code=400, detail="L'utilisateur a déjà un compte actif")

    # Génère un IBAN fictif
    iban = "FR" + str(random.randint(10, 99)) + str(random.randrange(10 ** 11, 10 ** 12))

    account = models.BankAccount(
        user_id=user_id,
        iban=iban,
        balance=0,
        clotured=False,
    )
    db.add(account)
    db.commit()
    db.refresh(account)
    return account


# ✅ GET - Récupérer tous les comptes
@app.get("/accounts/")
def get_accounts(db: Session = Depends(get_db)):
    accounts = db.query(models.BankAccount).all()
    return accounts


# ✅ GET - Voir un compte par ID
@app.get("/accounts/{account_id}")
def get_account(account_id: int, db: Session = Depends(get_db)):
    account = db.query(models.BankAccount).filter(models.BankAccount.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Compte introuvable")
    return account


# ✅ PUT - Clôturer un compte
@app.put("/accounts/{account_id}/close")
def close_account(account_id: int, db: Session = Depends(get_db)):
    account = db.query(models.BankAccount).filter(models.BankAccount.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Compte introuvable")

    if account.clotured:
        raise HTTPException(status_code=400, detail="Compte déjà clôturé")

    account.clotured = True
    db.commit()
    return {"message": f"Le compte {account_id} a été clôturé avec succès"}


class Item(BaseModel):
    name: str
    description: str
    price: float
    tax: float


@app.post("/items/")
def create_item(item: Item) -> Item:
    return item