from pydantic import BaseModel
from datetime import datetime


class CustomErrorModel(BaseModel):
    error: str
    data_consulta: datetime
