import random

from fastapi import FastAPI, HTTPException
from models import User, BankAccount
from typing import List


app = FastAPI(title="Bank API")

# Bases de données simulées
users_db: List[User] = []
accounts_db: List[BankAccount] = []

# Compteurs auto-incrément pour IDs
user_counter = 1
account_counter = 1

# 1️⃣ Créer un utilisateur
@app.post("/users/", response_model=User)
def create_user(name: str, email: str):
    global user_counter
    # Vérifier si l'email existe déjà
    for user in users_db:
        if user.email == email:
            raise HTTPException(status_code=400, detail="Utilisateur déjà existant")
    iban = "FR" + str(random.randint(10, 99)) + str(random.randrange(10 ** 11, 10 ** 12))
    print(iban)

    user = User(id=user_counter, name=name, email=email, iban=iban)
    users_db.append(user)
    user_counter += 1
    return user

# 2️⃣ Ouvrir un compte bancaire
@app.post("/accounts/", response_model=BankAccount)
def open_account(user_id: int):
    global account_counter
    # Vérifier que l'utilisateur existe
    user_exists = any(user.id == user_id for user in users_db)
    if not user_exists:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

    # Vérifier si l'utilisateur a déjà un compte
    for acc in accounts_db:
        if acc.user_id == user_id:
            raise HTTPException(status_code=400, detail="Compte déjà ouvert pour cet utilisateur")

    account = BankAccount(account_id=account_counter, user_id=user_id)
    accounts_db.append(account)
    account_counter += 1
    return account

# 3️⃣ Lister tous les comptes
@app.get("/accounts/", response_model=List[BankAccount])
def list_accounts():
    return accounts_db







