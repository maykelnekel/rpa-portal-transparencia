from pydantic import BaseModel
from datetime import datetime


class Person(BaseModel):
    nome_do_beneficio: str
    valor: float
    detalhes: dict


class SearchResults(BaseModel):
    termo_da_busca: str
    data_consulta: datetime
    beneficios: list[Person]
    screenshot_base64: str
