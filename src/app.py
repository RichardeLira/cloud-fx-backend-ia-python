from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.modules.receive_docs.receive_docs_controller import ReceiveDocsController
from dotenv import load_dotenv
import redis.asyncio as redis
from os import getenv

# Load environment variables from .env file
load_dotenv()
# Config redis for saving async data
redis_client = redis.from_url(hos=getenv("REDIS_HOST"), 
                              port=getenv(int(getenv("REDIS_PORT"))), 
                              decode_responses=True)
app = FastAPI()

receive_docs_controller = ReceiveDocsController()
app.include_router(receive_docs_controller.router, prefix="/file")

origins = [
    "http://localhost:8000",
]
app.add_middleware(
  CORSMiddleware, 
  allow_origins=origins, 
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)