from mem0 import Memory

config = {
    "version": "v1.1",
    "embedder": {
        "provider": "gemini",
        "config": {
            "model": "models/text-embedding-004",
        }
    }
}

mem_client = Memory.from_config(config)