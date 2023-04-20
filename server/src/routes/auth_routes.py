from fastapi import APIRouter, Response, Depends

from config.jwt_config import AuthJWT
from models.user import Login, Register
from services.user_services import get_user_id
from services import auth_services as a_s


router = APIRouter()


@router.post("/auth/register")
async def register(credentials: Register):
    return await a_s.create_new_user(credentials)


@router.post("/auth/login")
async def login(credentials: Login, response: Response, authorize: AuthJWT = Depends()):
    return await a_s.login_user(credentials, response, authorize)


@router.get("/auth/refresh_token")
async def refresh_token(response: Response, authorize: AuthJWT = Depends(), user_id: get_user_id = Depends()):
    return await a_s.refresh_token(authorize, response, str(user_id))


@router.get("/auth/logout")
async def logout(response: Response, authorize: AuthJWT = Depends()):
    return await a_s.logout_user(response, authorize)
