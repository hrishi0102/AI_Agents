from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()

client = OpenAI(
    api_key=os.getenv("ANTHROPIC_API_KEY"),
    base_url="https://api.anthropic.com/v1/"
)

class State(TypedDict):
    query: str
    result: str | None

def chat_bot(state: State):
    query = state["query"]
    llm_response = client.chat.completions.create(
    model="claude-sonnet-4-0", # Anthropic model name
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": query}
    ],
)
    result = llm_response.choices[0].message.content
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