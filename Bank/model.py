"""from pydantic import BaseModel, Field


class User(BaseModel):
    id: int
    name: str
    email: str
    iban: str


class BankAccount(BaseModel):
    account_id: int
    user_id: int
    balance: float = Field(default=0, description="Solde du compte")
    clotured: bool = Field(default=False, description="Compte actif ou clôturé")"""
