from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from core.my_database import get_db, Base, engine
from core.crud import create, read, update, delete
from core.schemas import HabitResponse, CreateHabit
import rust_analytics

Base.metadata.create_all(bind=engine)
app = FastAPI()

def format_habit_response(habit) -> HabitResponse:
    """Хелпер для безпечного розрахунку стріків через Rust та мапінгу у схему"""
    if habit.complete:
        date_list = [str(habit.complete)]
        current_strike, max_strike = rust_analytics.strikes(date_list)
    else:
        current_strike, max_strike = 0, 0
        
    return HabitResponse(
        id=habit.id,
        title=habit.title,
        create_at=str(getattr(habit, "create_at", "")), 
        complete=str(habit.complete) if habit.complete else "",
        current_strike=current_strike,
        max_strike=max_strike
    )

@app.post("/habits", response_model=HabitResponse, status_code=201)
def create_new_habit(habit: CreateHabit, db: Session = Depends(get_db)):
    db_habit = create(db=db, habit_data=habit)
    return format_habit_response(db_habit)
    
@app.get("/habits", response_model=list[HabitResponse])
def return_habits(db: Session = Depends(get_db)):
    habits = read(db=db)
    return [format_habit_response(h) for h in habits]

@app.patch('/habits/{habit_id}', response_model=HabitResponse)
def update_or_execute_habit(habit_id: int, db: Session = Depends(get_db)):
    updated_habit = update(db=db, habit_id=habit_id)
    if updated_habit is None: 
        raise HTTPException(status_code=404, detail="ERROR 404: Habit not found")
    return format_habit_response(updated_habit)
        
@app.delete('/habits/{habit_id}', status_code=204)
def delete_habit(habit_id: int, db: Session = Depends(get_db)):
    success = delete(db=db, habit_id=habit_id)
    if not success: 
        raise HTTPException(status_code=404, detail="ERROR 404: Habit not found")
