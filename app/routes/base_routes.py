from fastapi import FastAPI
from app.controllers.data_colector_controller import data_collector_router

app = FastAPI()
api_prefix = "/api/v1"
app.include_router(data_collector_router, prefix=api_prefix, tags=["data_collector"])
