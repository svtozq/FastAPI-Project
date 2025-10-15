from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from DB import models
from DB.database import get_db

router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.post("/")
def transfer_money(from_account_id: int, to_account_id: int, amount: float, db: Session = Depends(get_db)):
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Le montant doit être supérieur à 0")

    """if from_account_id == to_account_id:
        raise HTTPException(status_code=400, detail="Impossible de transférer vers le même compte")"""

    # Récupérer les comptes
    from_account = db.query(models.BankAccount).filter(models.BankAccount.id == from_account_id).first()
    to_account = db.query(models.BankAccount).filter(models.BankAccount.id == to_account_id).first()

    if not from_account or not to_account:
        raise HTTPException(status_code=404, detail="Compte introuvable")

    if from_account.clotured or to_account.clotured:
        raise HTTPException(status_code=400, detail="Un des comptes est clôturé")

    if from_account.balance < amount:
        raise HTTPException(status_code=400, detail="Solde insuffisant")

    # Effectuer la transaction
    from_account.balance -= amount
    to_account.balance += amount

    db.commit()
    db.refresh(from_account)
    db.refresh(to_account)

    return {
        "message": f"{amount}€ transférés de {from_account.iban} vers {to_account.iban}",
        "from_account_balance": from_account.balance,
        "to_account_balance": to_account.balance
    }
