from backend.schemas.user_schema import Token,BaseResponse



def token_reponse(access_token:str,refresh_token:str):
    token = Token(access_token=access_token,refresh_token=refresh_token)
    return BaseResponse(status="success",message="token created",data=token)

def register_response():
    return BaseResponse(status="success",message="register success")