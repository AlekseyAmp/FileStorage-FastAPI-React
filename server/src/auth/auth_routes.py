from datetime import datetime
from beanie import PydanticObjectId
from fastapi import APIRouter, Response, status, Depends, HTTPException, Request
from models.user import User, Login, Register
import auth.utils
from auth.oauth2 import AuthJWT

router = APIRouter()

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
    )

    response.set_cookie('access_token', access_token)
    response.set_cookie('logged_in', True)

    return {'status': 'success', 'access_token': access_token}


@router.get('/logout', status_code=status.HTTP_200_OK)
async def logout(response: Response, Authorize: AuthJWT = Depends()):
    Authorize.unset_jwt_cookies()
    response.set_cookie('logged_in', False)
    return {'status': 'success'}


async def get_user_id(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()
    return user_id


@router.get('/me')
async def get_user_info(get_user_id: get_user_id = Depends()):
    user = await User.get(PydanticObjectId(get_user_id))
    return {'email': user.email, 'id': user.id}
