
from fastapi import APIRouter, Depends, UploadFile

from services.user_services import get_user_id
from services.file_services import upload_file, download_file, rename_file, delete_file, in_basket_file, in_favorite_file
# from api.files.file_services import upload_file, download_file, delete_file, rename_file, get_all_files


router = APIRouter()


@router.post("/upload_file")
async def upload_file_endpoint(file: UploadFile, user_id: get_user_id = Depends()):
    return await upload_file(file, user_id)


@router.get("/download_file/{file_id}")
async def download_file_endpoint(file_id: str, user_id: get_user_id = Depends()):
    return await download_file(file_id, user_id)


@router.patch("/rename_file/{file_id}/{new_name}")
async def rename_file_endpoint(file_id: str, new_name: str, user_id: get_user_id = Depends()):
    return await rename_file(file_id, new_name, user_id)


@router.delete("/delete_file/{file_id}")
async def delete_file_endpoint(file_id: str, user_id: get_user_id = Depends()):
    return await delete_file(file_id, user_id)


@router.patch("/in_basket_file/{file_id}")
async def in_basket_file_endpoint(file_id: str, user_id: get_user_id = Depends()):
    return await in_basket_file(file_id, user_id)


@router.patch("/in_favorite_file/{file_id}")
async def in_favorite_file_endpoint(file_id: str, user_id: get_user_id = Depends()):
    return await in_favorite_file(file_id, user_id)
