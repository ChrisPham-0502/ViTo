from fastapi import FastAPI, HTTPException, Depends, status, Header
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.security import HTTPBearer
from pydantic import ValidationError

from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta

from typing import Optional
from schemas import SignUpModel, LoginModel, Token
from database import usersDB
import uvicorn

# FastAPI app
app = FastAPI()

# Security
SECRET_KEY = "ye_@evo=SUSJ022xQK0BB!WCAIcw(c"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


pwdContext = CryptContext(schemes=["bcrypt"], deprecated="auto")
def hash_password(password: str):
    return pwdContext.hash(password)

def verify_password(plainPassword, hashedPassword):
    return pwdContext.verify(plainPassword, hashedPassword)

def authenticateUser(email: str, password: str):
    user = usersDB.find_one({"email": email})
    if user == None:
        return False
    if verify_password(password, user["password"]) == False:
        return False
    return user

def createAccessToken(data: dict, expires_delta: Optional[timedelta] = None):
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=expires_delta)
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

reusable_oauth2 = HTTPBearer(
    scheme_name='Authorization'
)
def validate_token(http_authorization_credentials=Depends(reusable_oauth2)) -> str:
    try:
        payload = jwt.decode(http_authorization_credentials.credentials, SECRET_KEY, ALGORITHM)
        if payload.get('email') < datetime.now():
            raise HTTPException(status_code=403, detail="Token expired")
        return payload.get('email')
    
    except:
        raise HTTPException(
            status_code=403,
            detail=f"Could not validate credentials",
        )
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login/")

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
        "password": hashed_password
    }
    usersDB.insert_one(new_user)
    return {"status_code": status.HTTP_200_OK,
            "detail": "User registered successfully"}

# Token endpoint
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


if __name__ == "__main__":
    uvicorn.run(app)
