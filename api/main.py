import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from config import config as conf
from .auth.router import router as authRouter
from .content.router import router as contentRouter
from .news.router import router as newsRouter

app = FastAPI(
    title="Polina's Military Registration",
    description="API for Military Registration",
    version="2.2.8",
)

if not os.path.exists(conf.media_root):
    os.makedirs(conf.media_root)
    print(f"Папка {conf.media_root} успешно создана.")
app.mount("/media", StaticFiles(directory=conf.media_root), name="media")

app.include_router(authRouter, tags=["Auth"])
app.include_router(contentRouter, tags=["Content"])
app.include_router(newsRouter, tags=["News"])
