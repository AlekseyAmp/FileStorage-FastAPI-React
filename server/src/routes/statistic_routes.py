from fastapi import APIRouter, Depends

from services.user_services import get_user_id
from services import statistic_services as s_s


router = APIRouter()


@router.get("/statistic/today")
async def get_statistic_today(user_id: get_user_id = Depends()):
    return await s_s.get_statistic_today(user_id)
