from fastapi import FastAPI, HTTPException, Request, UploadFile, APIRouter, Depends
from config.database import GridFSSettings
from auth.oauth2 import AuthJWT
from fastapi.responses import StreamingResponse
from bson.objectid import ObjectId
from auth.auth_routes import get_user_id


app = FastAPI()

router = APIRouter()

grid_fs = GridFSSettings()


@router.post("/uploadfile")
async def upload_file(file: UploadFile, user_id: get_user_id = Depends()):
    file_id = grid_fs.file.put(
            file.file,
            filename=file.filename,
            content_type=file.content_type,
            metadata={
                "user_id": user_id,
                "is_deleted": False,
                "is_favorite": False,
            }
        )
    return {"file_id": str(file_id)}


@router.get("/downloadfile/{file_id}")
async def download_file(file_id: str, user_id: get_user_id = Depends()):
    file_obj = grid_fs.file.find_one({"_id": ObjectId(file_id), "metadata.user_id": user_id})
    if file_obj is None:
        raise HTTPException(status_code=404, detail="Файл не найден")

    file_stream = grid_fs.file.get(file_obj._id)
    headers = {
        "Content-Disposition": f"attachment; filename={file_obj.filename}",
        "Content-Type": file_obj.content_type,
    }

    return StreamingResponse(file_stream, headers=headers)
