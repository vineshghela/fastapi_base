
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app import models, schemas
from app.database import engine, SessionLocal
from app.dependencies import get_db
from app.security import create_access_token, get_current_active_user
from app.crud import crud_users
from app.utils import get_password_hash
import uuid

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud_users.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/users/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if email is already registered
    db_user = crud_users.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_user = models.User(
        username=user.username,
        email=user.email,
        password=user.password,
        is_active=True
    )
    print("cjkskfjsjkfkcsjkdskjffjksjk",db_user)
    return crud_users.create_user(db=db, user=db_user)


@app.get("/users/me/", response_model=schemas.User)
async def read_users_me(current_user: schemas.User = Depends(get_current_active_user)):
    return current_user

@app.post("/questions/", response_model=schemas.Question)
async def create_questions(
    question: schemas.QuestionCreate, 
    db: Session = Depends(get_db), 
    current_user: schemas.User = Depends(get_current_active_user)
):
    db_question = models.Questions(id=uuid.uuid4(), question_text=question.question_text)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    for choice in question.choices:
        db_choice = models.Choices(
            id=uuid.uuid4(),
            choice_text=choice.choice_text, 
            is_correct=choice.is_correct, 
            question_id=db_question.id
        )
        db.add(db_choice)
        db.commit()
    return {"message": f"Question created successfully by {current_user.username}"}