"""
# Bedrock Travel Recommendation API

This is a FastAPI backend powered by AWS Bedrock that returns travel recommendations based on a user's prompt.

## Setup
1. Clone this repo
2. Create a `.env` file with your AWS credentials:

```bash
AWS_REGION=us-east-1
BEDROCK_MODEL_ID=anthropic.claude-3-sonnet-20240229-v1:0
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the app:
```bash
uvicorn app.main:app --reload
```

## Endpoint
POST `/recommendations`

**Payload:**
```json
{
  "user_input": "What are the best places to visit in Upstate New York during July and August for a family with teenagers?"
}

**Response:**
```json
{
  "response": "List of places..."
}
```
"""
