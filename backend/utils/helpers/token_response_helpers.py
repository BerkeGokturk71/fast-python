from fastapi import HTTPException,status

from backend.app.core.security import verify_access_token


def token_is_available(token):
    token_data = verify_access_token(token)
    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token geçersiz veya süresi dolmuş."
        )