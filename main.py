import datetime
import random
import re
from passlib.hash import pbkdf2_sha256
import jwt
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import FastAPI, HTTPException
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

    class Config:
        orm_mode = True

class LoginRequest(BaseModel):
    email: str
    password: str

class BankAccount(BaseModel):
    id: int
    user_id: int
    iban: str
    balance: float
    clotured: bool

    class Config:
        orm_mode = True


secret_key = "very_secret_key"
algorithm = "HS256"

bearer_scheme = HTTPBearer()

def get_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=400, detail="Token expired !")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=400, detail="Invalid token !")

def generate_token(user: UserAccount):
    payload = {
        "sub": user.email,
        "user_id": user.id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    return jwt.encode(payload, secret_key, algorithm=algorithm)

@app.get("/me")
def me(user=Depends(get_user)):
    return user


@app.post("/users/")
def create_user(last_name: str, first_name: str, email: str, password: str, db: Session = Depends(get_db)):
    count = db.query(models.UserAccount).filter(models.UserAccount.email == email).count()

    if count > 0:
        raise HTTPException(status_code=400, detail="Email already registered")

    if not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email):
        raise HTTPException(status_code=400, detail="try again.. your mail address isn't valid !")

    if not re.fullmatch(r"[A-Za-z0-9@#$%^&+=]{8,}", password):
        raise HTTPException(status_code=400, detail="try again.. your password should be at least 8 characters long !")
    else:
        hashedPassword = pbkdf2_sha256.hash(password)

    now = datetime.datetime.now()

    user = models.UserAccount(
        last_name=last_name,
        first_name=first_name,
        email=email,
        password=hashedPassword,
        date=now
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    iban = "FR" + str(random.randint(10, 99)) + str(random.randrange(10 ** 11, 10 ** 12))

    bank = models.BankAccount(
        user_id=user.id,
        iban=iban,
        balance=0,
        clotured=False,
    )
    db.add(bank)
    db.commit()
    db.refresh(bank)

    return user, bank


@app.post("/login/")
def login(email, password, db: Session = Depends(get_db)):
    if not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email, ):
        raise HTTPException(status_code=400, detail="try again.. your mail address isn't valid !")

    user = db.query(models.UserAccount).filter(models.UserAccount.email == email).first()

    if user is None:
        raise HTTPException(status_code=400, detail="sorry this mail address isn't registered !")
    else:
        if not pbkdf2_sha256.verify(password, user.password):
            raise HTTPException(status_code=400, detail="try again.. your password is wrong !")

    token = generate_token(user)
    return {"your token": token}


@app.get("/users/")
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.UserAccount).all()
    if len(users) > 0:
        return {"users": users}
    else:
        return {"no users found"}


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