from datetime import timedelta,datetime
from jose import jwt,JWTError,ExpiredSignatureError
from backend.app.core.config import setting
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

def hash_password(password:str)->str:
    return pwd_context.hash(password)


def verify_password(plain_password,hashed_password)->bool:
    return pwd_context.verify(plain_password,hashed_password)

def create_access_token(data:dict):
    data_cpy = data.copy()
    expire = datetime.now() + timedelta(minutes=setting.JWT_EXPIRE_TIME)
    data_cpy["exp"] = expire
    token = jwt.encode(data_cpy, setting.JWT_SECRET, algorithm=setting.JWT_ALGORITHM)
    return token

def verify_access_token(access_token:str):
    try:
        payload = jwt.decode(access_token,setting.JWT_SECRET,setting.JWT_ALGORITHM)
        username = payload.get("sub")
        return username
    except ExpiredSignatureError:
        return "expired"
    except JWTError:
        return None

def create_refresh_token(data:dict):
    data_cpy = data.copy()
    expire = datetime.now()+ timedelta(days=setting.JWT_EXPIRE_TIME_REFRESH)
    data_cpy["exp"] = expire
    token = jwt.encode(data_cpy,setting.JWT_SECRET_REFRESH,algorithm=setting.JWT_ALGORITHM)
    return token

def verify_refresh_token(refresh_token:str):
    try:
        payload = jwt.decode(refresh_token,setting.JWT_SECRET_REFRESH,setting.JWT_ALGORITHM)
        username = payload.get("sub")
        return username
    except ExpiredSignatureError:
        return False
    except JWTError:
        return None

