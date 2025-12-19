from pydantic import BaseModel, Field
from typing import Any, Optional

class BaseResponse(BaseModel):
    status: str
    message: Optional[str] = None
    data: Optional[Any] = None

class UserCreate(BaseModel):
    username : str
    mail:str
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
    username:str
    is_premium:bool
    access_token :str
    refresh_token:str
    token_type:str ="bearer"

class VpnRegister(BaseModel):
    username:str
    server_name : str
    public_key : str

class VpnConfigResponse(BaseModel):
    status : str = Field(default="success")
    assigned_ip : str = Field(...)
    server_public_key : str = Field(...)
    endpoint : str = Field(...)
    allowed_ips : str = Field(default="0.0.0.0/0")

class BePremium(BaseModel):
    username:str
    is_premium : bool
