from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.tenders.router import router as tenders_router
from backend.bids.router import router as bids_router

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    yield
    
description: str = """
API для управления тендерами и предложениями.\n
Основные функции API включают управление тендерами 
(создание, изменение, получение списка)
и управление предложениями (создание, изменение, получение списка).
"""
app = FastAPI(
    title="Tender Management API",
    version="1.0",
    lifespan=lifespan,
    description=description,
    root_path="/api"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/ping")
async def ping():
    return "ok"


app.include_router(tenders_router)
app.include_router(bids_router)