from fastapi import HTTPException, UploadFile
from datetime import datetime
import urllib
import os

from starlette.responses import StreamingResponse

from models.file import File
from models.history import FileHistory
from services.history_services import get_history_files_today
from utils.file_utils import set_file_category, get_file


async def files_info(user_id: str):
    files = await File.find().to_list(None)
    
    count = len(files)
    size = sum(file.size for file in files)
    
    return {"count": count, "size": round(size / 1_073_741_824, 3)}


async def upload_file(file: UploadFile, user_id: str):
    directory = os.path.join("file_storage", user_id)
    if not os.path.exists(directory):
        os.makedirs(directory)

    file_path = os.path.join(directory, file.filename)
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())

    new_file = File(
        user_id=user_id,
        name=file.filename,
        content_type=set_file_category(file.filename.split('.')[1]),
        path=file_path,
        size=file.size,
        metadata={
            "created_at": datetime.now(),
            "is_favorite": False,
            "is_deleted": False
        }
    )

    await new_file.insert()
    
    try:
        history = await get_history_files_today(FileHistory, user_id)
    except HTTPException as e:
        if e.status_code == 404:
            new_history = FileHistory(
                    user_id=user_id,
                    history_list_today=[
                        {
                            "file_id": str(new_file.id),
                            "title": "Загрузка файла",
                            "description": f"Файл {file.filename} был успешно загружен на диск"
                        }
                    ]
                )
            await new_history.insert()
        else:
            history_dict = {
                "file_id": str(new_file.id),
                "title": "Загрузка файла",
                "description": f"Файл {new_file.name} успешно загружен на диск"
            }
            history.history_list_today.append(history_dict)
            await history.save()

    return {"file_id": new_file.id}


async def download_file(file_id: str, user_id: str):
    file = await get_file(file_id, user_id)
    file_path = file.path

    filename = urllib.parse.quote(file.name)

    history_dict = {
        "file_id": str(file.id),
        "title": "Скачивание файла",
        "description": f"Файл {file.name} успешно скачан"
    }
    history = await get_history_files_today(FileHistory, user_id)
    history.history_list_today.append(history_dict)
    await history.save()
    
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
        "file_id": str(file.id),
        "title": "Переименование файла",
        "description": f"Файл {file.name} переименован на {new_name}"
    }
    history = await get_history_files_today(FileHistory, user_id)
    history.history_list_today.append(history_dict)
    
    await file.save()
    await history.save()

    return {"new_name": file.name}


async def delete_file(file_id: str, user_id: str):
    file = await get_file(file_id, user_id)
    file_path = file.path

    if file.metadata["is_deleted"] == False:
        raise HTTPException(status_code=403, detail="Файл должен находиться в корзине")
    
    os.remove(file_path)

    history_dict = {
        "file_id": str(file.id),
        "title": "Удаление файла",
        "description": f"Файл {file.name} был удалён"
    }
    history = await get_history_files_today(FileHistory, user_id)
    history.history_list_today.append(history_dict)

    await file.delete()
    await history.save()

    return {"status": "succes"}


async def in_basket_file(file_id: str, user_id: str):
    file = await get_file(file_id, user_id)

    file.metadata["is_deleted"] = True

    history_dict = {
        "file_id": str(file.id),
        "title": "Перемещение файла в корзину",
        "description": f"Файл {file.name} был перемещён в корзину"
    }
    history = await get_history_files_today(FileHistory, user_id)
    history.history_list_today.append(history_dict)

    await file.save()
    await history.save()

    return {"status": "succes"}


async def in_favorite_file(file_id: str, user_id: str):
    file = await get_file(file_id, user_id)

    file.metadata["is_favorite"] = True

    history_dict = {
        "file_id": str(file.id),
        "title": "Перемещние файла в избранное",
        "description": f"Файл {file.name} был перемещён в избранное"
    }
    history = await get_history_files_today(FileHistory, user_id)
    history.history_list_today.append(history_dict)

    await file.save()
    await history.save()

    return {"status": "succes"}


async def get_moved_files(condition: str, user_id: str):
    files = []
    async for file in File.find():
        if file.user_id == user_id and file.metadata[condition] == True:
            files.append(file)
    return files
