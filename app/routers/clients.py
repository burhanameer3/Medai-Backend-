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
  
router = APIRouter(prefix="", tags=["Clients"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token")


# adding clients
@router.post("/client/add",response_model=schemas.ClientOut)
def add_client(client:schemas.ClientCreate,db:Session=Depends(get_db),current_user:models.User=Depends(get_current_user)):
    existing_client=db.query(models.Client).filter(models.Client.email==client.email).first()
    if existing_client:
        raise HTTPException(status_code=400,detail="Client with email already exists")
    created_client=crud.create_client(db=db,client=client,user_id=current_user.id)
    return created_client
# getting all clients
@router.get("/clients",response_model=List[schemas.ClientOut])
def show_clients(db:Session=Depends(get_db),current_user:models.User=Depends(get_current_user)):
    client_data=crud.get_clients(db,current_user.id)
    return client_data
# get a single client 
@router.get("/client/{client_id}",response_model=schemas.ClientOut)
def get_client(client_id:int,db:Session=Depends(get_db),current_user:models.User=Depends(get_current_user)):
    client=crud.get_client(db,client_id)
    if not client:
        raise HTTPException(status_code=404 ,detail="client not found")
    if client.user_id!=current_user.id:
        raise HTTPException(status_code=403,detail="Not aithorized to view this client")
    return client


# update a client 
@router.put("/client/{client_id}",response_model=schemas.ClientOut)
def update_client(client_info:schemas.ClientUpdate,client_id:int,db:Session=Depends(get_db),current_user:models.User=Depends(get_current_user)):
    db_client = crud.get_client(db, client_id)
    if not db_client:
        raise HTTPException(status_code=404, detail="Client not found or not yours")
    if db_client.user_id != current_user.id:
       raise HTTPException(status_code=403, detail="Not authorized")

    updated = crud.update_client(db, db_client, client_info)
    return updated



@router.delete("/client/{client_id}")
def delete_client(client_id:int,current_user:models.User=Depends(get_current_user),db:Session=Depends(get_db)):
    res=crud.delete_client(db,client_id,current_user.id)
    if not res:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found"
        )
    return 