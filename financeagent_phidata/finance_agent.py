from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.yfinance import YFinanceTools
from phi.tools.duckduckgo import DuckDuckGo
import os
from dotenv import load_dotenv

load_dotenv()

web_agent = Agent(name='Web Search Agent' ,tools=[DuckDuckGo()], model=Groq(id="llama-3.3-70b-versatile"),instructions=["Always search for the most recent information and include Sources in the search results."], show_tool_calls=True)


finance_agent = Agent(
    name='Finance Agent',
    description='This agent is responsible for fetching financial data.',
    role = 'Fetch Financial Data',
    model = Groq(id="llama-3.3-70b-versatile"),
    tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, stock_fundamentals=True, company_news = True)],
    instructions=["Always fetch the most recent data and news and include Sources in the search results.",
                  "Always use tables to display the data."],
    show_tool_calls= True,
    markdown= True
)

multi_agent = Agent(
    team=[web_agent, finance_agent],
    model=Groq(id="llama-3.1-70b-versatile"),
    instructions=[
        "First, search news for most recent information.",
        "Include sources of the result.",
        "Always use tables to display the data.",
        "Finally, provide a well researched answer.",
    ],
    show_tool_calls=True,
    markdown=True,
)

multi_agent.print_response("Summarize analyst recommendation and share latest news for NVDA stock", stream=True)