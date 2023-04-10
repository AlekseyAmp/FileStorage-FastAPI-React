from fastapi import Response, Depends, HTTPException
from datetime import datetime, timedelta

from models.user import User, Login, Register
from config.jwt_config import AuthJWT
from models.history import UserHistory
from services.history_services import set_history_today
from constants import auth_constants
from constants.history_constants import today_time
from utils import auth_utils


async def create_access_token(authorize: AuthJWT, user_id: str):
    access_token = authorize.create_access_token(
        subject=user_id,
        expires_time=timedelta(minutes=auth_constants.ACCESS_TOKEN_EXPIRES_IN)
    )
    return access_token


async def create_refresh_token(authorize: AuthJWT, user_id: str):
    refresh_token = authorize.create_refresh_token(
        subject=user_id,
        expires_time=timedelta(minutes=auth_constants.REFRESH_TOKEN_EXPIRES_IN)
    )
    return refresh_token


async def create_new_user(credentials: Register):
    if not auth_utils.is_valid_email(credentials.email):
        raise HTTPException(
            status_code=400,
            detail="Неверный адрес электронной почты"
        )

    email_exists = await User.find_one(
        User.email == credentials.email
    )

    if email_exists:
        raise HTTPException(
            status_code=409,
            detail="Аккаунт уже существует"
        )

    if credentials.password != credentials.password_repeat:
        raise HTTPException(
            status_code=400,
            detail="Пароли не совпадают"
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

    history_dict = {
        "title": "Регистрация",
        "description": f"Регистрация под почтой {new_user.email}",
        "time": today_time
    }
    await set_history_today(UserHistory, history_dict, str(new_user.id))

    return new_user


async def login_user(credentials: Login, response: Response,
                     authorize: AuthJWT = Depends()):
    user = await User.find_one({
        'email': credentials.email.lower()
    })

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Аккаунт не найден"
        )

    if not auth_utils.verify_password(credentials.password, user.password):
        raise HTTPException(
            status_code=400,
            detail="Неверная почта или пароль"
        )

    access_token = await create_access_token(authorize, str(user.id))
    refresh_token = await create_refresh_token(authorize, str(user.id))

    response.set_cookie("access_token",
                        access_token,
                        auth_constants.ACCESS_TOKEN_EXPIRES_IN * 60,
                        auth_constants.ACCESS_TOKEN_EXPIRES_IN * 60,
                        "/",
                        None,
                        False,
                        True,
                        "lax")

    response.set_cookie("refresh_token",
                        refresh_token,
                        auth_constants.REFRESH_TOKEN_EXPIRES_IN * 60,
                        auth_constants.REFRESH_TOKEN_EXPIRES_IN * 60,
                        "/",
                        None,
                        False,
                        True,
                        "lax"
                        )

    response.set_cookie("logged_in",
                        True,
                        auth_constants.ACCESS_TOKEN_EXPIRES_IN * 60,
                        auth_constants.ACCESS_TOKEN_EXPIRES_IN * 60,
                        "/",
                        None,
                        False,
                        False,
                        "lax")

    history_dict = {
        "title": "Вход",
        "description": f"Вход в диск",
        "time": today_time
    }
    await set_history_today(UserHistory, history_dict, str(user.id))

    return {"refresh_token": refresh_token, "access_token": access_token}


async def refresh_token(authorize: AuthJWT,
                        response: Response,
                        user_id: str):
    access_token = await create_access_token(authorize, user_id)

    response.set_cookie("access_token",
                        access_token,
                        auth_constants.ACCESS_TOKEN_EXPIRES_IN * 60,
                        auth_constants.ACCESS_TOKEN_EXPIRES_IN * 60,
                        "/",
                        None,
                        False,
                        True,
                        "lax")

    response.set_cookie("logged_in",
                        True,
                        auth_constants.ACCESS_TOKEN_EXPIRES_IN * 60,
                        auth_constants.ACCESS_TOKEN_EXPIRES_IN * 60,
                        "/",
                        None,
                        False,
                        False,
                        "lax")

    return access_token


async def logout_user(response: Response, authorize: AuthJWT = Depends()):
    authorize.unset_jwt_cookies()
    response.set_cookie("logged_in", False)
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    response.delete_cookie("email")
    return {"status": "success"}
