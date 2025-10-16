from Bank.models.model import User, BankAccount

# "Base de données" en mémoire
users_db = []
accounts_db = []

# -----------------------------
# 👤 UTILISATEURS
# -----------------------------
def add_user(user: User):
    users_db.append(user)

def get_user_by_id(user_id: int):
    return next((u for u in users_db if u.id == user_id), None)

def get_user_by_email(email: str):
    return next((u for u in users_db if u.email == email), None)

# -----------------------------
# 🏦 COMPTES BANCAIRES
# -----------------------------
def add_account(account: BankAccount):
    accounts_db.append(account)

def get_account_by_id(account_id: int):
    return next((a for a in accounts_db if a.account_id == account_id), None)

def get_account_by_user(user_id: int):
    """Renvoie le premier compte de l'utilisateur, qu'il soit actif ou non."""
    return next((a for a in accounts_db if a.user_id == user_id), None)

def get_active_account_by_user(user_id: int):
    """Renvoie uniquement le compte actif de l'utilisateur."""
    return next((a for a in accounts_db if a.user_id == user_id and not a.clotured), None)
