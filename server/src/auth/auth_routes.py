from fastapi import APIRouter, Response, status, Depends
from auth.jwt_confg import AuthJWT

from models.user import Login, Register
from api.users.user_services import get_user_id
from auth.auth_services import create_new_user, login_user, refresh_access_token, logout_user


router = APIRouter()


@router.post('/register')
async def register(credentials: Register):
    return await create_new_user(credentials)


@router.post('/login')
async def login(credentials: Login, response: Response, Authorize: AuthJWT = Depends()):
    return await login_user(credentials, response, Authorize)


@router.get('/refresh')
async def refresh_token(response: Response, Authorize: AuthJWT = Depends(), user_id: get_user_id = Depends()):
    return await refresh_access_token(Authorize, response, str(user_id))


@router.get('/logout', status_code=status.HTTP_200_OK)
async def logout(response: Response, Authorize: AuthJWT = Depends()):
    return await logout_user(response, Authorize)
