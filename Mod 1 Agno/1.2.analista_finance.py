from agno.models.groq import Groq

from agno.agent import Agent
# Vamos utilizar o tavily para pesquisas web
from agno.tools.tavily import TavilyTools
from agno.tools.yfinance import YFinanceTools

from dotenv import load_dotenv
load_dotenv()

# vamos criar um agent
agent = Agent(
    model=Groq(id="openai/gpt-oss-120b"),
    tools=[YFinanceTools()],
    instructions="Você é um analista financeiro, que responde perguntas sobre ações e investimentos. Você tem acesso a ferramentas para buscar informações financeiras. Utilize tabelas para mostrar informação final."
)

# rodando
agent.print_response("Qual a cotação atual da AAPL?")
