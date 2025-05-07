import json
from fastapi import APIRouter, HTTPException, Response
from app.services.data_collector_service import collect_data_async
from app.models.collect_data import CollectDataRequest

data_collector_router = APIRouter()


@data_collector_router.post("/collect_data")
async def collect_data_endpoint(body: CollectDataRequest):
    try:
        results = await collect_data_async(body.input_data, body.filter)
        response = {"status": "success", "results": results}
        return Response(content=json.dumps(response), media_type="application/json")
    except ValueError as e:
        print(f"Erro de valor: {e}")
        raise HTTPException(status_code=400, detail={"error": str(e)})
    except Exception as er:
        print(f"Erro inesperado: {er}")
        raise HTTPException(
            status_code=500, detail={"error": "Erro interno no servidor"}
        )
