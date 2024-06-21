# from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
# from sqlalchemy.orm import relationship
# from app.database import Base
# from sqlalchemy.dialects.postgresql import UUID
# import uuid


# class User(Base):
#     __tablename__ = 'users'
#     id =  Column(UUID(as_uuid=True), primary_key=True, index=True)
#     username = Column(String, unique=True, index=True)
#     email = Column(String, unique=True, index=True)
#     hashed_password = Column(String)
#     is_active = Column(Boolean, default=True)

# class Questions(Base):
#     __tablename__ = 'questions'
#     id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
#     question_text = Column(String, index=True)

# class Choices(Base):
#     __tablename__ = 'choices'
#     id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
#     choice_text = Column(String, index=True)
#     is_correct = Column(Boolean, default=False)
#     question_id = Column(UUID(as_uuid=True), ForeignKey("questions.id"))


# app/models.py
from sqlalchemy import Boolean, Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid

Base = declarative_base()

class Questions(Base):
    __tablename__ = 'questions'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    question_text = Column(String, index=True)

class Choices(Base):
    __tablename__ = 'choices'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    choice_text = Column(String, index=True)
    is_correct = Column(Boolean, default=False)
    question_id = Column(UUID(as_uuid=True), ForeignKey("questions.id"))

class User(Base):
    __tablename__ = 'users'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True, nullable=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)
