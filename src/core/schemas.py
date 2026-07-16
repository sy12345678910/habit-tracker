from datetime import datetime
from pydantic import BaseModel, Field, field_validator


class CreateHabit(BaseModel):
    title: str = Field(min_length=1, max_length=100, examples=["play chess"])
    complete: str = Field(examples=["2026-08-24"])

    @field_validator("complete")
    def is_datetime(cls, v: str) -> bool:
        try:
            datetime.strptime(v, "%Y-%m-%d")
            return v
        except ValueError:
            raise ValueError("incorrect date format, should be YYYY-MM-DD")
    
class HabitResponse(BaseModel):
    id: int
    title: str
    create_at: str
    complete: str
    max_strike: int
    current_strike: int
    
    class Config:
        from_attributes = True