from mem0 import Memory
from dotenv import load_dotenv
import os

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

config = {
    "version": "v1.1",
    "embedder": {
        "provider": "gemini",
        "config": {
            "api-key": GOOGLE_API_KEY,
            "model": "models/text-embedding-004",
        }
    },
    "llm": {
        "provider": "anthropic",
        "config": {
            "api-key": ANTHROPIC_API_KEY,
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