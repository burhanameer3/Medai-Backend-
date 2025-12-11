from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app import models
from app import schemas

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, username: str, email: str, hashed_password: str):
    user = models.User(username=username, email=email, hashed_password=hashed_password)
    db.add(user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        return None
    db.refresh(user)
    return user





# clients functionality 
def create_client(db:Session,client:schemas.ClientCreate,user_id:int):    
    db_client=models.Client(
        name=client.name,
        date_of_birth=client.date_of_birth,
        case_status=client.case_status,
        insurance_provider=client.insurance_provider,
        active_cases=client.active_cases,
        gender=client.gender,
        insurance_coverage_policy=client.insurance_coverage_policy,
        id_number=client.id_number,
        primary_contact_number=client.primary_contact_number,
        secondary_contact_number=client.secondary_contact_number,
        key_contact_name=client.key_contact_name,
        contact_person_phone=client.contact_person_phone,
        home_address=client.home_address,
        email=client.home_address,
        user_id=user_id

    )
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client
def get_clients(db:Session,user_id:int):
    pass