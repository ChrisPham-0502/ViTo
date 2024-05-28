from pydantic import BaseModel, EmailStr, Field

class SignUpModel(BaseModel):
    username: str
    email: EmailStr
    password: str
    repeatedPassword: str
    proUser: bool = Field(default=False)

class LoginModel(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class VitoClothes(BaseModel):
    linkHumanImage: str
    linkClothesImag: str

class VitoSize(BaseModel):
    heigth: str
    