import datetime
from passlib.hash import pbkdf2_sha256
import re
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

usersList = []
usersIdList = []

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
    for user in usersList:
        if user.email == email:
            raise HTTPException(status_code=400, detail="sorry this mail address is already registered !")

    if not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email):
        raise HTTPException(status_code=400, detail="try again.. your mail address isn't valid !")

    if not re.fullmatch(r"[A-Za-z0-9@#$%^&+=]{8,}", password):
        raise HTTPException(status_code=400, detail="try again.. your password should be at least 8 characters long !")
    else:
        hashedPassword = pbkdf2_sha256.hash(password)

    now = datetime.datetime.now()
    user = UserAccount(id=user_id, last_name=last_name, first_name=first_name, email=email, password=hashedPassword, date=now)
    usersList.append(user)
    return {"user": user}

@app.post("/login/")
def login(email, password):
    if not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email):
        raise HTTPException(status_code=400, detail="try again.. your mail address isn't valid !")

    if len(usersList) > 0:
        for user in usersList:
            if user.email == email:
                if not pbkdf2_sha256.verify(password, user.password):
                    raise HTTPException(status_code=400, detail="try again.. your password is wrong !")
            else:
                raise HTTPException(status_code=400, detail="sorry this mail address isn't registered !")
    else: return {"sorry this mail address isn't registered !"}

    return {"you successfully logged in"}

@app.get("/users/")
def get_users():
    if usersList:
        return {"users": usersList}
    else:
        raise HTTPException(status_code=404, detail="sorry there's no user registered !")