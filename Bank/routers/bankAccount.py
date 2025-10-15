from fastapi import APIRouter, HTTPException
from Bank.model import BankAccount  # ✅ corrigé
from Bank.data.memory_store import (  # ✅ corrigé
    add_account,
    get_account_by_id,
    get_user_by_id,
    get_account_by_user,
    accounts_db,
)

router = APIRouter(prefix="/accounts", tags=["Comptes bancaires"])
account_counter = 1  # ID auto-incrément

# Créer un compte bancaire
@router.post("/", response_model=BankAccount)
def open_account(user_id: int):
    global account_counter

    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")

    from Bank.data.memory_store import get_active_account_by_user

    if get_active_account_by_user(user_id):
        raise HTTPException(status_code=400, detail="L'utilisateur a déjà un compte actif")

    account = BankAccount(account_id=account_counter, user_id=user_id, balance=0)
    add_account(account)
    account_counter += 1
    return account


# Lister tous les comptes
@router.get("/", response_model=list[BankAccount])
def list_accounts():
    return accounts_db


# Voir les informations d’un compte
@router.get("/{account_id}", response_model=BankAccount)
def view_account(account_id: int):
    account = get_account_by_id(account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Compte introuvable")
    return account


# Clôturer un compte
@router.put("/{account_id}/close")
def close_account(account_id: int):
    account = get_account_by_id(account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Compte introuvable")
    if account.clotured:
        raise HTTPException(status_code=400, detail="Compte déjà clôturé")

    account.clotured = True
    return {"message": f"Le compte {account_id} a été clôturé avec succès"}
