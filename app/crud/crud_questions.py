from sqlalchemy.orm import Session
from app import models, schemas

def create_question(db: Session, question: schemas.QuestionCreate):
    db_question = models.Questions(question_text=question.question_text)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    for choice in question.choices:
        db_choice = models.Choices(choice_text=choice.choice_text, is_correct=choice.is_correct, question_id=db_question.id)
        db.add(db_choice)
    db.commit()
    db.refresh(db_question)
    return db_question
