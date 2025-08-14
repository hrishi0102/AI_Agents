from typing_extensions import TypedDict
from langgraph.graph import StateGraph

class State(TypedDict):
    query: str
    result: str | None

def chat_bot(state: State):
    query = state["query"]
    result = "Hello, how can I assist you today?"
    state["result"] = result
    return state

graph_builder = StateGraph(State)

graph_builder.add_node("chat_bot", chat_bot)