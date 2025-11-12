from pydantic import BaseModel

class Settings(BaseModel):
    DATABASE_URL:str = "sqlite:///./test.db"
    JWT_SECRET:str = "secretvpn"
    JWT_SECRET_REFRESH:str="refreshsecurevpn"
    JWT_ALGORITHM:str ="HS256"
    JWT_EXPIRE_TIME:int=60
    JWT_EXPIRE_TIME_REFRESH:int=30
setting = Settings()