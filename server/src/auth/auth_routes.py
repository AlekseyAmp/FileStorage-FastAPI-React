from fastapi import APIRouter, Response, status, Depends, HTTPException
from datetime import datetime, timedelta
from auth.jwt_confg import AuthJWT

from models.user import User, Login, Register
from api.users.user_services import get_user_id
from config.settings import settings
import auth.utils

router = APIRouter()
ACCESS_TOKEN_EXPIRES_IN = settings.ACCESS_TOKEN_EXPIRES_IN
REFRESH_TOKEN_EXPIRES_IN = settings.REFRESH_TOKEN_EXPIRES_IN


@router.post('/register', status_code=status.HTTP_201_CREATED)
async def register(credentials: Register):

    if not auth.utils.is_valid_email(credentials.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Неверный адрес электронной почты'
        )

    email_exists = await User.find_one(User.email == credentials.email)
    if email_exists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Аккаунт уже существует'
        )

    if credentials.password != credentials.password_repeat:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Пароли не совпадают'
        )

    new_user = User(
        email=credentials.email.lower(),
        password=auth.utils.hash_password(credentials.password),
        created_at=datetime.now(),
        storage_used=0,
        max_storage=15,
        is_premium=False
    )

    await new_user.insert()

    return {'status': 'success'}


@router.post('/login')
async def login(credentials: Login, response: Response, Authorize: AuthJWT = Depends()):
    user = await User.find_one({'email': credentials.email.lower()})

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Аккаунт не найден'
        )

    if not auth.utils.verify_password(credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Неверная почта или пароль'
        )

    access_token = Authorize.create_access_token(
        subject=str(user.id),
        expires_time=timedelta(minutes=ACCESS_TOKEN_EXPIRES_IN)
    )

    refresh_token = Authorize.create_refresh_token(
        subject=str(user.id),
        expires_time=timedelta(minutes=REFRESH_TOKEN_EXPIRES_IN)
    )

    # Store refresh and access tokens in cookie
    response.set_cookie('access_token', access_token, ACCESS_TOKEN_EXPIRES_IN * 60,
                        ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, True, 'lax')
    response.set_cookie('refresh_token', refresh_token,
                        REFRESH_TOKEN_EXPIRES_IN * 60, REFRESH_TOKEN_EXPIRES_IN * 60, '/', None, False, True, 'lax')
    response.set_cookie('logged_in', True, ACCESS_TOKEN_EXPIRES_IN * 60,
                        ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, False, 'lax')

    # Send both access
    return {'status': 'success', 'access_token': access_token}


@router.get('/refresh')
async def refresh_token(response: Response, Authorize: AuthJWT = Depends(), user_id: get_user_id = Depends()):
    access_token = Authorize.create_access_token(
        subject=str(user_id),
        expires_time=timedelta(minutes=ACCESS_TOKEN_EXPIRES_IN)
    )
    response.set_cookie('access_token', access_token, ACCESS_TOKEN_EXPIRES_IN * 60,
                        ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, True, 'lax')
    response.set_cookie('logged_in', True, ACCESS_TOKEN_EXPIRES_IN * 60,
                        ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, False, 'lax')

    return access_token


@router.get('/logout', status_code=status.HTTP_200_OK)
async def logout(response: Response, Authorize: AuthJWT = Depends()):
    Authorize.unset_jwt_cookies()
    response.delete_cookie('refresh_token')
    response.set_cookie('logged_in', False)
    return {'status': 'success'}
