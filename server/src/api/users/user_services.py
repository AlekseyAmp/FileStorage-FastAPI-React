from fastapi import Depends, HTTPException
from api.auth.jwt_confg import AuthJWT


async def get_user_id(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
        user_id = Authorize.get_jwt_subject()
        return user_id
    except:
        raise HTTPException(status_code=401,
                            detail="Не авторизован")
