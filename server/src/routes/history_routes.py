from fastapi import APIRouter, Depends

from services.user_services import get_user_id
from services import history_services as h_s


router = APIRouter()


@router.get("/history/all")
async def get_all_history(user_id: get_user_id = Depends()):
    return await h_s.get_all_history(user_id)


@router.get("/history/last_five")
async def get_last_five_history(user_id: get_user_id = Depends()):
    return await h_s.get_last_five_history(user_id)


@router.get("/history/me")
async def get_user_history(user_id: get_user_id = Depends()):
    return await h_s.get_user_history(user_id)
