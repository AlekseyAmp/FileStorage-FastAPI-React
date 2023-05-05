from fastapi import HTTPException
from beanie import PydanticObjectId

from models.user import User


async def get_user(user_id: str):
    user = await User.get(PydanticObjectId(user_id))

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Пользователь не найден"
        )

    if str(user.id) != user_id:
        raise HTTPException(
            status_code=403,
            detail="Отказано в доступе"
        )

    return user
