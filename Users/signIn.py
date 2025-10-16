import datetime
import re
from passlib.hash import pbkdf2_sha256
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from DB.database import SessionLocal, engine
from DB import models

app = FastAPI()

class UserAccount(BaseModel):
    id : int
    last_name : str
    first_name : str
    email : str
    password : str
    date : datetime.datetime

models.Base.metadata.create_all(bind=engine)

# Get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/")
def create_user(last_name: str, first_name: str, email: str, password: str, db: Session = Depends(get_db)):
    count = db.query(models.UserAccount).filter(models.UserAccount.email == email).count()

    if count > 0:
        raise HTTPException(status_code=400, detail="Email already registered")

    if not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email):
        raise HTTPException(status_code=400, detail="try again.. your mail address isn't valid !")

    if not re.fullmatch(r"[A-Za-z0-9@#$%^&+=]{8,}", password):
        raise HTTPException(status_code=400, detail="try again.. your password should be at least 8 characters long !")
    else:
        hashedPassword = pbkdf2_sha256.hash(password)

    now = datetime.datetime.now()

    user = models.UserAccount(
        last_name=last_name,
        first_name=first_name,
        email=email,
        password=hashedPassword,
        date=now
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return {"user": user}


@app.post("/login/")
def login(email, password, db: Session = Depends(get_db)):
    if not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email, ):
        raise HTTPException(status_code=400, detail="try again.. your mail address isn't valid !")

    user = db.query(models.UserAccount).filter(models.UserAccount.email == email).first()

    if user is None:
        raise HTTPException(status_code=400, detail="sorry this mail address isn't registered !")
    else:
        if not pbkdf2_sha256.verify(password, user.password):
            raise HTTPException(status_code=400, detail="try again.. your password is wrong !")

    return {"you successfully logged in"}


@app.get("/users/")
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.UserAccount).all()

    if len(users) > 0:
        return {"users": users}
    else:
        return {"no users found"}