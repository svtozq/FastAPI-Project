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





# Création automatique des tables dans la base SQLite
models.Base.metadata.create_all(bind=engine)
app = FastAPI()
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














