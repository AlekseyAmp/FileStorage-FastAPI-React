from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from routes import auth_routes, user_routes, file_routes, category_routes

from config.database import DbSettings


app = FastAPI()

dbSettings = DbSettings()


origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes.router, tags=['auth'], prefix='/api')
app.include_router(user_routes.router, tags=['user'], prefix='/api')
app.include_router(file_routes.router, tags=['file'], prefix='/api')
app.include_router(category_routes.router, tags=['category'], prefix='/api')

db_settings = DbSettings()


@app.on_event("startup")
async def startup():
    await db_settings.initialize_database()


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)


@app.get("/")
def root():
    return {"message": "go to /api"}


@app.get("/api")
def api_commands():
    return {
        "message": "Welcome to FastAPI with MongoDB",
        "all query": "/docs (without /api)",
        "register": "api/register",
        "login": "api/login",
        "refresh token": "api/refresh",
        "logout": "api/logout",
        "me": "api/me",
        "upload file": "api/uploadfile",
        "download file": "api/download_file/file_id",
        "rename file": "api/rename_file/file_id",
        "delete file": "api/delete_file/file_id",
        "in_basket_file": "api/in_basket_file/file_id",
        "in_favorite_file": "api/in_favorite_file/file_id",
        "documents": "api/category/documents",
        "images": "api/category/images",
        "music": "api/category/music",
        "videos": "api/category/videos",
    }
