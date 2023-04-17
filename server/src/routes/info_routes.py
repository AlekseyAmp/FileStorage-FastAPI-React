from fastapi import APIRouter, Depends

from services.user_services import get_user_id
from services import info_services as i_s

router = APIRouter()


@router.get("/info/files")
async def get_files_info(user_id: get_user_id = Depends()):
    return await i_s.get_files_info(user_id)


@router.get("/info/category/documents")
async def get_documents_info_category(user_id: get_user_id = Depends()):
    return await i_s.get_files_info_by_category("documents", user_id)


@router.get("/info/category/images")
async def get_images_info_category(user_id: get_user_id = Depends()):
    return await i_s.get_files_info_by_category("images", user_id)


@router.get("/info/category/music")
async def get_music_info_category(user_id: get_user_id = Depends()):
    return await i_s.get_files_info_by_category("music", user_id)


@router.get("/info/category/videos")
async def get_videos_info_category(user_id: get_user_id = Depends()):
    return await i_s.get_files_info_by_category("videos", user_id)
