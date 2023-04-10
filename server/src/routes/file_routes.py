
from fastapi import APIRouter, Depends, UploadFile

from services.user_services import get_user_id
from services import file_services as f_s


router = APIRouter()


@router.get("/files/info")
async def get_files_info(user_id: get_user_id = Depends()):
    return await f_s.get_files_info(user_id)


@router.post("/files/upload")
async def upload_file(file: UploadFile,
                      user_id: get_user_id = Depends()):
    return await f_s.create_new_file(file, user_id)


@router.get("/files/download/{file_id}")
async def download_file(file_id: str,
                        user_id: get_user_id = Depends()):
    return await f_s.download_file(file_id, user_id)


@router.patch("/files/rename/{file_id}/{new_name}")
async def rename_file(file_id: str,
                      new_name: str,
                      user_id: get_user_id = Depends()):
    return await f_s.rename_file(file_id, new_name, user_id)


@router.delete("/files/delete/{file_id}")
async def delete_file(file_id: str,
                      user_id: get_user_id = Depends()):
    return await f_s.delete_file(file_id, user_id)


@router.patch("/files/in_basket/{file_id}")
async def add_to_basket_file(file_id: str,
                             user_id: get_user_id = Depends()):
    return await f_s.add_to_basket_file(file_id, user_id)


@router.patch("/files/in_favorite/{file_id}")
async def add_to_favorite_file(file_id: str,
                               user_id: get_user_id = Depends()):
    return await f_s.add_to_favorite_file(file_id, user_id)


@router.get("/files/basket")
async def get_basket_files(user_id: get_user_id = Depends()):
    return await f_s.get_moved_files("is_deleted", user_id)


@router.get("/files/favorite")
async def get_favorite_files(user_id: get_user_id = Depends()):
    return await f_s.get_moved_files("is_favorite", user_id)
