"""
Gestion des comptes bancaires.

Ce module contient les endpoints permettant de créer, consulter
et clôturer des comptes bancaires pour les utilisateurs authentifiés.
"""



import datetime
import random
from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from DB.database import engine, get_db
from DB import models
from Users.signIn import get_user
from pydantic import BaseModel


router = APIRouter(prefix="/Bank", tags=["BankAccount"])
"""
Router FastAPI dédié à la gestion des comptes bancaires.
"""


class BankAccount(BaseModel):
    """
        Modèle représentant les données nécessaires
        à la création d'un compte bancaire.
    """
    type: str


"Partie de Lenny pour les comptes bancaires"
# ✅ POST - Créer un compte bancaire
@router.post("/accounts/")
def create_account(data : BankAccount, user=Depends(get_user), db: Session = Depends(get_db)):
    """
        Crée un nouveau compte bancaire pour l'utilisateur connecté.

        - Génère automatiquement un IBAN fictif
        - Vérifie la limite maximale de comptes
        - Définit un compte principal si aucun n'existe

        :return: Compte bancaire créé
    """



    # Génère un IBAN fictif
    iban = "FR" + str(random.randint(10, 99)) + str(random.randrange(10 ** 11, 10 ** 12))

    now = datetime.datetime.now()

    acc_type = data.type

    # Vérifie s’il a déjà un compte actif
    account_count = db.query(models.BankAccount).filter(
        models.BankAccount.user_id == user["user_id"],
        models.BankAccount.clotured == False
    ).count()

    if account_count >= 5:
        raise HTTPException(status_code=400, detail="L'utilisateur a atteint la limite de 5 comptes maximum")

    if account_count < 1 :
        account = models.BankAccount(
            user_id=user["user_id"],
            iban=iban,
            balance=0,
            clotured=False,
            type="Compte Principal",
            BankAccount_date=now,
        )

    elif account_count >= 1 :
        account = models.BankAccount(
            user_id=user["user_id"],
            iban=iban,
            balance=0,
            clotured=False,
            type=acc_type,
            BankAccount_date=now,
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
    """
        Récupère les informations de l'utilisateur connecté
        ainsi que la liste de ses comptes bancaires actifs.
    """
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

# ✅ GET - Détail d’un compte
@router.get("/account/detail/{account_id}")
def get_account_details(account_id: int, user=Depends(get_user), db: Session = Depends(get_db)):
    account = db.query(models.BankAccount).filter( models.BankAccount.id == account_id, models.BankAccount.user_id == user["user_id"] ).first()
    if not account: raise HTTPException(status_code=404, detail="Compte introuvable")
    return { "id": account.id, "iban": account.iban, "balance": account.balance, "type": account.type, "opened_at": account.BankAccount_date, "clotured": account.clotured, }


# ✅ PUT - Clôturer un compte
@router.put("/accounts/{account_id}/close")
def close_account(account_id: int, user=Depends(get_user), db: Session = Depends(get_db)):
    main_account = db.query(models.BankAccount).filter(
        models.BankAccount.user_id == user["user_id"],
        models.BankAccount.type == "Compte Principal"
    ).first()

    account = db.query(models.BankAccount).filter(
        models.BankAccount.id == account_id,
                models.BankAccount.user_id == user["user_id"]
    ).first()


    if not account:
        raise HTTPException(status_code=404, detail="Compte introuvable")

    if account.clotured:
        raise HTTPException(status_code=400, detail="Compte déjà clôturé")

    if account.type == main_account.type:
        raise HTTPException(status_code=400, detail="Vous ne pouvez pas cloturer votre compte principal")

    account.clotured = True
    db.commit()
    return {"message": f"Le compte {account_id} a été clôturé avec succès"}










