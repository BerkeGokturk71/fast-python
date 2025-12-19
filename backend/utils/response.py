from backend.schemas.user_schema import Token, BaseResponse, BePremium


def token_reponse(username:str,premium:bool, access_token:str,refresh_token:str):
    token = Token(username= username,is_premium=premium, access_token=access_token,refresh_token=refresh_token)
    return BaseResponse(status="success",message="token created",data=token)

def register_response():
    return BaseResponse(status="success",message="register success")

def be_premium_response(username:str,premium:bool,status:str):
    response = BePremium(username =username, is_premium = premium )
    return BaseResponse(status = status,message="null",data = response)