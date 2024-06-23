from sqlalchemy.orm import Session
from app.models import User
from app.schemas import UserCreate  # Ensure this import is correct
from app.utils import get_password_hash, verify_password
import uuid

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate): 
    print(user)
    hashed_password = get_password_hash(user.password)  
    db_user = User(
        id=uuid.uuid4(),
        username=user.username,
        email=user.email,# Use hashed password
        password= hashed_password,
        is_active=True
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if user and verify_password(password, user.password):
        return user
    return None
