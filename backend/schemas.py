from pydantic import BaseModel
from typing import Union
from sqlalchemy import DateTime
from datetime import datetime


class UserBase(BaseModel):
    email: str
    
class UserCreate(UserBase):
    gender: str
    first_name: str
    last_name: str
    latitude: float
    longitude: float
    
class User(UserCreate):
    uid: str
    run_id: str
    created_at: datetime
    run_iteration: int
    
    class Config:
        orm_mode = True
        # from_attributes = True
        
class TestUser(UserCreate):
    uid: str
    run_id: str
    created_at: datetime
    run_iteration: int
    
    class Config:
        orm_mode = True
        # from_attributes = True