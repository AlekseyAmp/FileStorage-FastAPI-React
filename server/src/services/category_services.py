from fastapi import HTTPException
from beanie import PydanticObjectId
from datetime import datetime
import os

from models.category import Category
from models.file import File
from models.history import CategoryHistory
from services.history_services import set_history_today
from utils.file_utils import get_file
from utils.category_utils import get_category


async def get_files_from_category(category_name: str, user_id: str):
    files = []
    async for file in File.find({
        "user_id": user_id,
        "category_name": category_name
    }):
        file_dict = {
            "file_id": str(file.id),
            "user_id": file.user_id,
            "name": file.name,
            "size": file.size,
            "content_type": file.content_type,
            "category_name": file.category_name,
            "is_favorite": file.metadata["is_favorite"],
            "is_basket": file.metadata["is_basket"],
            "date_created": file.metadata["date_created"],
            "time_created": file.metadata["time_created"]
        }
        files.append(file_dict)

    return files[::-1]


async def create_new_category(category_name: str, user_id: str):

    # Default categories(images, documents, music, videos) are abstract,
    # all files associated with them are in the DEFAULT_CATEGORY folder
    default_categories = ("images", "documents", "music", "videos")

    if category_name in default_categories:
        raise HTTPException(
            status_code=403,
            detail="Нельзя создать такую категорию, потому что она установлена по умолчанию"
        )

    directory = os.path.join("STORAGE", user_id)

    if not os.path.exists(directory):
        os.makedirs(directory)

    category_path = os.path.join(directory, category_name)

    if os.path.isdir(category_path):
        raise HTTPException(
            status_code=403,
            detail="Такая категория уже существует"
        )

    os.makedirs(category_path)

    new_category = Category(
        user_id=user_id,
        name=category_name,
        size=0,
        path=category_path,
        metadata={
            "is_favorite": False,
            "is_basket": False,
            "date_created": datetime.now().strftime("%d-%m-%Y"),
            "time_created": datetime.now().strftime("%H:%M:%S")
        }
    )
    await new_category.insert()

    history_dict = {
        "category_id": str(new_category.id),
        "category_name": new_category.name,
        "title": "Создание категории",
        "description": f"Категория {new_category.name} была создана",
        "time": datetime.now().strftime("%H:%M:%S")
    }
    await set_history_today(CategoryHistory, history_dict, user_id)

    return {"category_id": new_category.id}


async def delete_category(category_id: str, user_id: str):
    category = await get_category(category_id, user_id)

    default_categories = ("DEFAULT_CATEGORY", "images",
                          "documents", "music", "videos")

    if category.name in default_categories:
        raise HTTPException(
            status_code=403,
            detail="Невозможно удалить эту категорию, так как она установлена по умолчанию"
        )

    os.remove(category.path)
    await category.delete()


async def rename_category(category_id: str, new_name, user_id: str):
    default_categories = ("DEFAULT_CATEGORY", "images",
                          "documents", "music", "videos")

    if new_name in default_categories:
        raise HTTPException(
            status_code=403,
            detail="Невозможно переименовать эту категорию, так как она установлена по умолчанию"
        )

    category = await get_category(category_id, user_id)

    category_path = category.path
    dir_path = os.path.dirname(category_path)

    new_category_path = os.path.join(dir_path, new_name)

    os.rename(category_path, new_category_path)

    files = await get_files_from_category(category.name, user_id)
    for file_dict in files:
        file_id = file_dict['file_id']
        file = await get_file(file_id, user_id)

        new_file_path = os.path.join(new_category_path, file.name)

        await file.update({"$set": {"path": new_file_path}})
        await file.update({"$set": {"category_name": new_name}})

    await category.update({"$set": {"path": new_category_path}})
    await category.update({"$set": {"name": new_name}})

    return {"new_name": new_name}


async def change_size_category(category_name: str, action: str, size: int, user_id: str):
    async for category in Category.find({
        "user_id": user_id,
        "name": category_name
    }):
        category_id = str(category.id)

    category = await get_category(category_id, user_id)

    if action == "upload":
        await category.update({"$inc": {"size": size}})

    elif action == "delete":
        await category.update({"$dec": {"size": size}})
