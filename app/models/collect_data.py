from pydantic import BaseModel


class CollectDataRequest(BaseModel):
    input_data: str
    filter: bool | None = False
