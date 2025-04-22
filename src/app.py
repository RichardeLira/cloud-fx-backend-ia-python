from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.modules.receive_docs.receive_docs_controller import ReceiveDocsController
import redis.asyncio as redis

# Config redis for saving async data
redis_client = redis.from_url(hos="localhost", port=6379, decode_responses=True)
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