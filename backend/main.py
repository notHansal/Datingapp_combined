from typing import List
from fastapi import FastAPI, HTTPException,Depends
from sqlalchemy.orm import Session
import crud, database, schemas, api
from datetime import datetime
from models import User 
from database import engine, Base, Sessionlocal,get_db


def init_db():
    Base.metadata.create_all(bind=engine)

init_db()

app = FastAPI()



@app.get("/")
def read_root():
    return {"message": "Hello, World!"}



@app.post("/fetch-users/", response_model=List[schemas.User]
          )
async def fetch_users(num_users:int,db: Session = Depends(get_db)):
    users =  crud.fetch_and_store_users(db,num_users)
    return users



#@app.post("/users/", response_model=schemas.User)
#def create_user_endpoint(user: schemas.UserCreate, db: Session = Depends(get_db)):
    #return crud.create_user(db=db, user=user)
    
@app.get("/random_user/", response_model=schemas.User)
async def random_users(db: Session = Depends(get_db)):
    
    user = crud.get_random_user(db)
    
    if not user:
        raise HTTPException(status_code=404, detail="No users")
    return user


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.get("/users/email/{email}", response_model=schemas.User)
def read_user_by_email(email: str, db: Session = Depends(get_db)):
    db_user = crud.fetch_user_by_email(db, email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.get("/users/{email}/nearest", response_model=List[schemas.User])
def read_nearest_users(email: str, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_nearest_users(db, email, limit=limit)
    if users is None or len(users) == 0:
        raise HTTPException(status_code=404, detail="No nearby users found")
    return users



