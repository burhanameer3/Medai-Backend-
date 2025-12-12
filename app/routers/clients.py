from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from .users import get_current_user
from ..db.base import get_db
from app.db import crud
from app import schemas, models
from ..core import security
from typing import List
from datetime import datetime
import cloudinary.uploader
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
        raise HTTPException(status_code=403,detail="Not authorized to view this client")
    return client


# update a client
@router.put("/client/{client_id}", response_model=schemas.ClientOut)
async def update_client_endpoint(
    client_id: int,
    name: str = Form(...),
    date_of_birth: str = Form(...),
    case_status: bool = Form(...),
    insurance_provider: str = Form(None),
    active_cases: int = Form(None),
    gender: str = Form(...),
    insurance_coverage_policy: int = Form(None),
    id_number: str = Form(...),
    primary_contact_number: str = Form(...),
    secondary_contact_number: str = Form(None),
    key_contact_name: str = Form(None),
    contact_person_phone: str = Form(None),
    home_address: str = Form(...),
    email: str = Form(...),
    profile_image: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
   
    db_client = crud.get_client(db, client_id)
    if not db_client:
        raise HTTPException(status_code=404, detail="Client not found")
    if db_client.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    profile_url = None
    # Upload profile image if provided
    if profile_image and profile_image.filename:
        try:
            upload_result = cloudinary.uploader.upload(
                profile_image.file,
                folder="hospital/clients/profile"
            )
            profile_url = upload_result.get("secure_url")
            print(f"Image uploaded successfully: {profile_url}")
        except Exception as e:
            print(f"Cloudinary upload error: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to upload image: {str(e)}")

    # Convert date_of_birth string to datetime object
    try:
        date_obj = datetime.fromisoformat(date_of_birth.replace('Z', '+00:00'))
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use ISO format (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)")

    # Prepare update data
    update_data = {
        "name": name,
        "date_of_birth": date_obj,
        "case_status": case_status,
        "insurance_provider": insurance_provider,
        "active_cases": active_cases,
        "gender": gender,
        "insurance_coverage_policy": insurance_coverage_policy,
        "id_number": id_number,
        "primary_contact_number": primary_contact_number,
        "secondary_contact_number": secondary_contact_number,
        "key_contact_name": key_contact_name,
        "contact_person_phone": contact_person_phone,
        "home_address": home_address,
        "email": email
    }

    updated_client = crud.update_client(
        db=db,
        db_client=db_client,
        new_data=update_data,
        profile_image_url=profile_url
    )
    return updated_client



@router.delete("/client/{client_id}")
def delete_client(client_id:int,current_user:models.User=Depends(get_current_user),db:Session=Depends(get_db)):
    res=crud.delete_client(db,client_id,current_user.id)
    if not res:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found"
        )
    return {"message": "Client deleted successfully"}
