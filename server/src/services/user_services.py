from fastapi import Depends, HTTPException
from fastapi_jwt_auth.exceptions import MissingTokenError
from beanie import PydanticObjectId

from config.jwt_config import AuthJWT
from models.user import User


async def get_user_info(user_id: str):
    user = await User.get(PydanticObjectId(user_id))

    user_dict = {
        "user_id": user.id,
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
