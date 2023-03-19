from fastapi import FastAPI, APIRouter

app = FastAPI()

router = APIRouter()

@router.post("/uploadfolder")
async def upload_folder():
    return "Не реализовано"
