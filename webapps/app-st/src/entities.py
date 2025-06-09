from pydantic import BaseModel


class MLServiceConfig(BaseModel):
    id: str
    request_body_samples: list[str] = []
    service_url: str | None = None


class AppConfig(BaseModel):
    mlservices: dict[str, MLServiceConfig]
