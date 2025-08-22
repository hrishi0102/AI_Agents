from mem0 import Memory
from dotenv import load_dotenv
import os
import json
from openai import OpenAI
from google import genai

load_dotenv()

client = OpenAI(
    api_key=os.getenv("ANTHROPIC_API_KEY"),
    base_url="https://api.anthropic.com/v1/"
)


GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Mem0 opensource config
config = {
    "version": "v1.1",
    "embedder": {
        "provider": "gemini",
        "config": {
            "api_key": GOOGLE_API_KEY,
            "model": "models/text-embedding-004"
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
            "collection_name": "mem0",
            "host": "localhost",
            "port": 6333,
            "embedding_model_dims": 768
        }
    }
}

# Initialize Mem0 client
mem_client = Memory.from_config(config)

def chat():
    while True:
        user_input = input("You: ")

        # Get relevant memories
        relevant_memories = mem_client.search(query=user_input, user_id="hrishikesh")
        # Format memories for context
        memories = [f"ID: {mem.get('id')} Memory: {mem.get('memory')}" for mem in relevant_memories.get("results")]

        SYSTEM_PROMPT = f"You are a MEMORY AWARE helpful AI assistant. Here are some relevant memories for a specific user: {json.dumps(memories)}"

        response = client.chat.completions.create(
            model="claude-sonnet-4-20250514",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_input}
            ]
        )
        print("AI: ", response.choices[0].message.content)

        # Add conversation to memory using Mem0
        mem_client.add([
            {"role": "user", "content": user_input},
            {"role": "assistant", "content": response.choices[0].message.content}
        ],
        user_id="hrishikesh")

chat()