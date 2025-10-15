from pydantic import BaseModel, Field
from typing import Optional

class User(BaseModel):
    id: int
    name: str
    email: str
    iban : str

class BankAccount(BaseModel):
    account_id: int
    user_id: int
    balance: float = Field(default=0, description="Solde initial du compte")


















