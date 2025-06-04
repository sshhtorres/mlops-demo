from pydantic import BaseModel


class PredictRequestConfig(BaseModel):
    delimeter: str = ','
    csv_file_uri: str


class PredictRequest(BaseModel):
    config: PredictRequestConfig | None = None
    instances: list[list[float]] | None = None


class PredictResponseMetadata(BaseModel):
    categories: list[str]


class PredictResponse(BaseModel):
    model_id: str
    metadata: PredictResponseMetadata
    predictions: list[int]
