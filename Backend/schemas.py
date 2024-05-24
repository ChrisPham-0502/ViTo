from pydantic import BaseModel, EmailStr

class SignUpModel(BaseModel):
    username: str
    email: EmailStr
    password: str
    repeatedPassword: str

class LoginModel(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str