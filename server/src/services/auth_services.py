from fastapi import Response, status, Depends, HTTPException
from datetime import datetime, timedelta

from models.user import User, Login, Register
from config.jwt_config import AuthJWT
from constants import auth_constants
from utils import auth_utils


async def create_access_token(Authorize: AuthJWT, user_id: str):
    access_token = Authorize.create_access_token(
        subject=user_id,
        expires_time=timedelta(minutes=auth_constants.ACCESS_TOKEN_EXPIRES_IN)
    )
    return access_token


async def create_refresh_token(Authorize: AuthJWT, user_id: str):
    refresh_token = Authorize.create_refresh_token(
        subject=user_id,
        expires_time=timedelta(minutes=auth_constants.REFRESH_TOKEN_EXPIRES_IN)
    )
    return refresh_token


async def create_new_user(credentials: Register):
    if not auth_utils.is_valid_email(credentials.email):
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
        password=auth_utils.hash_password(credentials.password),
        created_at=datetime.now(),
        storage_used=0,
        max_storage=15,
        is_premium=False
    )

    await new_user.insert()
    return new_user


async def login_user(credentials: Login, response: Response, Authorize: AuthJWT = Depends()):
    user = await User.find_one({'email': credentials.email.lower()})

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Аккаунт не найден'
        )

    if not auth_utils.verify_password(credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Неверная почта или пароль'
        )

    access_token = await create_access_token(Authorize, str(user.id))
    refresh_token = await create_refresh_token(Authorize, str(user.id))

    response.set_cookie('access_token', access_token, auth_constants.ACCESS_TOKEN_EXPIRES_IN * 60,
                        auth_constants.ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, True, 'lax')
    response.set_cookie('refresh_token', refresh_token,
                        auth_constants.REFRESH_TOKEN_EXPIRES_IN * 60, auth_constants.REFRESH_TOKEN_EXPIRES_IN * 60, '/', None, False, True, 'lax')
    response.set_cookie('logged_in', True, auth_constants.ACCESS_TOKEN_EXPIRES_IN * 60,
                        auth_constants.ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, False, 'lax')

    return {'status': 'success', 'access_token': access_token}


async def refresh_access_token(Authorize: AuthJWT, response: Response, user_id: str):
    access_token = await create_access_token(Authorize, user_id)

    response.set_cookie('access_token', access_token, auth_constants.ACCESS_TOKEN_EXPIRES_IN * 60,
                        auth_constants.ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, True, 'lax')
    response.set_cookie('logged_in', True, auth_constants.ACCESS_TOKEN_EXPIRES_IN * 60,
                        auth_constants.ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, False, 'lax')

    return access_token


async def logout_user(response: Response, Authorize: AuthJWT = Depends()):
    Authorize.unset_jwt_cookies()
    response.set_cookie('logged_in', False)
    response.delete_cookie('refresh_token')
    return {'status': 'success'}
