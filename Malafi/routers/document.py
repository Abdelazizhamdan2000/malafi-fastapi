from fastapi import APIRouter, Depends, status, HTTPException
from .. import schemas, models
from ..database import get_db
from typing import List
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

router = APIRouter(
    prefix="/document",
    tags=['documents']
)

@router.get('/{national_id}', response_model=List[schemas.DocumentResponse])
def all(national_id, db: Session = Depends(get_db)):
    documents = db.query(models.Document).filter(models.Document.national_id == national_id).all()
    if not documents:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No documents for the user with a national ID {national_id}')

    return documents


@router.get('/{national_id}/expired', response_model=List[schemas.DocumentResponse])
def expired(national_id, db: Session = Depends(get_db)):
    documents = db.query(models.Document).filter(models.Document.national_id == national_id, models.Document.expiry_date < datetime.now()).all()
    if not documents:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No expired documents for the user with a national ID {national_id}')

    return documents


@router.get('/{national_id}/upcoming/{period}', response_model=List[schemas.DocumentResponse])
def upcoming(national_id, period: int, db: Session = Depends(get_db)):
    end_date = datetime.now() + timedelta(days=period)
    documents = db.query(models.Document).filter(models.Document.national_id == national_id, models.Document.expiry_date <= end_date, models.Document.expiry_date >= datetime.now()).all()
    if not documents:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No upcoming documents for the user with a national ID {national_id} in {period} days')
    
    return documents
