from pydantic import BaseModel
from typing import Any, Optional

class BaseResponse(BaseModel):
    status: str
    message: Optional[str] = None
    data: Optional[Any] = None

class UserCreate(BaseModel):
    uuid : str
    username : str
    password :str


class UserLogin(BaseModel):
    username:str
    password:str

  
class UserSchema(BaseModel):
    uuid :str
    hashed_password:str
    
    model_config = {
        "from_attributes": True  # ORM objesinden veri alınmasını sağlar
    }

class Token(BaseModel):
    access_token :str
    refresh_token:str
    token_type:str ="bearer"