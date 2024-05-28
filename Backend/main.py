from fastapi import FastAPI, HTTPException, Depends, status, Header
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware

from datetime import datetime, timedelta

from schemas import SignUpModel, LoginModel, Token
from database import usersDB
import uvicorn
from authorization import *

# from ModelAI.AI import VitoClothes, VitoHair, VitoSize
app = FastAPI(swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"})
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
        "proUser": input.proUser
    }
    usersDB.insert_one(new_user)
    return {"status_code": status.HTTP_200_OK,
            "detail": "User registered successfully"}


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login/")
@app.post("/login", response_model=Token)
async def loginForAccessToken(input: LoginModel,authorization:str=Header(None)):
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

@app.get('/books', dependencies=[Depends(validate_token)])
def list_books():
    return {'data': ['Sherlock Homes', 'Harry Potter', 'Rich Dad Poor Dad']}

@app.get('/admin', dependencies=[Depends(adminRequired)])
def admin_dashboard():
    return {'data': 'Admin Dashboard'}


if __name__ == "__main__":
    uvicorn.run("main:app", reload = True)
