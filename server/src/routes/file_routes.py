from fastapi import APIRouter, Depends, UploadFile

from services.user_services import get_user_id
from services import file_services as f_s
from services import category_services as categ_s

router = APIRouter()


@router.get("/files/{category_name}")
async def get_all_files_from_category(category_name: str, user_id: get_user_id = Depends()):
    return await categ_s.get_files_from_category(category_name, user_id)


@router.get("/files/info/total")
async def get_all_files_info(user_id: get_user_id = Depends()):
    return await f_s.get_all_files_info(user_id)


@router.get("/files/info/{category_name}")
async def get_all_files_info_by_category(category_name: str, user_id: get_user_id = Depends()):
    return await f_s.get_files_info_by_category(category_name, user_id)


@router.post("/files/upload/{category_name}")
async def upload_file_in_category(file: UploadFile, category_name: str, user_id: get_user_id = Depends()):
    return await f_s.create_new_file(file, category_name, user_id)


@router.get("/files/download/{file_id}")
async def download_file(file_id: str, user_id: get_user_id = Depends()):
    return await f_s.download_file(file_id, user_id)


@router.patch("/files/rename/{file_id}/{new_name}")
async def rename_file(file_id: str, new_name: str, user_id: get_user_id = Depends()):
    return await f_s.rename_file(file_id, new_name, user_id)


@router.patch("/files/to_basket/{file_id}")
async def add_to_basket_file(file_id: str, user_id: get_user_id = Depends()):
    return await f_s.add_to_basket_file(file_id, user_id)


@router.patch("/files/to_favorite/{file_id}")
async def add_to_favorite_file(file_id: str, user_id: get_user_id = Depends()):
    return await f_s.add_to_favorite_file(file_id, user_id)


@router.patch("/files/revert/{file_id}")
async def revert_moved_file_back(file_id: str, user_id: get_user_id = Depends()):
    return await f_s.revert_moved_file_back(file_id, user_id)


@router.delete("/files/delete/{file_id}")
async def delete_file(file_id: str, user_id: get_user_id = Depends()):
    return await f_s.delete_file(file_id, user_id)
