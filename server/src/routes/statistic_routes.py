from fastapi import APIRouter, Depends

from services.user_services import get_user_id
from services import statistic_services as s_s


router = APIRouter()


@router.get("/statistic")
async def get_all_statistic(user_id: get_user_id = Depends()):
    return await s_s.get_all_statistic(user_id)


@router.get("/statistic/today")
async def get_today_statistic(user_id: get_user_id = Depends()):
    return await s_s.get_today_statistic(user_id)
