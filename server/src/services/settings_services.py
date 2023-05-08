from fastapi import HTTPException

from models.user import User
from utils.user_utils import get_user
from utils.auth_utils import is_valid_email, hash_password


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


async def change_password(user_id: str, new_password: str):
    user = await get_user(user_id)

    await user.update({"$set": {"password": hash_password(new_password)}})

    return {"new_password": new_password}
