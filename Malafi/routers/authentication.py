from fastapi import APIRouter, Depends, status, HTTPException
from .. import schemas, database, models
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from sqlalchemy import or_


router = APIRouter(
    tags=['authentication']
)


pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post('/login')
def login(msg: schemas.Login, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == msg.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invalid Credentials')
    
    if not pwd_ctx.verify(msg.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invalid Credentials')

    return user

@router.post('/signup', response_model=schemas.UserResponse)
def sign_up(msg: schemas.User, db: Session = Depends(database.get_db)):
    citizen = db.query(models.Citizen).filter(models.Citizen.citizen_id == msg.national_id, models.Citizen.id_number == msg.id_number).first()
    user = db.query(models.User).filter(or_(models.User.id_number == msg.id_number, models.User.email == msg.email, models.User.phone_number == msg.phone_number)).first()
    if (not citizen) or user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invalid Data for the user')
    
    breakpoint()
    hashed_pwd = pwd_ctx.hash(msg.password)
    new_user = models.User(name=msg.name, email=msg.email, password=hashed_pwd, national_id=msg.national_id, id_number=msg.id_number, phone_number=msg.phone_number)
    db.add(new_user)
    db.commit()
    db.query(models.Document).filter(models.Document.national_id == new_user.national_id).update({'user_id': new_user.id})
    db.commit()
    db.refresh(new_user)

    documents = []
    for document in new_user.documents:
        documents.append({
            'title': document.title,
            'national_id': document.national_id,
            'expiry_date': document.expiry_date
        })
    
    response = {
        'name': new_user.name,
        'email': new_user.email,
        'national_id': new_user.national_id,
        'phone_number': new_user.phone_number,
        'documents': documents
    }

    return response