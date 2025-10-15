from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from DB.database import SessionLocal, engine
from DB import models

# Création automatique des tables dans la base SQLite
models.Base.metadata.create_all(bind=engine)
app = FastAPI()

# Dépendance pour obtenir une session de BDD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ✅ Exemple 1 : créer un utilisateur
@app.post("/users/")
def create_user(first_name: str, last_name: str, email: str, password: str, db: Session = Depends(get_db)):
    user = models.UserAccount(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=password
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# ✅ Exemple 2 : afficher tous les utilisateurs
@app.get("/users/")
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.UserAccount).all()
    return users

class Item(BaseModel):
    name:str
    description:str
    price:float
    tax:float

@app.post("/items/")
def create_item(item : Item) -> Item:
    return item
