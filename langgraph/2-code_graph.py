from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel
import os
load_dotenv()

client = OpenAI(
    api_key=os.getenv("ANTHROPIC_API_KEY"),
    base_url="https://api.anthropic.com/v1/"
)

gemini_client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

class ClassifyMessageResponse(BaseModel):
    is_coding: bool

class State(TypedDict):
    query: str
    result: str | None
    accuracy: str | None
    is_coding: bool | None

def classify_message(state: State):
    query = state["query"]

    SYSTEM_PROMPT = """
    You are a helpful assistant that classifies messages into different categories. 
    Your job is to classify whether the query is a coding question or related to coding or not.
    Return response in specified JSON boolean only
    The message to classify is: 
    """
    llm_response = client.beta.chat.completions.create(
        model="claude-sonnet-4-0",
        response_format=ClassifyMessageResponse,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": query}
        ],
    )