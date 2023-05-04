from fastapi import APIRouter, Depends

from services.user_services import get_user_id
from services import condition_services as con_s


router = APIRouter()


@router.get("/basket")
async def get_all_basket_files(user_id: get_user_id = Depends()):
    return await con_s.get_moved_files("is_basket", user_id)


@router.get("/favorite")
async def get_all_favorite_files(user_id: get_user_id = Depends()):
    return await con_s.get_moved_files("is_favorite", user_id)
