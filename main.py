import datetime
import random
import re
from passlib.hash import pbkdf2_sha256
from pydantic import BaseModel
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from DB.database import engine, get_db
from DB import models
#Pour importer depuis ma methode transaction
from Transactions.transactionDB import router as transactions_router
from Transactions.add_money import router as add_money_router
from Users.signIn import router as login_router
from Bank.BankAccount import router as Bank_router
from Beneficiaries.beneficiary import router as Beneficiaries_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI





# Création automatique des tables dans la base SQLite
models.Base.metadata.create_all(bind=engine)
app = FastAPI()

# middleware CORS pour autorisé l'échange entre le back et le front
origins = [
    "http://localhost:5173",  # URL de ton front
    "http://127.0.0.1:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        # quelles origines sont autorisées
    allow_credentials=True,
    allow_methods=["*"],          # autorise GET, POST, etc.
    allow_headers=["*"]           # autorise tous les headers
)


# Ouali lie mon code au main via router
app.include_router(transactions_router)
#route pour add_user
app.include_router(add_money_router)
#Route pour le login
app.include_router(login_router)
#Route pour le bank account
app.include_router(Bank_router)
#Route pour les benefiary
app.include_router(Beneficiaries_router)














