from fastapi import APIRouter, Depends

from services.user_services import get_user_id
from services import category_services as categ_s


router = APIRouter()


@router.get("/categories")
async def get_custom_categories(user_id: get_user_id = Depends()):
    return await categ_s.get_custom_categories(user_id)


@router.get("/categories/files/{category_name}")
async def get_files_from_category(category_name: str, user_id: get_user_id = Depends()):
    return await categ_s.get_files_from_category(category_name, user_id)


@router.post("/categories/create/{category_name}")
async def create_new_category(category_name: str, user_id: get_user_id = Depends()):
    return await categ_s.create_new_category(category_name, user_id)


@router.get("/categories/download/{category_name}")
async def download_category(category_name: str, user_id: get_user_id = Depends()):
    return await categ_s.download_category(category_name, user_id)


@router.patch("/categories/rename/{category_name}/{new_name}")
async def rename_category(category_name: str, new_name: str, user_id: get_user_id = Depends()):
    return await categ_s.rename_category(category_name, new_name, user_id)


@router.delete("/categories/delete/{category_name}")
async def delete_category(category_name: str, user_id: get_user_id = Depends()):
    return await categ_s.delete_category(category_name, user_id)
