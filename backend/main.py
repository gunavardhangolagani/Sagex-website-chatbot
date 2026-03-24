# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from routes.chatbot_route import router 
from utils.updater import check_for_website_updates 
import asyncio

async def polling_task():
    while True:
        check_for_website_updates()
        await asyncio.sleep(900) # Wait 15 minutes before checking again

@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(polling_task())
    yield
    task.cancel()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)