import re
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException
from main import app


class Beneficiary(BaseModel):
    id: int
    bank_account_id: int
    beneficiary_iban: str
    last_name: str
    first_name: str

beneficiariesList = []


@app.post("/")
def add_beneficiary(bank_account_id: int, beneficiary_iban: str, last_name: str, first_name: str):
    if not re.fullmatch(r"[A-Z0-9]{10,34}", beneficiary_iban):
        raise HTTPException(status_code=400, detail="Invalid IBAN format.")

    beneficiary_id = len(beneficiariesList) + 1

    beneficiary = Beneficiary(
        id=beneficiary_id,
        bank_account_id=bank_account_id,
        beneficiary_iban=beneficiary_iban,
        last_name=last_name,
        first_name=first_name,

    )

    beneficiariesList.append(beneficiary)
    return {"beneficiary": beneficiary}

@app.get("/")
def get_beneficiaries():
    return {"beneficiaries": beneficiariesList}
