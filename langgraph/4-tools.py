from typing_extensions import TypedDict
from typing import Annotated, Literal
from langchain.chat_models import init_chat_model
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode, tools_condition
import requests
from dotenv import load_dotenv
import os
load_dotenv()

llm = init_chat_model("anthropic:claude-3-5-sonnet-latest")

@tool()
def get_weather(city:str):
    """This tool fetches the current weather for a given city."""
    url = f"https://wttr.in/{city}?format=%C+%t"
    print(f"Fetching weather for {city}...")
    response = requests.get(url)
    if response.status_code == 200:
        return f"Weather data for {city}: {response.text}"
    else:
        return "Error fetching weather data"

tools = [get_weather]
llm_with_tools = llm.bind_tools(tools)

class State(TypedDict):
    messages: Annotated[list, add_messages]

def chatbot(state: State):
    message = llm_with_tools.invoke(state["messages"])
    return {"messages": [message]}

tool_node = ToolNode(tools=[get_weather])

graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", tool_node)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition,
)
# Any time a tool is called, we return to the chatbot to decide the next step
graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge("chatbot", END)

graph = graph_builder.compile()

def main():
    user_input = input("User: ")
    state = {"messages": [{"role": "user", "content": user_input}]}
    response = graph.stream(state, stream_mode="values")
    for event in response:
        if "messages" in event:
            event["messages"][-1].pretty_print()

main()