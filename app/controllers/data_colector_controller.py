import json
from datetime import datetime
from fastapi import APIRouter, Response, Body

from app.services.data_collector_service import collect_data_async_service
from app.models.collect_data import CollectDataRequest
from app.models.person import SearchResultsResponse
from app.models.error import CustomErrorModel
from app.utils.errors.CustomError import CustomError

data_collector_router = APIRouter()


@data_collector_router.post(
    "/collect_data",
    summary="Coletar Dados",
    description="Este endpoint realiza a coleta dados de pessoa física com base nos dados de entrada fornecidos.\n\nRetorna um objeto JSON contendo o status e os resultados da coleta de dados.",
    responses={
        200: {
            "description": "Coleta de dados bem-sucedida",
            "model": SearchResultsResponse,
        },
        404: {
            "description": "Nenhuma pessoa física encontrada com os dados fornecidos",
            "model": CustomErrorModel,
        },
        422: {
            "description": "Erro de validação dos dados",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
                                "loc": ["body", "input_data"],
                                "msg": "field required",
                                "type": "value_error.missing",
                            }
                        ]
                    }
                }
            },
        },
        500: {
            "description": "Erro interno do servidor",
            "model": CustomErrorModel,
        },
    },
)
async def collect_data_endpoint(
    body: CollectDataRequest = Body(
        ...,
        description="Os dados a serem usados para o processo de coleta.\n\n- **input_data**: dado obrigatório. Pode ser um nome, CPF ou NIS.\n- **filter**: filtro opcional para refinar a coleta de dados. Caso True irá filtrar por **Beneficiário de Programa Social**.",
        example={
            "input_data": "12345678909",
            "filter": False,
        },
    )
) -> SearchResultsResponse:
    try:
        results = await collect_data_async_service(body.input_data, body.filter)
        response: SearchResultsResponse = {"status": "sucesso", "resultados": results}
        return Response(content=json.dumps(response), media_type="application/json")
    except CustomError as e:
        print(f"Erro de valor: {e}")
        return Response(
            status_code=e.status_code,
            media_type="application/json",
            content=json.dumps(
                {
                    "erro": e.mensagem,
                    "data_consulta": datetime.now().isoformat(),
                },
            ),
        )
    except Exception as er:
        print(f"Internal server error: {er}")
        return Response(
            status_code=500,
            media_type="application/json",
            content=json.dumps(
                {
                    "erro": "Houve um erro inesperado no servidor.",
                    "data_consulta": datetime.now().isoformat(),
                },
            ),
        )
