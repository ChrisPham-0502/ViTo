from passlib.context import CryptContext
from jose import JWTError, jwt, ExpiredSignatureError
from datetime import datetime, timedelta
from database import usersDB
from typing import Optional
from fastapi.security import HTTPBearer
from fastapi import HTTPException, status, Depends
from security import Config

SECRET_KEY = Config.SECRET_KEY
ALGORITHM = Config.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = Config.ACCESS_TOKEN_EXPIRE_MINUTES

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

reusable_oauth2 = HTTPBearer(scheme_name='Authorization')
def validate_token(http_authorization_credentials=Depends(reusable_oauth2)) -> str:
    try:
        token = http_authorization_credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        token_data = payload
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token_data

def adminRequired(token_data: dict = Depends(validate_token)):
    email = token_data.get("sub")
    user = usersDB.find_one({"email": email})
    if user["email"] != "vito@gmail.com":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this resource",
        )
    return user
