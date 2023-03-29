from fastapi import HTTPException, UploadFile
from datetime import datetime
import urllib
import os

from starlette.responses import StreamingResponse
from beanie import PydanticObjectId

from models.file import File


async def get_file(file_id: str, user_id: str):
    file = await File.get(PydanticObjectId(file_id))

    if not file:
        raise HTTPException(status_code=404, detail="Файл не найден")

    if file.user_id != user_id:
        raise HTTPException(status_code=403, detail="Отказано в доступе")

    return file


async def upload_file(file: UploadFile, user_id: str):
    file_path = os.path.join("file_storage", file.filename)
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())

    new_file = File(
        user_id=user_id,
        name=file.filename,
        content_type=file.content_type,
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

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Файл не найден")

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

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Файл не найден")

    dir_path = os.path.dirname(file_path)
    ext = os.path.splitext(file_path)[1]
    new_file_path = os.path.join(dir_path, new_name + ext)

    os.rename(file_path, new_file_path)
    file.name = new_name + ext
    file.path = f"file_storage\{file.name}"
    await file.save()
    return {"new_name": file.name}


async def delete_file(file_id: str, user_id: str):
    file = await get_file(file_id, user_id)
    file_path = file.path

    if file.metadata["is_deleted"] == False:
        raise HTTPException(status_code=403, detail="Файл должен находиться в корзине")


    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Файл не найден")

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
