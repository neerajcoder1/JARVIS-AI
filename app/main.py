from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api.routes import router
from app.core.logger import logger
from app.core.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"{settings.JARVIS_NAME} API started")
    yield

app = FastAPI(title=settings.JARVIS_NAME, lifespan=lifespan)

from fastapi.staticfiles import StaticFiles

app.include_router(router)

import os
static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "ui")
if not os.path.exists(static_dir):
    os.makedirs(static_dir)

app.mount("/", StaticFiles(directory=static_dir, html=True), name="ui")
