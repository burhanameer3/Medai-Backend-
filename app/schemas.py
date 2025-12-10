from typing import Annotated
from pydantic import BaseModel, StringConstraints

UsernameStr = Annotated[str, StringConstraints(
    min_length=3,
    max_length=50,
    pattern=r"^[A-Za-z0-9_.-]+$"
)]

EmailStr = Annotated[str, StringConstraints(
    min_length=5,
    max_length=100,
    pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
)]

PasswordStr = Annotated[str, StringConstraints(min_length=8, max_length=72)]

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

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "bearer"

class RefreshToken(BaseModel):
    refresh_token: str