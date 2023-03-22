from fastapi import APIRouter, Depends

from api.categories.category_service import get_files_by_category
from api.users.user_services import get_user_id


router = APIRouter()


@router.get("/category/documents")
async def get_documents_category(user_id: get_user_id = Depends()):
    return {"files": await get_files_by_category("documents", user_id)}


@router.get("/category/images")
async def get_videos_category(user_id: get_user_id = Depends()):
    return {"files": await get_files_by_category("images", user_id)}


@router.get("/category/music")
async def get_music_category(user_id: get_user_id = Depends()):
    return {"files": await get_files_by_category("music", user_id)}


@router.get("/category/videos")
async def get_videos_category(user_id: get_user_id = Depends()):
    return {"files": await get_files_by_category("videos", user_id)}
