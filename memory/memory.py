from mem0 import Memory
from dotenv import load_dotenv
import os
from openai import OpenAI
from google import genai

load_dotenv()

client = OpenAI(
    api_key=os.getenv("ANTHROPIC_API_KEY"),
    base_url="https://api.anthropic.com/v1/"
)


GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

config = {
    "version": "v1.1",
    "embedder": {
        "provider": "gemini",
        "config": {
            "api_key": GOOGLE_API_KEY,
            "model": "models/text-embedding-004",
        }
    },
    "llm": {
        "provider": "anthropic",
        "config": {
            "api_key": ANTHROPIC_API_KEY,
            "model": "claude-sonnet-4-20250514",
        }
    },
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "host": "localhost",
            "port": 6333
        }
    }
}

mem_client = Memory.from_config(config)

def chat():
    while True:
        user_input = input("You: ")
        response = client.chat.completions.create(
            model="claude-sonnet-4-20250514",
            messages=[
                {"role": "user", "content": user_input}
            ]
        )
        print("AI: ", response.choices[0].message.content)

chat()