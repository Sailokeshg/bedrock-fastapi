from fastapi import HTTPException
from typing import Optional


class BedrockAPIException(HTTPException):
    def __init__(self, detail: str, status_code: int = 500):
        super().__init__(status_code=status_code, detail=detail)


class InvalidInputException(HTTPException):
    def __init__(self, detail: str = "Invalid input provided"):
        super().__init__(status_code=400, detail=detail)


class ExternalServiceException(HTTPException):
    def __init__(self, service: str, detail: Optional[str] = None):
        message = f"External service '{service}' is unavailable"
        if detail:
            message += f": {detail}"
        super().__init__(status_code=503, detail=message)
