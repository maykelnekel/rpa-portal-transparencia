from pydantic import BaseModel
from datetime import datetime


class CustomError(BaseModel):
    mensagem: str
    termo_da_busca: str
    data_consulta: datetime
