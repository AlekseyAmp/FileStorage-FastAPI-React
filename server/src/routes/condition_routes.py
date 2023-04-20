from fastapi import APIRouter, Depends

from services.user_services import get_user_id
from services import condition_services as con_s


router = APIRouter()


@router.patch("/basket/add/file/{file_id}")
async def add_to_basket_file(file_id: str, user_id: get_user_id = Depends()):
    return await con_s.add_to_basket_file(file_id, user_id)


@router.get("/basket")
async def get_basket_files(user_id: get_user_id = Depends()):
    return await con_s.get_moved_files("is_basket", user_id)


@router.patch("/favorite/add/file/{file_id}")
async def add_to_favorite_file(file_id: str, user_id: get_user_id = Depends()):
    return await con_s.add_to_favorite_file(file_id, user_id)


@router.get("/favorite")
async def get_favorite_files(user_id: get_user_id = Depends()):
    return await con_s.get_moved_files("is_favorite", user_id)


@router.patch("/revert/file/{file_id}")
async def revert_moved_file_back(file_id: str, user_id: get_user_id = Depends()):
    return await con_s.revert_moved_file_back(file_id, user_id)
