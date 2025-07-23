import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.models.schemas import (
    TravelPromptRequest,
    TravelRecommendationResponse,
    HealthCheckResponse
)
from app.services.bedrock_client import bedrock_service
from app.exceptions import BedrockAPIException, InvalidInputException, ExternalServiceException

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    logger.info("Starting Bedrock Travel Recommendation API")
    yield
    logger.info("Shutting down Bedrock Travel Recommendation API")


app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
    description=settings.api_description,
    lifespan=lifespan
)

# Security middleware
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


# Exception handlers
@app.exception_handler(BedrockAPIException)
async def bedrock_exception_handler(request, exc: BedrockAPIException):
    logger.error(f"Bedrock API error: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "type": "bedrock_error"}
    )


@app.exception_handler(ExternalServiceException)
async def external_service_exception_handler(request, exc: ExternalServiceException):
    logger.error(f"External service error: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "type": "service_unavailable"}
    )


@app.exception_handler(InvalidInputException)
async def invalid_input_exception_handler(request, exc: InvalidInputException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "type": "validation_error"}
    )


# Health check endpoint
@app.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """Health check endpoint for monitoring."""
    return HealthCheckResponse(version=settings.api_version)


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": f"Welcome to the {settings.api_title}!",
        "version": settings.api_version,
        "docs_url": "/docs",
        "health_check": "/health"
    }


# Main recommendations endpoint
@app.post("/recommendations", response_model=TravelRecommendationResponse)
async def get_travel_recommendations(request: TravelPromptRequest):
    """
    Get AI-powered travel recommendations based on user input.

    - user_input: Your travel query (10-1000 characters)

    Returns detailed travel recommendations tailored to your request.
    """
    try:
        logger.info(
            f"Processing travel recommendation request: {request.user_input[:100]}...")

        response_text, tokens_used = bedrock_service.get_travel_recommendations(
            request.user_input
        )

        logger.info("Successfully generated travel recommendations")

        return TravelRecommendationResponse(
            response=response_text,
            model_id=settings.bedrock_model_id,
            tokens_used=tokens_used
        )

    except (BedrockAPIException, ExternalServiceException, InvalidInputException):
        # These exceptions are handled by the exception handlers
        raise
    except Exception as e:
        logger.error(f"Unexpected error in recommendations endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while processing your request"
        )