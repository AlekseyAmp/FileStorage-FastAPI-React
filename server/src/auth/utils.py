from passlib.context import CryptContext
import re
from fastapi import HTTPException, Depends, Request
from fastapi_jwt_auth import AuthJWT

def is_valid_email(email: str) -> bool:
    pat = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
    if re.match(pat, email):
        return True
    return False


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str):
    return pwd_context.verify(password, hashed_password)


async def check_auth(request: Request, Authorize: AuthJWT):
    access_token = request.cookies.get('access_token')
    if not access_token:
        raise HTTPException(
            status_code=401,
            detail='Вы не авторизованы'
        )
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()
    return user_id
