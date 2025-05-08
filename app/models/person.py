from pydantic import BaseModel
from datetime import datetime


class PersonDetails(BaseModel):
    mes_folha: str
    mes_referencia: str
    uf: str
    municipio: str
    quantidade_de_dependentes: str
    valor: str


class Person(BaseModel):
    nome_do_beneficio: str
    valor: str
    detalhes: list[PersonDetails]


class SearchResults(BaseModel):
    termo_da_busca: str
    data_consulta: datetime
    beneficios: list[Person]
    screenshot_base64: str


class SearchResultsResponse(BaseModel):
    status: str
    resultados: SearchResults
