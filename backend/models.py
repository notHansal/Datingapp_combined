from sqlalchemy import Column, Integer, String, Float, func,DateTime
from datetime import datetime
from database import Base
from sqlalchemy_utils import PasswordType



class User(Base):
    __tablename__ = 'users'

    uid = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    gender = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    run_id =Column(String,index=True)
    run_iteration = Column(Integer)
    