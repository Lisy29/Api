from sqlalchemy.orm import Session
import models_db, schemas_db

def create_passenger_satisfaction(db: Session, passenger: schemas_db.Questions_passenger_satisfactionCreate, predicted_satisfaction: str | None = None):
    db_passenger = models_db.Questions_passenger_satisfaction(**passenger.dict(), predicted_satisfaction=predicted_satisfaction)
    db.add(db_passenger)
    db.commit()
    db.refresh(db_passenger)
    return db_passenger

def get_passenger_satisfaction(db: Session, passenger_id: int):
    return db.query(models_db.Questions_passenger_satisfaction).filter(models_db.Questions_passenger_satisfaction.id == passenger_id).first()

def get_all_passenger_satisfaction(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models_db.Questions_passenger_satisfaction).offset(skip).limit(limit).all()

def update_passenger_satisfaction(db: Session, passenger_id: int, predicted_satisfaction: str):
    db_passenger = db.query(models_db.Questions_passenger_satisfaction).filter(models_db.Questions_passenger_satisfaction.id == passenger_id).first()
    if db_passenger:
        db_passenger.predicted_satisfaction = predicted_satisfaction
        db.commit()
        db.refresh(db_passenger)
    return db_passenger

     


