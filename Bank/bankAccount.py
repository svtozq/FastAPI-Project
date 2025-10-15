from fastapi import APIRouter, Depends
from sqlmodel import Session
from DB.database import get_session
from DB.database import bankUser

router = APIRouter(prefix="/accounts", tags=["accounts"])

@router.post("/create")
def create_account(user_id: int, db: Session = Depends(get_session)):
    account = bankUser(iban=user_id, balance=0, clotured=False)
    db.add(account)
    db.commit()
    db.refresh(account)
    return {"message": "Compte créé avec succès", "account_number": account.account_number}
