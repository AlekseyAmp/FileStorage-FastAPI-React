from fastapi import HTTPException
from beanie import PydanticObjectId

from models.user import User


async def get_user(user_id: str):
    user = await User.get(PydanticObjectId(user_id))

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if str(user.id) != user_id:
        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    return user
