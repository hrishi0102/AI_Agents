# Checkpoint is basically a built-in persistance layer.
# When you compile a graph with checkpointer it saves a checkpoint of graph state at every super step
# We use thread_id to manage different user sessions

from typing_extensions import TypedDict
from typing import Annotated
from langchain.chat_models import init_chat_model
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.mongodb import MongoDBSaver
from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()

class State(TypedDict):
    messages: Annotated[list, add_messages] 

llm = init_chat_model("anthropic:claude-3-5-sonnet-latest")

def compile_graph_with_checkpointer(checkpointer):
    graph_with_checkpointer = graph_builder.compile(checkpointer=checkpointer)
    return graph_with_checkpointer

def chat_node(state: State):
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

graph_builder = StateGraph(State)
graph_builder.add_node("chat_node", chat_node)
graph_builder.add_edge(START, "chat_node")
graph_builder.add_edge("chat_node", END)

# Use this graph when checkpointing not needed
graph = graph_builder.compile()

def main():
    DB_URI = "mongodb://admin:password@localhost:27017"
    config = {"configurable": {"thread_id": "2"}}
    print("Connecting to MongoDB...")
    with MongoDBSaver.from_conn_string(DB_URI) as mongo_checkpointer:
        graph_with_mongo = compile_graph_with_checkpointer(mongo_checkpointer)
        print("Graph compiled with MongoDB checkpointer")
        query = input(">: ")
        _state = {"messages": [{"role": "user", "content": query}]}
        graph_result = graph_with_mongo.invoke(_state,config)
        print("graph_result:", graph_result)

main()