# app/bedrock_client.py
import json
import boto3
import os

region = os.getenv("AWS_REGION", "us-east-1")
model_id = os.getenv("BEDROCK_MODEL_ID", "amazon.nova-micro-v1:0")

bedrock = boto3.client("bedrock-runtime", region_name=region)


def query_bedrock(prompt: str) -> str:
    payload = {
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "text": prompt
                    }
                ]
            }
        ],
        "inferenceConfig": {
            "maxTokens": 300,
            "temperature": 0.7,
            "topP": 0.9
        }
    }

    response = bedrock.invoke_model(
        modelId=model_id,
        body=json.dumps(payload),
        contentType="application/json",
        accept="application/json"
    )

    response_body = json.loads(response["body"].read().decode())

    # Extract the response text from the Nova model response format
    if "output" in response_body and "message" in response_body["output"]:
        content = response_body["output"]["message"]["content"]
        if content and len(content) > 0:
            return content[0].get("text", "No output received.")

    return "No output received."
