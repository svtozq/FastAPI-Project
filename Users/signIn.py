import datetime
import hashlib
import re
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

usersList = []
usersIdList = []
mailsList = []
passwordsList = []

class UserAccount(BaseModel):
    id : int
    last_name : str
    first_name : str
    email : str
    password : str
    date : datetime.datetime

@app.post("/signin/")
def signin(last_name, first_name, email, password):
    user_id = 1
    if user_id in usersIdList:
        user_id += 1

    if email in mailsList:
        raise HTTPException(status_code=400, detail="sorry this mail address is already registered !")

    if not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email):
        raise HTTPException(status_code=400, detail="try again.. your mail address isn't valid !")

    if not re.fullmatch(r"[A-Za-z0-9@#$%^&+=]{8,}", password):
        raise HTTPException(status_code=400, detail="try again.. your password should be at least 8 characters long !")
    else:
        hashedPassword = hashlib.sha256(password.encode()).hexdigest()

    now = datetime.datetime.now()
    user = UserAccount(id=user_id, last_name=last_name, first_name=first_name, email=email, password=hashedPassword, date=now)
    usersList.append(user)
    usersIdList.append(user.id)
    mailsList.append(user.email)
    passwordsList.append(hashedPassword)
    return {"user": user}

@app.post("/login/")
def login(email, password):
    if not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email):
        raise HTTPException(status_code=400, detail="try again.. your mail address isn't valid !")

    if not email in mailsList:
        raise HTTPException(status_code=400, detail="sorry this mail address isn't registered !")

    hashedPassword = hashlib.sha256(password.encode()).hexdigest()
    if not hashedPassword in passwordsList:
        raise HTTPException(status_code=400, detail="try again.. your password isn't valid !")

    return {"you successfully logged in"}

@app.get("/users/mails/")
def get_mails():
    if mailsList:
        return {"mails": mailsList}
    else:
        raise HTTPException(status_code=404, detail="sorry there's no mail address registered !")

@app.get("/users/")
def get_users():
    if usersList:
        return {"users": usersList}
    else:
        raise HTTPException(status_code=404, detail="sorry there's no user registered !")