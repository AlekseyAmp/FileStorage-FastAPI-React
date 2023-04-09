from fastapi import APIRouter, Depends
from services.user_services import get_user_id
from services.history_services import get_history
from models.history import FileHistory, UserHistory


router = APIRouter()


@router.get("/get_files_history")
async def get_files_history_history(user_id: get_user_id = Depends()):
    return await get_history(FileHistory, user_id)


@router.get("/get_users_history")
async def get_users_history_endpoint(user_id: get_user_id = Depends()):
    return await get_history(UserHistory, user_id)