import uuid
from sqlalchemy import Column,String,Integer,ForeignKey,DateTime
from sqlalchemy.orm import relationship
from backend.db.base import Base
from datetime import datetime
class Users(Base):
    __tablename__ = "users"
    id = Column(String,primary_key=True, default= lambda:str(uuid.uuid4()))
    username = Column(String,primary_key=True,nullable=False)
    hashed_password = Column(String,nullable=False)

    tokens = relationship("RefreshToken",back_populates="users",cascade="all,delete")

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    id = Column(Integer,primary_key=True,index=True)
    user_id = Column(String,ForeignKey("users.id"))
    refresh_token = Column(String,nullable=True,unique=True)
    last_login = Column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)
    device_name = Column(String,nullable=True)

    users = relationship("Users",back_populates="tokens")