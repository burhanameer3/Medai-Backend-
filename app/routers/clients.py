from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from .users import get_current_user
from ..db.base import get_db
from app.db import crud
from app import schemas, models
from ..core import security
from typing import List
  
router = APIRouter(prefix="/", tags=["Clients"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token")



@router.post("/client/add",response_model=schemas.ClientOut)
def add_client(client:schemas.ClientCreate,db:Session=Depends(get_db),current_user:models.User=Depends(get_current_user)):
    existing_client=db.query(models.Client).filter(models.Client.email==client.email).first()
    if existing_client:
        raise HTTPException(status_code=400,detail="Client with email already exists")
    created_client=crud.create_client(db=db,client=client,user_id=current_user.id)
    return created_client




@router.get("/clients",response_model=List[schemas.ClientOut])
def show_clients(db:Session=Depends(get_db),current_user:models.User=Depends(get_current_user)):
    pass