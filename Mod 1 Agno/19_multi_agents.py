from agno.team import Team
from agno.agent import Agent
from agno.tools.hackernews import HackerNewsTools
from agno.tools.yfinance import YFinanceTools
from agno.models.groq import Groq

from dotenv import load_dotenv
load_dotenv()

news_agent = Agent(
    name="News Agent",
    role="Get trending tech news from HackerNews",
    tools=[HackerNewsTools()]
)

finance_agent = Agent(
    name="Finance Agent",
    role="Get stock prices and financial data",
    tools=[YFinanceTools()]
)

team = Team(
    name="Research Team",
    members=[news_agent, finance_agent],
    model=Groq(id="openai/gpt-oss-120b"),
    instructions="Delegate to the appropriate agent based on the request."
)

team.print_response("Quais as principais notícias sobre Inteligência Artificial (IA) e o desempenho das ações da NVIDIA (NVDA) em setembro de 2026?", stream=True)