from fastapi import HTTPException
from beanie import PydanticObjectId

from constants.category_constants import ALLOWED_FORMATS
from models.file import File


async def get_file(file_id: str, user_id: str):
    file = await File.get(PydanticObjectId(file_id))

    if not file:
        raise HTTPException(status_code=404, detail="Файл не найден")

    if file.user_id != user_id:
        raise HTTPException(status_code=403, detail="Отказано в доступе")

    return file


def set_file_category(fileformat):
    for category in ALLOWED_FORMATS:
        if fileformat in ALLOWED_FORMATS[category]:
            return category
    return False


def is_allowed_format(fileformat, category):
    if fileformat in ALLOWED_FORMATS[category]:
        return True
    return False
