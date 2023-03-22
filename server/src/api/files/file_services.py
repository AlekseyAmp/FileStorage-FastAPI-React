from fastapi import HTTPException, UploadFile
from fastapi.responses import StreamingResponse

from beanie import PydanticObjectId
import urllib

from config.database import GridFSSettings


grid_fs = GridFSSettings()


async def upload_file(file: UploadFile, user_id: str):
    file_id = grid_fs.file.put(
        file.file,
        filename=file.filename.split('.')[0],
        fileformat=file.filename.split('.')[1],
        content_type=file.content_type,
        metadata={
            "user_id": user_id,
            "is_favorite": False,
            "is_deleted": False,
        }
    )
    return {"succes": PydanticObjectId(file_id)}


async def download_file(file_id: str, user_id: str):
    file_obj = grid_fs.file.find_one({"_id": PydanticObjectId(file_id), "metadata.user_id": user_id})

    if file_obj is None:
        raise HTTPException(status_code=404, detail="Файл не найден")

    file_stream = grid_fs.file.get(file_obj._id)
    filename = urllib.parse.quote(file_obj.filename)
    headers = {
        "Content-Disposition": f"attachment; filename*=UTF-8''{filename}",
        "Content-Type": file_obj.content_type,
    }
    return StreamingResponse(file_stream, headers=headers)


async def get_all_files(user_id: str):
    files = list()

    for file_obj in grid_fs.file.find({"metadata.user_id": user_id}):
        file = {
            "file_id": str(file_obj._id),
            "filename": file_obj.filename,
            "fileformat": file_obj.fileformat,
            "size": file_obj.length,
            "content_type": file_obj.content_type,
            "is_favorite": file_obj.metadata["is_favorite"],
            "is_deleted": file_obj.metadata["is_deleted"],
            "upload_date": file_obj.upload_date,
        }
        files.append(file)
    return {"files": files}
