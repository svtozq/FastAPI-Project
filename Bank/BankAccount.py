import random
from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from DB.database import engine, get_db
from DB import models


router = APIRouter(prefix="/Bank", tags=["BankAccount"])






"Partie de Lenny pour les comptes bancaires"
# ✅ POST - Créer un compte bancaire
@router.post("/accounts/")
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
@router.get("/accounts/")
def get_accounts(db: Session = Depends(get_db)):
    accounts = db.query(models.BankAccount).all()
    return accounts


# ✅ GET - Voir un compte par ID
@router.get("/accounts/{account_id}")
def get_account(account_id: int, db: Session = Depends(get_db)):
    account = db.query(models.BankAccount).filter(models.BankAccount.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Compte introuvable")
    return account


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
