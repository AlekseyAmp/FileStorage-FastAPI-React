from fastapi import APIRouter, Depends

from services.user_services import get_user_id
from services import category_services as c_s

router = APIRouter()


@router.get("/category/documents")
async def get_documents_category(user_id: get_user_id = Depends()):
    return await c_s.get_files_by_category("documents", user_id)


@router.get("/category/images")
async def get_images_category(user_id: get_user_id = Depends()):
    return await c_s.get_files_by_category("images", user_id)


@router.get("/category/music")
async def get_music_category(user_id: get_user_id = Depends()):
    return await c_s.get_files_by_category("music", user_id)


@router.get("/category/videos")
async def get_videos_category(user_id: get_user_id = Depends()):
    return await c_s.get_files_by_category("videos", user_id)
