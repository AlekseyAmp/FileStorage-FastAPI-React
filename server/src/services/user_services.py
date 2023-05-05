from fastapi import Depends, HTTPException
from fastapi_jwt_auth.exceptions import MissingTokenError
from beanie import PydanticObjectId

from config.jwt_config import AuthJWT
from models.user import User
from utils.user_utils import get_user
from utils.auth_utils import is_valid_email


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


async def change_email(user_id: str, new_email: str):
    user = await get_user(user_id)

    if not is_valid_email(new_email):
        raise HTTPException(
            status_code=400,
            detail="Неверный адрес электронной почты"
        )

    async for user_elem in User.find({
        "email": new_email
    }):
        if user_elem:
            raise HTTPException(
                status_code=403,
                detail="Данный email уже занят"
            )

    await user.update({"$set": {"email": new_email}})
    await user.update({"$set": {"username": new_email.split('@')[0]}})

    return {"new_email": new_email}
