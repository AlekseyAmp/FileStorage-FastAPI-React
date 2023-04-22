from fastapi import APIRouter, Depends

from services.user_services import get_user_id
from services import info_services as i_s

router = APIRouter()


@router.get("/info/files")
async def get_files_info(user_id: get_user_id = Depends()):
    return await i_s.get_files_info(user_id)


@router.get("/info/categories")
async def get_custom_categories_info(user_id: get_user_id = Depends()):
    return await i_s.get_custom_categories_info(user_id)


@router.get("/info/categories/{category_name}")
async def get_files_info_by_category(category_name: str, user_id: get_user_id = Depends()):
    return await i_s.get_files_info_by_category(category_name, user_id)
