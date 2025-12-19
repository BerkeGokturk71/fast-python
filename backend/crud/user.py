from sqlalchemy.orm import Session
from backend.models.users import Users
from backend.app.core.security import hash_password


def create_user(db:Session,username:str,mail:str,password:str):
    db_user = Users(username=username,mail=mail,hashed_password=hash_password(password=password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db:Session,user_id:str):
    return db.query(Users).filter(Users.id == user_id).first()

def get_user_uuid(db:Session,username:str):
    return db.query(Users).filter(Users.username==username).first()