from fastapi import APIRouter, Depends

from services import user_services as u_s


router = APIRouter()


@router.get("/users/info")
async def get_user_info(user_id: u_s.get_user_id = Depends()):
    return await u_s.get_user_info(user_id)
