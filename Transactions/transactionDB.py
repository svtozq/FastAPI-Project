from datetime import datetime

from pydantic import BaseModel
from sqlalchemy import or_, and_
from sqlalchemy import or_, desc
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from DB import models
from DB.database import get_db
from Users.signIn import get_user


router = APIRouter(prefix="/transactions", tags=["Transactions"])


# Fonction qui permet de transferer de l'argent du compte connecter a un compte existant

class TransferRequest(BaseModel):
    message: str
    to_account_id: str
    amount: float

@router.post("/")
def transfer_money(request: TransferRequest, user=Depends(get_user),db: Session = Depends(get_db)):
    message = request.message
    to_account_id = request.to_account_id
    amount = request.amount

    if amount <= 0:
        raise HTTPException(status_code=400, detail="Le montant doit être supérieur à 0")

    # 🔹 Récupérer le compte bancaire de l'utilisateur connecté (compte source)
    from_account = db.query(models.BankAccount).filter(models.BankAccount.user_id == user["user_id"]).first()

    #Condition
    if not from_account:
        raise HTTPException(status_code=404, detail="Compte de l'utilisateur non trouvé")

    if from_account.iban == to_account_id:
        raise HTTPException(status_code=400, detail="Impossible de transférer vers le même compte")

    # Récupérer les comptes
    to_account = db.query(models.BankAccount).filter(models.BankAccount.iban == to_account_id).first()
    to_account_user = db.query(models.UserAccount).filter(models.UserAccount.id == to_account.user_id).first()

    if not user["user_id"] or not to_account:
        raise HTTPException(status_code=404, detail="Compte introuvable")

    if from_account.clotured or to_account.clotured:
        raise HTTPException(status_code=400, detail="Un des comptes est clôturé")

    if from_account.balance < amount:
        raise HTTPException(status_code=400, detail="Solde insuffisant")

    # Effectuer la transaction
    from_account.balance -= amount
    to_account.balance += amount

    # 🔹 Enregistrer la transaction
    transaction = models.Transaction(
        sender_last_name=to_account_user.last_name,
        sender_first_name=to_account_user.first_name,
        from_account_id=from_account.id,
        to_account_id=to_account.id,
        message=message,
        balance=amount,
        transaction_date=datetime.utcnow()
    )

    # Met a jour la base de donnée
    db.add(transaction)

    db.commit()
    db.refresh(from_account)
    db.refresh(to_account)

    return {
        "message": f"{amount}€ transférés de {from_account.iban} vers {to_account.iban}",
        "from_account_balance": from_account.balance,
        "to_account_balance": to_account.balance
    }


class transfer_money_id(BaseModel):
    amount: float
    message: str
    iban_account: str

@router.post("/transfer_money_id")
def transfer_money_id(request: transfer_money_id,user=Depends(get_user),db: Session = Depends(get_db)):
    to_account_id = request.iban_account
    amount = request.amount
    message = request.message

    if amount <= 0:
        raise HTTPException(status_code=400, detail="Le montant doit être supérieur à 0")

    # 🔹 Récupérer le compte bancaire de l'utilisateur connecté (compte source)
    from_account = db.query(models.BankAccount).filter(models.BankAccount.user_id == user["user_id"]).first()

    #Condition
    if not from_account:
        raise HTTPException(status_code=404, detail="Compte de l'utilisateur non trouvé")

    if from_account.iban == to_account_id:
        raise HTTPException(status_code=400, detail="Impossible de transférer vers le même compte")

    # Récupérer les comptes
    to_account = db.query(models.BankAccount).filter(models.BankAccount.iban == to_account_id).first()
    to_account_user = db.query(models.UserAccount).filter(models.UserAccount.id == to_account.user_id).first()

    if not user["user_id"] or not to_account:
        raise HTTPException(status_code=404, detail="Compte introuvable")

    if from_account.clotured or to_account.clotured:
        raise HTTPException(status_code=400, detail="Un des comptes est clôturé")

    if from_account.balance < amount:
        raise HTTPException(status_code=400, detail="Solde insuffisant")

    # Effectuer la transaction
    from_account.balance -= amount
    to_account.balance += amount

    # 🔹 Enregistrer la transaction
    transaction = models.Transaction(
        sender_last_name=to_account_user.last_name,
        sender_first_name=to_account_user.first_name,
        from_account_id=from_account.id,
        to_account_id=to_account.id,
        message=message,
        balance=amount,
        transaction_date=datetime.utcnow()
    )

    # Met a jour la base de donnée
    db.add(transaction)

    db.commit()
    db.refresh(from_account)
    db.refresh(to_account)

    return {
        "message": f"{amount}€ transférés de {from_account.iban} vers {to_account.iban}",
        "from_account_balance": from_account.balance,
        "to_account_balance": to_account.balance
    }


# Fonction qui enregistre la transaction
@router.get("/history/")
def get_history_transaction(user=Depends(get_user), db: Session = Depends(get_db)):

    # 🔹 Récupérer le compte bancaire de l'utilisateur connecté (compte source)
    account = db.query(models.BankAccount).filter(models.BankAccount.user_id == user["user_id"]).first()

    # Condition
    if not account:
        raise HTTPException(status_code=404, detail="Compte utilisateur introuvable")

    # Requete qui recupere l'utilisateur qui est en lien avec la transaction
    transactions = db.query(models.Transaction).filter(
        or_(
            models.Transaction.from_account_id == account.id,
            models.Transaction.to_account_id == account.id
        )
    ).order_by(desc(models.Transaction.transaction_date)).all()

    if not transactions:
        raise HTTPException(status_code=404, detail="Aucune transaction trouvée pour cet utilisateur")

    return [
        {
            "id": t.id,
            "sender_first_name": t.sender_first_name,
            "sender_last_name": t.sender_last_name,
            "from_account_id": t.from_account_id,
            "to_account_id": t.to_account_id,
            "amount": t.balance,
            "message":t.message,
            "transaction_date": t.transaction_date.strftime("%Y-%m-%d %H:%M:%S") if t.transaction_date else None
        }
        for t in transactions
    ]





# Cette fonction recupere une transaction en particulier et ces informations du user connecté
@router.get("/history_id/")
def get_transaction_Byid(id: int,user=Depends(get_user), db: Session = Depends(get_db)):

    # Récupére le compte bancaire de l’utilisateur connecté
    account = db.query(models.BankAccount).filter(models.BankAccount.user_id == user["user_id"]).first()
    if not account:
        raise HTTPException(status_code=404, detail="Compte utilisateur introuvable")

    if not id:
        raise HTTPException(status_code=404, detail="Transaction introuvable")

    # Requete qui recupere le compte bancaire de l'utilisateur connecté et le compte bancaire de l'utilisateur en lien avec la transaction
    t = db.query(models.Transaction).filter(
        and_(
            models.Transaction.id == id,
            or_(
                models.Transaction.from_account_id == account.id,
                models.Transaction.to_account_id == account.id
            )
        )
    ).first()

    '''if not t:
        raise HTTPException(status_code=404, detail="Aucune transaction trouvée pour cet utilisateur")'''

    return [
        {
            "id": t.id,
            "first_name": t.sender_first_name,
            "last_name": t.sender_last_name,
            "from_account_id": t.from_account_id,
            "to_account_id": t.to_account_id,
            "amount": t.balance,
            "message":t.message,
            "transaction_date": t.transaction_date.strftime("%Y-%m-%d %H:%M:%S") if t.transaction_date else None
        }
    ]