from sqlalchemy.orm import Session
from sqlalchemy import  func
from datetime import datetime
from geopy.distance import geodesic 
import models, schemas,api
from models import User
from fastapi import HTTPException
from typing import List
import uuid
from schemas import TestUser
#Ge
# def fetch_user(db:Session, user_id: int):
#     return db.query(models.User).filter(models.User.uid == user_id).first()

def fetch_user_by_email(db:Session, email_id:str):
    return db.query(models.User).filter(models.User.email == email_id).first()


def fetch_and_store_users(db: Session, number_of_users: int) -> List[User]:
    run_id = str(uuid.uuid4())
    try:
        users_data = api.get_random_users(number_of_users)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error fetching users from external API")

    users = []

    for i in range(number_of_users):
        user_data = users_data[i]

        existing_user = db.query(User).filter_by(email=user_data['email']).first()
        if existing_user:
            continue

        user = User(
            email=user_data['email'],
            first_name=user_data['name']['first'],
            last_name=user_data['name']['last'],
            gender=user_data['gender'],
            latitude=float(user_data['location']['coordinates']['latitude']),
            longitude=float(user_data['location']['coordinates']['longitude']),
            uid = user_data["login"]["uuid"],
            run_id=run_id,
            run_iteration=i + 1,
            created_at=datetime.utcnow()
        )
        users.append(user)
        db.add(user)

    db.commit()
    
    return users

   

def get_random_user(db: Session):
    return db.query(models.User).order_by(func.random()).first()


#Create
# def create_user(db:Session,user: schemas.UserCreate):
#     max_run_id = db.query(func.max(models.User.run_id)).scalar() or 0

#     new_run_id = max_run_id + 1
    
#     new_user= models.User(
#     email = user.email,
#     first_name = user.first_name,
#     last_name = user.last_name,
#     gender = user.gender,
#     latitude = user.latitude,
#     longitude = user.longitude,
#     run_id = new_run_id,
#     datetime = datetime.utcnow())
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return new_user

    
def get_nearest_users(db:Session,email:str,limit: int = 100):
    user = fetch_user_by_email(db, email)
    if not user:
        return None
    all_users = db.query(models.User).filter(models.User.email != email).all()
    
    user_location = (user.latitude, user.longitude)
    distances = []
    for u in all_users:
        distance = geodesic(user_location, (u.latitude,u.longitude)).km
        distances.append((u, distance))
        
    sorted_users = sorted(distances, key =lambda x:x[1])
    return [user for user,distance in sorted_users[:limit]]

