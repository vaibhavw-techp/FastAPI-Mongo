from fastapi import FastAPI
from router.channel_router import router

app = FastAPI()

app.include_router(router)