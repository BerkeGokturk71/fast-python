from fastapi import Depends,APIRouter,HTTPException,status
from backend.schemas.user_schema import Token,UserCreate,UserLogin,BaseResponse
from sqlalchemy.orm import Session
from backend.db.session import get_db
from backend.models.users import Users,RefreshToken
from backend.app.core.security import verify_password,create_access_token,create_refresh_token,verify_refresh_token
from backend.utils.response import token_reponse,register_response
from backend.crud.user import create_user
from backend.crud.refresh import db_refresh_token

router_auth = APIRouter(prefix="/auth", tags=["Authentication"])

@router_auth.post(path="/login",response_model=BaseResponse)
async def login_user(user:UserLogin,db:Session=Depends(get_db)):
    db_user = db.query(Users).filter(Users.username == user.username).first()

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="kullanıcı yok"
        )

    if verify_password(user.password,db_user.hashed_password):
        access_token = create_access_token(data={"sub":db_user.username})
        refresh_token= create_refresh_token(data={"sub":db_user.username})
        #token_repo = TokenRepository()
        #await token_repo.store_access(access_jti, db_user.id)
        #await token_repo.store_refresh(refresh_jti, db_user.id)

        db_refresh_token(db=db, refresh_token = refresh_token, user_uuid=db_user.id)
        return token_reponse(username=db_user.username,premium=db_user.is_premium, access_token=access_token,refresh_token=refresh_token)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="şifre hatali")

@router_auth.post(path="/register",response_model=BaseResponse)
def register(user:UserCreate,db:Session = Depends(get_db)):
    create_user(db,user.username,user.mail,user.password)
    return register_response()

@router_auth.post(path="/refresh",response_model=BaseResponse)
def refresh(refresh:Token,db:Session=Depends((get_db))):
    db_refresh = db.query(RefreshToken).filter(RefreshToken.refresh_token==refresh.refresh_token).first()

    if not db_refresh:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="refresh token yok"
        )
    if not verify_refresh_token(db_refresh.refresh_token):
        raise HTTPException(status_code=401, detail="Refresh token expired")

    new_access_token = create_access_token(data={})
    return token_reponse(access_token=new_access_token,refresh_token=refresh.refresh_token)

