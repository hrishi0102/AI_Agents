import typer
from typing import Optional,List
from phi.agent import Agent
from phi.model.groq import Groq
from phi.storage.agent.postgres import PgAgentStorage
from phi.knowledge.pdf import PDFUrlKnowledgeBase
from phi.vectordb.pgvector import PgVector
# from phi.embedder.google import GeminiEmbedder
from phi.embedder.voyageai import VoyageAIEmbedder


import os
from dotenv import load_dotenv
load_dotenv()

# Create a pgvector database (postgresql)
db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"


# Create a knowledge base from a PDF file and add VectorDB
knowledge_base = PDFUrlKnowledgeBase(
    urls=["https://phi-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf"],
    vector_db = PgVector(table_name="recipes", 
                         db_url=db_url,
                         embedder=VoyageAIEmbedder(model="voyage-3",api_key=os.getenv('VOYAGE_API_KEY')),
                         # embedder=GeminiEmbedder(api_key=os.getenv('GEMINI_API_KEY'), dimensions=1536),
    )
)

knowledge_base.load(recreate=False)

# Create a storage for agent data
# Store Agent sessions in a database like PostgreSQL.
storage = PgAgentStorage(table_name="pdf_assistant", db_url=db_url)

# Create the agent
agent = Agent(
    model= Groq(id="llama3-groq-70b-8192-tool-use-preview", api_key=os.getenv('GROQ_API_KEY')),
    storage = storage,
    knowledge = knowledge_base,
    show_tool_calls=True,
    search_knowledge=True,
    read_chat_history=True,
) 


agent.print_response("How do I make pad thai?", markdown=True)



## For CLI interface
# def pdf_assistant(user: str = "user"):
# run_id: Optional[str] = None

#     assistant = Assistant(
#         run_id=run_id,
#         user_id=user,
#         knowledge_base=knowledge_base,
#         use_tools=True,
#         show_tool_calls=True,
#         # Uncomment the following line to use traditional RAG
#         # add_references_to_prompt=True,
#     )
#     if run_id is None:
#         run_id = assistant.run_id
#         print(f"Started Run: {run_id}\n")
#     else:
#         print(f"Continuing Run: {run_id}\n")

#     while True:
#         assistant.cli_app(markdown=True)

# if **name** == "**main**":
# typer.run(pdf_assistant)
