from pydantic import BaseModel

class HealthCheckResponse(BaseModel):
    message: str = "healthy"

class ErrorDetail(BaseModel):
    code: str = "SERVICE_UNAVAILABLE"
    message: str = "Service is unhealthy"

class HealthCheckFailResponse(BaseModel):
    message: str = "unhealthy"
    errors: list[ErrorDetail]