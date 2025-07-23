from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime


class TravelPromptRequest(BaseModel):
    user_input: str = Field(
        ...,
        min_length=10,
        max_length=1000,
        description="User's travel recommendation query",
        example="What are the best places to visit in Upstate New York during July and August for a family with teenagers?"
    )

    @validator('user_input')
    def validate_user_input(cls, v):
        if not v.strip():
            raise ValueError('User input cannot be empty')
        return v.strip()


class TravelRecommendationResponse(BaseModel):
    response: str = Field(...,
                          description="AI-generated travel recommendation")
    model_id: str = Field(..., description="Bedrock model used for generation")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    tokens_used: Optional[int] = None


class HealthCheckResponse(BaseModel):
    status: str = "healthy"
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    version: str
