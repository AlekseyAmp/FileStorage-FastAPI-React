from fastapi import APIRouter, Depends

from api.categories.category_service import get_files_by_category
from api.users.user_services import get_user_id


router = APIRouter()


@router.get("/category/documents")
def get_documents_category(user_id: get_user_id = Depends()):
    return {"files": get_files_by_category("documents", user_id)}


@router.get("/category/images")
def get_videos_category(user_id: get_user_id = Depends()):
    return {"files": get_files_by_category("images", user_id)}


@router.get("/category/music")
def get_music_category(user_id: get_user_id = Depends()):
    return {"files": get_files_by_category("music", user_id)}


@router.get("/category/videos")
def get_videos_category(user_id: get_user_id = Depends()):
    return {"files": get_files_by_category("videos", user_id)}
