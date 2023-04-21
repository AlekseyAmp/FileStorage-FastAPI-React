from fastapi import HTTPException
from beanie import PydanticObjectId

from models.category import Category
from constants.category_constants import ALLOWED_FORMATS


async def get_category(category_name: str, user_id: str):
    category = await Category.find_one({
        "user_id": user_id,
        "name": category_name
    })

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Категория не найдена"
        )

    if category.user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="Отказано в доступе"
        )

    return category


def set_file_category(fileformat: str):
    for category in ALLOWED_FORMATS:
        if fileformat in ALLOWED_FORMATS[category]:
            return category
    return False
