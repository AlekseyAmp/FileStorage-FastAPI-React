from fastapi import HTTPException, UploadFile
from beanie import PydanticObjectId
from datetime import datetime
import urllib
import os

from starlette.responses import StreamingResponse

from models.file import File
from models.user import User
from services.history_services import set_history_today
from services.statistic_services import set_statistic_today
from services.category_services import create_new_category, change_size_category
from utils.file_utils import get_file
from utils.category_utils import set_file_category


async def get_all_files_info(user_id: str):
    files_info_dict = {
        "total_count": 0,
        "total_size": 0
    }

    async for file in File.find({
        "user_id": user_id,
    }):
        files_info_dict["total_count"] += 1
        files_info_dict["total_size"] += file.size

    return files_info_dict


async def get_files_info_by_category(category_name: str, user_id: str):
    files_info_dict = {
        "total_count": 0,
        "total_size": 0
    }

    async for file in File.find({
        "user_id": user_id,
        "category_name": category_name,
        "metadata.is_basket": False,
        "metadata.is_favorite": False
    }):
        files_info_dict["total_count"] += 1
        files_info_dict["total_size"] += file.size

    return files_info_dict


async def create_new_file(file: UploadFile, category_name: str, user_id: str):
    user = await User.get(PydanticObjectId(user_id))

    if user.metadata["storage_used"] >= user.metadata["max_storage"]:
        raise HTTPException(
            status_code=403,
            detail="Место на диске переполнено"
        )

    category_name = category_name.lower()

    """
    Default categories(images, documents, music, videos) are abstract,
    All files associated with them are in the DEFAULT_CATEGORY folder
    """

    default_categories = ("images", "documents", "music", "videos")

    if category_name in default_categories:
        raise HTTPException(
            status_code=403,
            detail="Используйте DEFAULT_CATEGORY, чтобы загрузить файл в категорию по умолчанию"
        )

    directory = os.path.join("STORAGE", user_id, category_name)
    category_path = os.path.join(directory)

    if category_name == "default_category":
        if not os.path.isdir(category_path):
            await create_new_category(category_name, user_id)
        await change_size_category(category_name, "upload", file.size, user_id)
        category_name = set_file_category(file.filename.split('.')[1])

    if not os.path.isdir(category_path):
        raise HTTPException(
            status_code=404,
            detail="Такой категории не существует"
        )

    file_name = file.filename
    file_path = os.path.join(directory, file_name)

    if os.path.isfile(file_path):
        file_name, ext = os.path.splitext(file_name)
        suffix = 1
        while os.path.isfile(os.path.join(directory, f"{file_name} ({suffix}){ext}")):
            suffix += 1
        file_name = f"{file_name} ({suffix}){ext}"
        file_path = os.path.join(directory, file_name)

    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())

    new_file = File(
        user_id=user_id,
        name=file_name,
        content_type=set_file_category(file_name.split('.')[1]),
        category_name=category_name,
        path=file_path,
        size=file.size,
        metadata={
            "is_favorite": False,
            "is_basket": False,
            "date_created": datetime.now().strftime("%d-%m-%Y"),
            "time_created": datetime.now().strftime("%H:%M:%S")
        }
    )
    await new_file.insert()

    await user.update({"$inc":
                      {f"metadata.storage_used": file.size}})

    """
    Block code 99-100

    There is no need to set the default category sizes,
    they are set by the function (get_files_info_by_category in info_services.py),
    but the categories that the user creates must be changed using the function
    (change_size_category)
    """
    if category_name not in default_categories:
        await change_size_category(category_name, "upload", file.size, user_id)

    history_dict = {
        "file_id": str(new_file.id),
        "file_name": new_file.name,
        "file_content_type": new_file.content_type,
        "file_category_name": new_file.category_name,
        "title": "Загрузка файла",
        "description": f"Файл {new_file.name} загружен на диск",
        "time": datetime.now().strftime("%H:%M:%S")
    }
    await set_history_today(history_dict, user_id)

    await set_statistic_today("upload", user_id)
    return {"file_id": new_file.id}


async def download_file(file_id: str, user_id: str):
    file = await get_file(file_id, user_id)

    file_name = urllib.parse.quote(file.name)

    history_dict = {
        "file_id": str(file_id),
        "file_name": file.name,
        "file_content_type": file.content_type,
        "file_category_name": file.category_name,
        "title": "Скачивание файла",
        "description": f"Файл {file.name} скачан с диска",
        "time": datetime.now().strftime("%H:%M:%S")
    }
    await set_history_today(history_dict, user_id)

    await set_statistic_today("download", user_id)

    return StreamingResponse(
        open(file.path, "rb"),
        media_type="application/octet-stream",
        headers={
            "Content-Disposition": f"attachment; filename*=UTF-8''{file_name}",
            "Content-Type": file.content_type,
        }
    )


async def rename_file(file_id: str, new_name: str, user_id: str):
    file = await get_file(file_id, user_id)

    dir_path = os.path.dirname(file.path)
    ext = os.path.splitext(file.path)[1]
    new_file_path = os.path.join(dir_path, new_name + ext)

    history_dict = {
        "file_id": str(file_id),
        "file_name": new_name,
        "file_content_type": file.content_type,
        "file_category_name": file.category_name,
        "title": "Переименование файла",
        "description": f"Файл {file.name} была переименован на {new_name}",
        "time": datetime.now().strftime("%H:%M:%S")
    }

    os.rename(file.path, new_file_path)
    await file.update({"$set": {"path": new_file_path}})
    await file.update({"$set": {"name": new_name + ext}})

    await set_history_today(history_dict, user_id)

    return {"new_name": new_name}


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

    default_categories = ("images", "documents", "music", "videos")

    category_name = file.category_name

    if category_name in default_categories:
        category_name = "default_category"

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

    await change_size_category(category_name, "delete", file.size, user_id)

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

    default_categories = ("images", "documents", "music", "videos")

    category_name = file.category_name

    if category_name in default_categories:
        category_name = "default_category"

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

    await change_size_category(category_name, "delete", file.size, user_id)

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

    default_categories = ("images", "documents", "music", "videos")

    category_name = file.category_name

    if category_name in default_categories:
        category_name = "default_category"

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

    await change_size_category(category_name, "upload", file.size, user_id)

    return {"status": "succes"}


async def delete_file(file_id: str, user_id: str):
    user = await User.get(PydanticObjectId(user_id))

    default_categories = ("images", "documents", "music", "videos")

    file = await get_file(file_id, user_id)

    category_name = file.category_name

    if category_name in default_categories:
        category_name = "default_category"

    if not file.metadata["is_basket"]:
        raise HTTPException(
            status_code=403,
            detail="Файл должен находиться в корзине"
        )

    history_dict = {
        "file_id": str(file_id),
        "file_name": file.name,
        "file_content_type": file.content_type,
        "file_category_name": file.category_name,
        "title": "Удаление файла",
        "description": f"Файл {file.name} был удалён с диска",
        "time": datetime.now().strftime("%H:%M:%S")
    }

    os.remove(file.path)
    await file.delete()

    await user.update({"$inc":
                      {f"metadata.storage_used": -file.size}})

    await change_size_category(category_name, "delete", file.size, user_id)

    await set_history_today(history_dict, user_id)

    await set_statistic_today("deleted", user_id)

    return {"status": "succes"}
