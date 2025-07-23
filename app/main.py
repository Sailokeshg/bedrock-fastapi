from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from app.bedrock_client import query_bedrock

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Prompt(BaseModel):
    user_input: str


@app.get("/")
def root():
    return {"message": "Welcome to the Bedrock AI Travel Recommendation API!"}


@app.post("/recommendations")
def get_recommendations(prompt: Prompt):
    response = query_bedrock(prompt.user_input)
    return {"response": response}
