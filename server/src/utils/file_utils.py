from fastapi import HTTPException
from beanie import PydanticObjectId

from constants.category_constants import ALLOWED_FORMATS
from models.file import File


async def get_file(file_id: str, user_id: str):
    file = await File.get(PydanticObjectId(file_id))

    if not file:
        raise HTTPException(
            status_code=404,
            detail="File not found"
        )

    if file.user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    return file


def is_allowed_format(fileformat: str, category: str):
    if fileformat in ALLOWED_FORMATS[category]:
        return True
    return False
