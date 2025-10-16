"""import random
from fastapi import FastAPI, HTTPException
from Bank.models.model import User, BankAccount
from Bank.data.memory_store import add_user, add_account, users_db, get_user_by_email
from Bank.routers import bankAccount

app = FastAPI(title="Bank API - Mémoire")

user_counter = 1       # ID auto-incrément pour les utilisateurs
account_counter = 1    # ID auto-incrément pour les comptes

# 🔗 Inclusion du router "comptes bancaires"
app.include_router(bankAccount.router)


# 👤 Créer un utilisateur (avec compte auto-créé)
@app.post("/users/")
def create_user(name: str, email: str):
    """
    Crée un utilisateur et ouvre automatiquement son compte principal.
    """
    global user_counter, account_counter

    # Vérifie si l'email existe déjà
    if get_user_by_email(email):
        raise HTTPException(status_code=400, detail="Utilisateur déjà existant")

    # Génère un IBAN fictif
    iban = "FR" + str(random.randint(10, 99)) + str(random.randrange(10 ** 11, 10 ** 12))
    user = User(id=user_counter, name=name, email=email, iban=iban)
    add_user(user)

    # ✅ Création automatique d’un compte principal pour le nouvel utilisateur
    main_account = BankAccount(
        account_id=account_counter,
        user_id=user.id,
        balance=0,
        clotured=False
    )
    add_account(main_account)
    account_counter += 1
    user_counter += 1

    return {
        "message": f"Utilisateur '{user.name}' créé avec succès ✅",
        "compte": f"Compte principal ouvert automatiquement avec ID {main_account.account_id}",
        "user": user,
        "account": main_account
    }


# 📋 Lister tous les utilisateurs
@app.get("/users/", response_model=list[User])
def list_users():
    """Affiche la liste de tous les utilisateurs créés."""
    return users_db
"""