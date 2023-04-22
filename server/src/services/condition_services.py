from fastapi import HTTPException
from datetime import datetime

from models.file import File
from services.history_services import set_history_today
from utils.file_utils import get_file


async def get_moved_files(condition: str, user_id: str):
    files = []
    async for file in File.find({
        "user_id": user_id
    }):
        if file.metadata[condition]:
            file_dict = {
                "file_id": str(file.id),
                "file_name": file.name,
                "file_size": file.size,
                "file_content_type": file.content_type,
                "file_category_name": file.category_name,
                "is_favorite": file.metadata["is_favorite"],
                "is_basket": file.metadata["is_basket"],
                "date_created": file.metadata["date_created"],
                "time_created": file.metadata["time_created"]
            }
            files.append(file_dict)

    return files[::-1]


async def add_to_basket_file(file_id: str, user_id: str):
    file = await get_file(file_id, user_id)

    if file.metadata["is_favorite"]:
        raise HTTPException(
            status_code=403,
            detail="Файл находится в избранном"
        )

    if file.metadata["is_basket"]:
        raise HTTPException(
            status_code=403,
            detail="Файл уже находится в корзине"
        )

    history_dict = {
        "file_id": str(file_id),
        "file_name": file.name,
        "file_content_type": file.content_type,
        "file_category_name": file.category_name,
        "title": "Добавление файла в корзину",
        "description": f"Файл {file.name} был перемещён в корзину",
        "time": datetime.now().strftime("%H:%M:%S")
    }

    await file.update({"$set": {"metadata.is_basket": True}})

    await set_history_today(history_dict, user_id)

    return {"status": "succes"}


async def add_to_favorite_file(file_id: str, user_id: str):
    file = await get_file(file_id, user_id)

    if file.metadata["is_basket"]:
        raise HTTPException(
            status_code=403,
            detail="Файл находится в корзине"
        )

    if file.metadata["is_favorite"]:
        raise HTTPException(
            status_code=403,
            detail="Файл уже находится в избранном"
        )

    history_dict = {
        "file_id": str(file_id),
        "file_name": file.name,
        "file_content_type": file.content_type,
        "file_category_name": file.category_name,
        "title": "Добавление файла в избранное",
        "description": f"Файл {file.name} был перемещён в избранное",
        "time": datetime.now().strftime("%H:%M:%S")
    }

    await file.update({"$set": {"metadata.is_favorite": True}})

    await set_history_today(history_dict, user_id)

    return {"status": "succes"}


async def revert_moved_file_back(file_id: str, user_id: str):
    file = await get_file(file_id, user_id)

    file_location = ''

    if file.metadata["is_basket"]:
        await file.update({"$set": {"metadata.is_basket": False}})
        file_location = "корзины"

    elif file.metadata["is_favorite"]:
        await file.update({"$set": {"metadata.is_favorite": False}})
        file_location = "избранного"

    elif (not file.metadata["is_favorite"]) and (not file.metadata["is_basket"]):
        raise HTTPException(
            status_code=403,
            detail="Файл не находится ни в корзине, ни в избранном"
        )

    history_dict = {
        "file_id": str(file_id),
        "file_name": file.name,
        "file_contentType": file.content_type,
        "file_categoryName": file.category_name,
        "title": f"Удаление файла из {file_location}",
        "description": f"Файл {file.name} был убран из {file_location}",
        "time": datetime.now().strftime("%H:%M:%S")
    }
    await set_history_today(history_dict, user_id)

    return {"status": "succes"}
