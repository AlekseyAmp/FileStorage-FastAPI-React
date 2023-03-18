from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config.settings import settings
from config.database import DbSettings

dbSettings = DbSettings()

from auth import routes

app = FastAPI()



origins = [
    settings.CLIENT_ORIGIN,
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def init_db():
    await dbSettings.initialize_database()
    # await startMinio()


app.include_router(routes.router, tags=['Auth'], prefix='/api')


@app.get("/api")
def root():
    return {"message": "Welcome to FastAPI with MongoDB"}
