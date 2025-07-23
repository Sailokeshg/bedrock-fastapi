from pydantic_settings import BaseSettings
from typing import Optional, List


class Settings(BaseSettings):
    # AWS Configuration
    aws_region: str = "us-east-1"
    bedrock_model_id: str = "amazon.nova-micro-v1:0"
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None
    
    # API Configuration
    api_title: str = "Bedrock Travel Recommendation API"
    api_version: str = "1.0.0"
    api_description: str = "FastAPI backend powered by AWS Bedrock for travel recommendations"
    
    # CORS Configuration
    allowed_origins: List[str] = ["*"]
    
    # Bedrock Configuration
    max_tokens: int = 300
    temperature: float = 0.7
    top_p: float = 0.9
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()