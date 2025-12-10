from typing import Annotated, Optional
from pydantic import BaseModel, constr, EmailStr

UsernameStr = constr(min_length=3, max_length=50, pattern=r"^[A-Za-z0-9_.-]+$")
PasswordStr = constr(min_length=8, max_length=72)

class UserCreate(BaseModel):
    username: UsernameStr
    email: EmailStr
    password: PasswordStr

class UserLogin(BaseModel):
    email: EmailStr
    password: PasswordStr

class UserOut(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool

    model_config = {"from_attributes": True}

class Token(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "bearer"

class RefreshToken(BaseModel):
    refresh_token: str