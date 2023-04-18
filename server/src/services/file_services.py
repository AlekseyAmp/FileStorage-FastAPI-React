from fastapi import HTTPException, UploadFile
from beanie import PydanticObjectId
from datetime import datetime
import urllib
import os

from starlette.responses import StreamingResponse

from models.file import File
from models.history import FileHistory
from services.history_services import set_history_today
from services.statistic_services import set_statistic_today
from utils.file_utils import set_file_category


async def get_file(file_id: str, user_id: str):
    file = await File.get(PydanticObjectId(file_id))

    if not file:
        raise HTTPException(
            status_code=404,
            detail="Файл не найден"
        )

    if file.user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="Отказано в доступе"
        )

    return file


async def create_new_file(file: UploadFile, user_id: str):
    directory = os.path.join("file_storage", user_id)
    if not os.path.exists(directory):
        os.makedirs(directory)

    file_name = file.filename
    file_path = os.path.join(directory, file_name)

    if os.path.isfile(file_path):
        file_name, file_extension = os.path.splitext(file_name)
        suffix = 1
        while os.path.isfile(os.path.join(directory, f"{file_name} ({suffix}){file_extension}")):
            suffix += 1
        file_name = f"{file_name} ({suffix}){file_extension}"
        file_path = os.path.join(directory, file_name)

    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())

    new_file = File(
        user_id=user_id,
        name=file_name,
        content_type=set_file_category(file_name.split('.')[1]),
        path=file_path,
        size=file.size,
        metadata={
            "is_favorite": False,
            "is_deleted": False,
            "date_created": datetime.now().strftime("%d-%m-%Y"),
            "time_created": datetime.now().strftime("%H:%M:%S")
        }
    )
    await new_file.insert()

    history_dict = {
        "file_id": str(new_file.id),
        "file_name": new_file.name,
        "file_contentType": new_file.content_type,
        "title": "Загрузка файла",
        "description": f"Файл {new_file.name} загружен на диск",
        "time": datetime.now().strftime("%H:%M:%S")
    }
    await set_history_today(FileHistory, history_dict, user_id)

    await set_statistic_today("upload", user_id)

    return {"file_id": new_file.id}


async def download_file(file_id: str, user_id: str):
    file = await get_file(file_id, user_id)

    file_path = file.path
    filename = urllib.parse.quote(file.name)

    history_dict = {
        "file_id": str(file_id),
        "title": "Скачивание файла",
        "file_name": file.name,
        "file_contentType": file.content_type,
        "description": f"Файл {file.name} скачан с диска",
        "time": datetime.now().strftime("%H:%M:%S")
    }
    await set_history_today(FileHistory, history_dict, user_id)

    await set_statistic_today("download", user_id)

    return StreamingResponse(
        open(file_path, "rb"),
        media_type="application/octet-stream",
        headers={
            "Content-Disposition": f"attachment; filename*=UTF-8''{filename}",
            "Content-Type": file.content_type,
        }
    )


async def rename_file(file_id: str, new_name: str, user_id: str):
    file = await get_file(file_id, user_id)

    file_path = file.path
    dir_path = os.path.dirname(file_path)
    ext = os.path.splitext(file_path)[1]
    new_file_path = os.path.join(dir_path, new_name + ext)

    os.rename(file_path, new_file_path)
    file.name = new_name + ext
    file.path = f"file_storage/{user_id}/{file.name}"

    history_dict = {
        "file_id": str(file_id),
        "file_name": file.name,
        "file_contentType": file.content_type,
        "title": "Переименование файла",
        "description": f"Файл {file.name} переиенован на {new_name}",
        "time": datetime.now().strftime("%H:%M:%S")
    }
    await set_history_today(FileHistory, history_dict, user_id)

    await file.save()

    return {"new_name": file.name}


async def delete_file(file_id: str, user_id: str):
    file = await get_file(file_id, user_id)

    if not file.metadata["is_deleted"]:
        raise HTTPException(
            status_code=403,
            detail="Файл должен находиться в корзине"
        )

    file_path = file.path
    os.remove(file_path)

    history_dict = {
        "file_id": str(file_id),
        "file_name": file.name,
        "file_contentType": file.content_type,
        "title": "Удаление файла",
        "description": f"Файл {file.name} был удалён с диска",
        "time": datetime.now().strftime("%H:%M:%S")
    }
    await set_history_today(FileHistory, history_dict, user_id)

    await set_statistic_today("deleted", user_id)

    await file.delete()

    return {"status": "succes"}


async def add_to_basket_file(file_id: str, user_id: str):
    file = await get_file(file_id, user_id)

    if file.metadata["is_favorite"]:
        raise HTTPException(
            status_code=403,
            detail="Файл находится в избранном"
        )

    if file.metadata["is_deleted"]:
        raise HTTPException(
            status_code=403,
            detail="Файл уже находится в корзине"
        )

    file.metadata["is_deleted"] = True

    history_dict = {
        "file_id": str(file_id),
        "file_name": file.name,
        "file_contentType": file.content_type,
        "title": "Добавление файла в корзину",
        "description": f"Файл {file.name} был перемещён в корзину",
        "time": datetime.now().strftime("%H:%M:%S")
    }
    await set_history_today(FileHistory, history_dict, user_id)

    await file.save()

    return {"status": "succes"}


async def add_to_favorite_file(file_id: str, user_id: str):
    file = await get_file(file_id, user_id)

    if file.metadata["is_deleted"]:
        raise HTTPException(
            status_code=403,
            detail="Файл находится в корзине"
        )

    if file.metadata["is_favorite"]:
        raise HTTPException(
            status_code=403,
            detail="Файл уже находится в избранном"
        )

    file.metadata["is_favorite"] = True

    history_dict = {
        "file_id": str(file_id),
        "file_name": file.name,
        "file_contentType": file.content_type,
        "title": "Добавление файла в избранное",
        "description": f"Файл {file.name} был перемещён в избранное",
        "time": datetime.now().strftime("%H:%M:%S")
    }
    await set_history_today(FileHistory, history_dict, user_id)

    await file.save()

    return {"status": "succes"}


async def revert_moved_file_back(file_id: str, user_id: str):
    file = await get_file(file_id, user_id)

    file_location = ''

    if file.metadata["is_deleted"]:
        file.metadata["is_deleted"] = False
        file_location = "корзины"

    elif file.metadata["is_favorite"]:
        file.metadata["is_favorite"] = False
        file_location = "избранного"

    elif (not file.metadata["is_favorite"]) \
            and (not file.metadata["is_deleted"]):
        raise HTTPException(
            status_code=403,
            detail="Файл не находится ни в корзине, ни в избранном"
        )

    history_dict = {
        "file_id": str(file_id),
        "file_name": file.name,
        "file_contentType": file.content_type,
        "title": f"Удаление файла из {file_location}",
        "description": f"Файл {file.name} был убран из {file_location}",
        "time": datetime.now().strftime("%H:%M:%S")
    }
    await set_history_today(FileHistory, history_dict, user_id)

    await file.save()

    return {"status": "succes"}


async def get_moved_files(condition: str, user_id: str):
    files = []
    async for file in File.find({
        "user_id": user_id
    }):
        if file.metadata[condition]:
            file_dict = {
                "file_id": str(file.id),
                "name": file.name,
                "size": file.size,
                "content_type": file.content_type,
                "is_favorite": file.metadata["is_favorite"],
                "is_deleted": file.metadata["is_deleted"],
                "date_created": file.metadata["date_created"],
                "time_created": file.metadata["time_created"]
            }
            files.append(file_dict)

    return files[::-1]
