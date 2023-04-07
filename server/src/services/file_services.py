from fastapi import HTTPException, UploadFile
from datetime import datetime
import urllib
import os

from starlette.responses import StreamingResponse
from beanie import PydanticObjectId

from models.file import File
from constants.category_constants import ALLOWED_FORMATS

def get_file_category(fileformat):
    for category in ALLOWED_FORMATS:
        if fileformat in ALLOWED_FORMATS[category]:
            return category
    return 0


async def get_file(file_id: str, user_id: str):
    file = await File.get(PydanticObjectId(file_id))

    if not file:
        raise HTTPException(status_code=404, detail="Файл не найден")

    if file.user_id != user_id:
        raise HTTPException(status_code=403, detail="Отказано в доступе")

    return file


async def get_moved_files(condition: str, user_id: str):
    files = []
    async for file in File.find():
        if file.user_id == user_id and file.metadata[condition] == True:
            file_dict = {
                "file_id": str(file.id),
                "name": file.name,
                "size": file.size,
                "content_type": file.content_type,
                "is_favorite": file.metadata["is_favorite"],
                "is_deleted": file.metadata["is_deleted"],
                "created_at": file.metadata["created_at"],
            }
            files.append(file_dict)
    return files


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
        content_type=get_file_category((file.content_type).split('/')[1]),
        path=file_path,
        size=file.size,
        metadata={
            "created_at": datetime.now(),
            "is_favorite": False,
            "is_deleted": False
        }
    )

    await new_file.insert()

    return {"file_id": new_file.id}


async def download_file(file_id: str, user_id: str):
    file = await get_file(file_id, user_id)
    file_path = file.path

    filename = urllib.parse.quote(file.name)

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
    await file.save()
    return {"new_name": file.name}


async def delete_file(file_id: str, user_id: str):
    file = await get_file(file_id, user_id)
    file_path = file.path

    if file.metadata["is_deleted"] == False:
        raise HTTPException(status_code=403, detail="Файл должен находиться в корзине")

    os.remove(file_path)
    await file.delete()
    return {"status": "succes"}


async def in_basket_file(file_id: str, user_id: str):
    file = await get_file(file_id, user_id)

    file.metadata["is_deleted"] = True
    await file.save()

    return {"status": "succes"}


async def in_favorite_file(file_id: str, user_id: str):
    file = await get_file(file_id, user_id)

    file.metadata["is_favorite"] = True
    await file.save()

    return {"status": "succes"}
