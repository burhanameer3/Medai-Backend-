from sqlalchemy import Column, DateTime, Integer, String, Boolean,Enum,ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .db.base import Base
import enum


class GenderEnum(str, enum.Enum):
    male = "male"
    female = "female"
    other = "other"


class RoleEnum(str,enum.Enum):
    admin="admin"
    superadmin="superadmin"
    staff="staff"
    editor="editor"
    viewer="viewer"


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=False, index=True, nullable=False)
    email=Column(String,unique=True,index=True,nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
    role=Column(Enum(RoleEnum,default=RoleEnum.admin))
    clients = relationship("Client", back_populates="user")

class Client(Base):
    __tablename__="clients"
    client_id=Column(Integer,primary_key=True,index=True)
    name=Column(String,nullable=False,index=True)
    date_of_birth = Column(DateTime, nullable=False)
    case_status=Column(Boolean,nullable=False)
    insurance_provider = Column(String, nullable=True)  # fixed spelling
    active_cases=Column(Integer)
    gender=Column(Enum(GenderEnum),nullable=False)
    insurance_coverage_policy = Column(Integer, nullable=False)
    id_number=Column(String,nullable=False)
    primary_contact_number=Column(String(20))
    secondary_contact_number=Column(String(20))
    key_contact_name=Column(String) 
    contact_person_phone=Column(String(20))
    home_address=Column(String(300))
    email=Column(String,unique=False,index=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    # Relationship back to User
    user = relationship("User", back_populates="clients")
