import enum
from typing import Annotated, Optional
from pydantic import BaseModel, constr, EmailStr, StringConstraints
from datetime import datetime
UsernameStr = Annotated[str, StringConstraints(min_length=3, max_length=50, pattern=r"^[A-Za-z0-9_.\-\s]+$")]
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

    model_config = {"from_attributes": True}

class Token(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "bearer"

class RefreshToken(BaseModel):
    refresh_token: str




# enum datatype for gender
class GenderEnum(str, enum.Enum):
    male = "male"
    female = "female"
    other = "other"


class ClientBase(BaseModel):
    name: str
    date_of_birth: datetime
    case_status: bool
    insurance_provider: str | None = None
    active_cases: int | None = None
    gender: GenderEnum
    insurance_coverage_policy: int
    id_number: str
    primary_contact_number: str | None = None
    secondary_contact_number: str | None = None
    key_contact_name: str | None = None
    contact_person_phone: str | None = None
    home_address: str | None = None
    email: str | None = None


class ClientCreate(ClientBase):
    pass


class ClientOut(ClientBase):
    client_id: int
    user_id: int
    # created_at: datetime

    class Config:
        orm_mode = True



class ClientUpdate(BaseModel):
    name: str
    date_of_birth: datetime
    case_status: bool
    insurance_provider: str | None
    active_cases: int
    gender: str
    insurance_coverage_policy: int | None
    id_number: str
    primary_contact_number: str
    secondary_contact_number: str | None
    key_contact_name: str | None
    contact_person_phone: str | None
    home_address: str
    email: str