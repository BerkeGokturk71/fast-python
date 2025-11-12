from sqlalchemy.orm import Session
from backend.models.users import RefreshToken


def db_refresh_token(db:Session, refresh_token:str, user_uuid:str, device_name=None):
    db_refresh_token = RefreshToken(user_id=user_uuid,refresh_token=refresh_token,device_name=device_name)
    db.add(db_refresh_token)
    db.commit()
    db.refresh(db_refresh_token)

def get_refresh_token(db:Session,user_uuid:str):
    db_query = db.query(RefreshToken).filter(RefreshToken.user_id==user_uuid).first()
    return db_query

