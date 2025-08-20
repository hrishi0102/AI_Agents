from typing_extensions import TypedDict
from typing import Annotated, Literal
from langchain.chat_models import init_chat_model
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END

llm = init_chat_model("anthropic:claude-3-5-sonnet-latest")

class State(TypedDict):
    messages: Annotated[list, add_messages]

def chatbot(state: State):
    message = llm.invoke(state["messages"])
    return {"messages": [message]}

graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

graph = graph_builder.compile()

def main():
    user_input = input("User: ")
    state = {"messages": [{"role": "user", "content": user_input}]}
    response = graph.invoke(state)
    print("Bot:", response["messages"][0]["content"])

main()