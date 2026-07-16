from datetime import date
from sqlalchemy import Column, Integer, String
from core.my_database import Base

class Habit(Base):
    __tablename__ = "habits"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    create_at = Column(String, default=lambda: date.today().strftime("%Y-%m-%d"))
    complete = Column(String)
    max_strike = Column(Integer)
    current_strike = Column(Integer)
        
    
    
    def build_struct(self):    
        struct = {
            "id": self.id,
            "title": self.title,
            "create_at": self.create_at,
            "complete": self.complete,
        }
        
        return struct