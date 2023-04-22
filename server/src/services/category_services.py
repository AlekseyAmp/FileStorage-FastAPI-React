from fastapi import HTTPException
from datetime import datetime
import shutil
import os

from models.category import Category
from models.file import File
from services.history_services import set_history_today
from services.statistic_services import set_statistic_today
from utils.file_utils import get_file
from utils.category_utils import get_category


async def get_custom_categories(user_id: str):
    categories = []
    async for category in Category.find({
        "user_id": user_id,
    }):
        if category.name == "default_category":
            continue

        category_dict = {
            "category_id": str(category.id),
            "category_name": category.name,
            "category_size": category.size,
            "is_favorite": category.metadata["is_favorite"],
            "is_basket": category.metadata["is_basket"],
            "date_created": category.metadata["date_created"],
            "time_created": category.metadata["time_created"]
        }
        categories.append(category_dict)

    return categories[::-1]


async def get_files_from_category(category_name: str, user_id: str):
    files = []
    async for file in File.find({
        "user_id": user_id,
        "category_name": category_name.lower()
    }):
        file_dict = {
            "file_id": str(file.id),
            "user_id": file.user_id,
            "file_name": file.name,
            "file_size": file.size,
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

    if category_name.lower() in default_categories:
        raise HTTPException(
            status_code=403,
            detail="Нельзя создать такую категорию, потому что она установлена по умолчанию"
        )

    if category_name.lower() == "default_category":
        category_name = "default_category"

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
        name_for_search=category_name.lower(),
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
    await set_history_today(history_dict, user_id)

    return {"category_name": new_category.name}


async def rename_category(category_name: str, new_name: str, user_id: str):
    default_categories = ("default_category", "images", "documents", "music", "videos")

    if category_name.lower() in default_categories:
        raise HTTPException(
            status_code=403,
            detail="Невозможно переименовать эту категорию, так как она установлена по умолчанию"
        )

    if new_name.lower() in default_categories:
        raise HTTPException(
            status_code=403,
            detail="Невозможно переименовать эту категорию, так как новое имя является категорией по умолчанию"
        )

    category = await get_category(category_name, user_id)

    dir_path = os.path.dirname(category.path)

    new_category_path = os.path.join(dir_path, new_name)

    files = await get_files_from_category(category_name, user_id)
    for file_dict in files:
        file_id = file_dict['file_id']
        file = await get_file(file_id, user_id)

        new_file_path = os.path.join(new_category_path, file.name)

        await file.update({"$set": {"path": new_file_path}})
        await file.update({"$set": {"category_name": new_name}})

    history_dict = {
        "category_id": str(category.id),
        "category_name": category_name,
        "title": "Переименование категории",
        "description": f"Категория {category_name} была переименована на {new_name}",
        "time": datetime.now().strftime("%H:%M:%S")
    }

    os.rename(category.path, new_category_path)
    await category.update({"$set": {"path": new_category_path}})
    await category.update({"$set": {"name": new_name}})
    await category.update({"$set": {"name_for_search": new_name.lower()}})

    await set_history_today(history_dict, user_id)

    return {"new_name": new_name}


async def delete_category(category_name: str, user_id: str):
    default_categories = ("default_category", "images", "documents", "music", "videos")

    if category_name.lower() in default_categories:
        raise HTTPException(
            status_code=403,
            detail="Невозможно удалить эту категорию, так как она установлена по умолчанию"
        )
    
    category = await get_category(category_name.lower(), user_id)

    files = await get_files_from_category(category_name, user_id)
    for file_dict in files:
        file_id = file_dict['file_id']
        file = await get_file(file_id, user_id)
        await file.delete()

    history_dict = {
        "category_id": str(category.id),
        "category_name": category_name,
        "title": "Удаление категории",
        "description": f"Категория {category_name} была удалена",
        "time": datetime.now().strftime("%H:%M:%S")
    }

    shutil.rmtree(category.path)
    await category.delete()

    await set_history_today(history_dict, user_id)

    return {"status": "succes"}


async def change_size_category(category_name: str, action: str, size: int, user_id: str):
    category = await get_category(category_name, user_id)

    if action == "upload":
        await category.update({"$inc": {"size": size}})

    elif action == "delete":
        await category.update({"$inc": {"size": -size}})

    return {"status": "succes"}
