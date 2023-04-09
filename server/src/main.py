from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from routes import auth_routes, user_routes, file_routes, category_routes, history_routes

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
app.include_router(history_routes.router, tags=['history'], prefix='/api')

db_settings = DbSettings()


@app.on_event("startup")
async def startup():
    await db_settings.initialize_database()


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)


@app.get("/")
def root():
    return {"message": "go to /docs"}
