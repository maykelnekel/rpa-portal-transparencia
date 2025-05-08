from fastapi import FastAPI
from app.controllers.data_colector_controller import data_collector_router

app = FastAPI(
    title="RPA Portal da Transparência",
    description="Um RPA que automatiza a coleta de dados de pessoa física do [Portal da Transparência](https://portaldatransparencia.gov.br/pessoa/visao-geral).\n\n[Repositório no GitHub](https://github.com/maykelnekel/rpa-portal-transparencia)",
    contact={
        "name": "Maykel Nekel",
        "url": "https://github.com/maykelnekel",
        "email": "maykelnekel@gmail.com",
    },
    url="",
    version="1.0.0",
)
api_prefix = "/api/v1"
app.include_router(data_collector_router, prefix=api_prefix, tags=["Coleta de Dados"])
