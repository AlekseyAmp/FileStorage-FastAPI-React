from fastapi import APIRouter, Depends, UploadFile

from services.user_services import get_user_id
from services import file_services as f_s


router = APIRouter()


@router.post("/files/upload/{category_name}")
async def upload_file_in_category(file: UploadFile, category_name: str, user_id: get_user_id = Depends()):
    return await f_s.create_new_file(file, category_name, user_id)


@router.get("/files/read/{file_id}")
async def read_file(file_id: str, user_id: get_user_id = Depends()):
    return await f_s.read_file(file_id, user_id)


@router.get("/files/download/{file_id}")
async def download_file(file_id: str, user_id: get_user_id = Depends()):
    return await f_s.download_file(file_id, user_id)


@router.patch("/files/rename/{file_id}/{new_name}")
async def rename_file(file_id: str, new_name: str, user_id: get_user_id = Depends()):
    return await f_s.rename_file(file_id, new_name, user_id)


@router.delete("/files/delete/{file_id}")
async def delete_file(file_id: str, user_id: get_user_id = Depends()):
    return await f_s.delete_file(file_id, user_id)
