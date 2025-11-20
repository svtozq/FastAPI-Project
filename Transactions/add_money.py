from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from DB import models
from DB.database import get_db
from Users.signIn import get_user
from pydantic import BaseModel

router = APIRouter(prefix="/transactions", tags=["Transactions"])

class AddMoneyRequest(BaseModel):
    amount: float
    from_account_id: int
    to_account_id: int

"""ajouter de l'argent au compte de l'utilisateur"""
@router.post("/add-money")
def add_money(request: AddMoneyRequest, db: Session = Depends(get_db), user=Depends(get_user)):
    amount = request.amount
    from_account_id = request.from_account_id
    to_account_id = request.to_account_id

    # Vérification montant
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Le montant doit etre superieur a 0")

    # Empêcher le transfert vers soi-même
    if from_account_id == to_account_id:
        raise HTTPException(status_code=400, detail="Impossible de transférer vers le même compte.")

    # Récupérer compte source
    from_account = db.query(models.BankAccount).filter(
        models.BankAccount.id == from_account_id,
        models.BankAccount.user_id == user["user_id"]
    ).first()

    if not from_account:
        raise HTTPException(status_code=404, detail="Compte source introuvable")

    if from_account.clotured:
        raise HTTPException(status_code=400, detail="Le compte source est clôturé")

    # Récupérer compte destinataire
    to_account = db.query(models.BankAccount).filter(
        models.BankAccount.id == to_account_id,
        models.BankAccount.user_id == user["user_id"]
    ).first()

    if not to_account:
        raise HTTPException(status_code=404, detail="Compte destinataire introuvable")

    if to_account.clotured:
        raise HTTPException(status_code=400, detail="Le compte destinataire est clôturé")

    # Vérification solde suffisant
    if from_account.balance < amount:
        raise HTTPException(status_code=400, detail="Solde insuffisant sur le compte source")

    # --- TRANSFERT ---
    from_account.balance -= amount
    to_account.balance += amount

    db.commit()
    db.refresh(from_account)
    db.refresh(to_account)

    return {
        "message": f"Transfert de {amount} € effectué : {from_account.type} → {to_account.type}",
        "from_new_balance": from_account.balance,
        "to_new_balance": to_account.balance
    }




