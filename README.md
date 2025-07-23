# Bedrock Travel Recommendation API

A production-ready FastAPI backend powered by AWS Bedrock for generating AI-driven travel recommendations.

## Features

- **Production-ready architecture** with proper error handling and logging
- **AWS Bedrock integration** for AI-powered travel recommendations
- **Input validation** with Pydantic models
- **Comprehensive error handling** with custom exceptions
- **Health check endpoint** for monitoring
- **CORS support** for cross-origin requests
- **Structured logging** for better debugging
- **Environment-based configuration** for different deployment environments

## Project Structure

```
subscribe_be/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application and endpoints
│   ├── config.py              # Application settings and configuration
│   ├── exceptions.py          # Custom exception classes
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py         # Pydantic models for request/response
│   └── services/
│       ├── __init__.py
│       └── bedrock_client.py  # AWS Bedrock service client
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variables template
└── README.md                 # Project documentation
```

## Setup

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd subscribe_be
   ```

2. **Create virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**

   ```bash
   cp .env.example .env
   # Edit .env with your AWS credentials and settings
   ```

5. **Set up AWS credentials**
   - Option 1: Add to `.env` file
   - Option 2: Use AWS CLI `aws configure`
   - Option 3: Use IAM roles (recommended for production)

## Environment Variables

Create a `.env` file with the following variables:

```env
# AWS Configuration
AWS_REGION=us-east-1
BEDROCK_MODEL_ID=amazon.nova-micro-v1:0
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here

# API Configuration
API_TITLE=Bedrock Travel Recommendation API
API_VERSION=1.0.0
ALLOWED_ORIGINS=["http://localhost:3000","https://yourdomain.com"]

# Bedrock Configuration
MAX_TOKENS=300
TEMPERATURE=0.7
TOP_P=0.9
```

## Running the Application

### Development

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## API Endpoints

### Health Check

```
GET /health
```

Returns the API health status and version.

### Root

```
GET /
```

Returns API information and available endpoints.

### Travel Recommendations

```
POST /recommendations
```

**Request Body:**

```json
{
  "user_input": "What are the best places to visit in Upstate New York during July and August for a family with teenagers?"
}
```

**Response:**

```json
{
  "response": "Here are some great travel recommendations...",
  "model_id": "amazon.nova-micro-v1:0",
  "timestamp": "2025-07-23T10:30:00Z",
  "tokens_used": 245
}
```

## API Documentation

Once the server is running, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Error Handling

The API includes comprehensive error handling for:

- **Bedrock API errors** (500, 429, 400)
- **External service unavailability** (503)
- **Input validation errors** (400)
- **Authentication failures** (503)

## Production Deployment

### Docker (Recommended)

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app/ ./app/
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Environment Variables for Production

- Use AWS IAM roles instead of access keys
- Set `ALLOWED_ORIGINS` to your actual domain
- Configure proper logging levels
- Use a reverse proxy (nginx) for SSL termination

## Monitoring

- Health check endpoint: `/health`
- Structured logging with timestamps
- Error tracking with custom exception types
- Token usage monitoring for cost optimization

## Security

- CORS configuration for cross-origin requests
- Input validation with Pydantic
- Trusted host middleware
- Environment-based configuration
- No hardcoded secrets

## Contributing

1. Follow the existing code structure
2. Add proper type hints
3. Include error handling for new features
4. Update documentation for new endpoints
5. Add validation for new input models
