
from fastapi import APIRouter, Depends, UploadFile

from api.users.user_services import get_user_id
from api.files.file_services import upload_file, download_file, rename_file, get_all_files, in_basket_file


router = APIRouter()


@router.post("/upload_file")
def upload_file_endpoint(file: UploadFile, user_id: get_user_id = Depends()):
    return {"file_id": upload_file(file, user_id)}


@router.get("/download_file/{file_id}")
def download_file_endpoint(file_id: str, user_id: get_user_id = Depends()):
    return download_file(file_id, user_id)


# @router.patch("/in_basket_file/{file_id}")
# def in_basket_file_endpoint(file_id: str, user_id: get_user_id = Depends()):
#     return in_basket_file(file_id, user_id)


@router.patch("/rename_file/{file_id}/{new_name}")
def rename_file_endpoint(file_id: str, new_name: str, user_id: get_user_id = Depends()):
    return rename_file(file_id, new_name, user_id)


@router.get("/all_files")
def get_all_files_endpoint(user_id: get_user_id = Depends()):
    return get_all_files(user_id)
