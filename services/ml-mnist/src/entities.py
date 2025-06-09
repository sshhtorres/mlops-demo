from pydantic import BaseModel


class PredictRequest(BaseModel):
    instances: list[str] | None = None


class PredictResponse(BaseModel):
    model_id: str
    predictions: list[int]
