from fastapi import Depends, HTTPException
from fastapi_jwt_auth.exceptions import MissingTokenError

from config.jwt_config import AuthJWT
from utils.user_utils import get_user


async def get_user_info(user_id: str):
    user = await get_user(user_id)

    user_dict = {
        "email": user.email,
        "username": user.username
    }

    return user_dict


async def get_user_id(authorize: AuthJWT = Depends()):
    try:
        authorize.jwt_required()
        user_id = authorize.get_jwt_subject()
        return user_id
    except (MissingTokenError):
        raise HTTPException(
            status_code=401,
            detail="Не авторизован"
        )
