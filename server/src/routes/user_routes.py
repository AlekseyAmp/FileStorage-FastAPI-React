from fastapi import APIRouter, Depends
from beanie import PydanticObjectId

from models.user import User
from services.user_services import get_user_id


router = APIRouter()


@router.get('/me')
async def get_user_info(user_id: get_user_id = Depends()):
    user = await User.get(PydanticObjectId(user_id))
    return {"email": user.email}
