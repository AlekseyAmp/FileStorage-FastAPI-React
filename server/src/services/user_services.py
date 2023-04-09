from fastapi import Depends, HTTPException
from config.jwt_config import AuthJWT


async def get_user_id(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
        user_id = Authorize.get_jwt_subject()
        return user_id
    except:
        raise HTTPException(status_code=401,
                            detail="Не авторизован")


