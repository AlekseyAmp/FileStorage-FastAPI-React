from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from auth import auth_routes

from api.users import user_routes
from api.files import file_routes
from api.categories import category_routes

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


@app.on_event("startup")
async def init_db():
    await dbSettings.initialize_database()


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)


@app.get("/")
def root():
    return {"message": "go to /api"}

@app.get("/api")
def api_root():
    return {
        "message": "Welcome to FastAPI with MongoDB",
        "all query": "/docs (without /api)",
        "register": "api/register",
        "login": "api/login",
        "logout": "api/logout",
        "me": "api/me",
        "upload file": "api/uploadfile",
        "upload folders": "api/uploadfolder",
    }
