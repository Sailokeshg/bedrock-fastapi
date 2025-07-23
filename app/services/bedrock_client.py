import json
import boto3
import logging
from typing import Optional, Dict, Any
from botocore.exceptions import ClientError, NoCredentialsError, BotoCoreError

from app.config import settings
from app.exceptions import BedrockAPIException, ExternalServiceException

logger = logging.getLogger(__name__)


class BedrockService:
    def __init__(self):
        try:
            self.client = boto3.client(
                "bedrock-runtime",
                region_name=settings.aws_region,
                aws_access_key_id=settings.aws_access_key_id,
                aws_secret_access_key=settings.aws_secret_access_key
            )
            logger.info(
                f"Bedrock client initialized for region: {settings.aws_region}")
        except (NoCredentialsError, ClientError) as e:
            logger.error(f"Failed to initialize Bedrock client: {str(e)}")
            raise ExternalServiceException("Bedrock", "Authentication failed")

    def _build_payload(self, prompt: str) -> Dict[str, Any]:
        """Build the payload for Bedrock API request."""
        return {
            "messages": [
                {
                    "role": "user",
                    "content": [{"text": prompt}]
                }
            ],
            "inferenceConfig": {
                "maxTokens": settings.max_tokens,
                "temperature": settings.temperature,
                "topP": settings.top_p
            }
        }

    def _parse_response(self, response_body: Dict[str, Any]) -> tuple[str, Optional[int]]:
        """Parse Bedrock response and extract text content."""
        try:
            if "output" in response_body and "message" in response_body["output"]:
                content = response_body["output"]["message"]["content"]
                if content and len(content) > 0:
                    text = content[0].get("text", "")
                    if text:
                        # Extract token usage if available
                        tokens_used = None
                        if "usage" in response_body:
                            tokens_used = response_body["usage"].get(
                                "outputTokens")
                        return text, tokens_used

            logger.warning("No valid content found in Bedrock response")
            return "No travel recommendations could be generated at this time.", None

        except (KeyError, IndexError, TypeError) as e:
            logger.error(f"Error parsing Bedrock response: {str(e)}")
            raise BedrockAPIException("Failed to parse AI response")

    def get_travel_recommendations(self, prompt: str) -> tuple[str, Optional[int]]:
        """
        Query Bedrock for travel recommendations.

        Args:
            prompt: User's travel query

        Returns:
            Tuple of (recommendation_text, tokens_used)

        Raises:
            BedrockAPIException: If the API call fails
            ExternalServiceException: If Bedrock service is unavailable
        """
        try:
            payload = self._build_payload(prompt)

            logger.info(
                f"Querying Bedrock with model: {settings.bedrock_model_id}")

            response = self.client.invoke_model(
                modelId=settings.bedrock_model_id,
                body=json.dumps(payload),
                contentType="application/json",
                accept="application/json"
            )

            response_body = json.loads(response["body"].read().decode())
            return self._parse_response(response_body)

        except ClientError as e:
            error_code = e.response.get('Error', {}).get('Code', 'Unknown')
            logger.error(f"AWS Bedrock API error [{error_code}]: {str(e)}")

            if error_code in ['ThrottlingException', 'TooManyRequestsException']:
                raise BedrockAPIException(
                    "Service temporarily unavailable. Please try again later.", 429)
            elif error_code == 'ValidationException':
                raise BedrockAPIException("Invalid request parameters", 400)
            else:
                raise ExternalServiceException(
                    "Bedrock", f"API error: {error_code}")

        except BotoCoreError as e:
            logger.error(f"Boto3 error: {str(e)}")
            raise ExternalServiceException("Bedrock", "Connection error")

        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {str(e)}")
            raise BedrockAPIException(
                "Invalid response format from AI service")

        except Exception as e:
            logger.error(f"Unexpected error in Bedrock query: {str(e)}")
            raise BedrockAPIException(
                "An unexpected error occurred while processing your request")


# Global instance
bedrock_service = BedrockService()
