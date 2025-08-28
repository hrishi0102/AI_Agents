from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langchain.schema import SystemMessage
from langchain.chat_models import init_chat_model
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv
import os
load_dotenv()

class State(TypedDict):
    messages: Annotated[list, add_messages]

@tool
def run_command(cmd: str):
    """Takes a command line prompt and executes it on user's machine and returns the output of the command
    Example: run_command(cmd='ls') where ls is the command to list files
    """
    result = os.system(cmd)
    return result

available_tools = [run_command]

llm = init_chat_model(model_provider="openai", model="gpt-4.1")
llm_with_tools = llm.bind_tools(tools=available_tools)

def chatbot(state: State):
    SYSTEM_PROMPT = SystemMessage(content="You are a helpful assistant who takes input from user and helps them. Based on avaiable tools you choose the correct tool and execute it. Always make sure your generated output and files are in the output/ folder. If not, please create folder.")
    messages = llm_with_tools.invoke([SYSTEM_PROMPT] + state["messages"])
    return {"messages": messages}

tool_node = ToolNode(tools=available_tools) 

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