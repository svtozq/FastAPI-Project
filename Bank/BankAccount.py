import random
from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from DB.database import engine, get_db
from DB import models
from Users.signIn import get_user


router = APIRouter(prefix="/Bank", tags=["BankAccount"])


"Partie de Lenny pour les comptes bancaires"
# ✅ POST - Créer un compte bancaire
@router.post("/accounts/")
def create_account(user=Depends(get_user), db: Session = Depends(get_db)):

    # Vérifie s’il a déjà un compte actif
    account_count = db.query(models.BankAccount).filter(
        models.BankAccount.user_id == user["user_id"]
    ).count()

    if account_count >= 5:
        raise HTTPException(status_code=400, detail="L'utilisateur a atteint la limite de 5 comptes maximum")

    # Génère un IBAN fictif
    iban = "FR" + str(random.randint(10, 99)) + str(random.randrange(10 ** 11, 10 ** 12))

    account = models.BankAccount(
        user_id=user["user_id"],
        iban=iban,
        balance=0,
        clotured=False,
    )
    db.add(account)
    db.commit()
    db.refresh(account)
    return account


# ✅ GET - Récupérer tous les comptes
@router.get("/all_accounts/")
def get_accounts(db: Session = Depends(get_db)):
    accounts = db.query(models.BankAccount).all()
    return accounts


@router.get("/accounts/me")
def get_user_accounts(user=Depends(get_user), db: Session = Depends(get_db)):
    # Récupère les infos complètes depuis la DB
    db_user = db.query(models.UserAccount).filter(models.UserAccount.id == user["user_id"]).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")

    # Récupère ses comptes actifs
    accounts = db.query(models.BankAccount).filter(
        models.BankAccount.user_id == db_user.id,
        models.BankAccount.clotured == False
    ).all()

    return {
        "user": {
            "id": db_user.id,
            "email": db_user.email,
            "first_name": db_user.first_name,
            "last_name": db_user.last_name
        },
        "accounts": accounts
    }


# ✅ PUT - Clôturer un compte
@router.put("/accounts/{account_id}/close")
def close_account(account_id: int, db: Session = Depends(get_db)):
    account = db.query(models.BankAccount).filter(models.BankAccount.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Compte introuvable")

    if account.clotured:
        raise HTTPException(status_code=400, detail="Compte déjà clôturé")

    account.clotured = True
    db.commit()
    return {"message": f"Le compte {account_id} a été clôturé avec succès"}


