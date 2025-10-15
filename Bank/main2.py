"""import random
from fastapi import FastAPI, HTTPException
from Bank.model import User                # ✅ corrigé
from Bank.data.memory_store import add_user, users_db, get_user_by_email  # ✅ corrigé
from Bank.routers import bankAccount       # ✅ corrigé


app = FastAPI(title="Bank API - Mémoire")
user_counter = 1  # ID auto-incrément

# Inclusion du router comptes
app.include_router(bankAccount.router)

# Créer un utilisateur
@app.post("/users/", response_model=User)
def create_user(name: str, email: str):
    global user_counter

    if get_user_by_email(email):
        raise HTTPException(status_code=400, detail="Utilisateur déjà existant")

    iban = "FR" + str(random.randint(10, 99)) + str(random.randrange(10 ** 11, 10 ** 12))
    user = User(id=user_counter, name=name, email=email, iban=iban)
    add_user(user)
    user_counter += 1
    return user

# Lister tous les utilisateurs
@app.get("/users/", response_model=list[User])
def list_users():
    return users_db
"""