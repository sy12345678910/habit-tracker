from datetime import date
from sqlalchemy.orm import Session
import core.models as models
import core.schemas as schemas

def create(db: Session, habit_data: schemas.CreateHabit):
    habit = models.Habit(complete=habit_data.complete, title=habit_data.title)
    db.add(habit)
    db.commit()
    db.refresh(habit)
    return habit

def read(db: Session):
    return db.query(models.Habit).all()

def update(db: Session, habit_id: int):
    habit = db.query(models.Habit).filter(models.Habit.id == habit_id).first()
    if habit:
        habit.complete = date.today().strftime("%Y-%m-%d")
        db.commit()
        db.refresh(habit)
        return habit
    return None

def delete(db: Session, habit_id: int) -> bool:
    habit = db.query(models.Habit).filter(models.Habit.id == habit_id).first()
    if habit:
        db.delete(habit)
        db.commit()
        return True
    return False
