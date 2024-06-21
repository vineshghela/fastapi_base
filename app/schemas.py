# app/schemas.py
from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID

class ChoiceBase(BaseModel):
    choice_text: str
    is_correct: bool

class ChoiceCreate(ChoiceBase):
    pass

class QuestionBase(BaseModel):
    question_text: str
    choices: List[ChoiceBase]

class QuestionCreate(QuestionBase):
    pass

class Question(QuestionBase):
    id: UUID
    choices: List[ChoiceCreate]

    class Config:
        orm_mode = True

class Choice(ChoiceBase):
    id: UUID
    question_id: UUID

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    username: str
    email: Optional[str] = None

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: UUID
    is_active: bool

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None