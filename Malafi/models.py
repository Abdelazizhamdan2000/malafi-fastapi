from .database import Base
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

class Document(Base):
    __tablename__ = 'documents'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    expiry_date = Column(DateTime, index = True, nullable=False)
    national_id = Column(String, nullable = False)
    owner = relationship("User", back_populates="documents")
    user_id = Column(Integer, ForeignKey('users.id'))

class Citizen(Base):
    __tablename__ = "citizens"
    citizen_id = Column(String, primary_key=True, index=True)
    id_number = Column(String, nullable=False, unique=True)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    national_id = Column(String, nullable = False, unique=True)
    id_number = Column(String, nullable=False, unique=True)
    email = Column(String, nullable = False, unique=True)
    password = Column(String, nullable = False)
    phone_number = Column(String, nullable = False)
    documents = relationship("Document", back_populates="owner")