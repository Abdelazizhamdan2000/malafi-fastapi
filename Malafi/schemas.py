from datetime import datetime
from pydantic import BaseModel
from typing import List

class DocumentBase(BaseModel):
    title: str
    national_id: str
    expiry_date: datetime


class Document(BaseModel):
    title: str
    national_id: str
    expiry_date: datetime
    class Confing:
        orm_mode = True


class UserResponse(BaseModel):
    name: str
    email: str
    phone_number: str
    national_id: str
    documents: List[Document]
    class Config:
        orm_mode = True


class DocumentResponse(BaseModel):
    title: str
    national_id: str
    expiry_date: datetime
    class Config:
        orm_mode = True


class User(BaseModel):
    name: str
    email: str
    phone_number: str
    password: str
    national_id: str
    id_number: str


class Login(BaseModel):
    email: str
    password: str
