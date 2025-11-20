import re
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException
from datetime import datetime
from sqlalchemy import or_, and_

from sqlalchemy import or_, desc
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from DB import models
from DB.database import get_db
from Users.signIn import get_user
from DB.models import Beneficiary, BankAccount

router = APIRouter(prefix="/beneficiary", tags=["Beneficiary"])





@router.post("/")
def add_beneficiary(beneficiary_iban: str,last_name: str,first_name: str,db: Session = Depends(get_db),user=Depends(get_user)):
    # 🔹 Récupérer le compte de l'utilisateur connecté
    from_account = db.query(models.BankAccount).filter(models.BankAccount.user_id == user["user_id"]).first()

    if not from_account:
        raise HTTPException(status_code=404, detail="Compte utilisateur introuvable")

    # 🔹 Vérifier que l'utilisateur ne s'ajoute pas lui-même
    if beneficiary_iban == from_account.iban:
        raise HTTPException(status_code=400, detail="Vous ne pouvez pas vous ajouter vous-même")

    # 🔹 Vérifier que l'IBAN du bénéficiaire existe
    bank_account = db.query(models.BankAccount).filter(models.BankAccount.iban == beneficiary_iban).first()

    if not bank_account:
        raise HTTPException(status_code=400, detail="Cet IBAN n'est associé à aucun compte")

    # 🔹 Vérifier si le bénéficiaire existe déjà
    existing_beneficiary = db.query(models.Beneficiary).filter(
        models.Beneficiary.user_id == user["user_id"],
        models.Beneficiary.bank_account_id == bank_account.id
    ).first()

    if existing_beneficiary:
        raise HTTPException(status_code=400, detail="Le bénéficiaire existe déjà")

    # 🔹 Créer le bénéficiaire
    beneficiary = models.Beneficiary(
        bank_account_id=bank_account.iban,
        user_id=user["user_id"],
        last_name=last_name,
        first_name=first_name,
        Beneficiary_date=datetime.utcnow()
    )

    db.add(beneficiary)
    db.commit()
    db.refresh(beneficiary)

    return {
        "message": "Bénéficiaire ajouté avec succès",
        "beneficiary": {
            "id": beneficiary.id,
            "last_name": beneficiary.last_name,
            "first_name": beneficiary.first_name,
            "iban": bank_account.iban,
            "creation_date": beneficiary.Beneficiary_date.strftime("%Y-%m-%d %H:%M:%S")
        }
    }


@router.get("/")
def get_beneficiary(db: Session = Depends(get_db), user=Depends(get_user)):
    beneficiaries = (
        db.query(models.Beneficiary)
        .filter(models.Beneficiary.user_id == user["user_id"])
        .all()
    )

    return {"beneficiaries": beneficiaries}

