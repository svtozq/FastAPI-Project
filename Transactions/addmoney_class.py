from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Bank API in RAM")

# Simulation d'une "base de données" en mémoire
dico_accounts = {
    "alice": 1000,
    "bob": 500,
    "charlie": 250
}

class add_money(BaseModel):
    username: str
    amount: int

"""ajouter de l'argent au compte de l'utilisateur"""

@app.post("/accounts/add_money/")
def add_money(data: add_money):
    username = data.username.lower()
    amount = data.amount

    if username not in dico_accounts:
        raise HTTPException(status_code=404, detail="User not found")

    if amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")

    dico_accounts[username] += amount
    new_balance = dico_accounts[username]

    return {
        "message": f"{amount}€ added successfully to {username}'s account.",
        "new_balance": new_balance
    }


"""voir le solde du compte"""

@app.get("/accounts/{username}")
def get_balance(username: str):
    username = username.lower()
    if username not in dico_accounts:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "username": username,
        "balance": dico_accounts[username]
    }
