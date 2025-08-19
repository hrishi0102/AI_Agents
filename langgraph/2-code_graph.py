from typing_extensions import TypedDict
from typing import Literal
from langgraph.graph import StateGraph, START, END
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel
from IPython.display import Image, display
import os
load_dotenv()

client = OpenAI(
    api_key=os.getenv("ANTHROPIC_API_KEY"),
    base_url="https://api.anthropic.com/v1/"
)

gemini_client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

class ClassifyMessageResponse(BaseModel):
    is_coding: bool

class State(TypedDict):
    query: str
    result: str | None
    is_coding: bool | None

def classify_message(state: State):
    query = state["query"]

    SYSTEM_PROMPT = """
    You are a helpful assistant that classifies messages into different categories. 
    Your job is to classify whether the query is a coding question or related to coding or not.
    Return response in specified JSON boolean only
    {"is_coding": boolean}

    Rules:
    - Do NOT include code fences
    - Do NOT add extra text, explanation, or comments
    - Return only a single JSON object
    The message to classify is: 
    """
    llm_response = gemini_client.beta.chat.completions.parse(
        model="gemini-2.5-flash",
        response_format=ClassifyMessageResponse,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": query}
        ],
    )

    is_coding = llm_response.choices[0].message.parsed.is_coding
    state["is_coding"] = is_coding

    return state

def route_query(state: State) -> Literal["general_query", "coding_query"]:
    if state["is_coding"]:
        print("Routing to coding query handler")
        return "coding_query"
    else:
        print("Routing to general query handler")
        return "general_query"

def general_query(state: State):
    query = state["query"]
    print("Using Gemini to process general query")
    llm_response = gemini_client.chat.completions.create(
        model="gemini-2.5-flash",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": query}
        ],
    )
    result = llm_response.choices[0].message.content
    state["result"] = result
    return state

def coding_query(state: State):
    query = state["query"]
    print("Using Claude to process coding query")
    llm_response = client.chat.completions.create(
        model="claude-sonnet-4-20250514",
        messages=[
            {"role": "system", "content": "You are a helpful coding assistant."},
            {"role": "user", "content": query}
        ],
    )
    result = llm_response.choices[0].message.content
    state["result"] = result
    return state

graph_builder = StateGraph(State)
graph_builder.add_node("classify_message", classify_message)
graph_builder.add_node("route_query", route_query)
graph_builder.add_node("general_query", general_query)
graph_builder.add_node("coding_query", coding_query)
graph_builder.add_edge(START, "classify_message")
graph_builder.add_conditional_edges("classify_message", route_query)
graph_builder.add_edge("general_query", END)
graph_builder.add_edge("coding_query", END)
graph = graph_builder.compile()

def main():
    # display(Image(graph.get_graph().draw_mermaid_png()))
    query = input("> : ")
    _state = {
        "query": query,
        "result": None,
        "is_coding": None
    }

    # graph_result = graph.invoke(_state)  # Uncomment this line if you want to use invoke directly
    # print("graph_result:", graph_result)

    # Add streaming
    for event in graph.stream(_state):
        print("Event:", event)

main()
