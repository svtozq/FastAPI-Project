from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from DB import models
from DB.database import get_db
from Users.signIn import get_user

router = APIRouter(prefix="/transactions", tags=["Transactions"])

"""ajouter de l'argent au compte de l'utilisateur"""

@router.post("/add-money")
def add_money(account_id : int, amount: float,db:Session = Depends(get_db), user=Depends(get_user)):

    if amount <= 0:
        raise HTTPException(status_code=400, detail="Le montant doit etre superieur a 0")

    account = db.query(models.BankAccount).filter(models.BankAccount.id == account_id,models.BankAccount.user_id == user["user_id"]).first()

    if not account:
        raise HTTPException(status_code=404, detail="Compte introuvable")

    if account.clotured:
        raise HTTPException(status_code=400, detail="Le compte est clôturé")

    account.balance += amount

    db.commit()
    db.refresh(account)
    return {
        "message": f"{amount}€ on été ajouté a votre compte : {account.iban}.",
        "new_balance": account.balance
    }




