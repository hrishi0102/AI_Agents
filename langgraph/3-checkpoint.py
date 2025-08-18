from typing_extensions import TypedDict
from typing import Annotated
from langchain.chat_models import init_chat_model
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()

class State(TypedDict):
    messages: Annotated[list, add_messages] 

llm = init_chat_model("anthropic:claude-3-5-sonnet-latest")

def chat_node(state: State):
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

graph_builder = StateGraph(State)
graph_builder.add_node("chat_node", chat_node)
graph_builder.add_edge(START, "chat_node")
graph_builder.add_edge("chat_node", END)

graph = graph_builder.compile()

def main():
    query = input(">: ")
    _state = {"messages": [{"role": "user", "content": query}]}
    graph_result = graph.invoke(_state)
    print("graph_result:", graph_result)

main()