from fastapi import FastAPI, HTTPException, Depends, status, Header
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from fastapi.background import BackgroundTasks

from bson import json_util
import json

from datetime import datetime, timedelta

from schemas import *
from database import usersDB, dashboardDB
import uvicorn
from authorization import *
from background import saveDailyStatistics
from apscheduler.schedulers.background import BackgroundScheduler


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
scheduler = BackgroundScheduler()
scheduler.add_job(saveDailyStatistics, 'cron', hour=16, minute=31)  
scheduler.start()


@app.post("/register")
async def register_user(input: SignUpModel):
    if input.password != input.repeatedPassword:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords do not match"
        )
    user_exists = usersDB.find_one({"email": input.email})
    if user_exists != None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    hashed_password = hash_password(input.password)

    new_user = {
        "username": input.username,
        "email": input.email,
        "password": hashed_password,
        "proUser": input.proUser,
        "registeredAt": datetime.utcnow()
    }
    usersDB.insert_one(new_user)
    return {"status_code": status.HTTP_200_OK,
            "detail": "User registered successfully"}


@app.post("/login")
async def loginForAccessToken(input: LoginModel):
    user = authenticateUser(input.email, input.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = createAccessToken(data={"sub": user["email"]}, expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}


@app.get('/showStatistic', dependencies=[Depends(adminRequired)])
def adminStatistic():
    totalUsers = usersDB.count_documents({})
    proUsers = usersDB.count_documents({"proUser": True})
    revenue = proUsers*60000
    return {"totalUsers": str(totalUsers), "proUsers": str(proUsers), "revenue": str(revenue)}


@app.put('/updateToPro', dependencies=[Depends(adminRequired)])
def updateToPro(input: configEmail):
    user = usersDB.find_one({"email": input.email})
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    if user.get("proUser") is True:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is already a pro user"
        )
    
    usersDB.update_one({"email": input.email}, {"$set": {"proUser": True}})
    return {
        "status_code": status.HTTP_200_OK, 
        "detail": "User updated to pro successfully"
        }


@app.get('/getAllUsers', dependencies=[Depends(adminRequired)])
def getAllUserEmails():
    user_data = usersDB.find({}, {"_id": 0, "email": 1, "proUser": 1})
    users_list = [{"email": user['email'], "proUser": user['proUser']} for user in user_data]
    return {"status_code": status.HTTP_200_OK, "emails": users_list}


@app.get("/getDashboard", dependencies=[Depends(adminRequired)])
async def getDailyAmountOfUsers():
    cursor = dashboardDB.find({})
    dailyStatistics = []
    for document in cursor:
        date_str = document["date"].strftime("%m-%d")
        dailyStatistics.append({
            "date": date_str,
            "totalUsers": document["totalUsers"],
            "proUsers": document["totalProUsers"]
        })
    return  {"status_code": status.HTTP_200_OK, "data": dailyStatistics}

if __name__ == "__main__":
    uvicorn.run("main:app",host='127.0.0.1', port = 8000, reload = True)