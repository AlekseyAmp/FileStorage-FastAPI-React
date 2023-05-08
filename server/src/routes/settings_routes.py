from fastapi import APIRouter, Depends

from services.user_services import get_user_id
from services import settings_services as set_s


router = APIRouter()


@router.patch("/settings/email/{new_email}")
async def change_email(new_email: str, user_id: get_user_id = Depends()):
    return await set_s.change_email(user_id, new_email)


@router.patch("/settings/password/{new_password}")
async def change_password(new_password: str, user_id: get_user_id = Depends()):
    return await set_s.change_password(user_id, new_password)
