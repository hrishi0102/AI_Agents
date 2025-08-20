from typing_extensions import TypedDict
from typing import Annotated, Literal
from langchain.chat_models import init_chat_model
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.mongodb import MongoDBSaver
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.types import Command, interrupt
import requests
from dotenv import load_dotenv
import os
load_dotenv()

llm = init_chat_model("anthropic:claude-3-5-sonnet-latest")

@tool
def human_assistance(query: str) -> str:
    """Request assistance from a human."""
    # Interrupt saves the state in DB and kills the graph
    human_response = interrupt({"query": query})
    return human_response["data"]
 
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

tools = [get_weather, human_assistance]
llm_with_tools = llm.bind_tools(tools)

def compile_graph_with_checkpointer(checkpointer):
    graph_with_checkpointer = graph_builder.compile(checkpointer=checkpointer)
    return graph_with_checkpointer

class State(TypedDict):
    messages: Annotated[list, add_messages]

def chatbot(state: State):
    message = llm_with_tools.invoke(state["messages"])
    assert len(message.tool_calls) <= 1
    return {"messages": [message]}

tool_node = ToolNode(tools=[get_weather, human_assistance])

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

def user_chat():
    DB_URI = "mongodb://admin:password@localhost:27017"
    config = {"configurable": {"thread_id": "6"}}
    print("Connecting to MongoDB...")
    with MongoDBSaver.from_conn_string(DB_URI) as mongo_checkpointer:
        graph_with_mongo = compile_graph_with_checkpointer(mongo_checkpointer)
        print("Graph compiled with MongoDB checkpointer")
        while True: 
            user_input = input("User: ")
            state = {"messages": [{"role": "user", "content": user_input}]}
            response = graph_with_mongo.stream(state, config, stream_mode="values")
            for event in response:
                if "messages" in event:
                    event["messages"][-1].pretty_print()

user_chat()


# Human in loop interruption. Call when user_chat() last message is a tool call to human_assistance
def admin_call():
    DB_URI = "mongodb://admin:password@localhost:27017"
    # config = {"configurable": {"thread_id": "5"}}
    print("Connecting to MongoDB...")
    with MongoDBSaver.from_conn_string(DB_URI) as mongo_checkpointer:
        config = {"configurable": {"thread_id": "6"}, "checkpointer": mongo_checkpointer}
        graph_with_mongo = compile_graph_with_checkpointer(mongo_checkpointer)
        state = graph_with_mongo.get_state(config=config)
        last_message = state.values['messages'][-1]
        tool_calls = getattr(last_message, "tool_calls", [])
        user_query = None

        for call in tool_calls:
            if call.get("name") == "human_assistance":
                args = call.get("args", {})
                try:
                    user_query = args.get("query")
                except Exception as e:
                    print(f"Error extracting user query: {e}")
        print("User has a query:", user_query)
        solution = input("Admin: ")

        resume_command = Command(resume={"data" : solution})

        response = graph_with_mongo.stream(resume_command, config, stream_mode="values")
        for event in response:
            if "messages" in event:
                event["messages"][-1].pretty_print()

# admin_call()