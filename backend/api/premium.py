from fastapi import Depends,APIRouter,HTTPException,status
from sqlalchemy.orm import Session
from backend.db.session import get_db
from backend.models.users import Users
from backend.app.core.security import verify_access_token
from backend.utils.response import  be_premium_response
from fastapi.security.oauth2 import OAuth2PasswordBearer

router_premium = APIRouter(prefix="/premium", tags=["Be Premium"])

oAuthBearer = OAuth2PasswordBearer(tokenUrl="token")
@router_premium.post("/user")
def premium(token : str = Depends(oAuthBearer),db : Session = Depends(get_db)):
    user_token_get_name = verify_access_token(token)
    if( not user_token_get_name):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token geçersiz veya süresi dolmuş."
        )
    user = db.query(Users).filter(Users.username == user_token_get_name).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = "Kullanıcı bulunamadı."
        )
    if user.is_premium == True:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail= "Zaten Premiumlusun"
        )

    user.is_premium = True
    db.commit()
    db.refresh(user)
    return be_premium_response(username=user.username,premium=user.is_premium,status = str(status.HTTP_201_CREATED))