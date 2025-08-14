from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END

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
graph_builder.add_edge(START, "chat_bot")
graph_builder.add_edge("chat_bot", END)

graph = graph_builder.compile()

def main():
    user = input("> : ")
    _state = {"query": user, "result": None}
    graph_result = graph.invoke(_state)
    print("graph_result:", graph_result)

main()