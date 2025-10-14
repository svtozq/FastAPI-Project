import datetime
import hashlib
import re
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class userAccount(BaseModel):
    id : int
    last_name : str
    first_name : str
    email : str
    password : str
    date : datetime.datetime

@app.post("/signin/")
def create_account(last_name, first_name, email, password):
    if not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email):
        raise HTTPException(status_code=400, detail="try again.. your mail address isn't valid !")

    if not re.fullmatch(r"[A-Za-z0-9@#$%^&+=]{8,}", password):
        raise HTTPException(status_code=400, detail="try again.. your password should be at least 8 characters long !")
    else:
        hashedPassword = hashlib.sha256(password.encode()).hexdigest()

    now = datetime.datetime.now()
    user = userAccount(id=1, last_name=last_name, first_name=first_name, email=email, password=hashedPassword, date=now)
    return {"user": user}
